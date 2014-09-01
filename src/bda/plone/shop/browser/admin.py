from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.orders.common import get_vendors_for
from bda.plone.orders.interfaces import IVendor
from bda.plone.shop import message_factory as _
from operator import attrgetter
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import adapter
from zope.component import getAdapters
from zope.component.interfaces import ISite
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer
from zope.security import checkPermission
import plone.api


VIEW_OWN_ORDERS_PERMISSION = 'bda.plone.orders.ViewOwnOrders'
VIEW_ORDERS_PERMISSION = 'bda.plone.orders.ViewOrders'
EXPORT_ORDERS_PERMISSION = 'bda.plone.orders.ExportOrders'
MANAGE_TEAMPLETS_PERMISSION = 'bda.plone.orders.ManageTemplates'
MANAGE_DISCOUNT_PERMISSION = 'bda.plone.discount.ManageDiscount'


class IShopPortletLink(Interface):
    """Adapter interface for providing links displayed in shop portlet.
    """

    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Link URL")
    title = Attribute(u"Link title")
    order = Attribute(u"Link order in listing")
    cssclass = Attribute(u"Css class for the link")


@implementer(IShopPortletLink)
@adapter(Interface)
class ShopPortletLink(object):
    """Abstract shop portlet link.
    """

    def __init__(self, context, view_permissions=[VIEW_ORDERS_PERMISSION]):
        self.context = context
        self.display = False
        for permission in view_permissions:
            self.display = checkPermission(permission, context)
            if self.display:
                break
        self.url = self.title = None
        self.order = 0
        self.cssclass = None


class ShopPortletMyOrdersLink(ShopPortletLink):

    def __init__(self, context):
        # XXX: buy items permission is meant to control whether a user can buy
        #      a specific item. Change check to whether a user is customer
        #      somewhere in the portal, which is semantically the correct way.
        permissions = [VIEW_OWN_ORDERS_PERMISSION]
        super(ShopPortletMyOrdersLink, self).__init__(
            context, view_permissions=permissions)
        site = plone.api.portal.get()
        self.url = '%s/@@myorders' % site.absolute_url()
        self.title = _('my_orders', default=u'My Orders')
        self.order = 20
        self.cssclass = 'myorders'


class ShopPortletOrdersLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopPortletOrdersLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        site = plone.api.portal.get()
        self.url = '%s/@@orders' % site.absolute_url()
        self.title = _('orders', default=u'Orders')
        self.order = 10
        self.cssclass = 'orders'


class ShopPortletExportOrdersLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [EXPORT_ORDERS_PERMISSION]
        super(ShopPortletExportOrdersLink, self).__init__(
            context, view_permissions=permissions)
        site = plone.api.portal.get()
        self.url = '%s/@@exportorders' % site.absolute_url()
        self.title = _('exportorders', default=u'Export Orders')
        self.order = 30
        self.cssclass = 'export_orders'


class ShopPortletExportOrdersItemLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [EXPORT_ORDERS_PERMISSION]
        super(ShopPortletExportOrdersItemLink, self).__init__(
            context, view_permissions=permissions)
        if IPloneSiteRoot.providedBy(context):
            self.display = False
            return
        self.url = '%s/@@exportorders_contextual' % self.context.absolute_url()
        self.title = _(
            'exportorders_item', default=u'Export Orders on this Item')
        self.order = 40
        self.cssclass = 'export_orders_item'


class ShopPortletMailTemplatesLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [MANAGE_TEAMPLETS_PERMISSION]
        super(ShopPortletMailTemplatesLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = ISite.providedBy(context) \
                or IVendor.providedBy(context)
        self.url = '%s/@@mailtemplates' % context.absolute_url()
        self.title = _('mailtemplates', default=u'Notification Templates')
        self.order = 50
        self.cssclass = 'mailtemplates'


class ShopPortletCartDiscountLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(ShopPortletCartDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = ISite.providedBy(context)
        self.url = '%s/@@cart_discount' % context.absolute_url()
        self.title = _('cart_discount', default=u'Cart Discount')
        self.order = 60
        self.cssclass = 'cart_discount'


class ShopPortletCartItemDiscountLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(ShopPortletCartItemDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = ISite.providedBy(context) \
                or IDiscountSettingsEnabled.providedBy(context)
        self.url = '%s/@@item_discount' % context.absolute_url()
        self.title = _('item_discount', default=u'Item Discount')
        self.order = 70
        self.cssclass = 'item_discount'


class IShopAdminPortlet(IPortletDataProvider):
    """A portlet rendering shop portlet links.
    """


@implementer(IShopAdminPortlet)
class ShopAdminAssignment(base.Assignment):
    title = _(u'shop_portlet', default=u'Shop Portlet')


class ShopAdminRenderer(base.Renderer):
    render = ViewPageTemplateFile('admin.pt')

    @property
    def available(self):
        return bool(self.links())

    def links(self):
        def unsorted_links():
            for name, link in getAdapters((self.context,), IShopPortletLink):
                if link.display:
                    yield link
        return sorted(unsorted_links(), key=attrgetter('order'))


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()
