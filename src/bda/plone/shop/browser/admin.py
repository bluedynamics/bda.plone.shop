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
from bda.plone.orders.interfaces import IVendor
from .. import message_factory as _

import plone.api


MANAGE_PORTAL = 'cmf.ManagePortal'
MODIFY_CONTENT_PERMISSION = 'cmf.ModifyPortalContent'
VIEW_ORDERS_PERMISSION = 'bda.plone.orders.ViewOrders'
VENDOR_ORDERS_PERMISSION = 'bda.plone.order.VendorOrders'
CUSTOMER_ORDERS_PERMISSION = 'bda.plone.orders.CustomerOrders'
ALL_ORDERS_PERMISSION = 'bda.plone.orders.AllOrders'


class IShopAdminLink(Interface):
    """Adapter interface for providing links displayed in shop admin portlet.
    """

    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Link URL")
    title = Attribute(u"Link title")
    order = Attribute(u"Link order in listing")


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


class ShopAdminOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [
            MANAGE_PORTAL, ALL_ORDERS_PERMISSION, VENDOR_ORDERS_PERMISSION,
        ]
        super(ShopAdminOrdersLink, self).__init__(
            context, view_permissions=permissions)
        self.url = '%s/@@orders' % context.absolute_url()
        self.title = _('orders', default=u'Orders')
        self.order = 10


class ShopAdminMyOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [
            MANAGE_PORTAL, CUSTOMER_ORDERS_PERMISSION,
        ]
        super(ShopAdminMyOrdersLink, self).__init__(
            context, view_permissions=permissions)
        self.url = '%s/@@orders?ordersfilter.customer=%s' % (
            context.absolute_url(), plone.api.user.get_current().getId())
        self.title = _('my_orders', default=u'My Orders')
        self.order = 20


class ShopAdminExportOrdersLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [
            MANAGE_PORTAL, ALL_ORDERS_PERMISSION, VENDOR_ORDERS_PERMISSION,
        ]
        super(ShopAdminExportOrdersLink, self).__init__(
            context, view_permissions=permissions)
        self.url = '%s/@@exportorders' % context.absolute_url()
        self.title = _('exportorders', default=u'Export Orders')
        self.order = 30


class ShopAdminMailTemplatesLink(ShopAdminLink):

    def __init__(self, context):
        permissions = [
            MANAGE_PORTAL, MODIFY_CONTENT_PERMISSION,
        ]
        super(ShopAdminMailTemplatesLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = IPloneSiteRoot.providedBy(context) \
                or IVendor.providedBy(context)
        self.url = '%s/@@mailtemplates' % context.absolute_url()
        self.title = _('mailtemplates', default=u'Notification Templates')
        self.order = 40


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

    @property
    def links(self):
        ret = list()
        for _, adapter in getAdapters((self.context,), IShopAdminLink):
            ret.append(adapter)
        return sorted(ret, key=lambda x: x.order)


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()
