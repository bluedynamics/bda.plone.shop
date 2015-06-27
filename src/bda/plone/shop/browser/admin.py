# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.orders.common import get_vendors_for
from bda.plone.orders.interfaces import IBuyable
from bda.plone.orders.interfaces import IVendor
from bda.plone.shop import message_factory as _
from operator import attrgetter
from plone.app.portlets.portlets import base
from plone.folder.interfaces import IFolder
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
MANAGE_SHOP_PERMISSION = 'cmf.ManagePortal'


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

        # Find the nearest context, where this functionality can be bound to.
        def _find_context(ctx):
            return ctx\
                if ISite.providedBy(ctx) or IVendor.providedBy(ctx)\
                else _find_context(aq_parent(ctx))
        context = _find_context(context)

        if IPloneSiteRoot.providedBy(context):
            self.title = _(
                'orders_global',
                default=u'Orders (global)'
            )
        elif ISite.providedBy(context):
            self.title = _(
                'orders_site',
                default=u'Orders (site-wide)'
            )
        elif IVendor.providedBy(context):
            self.title = _(
                'orders_vendor',
                default=u'Orders (vendor specific)'
            )

        self.url = '%s/@@orders' % context.absolute_url()
        self.order = 10
        self.cssclass = 'orders'


class ShopPortletOrdersInContextLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopPortletOrdersInContextLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # Go to appropriate context
        if not IBuyable.providedBy(context) \
                and not IFolder.providedBy(context) \
                and not IPloneSiteRoot.providedBy(context):
            context = context.aq_inner.aq_parent
        self.url = '%s/@@orders' % context.absolute_url()
        self.title = _('orders_in_context', default=u'Orders in Context')
        self.order = 11
        self.cssclass = 'orders'


class ShopPortletBookingsLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopPortletBookingsLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False

        # Find the nearest context, where this functionality can be bound to.
        def _find_context(ctx):
            return ctx\
                if ISite.providedBy(ctx) or IVendor.providedBy(ctx)\
                else _find_context(aq_parent(ctx))
        context = _find_context(context)

        if IPloneSiteRoot.providedBy(context):
            self.title = _(
                'bookings_global',
                default=u'Bookings (global)'
            )
        elif ISite.providedBy(context):
            self.title = _(
                'bookings_site',
                default=u'Bookings (site-wide)'
            )
        elif IVendor.providedBy(context):
            self.title = _(
                'bookings_vendor',
                default=u'Bookings (vendor specific)'
            )

        self.url = '%s/@@bookings' % context.absolute_url()
        self.order = 21
        self.cssclass = 'bookings'


class ShopPortletBookingsInContextLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopPortletBookingsInContextLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # Go to appropriate context
        if not IBuyable.providedBy(context) \
                and not IFolder.providedBy(context) \
                and not IPloneSiteRoot.providedBy(context):
            context = context.aq_inner.aq_parent
        self.url = '%s/@@bookings' % context.absolute_url()
        self.title = _('bookings_in_context', default=u'Bookings in Context')
        self.order = 22
        self.cssclass = 'bookings'


class ShopPortletContactsLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ShopPortletContactsLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        site = plone.api.portal.get()
        self.url = '%s/@@contacts' % site.absolute_url()
        self.title = _('contacts', default=u'Contacts')
        self.order = 23
        self.cssclass = 'bookings'


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

        # Find the nearest context, where this functionality can be bound to.
        def _find_context(ctx):
            return ctx\
                if ISite.providedBy(ctx) or IVendor.providedBy(ctx)\
                else _find_context(aq_parent(ctx))
        context = _find_context(context)

        if IPloneSiteRoot.providedBy(context):
            self.title = _(
                'mailtemplates_global',
                default=u'Notification Templates (global)'
            )
        elif ISite.providedBy(context):
            self.title = _(
                'mailtemplates_site',
                default=u'Notification Templates (site-wide)'
            )
        elif IVendor.providedBy(context):
            self.title = _(
                'mailtemplates_vendor',
                default=u'Notification Templates (vendor specific)'
            )

        self.url = '%s/@@mailtemplates' % context.absolute_url()
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


class ShopPortletControlpanelLink(ShopPortletLink):

    def __init__(self, context):
        permissions = [MANAGE_SHOP_PERMISSION]
        super(ShopPortletControlpanelLink, self).__init__(
            context, view_permissions=permissions)

        # Find the nearest context, where this functionality can be bound to.
        def _find_context(ctx):
            return ctx\
                if ISite.providedBy(ctx)\
                else _find_context(aq_parent(ctx))
        context = _find_context(context)

        if IPloneSiteRoot.providedBy(context):
            self.title = _(
                'shop_controlpanel_global',
                default=u'Shop Controlpanel (global)'
            )
        elif ISite.providedBy(context):
            self.title = _(
                'shop_controlpanel_site',
                default=u'Shop Controlpanel (site-wide)'
            )

        self.url = '%s/@@shop_controlpanel' % context.absolute_url()
        self.order = 50
        self.cssclass = 'controlpanel'


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
