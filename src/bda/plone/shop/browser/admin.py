from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Attribute
from zope.component import adapter
from zope.component import getAdapters
from zope.security import checkPermission
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.orders.interfaces import IVendor
from bda.plone.orders.common import get_vendors_for
from .. import message_factory as _

import plone.api


VIEW_ORDERS_PERMISSION = 'bda.plone.orders.ViewOrders'
MANAGE_TEAMPLETS_PERMISSION = 'bda.plone.orders.ManageTemplates'
MANAGE_DISCOUNT_PERMISSION = 'bda.plone.discount.ManageDiscount'


class IShopAdminLink(Interface):
    """Adapter interface for providing links displayed in shop admin portlet.
    """

    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Link URL")
    title = Attribute(u"Link title")
    order = Attribute(u"Link order in listing")
    cssclass = Attribute(u"Css class for the link")


@implementer(IShopAdminLink)
@adapter(Interface)
class ShopAdminLink(object):
    """Abstract shop administration link.
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


class ShopAdminOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopAdminOrdersLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        site = plone.api.portal.get()
        self.url = '%s/@@orders' % site.absolute_url()
        self.title = _('orders', default=u'Orders')
        self.order = 10
        self.cssclass = 'orders'


class ShopAdminMyOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopAdminMyOrdersLink, self).__init__(
            context, view_permissions=permissions)
        site = plone.api.portal.get()
        self.url = '%s/@@myorders' % site.absolute_url()
        self.title = _('my_orders', default=u'My Orders')
        self.order = 20
        self.cssclass = 'myorders'


class ShopAdminExportOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopAdminExportOrdersLink, self).__init__(
            context, view_permissions=permissions)
        site = plone.api.portal.get()
        self.url = '%s/@@exportorders' % site.absolute_url()
        self.title = _('exportorders', default=u'Export Orders')
        self.order = 30
        self.cssclass = 'export_orders'


class ShopAdminMailTemplatesLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [MANAGE_TEAMPLETS_PERMISSION]
        super(ShopAdminMailTemplatesLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = IPloneSiteRoot.providedBy(context) \
                or IVendor.providedBy(context)
        self.url = '%s/@@mailtemplates' % context.absolute_url()
        self.title = _('mailtemplates', default=u'Notification Templates')
        self.order = 40
        self.cssclass = 'mailtemplates'


class ShopAdminCartDiscountLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(ShopAdminCartDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = IPloneSiteRoot.providedBy(context)
        self.url = '%s/@@cart_discount' % context.absolute_url()
        self.title = _('cart_discount', default=u'Cart Discount')
        self.order = 40
        self.cssclass = 'cart_discount'


class ShopAdminCartItemDiscountLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(ShopAdminCartItemDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = IPloneSiteRoot.providedBy(context) \
                or IDiscountSettingsEnabled.providedBy(context)
        self.url = '%s/@@item_discount' % context.absolute_url()
        self.title = _('item_discount', default=u'Item Discount')
        self.order = 40
        self.cssclass = 'item_discount'


class IShopAdminPortlet(IPortletDataProvider):
    """A portlet rendering shop administration links.
    """


@implementer(IShopAdminPortlet)
class ShopAdminAssignment(base.Assignment):
    title = _(u'shop_admin', default=u'Shop Administration')


class ShopAdminRenderer(base.Renderer):
    render = ViewPageTemplateFile('admin.pt')

    @property
    def show(self):
        return checkPermission(VIEW_ORDERS_PERMISSION, self.context)

    def links(self):
        ret = list()
        for _, adapter in getAdapters((self.context,), IShopAdminLink):
            ret.append(adapter)
        return sorted(ret, key=lambda x: x.order)


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()
