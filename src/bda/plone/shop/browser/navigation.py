# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.orders.common import get_vendors_for
from bda.plone.orders.interfaces import IBuyable
from bda.plone.orders.interfaces import IVendor
from bda.plone.shop import message_factory as _
from operator import attrgetter
from plone import api
from plone.folder.interfaces import IFolder
from zope.component import adapter
from zope.component import getAdapters
from zope.component.interfaces import ISite
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer
from zope.security import checkPermission


###############################################################################
# general
###############################################################################

VIEW_OWN_ORDERS_PERMISSION = 'bda.plone.orders.ViewOwnOrders'
VIEW_ORDERS_PERMISSION = 'bda.plone.orders.ViewOrders'
EXPORT_ORDERS_PERMISSION = 'bda.plone.orders.ExportOrders'
MANAGE_TEAMPLETS_PERMISSION = 'bda.plone.orders.ManageTemplates'
MANAGE_DISCOUNT_PERMISSION = 'bda.plone.discount.ManageDiscount'
MANAGE_SHOP_PERMISSION = 'cmf.ManagePortal'


class IShopNavigationLink(Interface):
    """Adapter interface for providing shop navigation links.
    """
    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Link URL")
    title = Attribute(u"Link title")
    order = Attribute(u"Link order in listing")
    cssclass = Attribute(u"CSS class for the link")


@implementer(IShopNavigationLink)
@adapter(Interface)
class ShopNavigationLink(object):
    """Abstract shop navigation link.
    """
    # context on which this link gets rendered
    context = None
    # flag whether to display link
    display = False
    # target URL of this link
    url = None
    # title of this link
    title = None
    # order in which this link gets rendered
    order = 0
    # additional CSS class to render
    cssclass = None

    def __init__(self, context, view_permissions=[VIEW_ORDERS_PERMISSION]):
        """Instanciate shop navigation link.

        Sets ``context`` and checks whether current user has one of the given
        ``view_permissions`` on context. If not, ``display`` gets set to
        ``False``.
        """
        self.context = context
        for permission in view_permissions:
            self.display = checkPermission(permission, context)
            if self.display:
                break


class ShopNavigation(object):
    """Base object for shop navigation.
    """

    @property
    def available(self):
        """Flag whether shop navigation links are available in context.
        """
        return bool(self.links())

    def links(self):
        """Sorted list of ``IShopNavigationLink`` implementing instances.
        """
        def unsorted_links():
            for _, link in getAdapters((self.context,), IShopNavigationLink):
                if link.display:
                    yield link
        return sorted(unsorted_links(), key=attrgetter('order'))


###############################################################################
# orders related
###############################################################################

class MyOrdersLink(ShopNavigationLink):
    """Link for navigating to ``My Orders`` view.
    """
    title = _('my_orders', default=u'My Orders')
    order = 20
    cssclass = 'myorders'

    def __init__(self, context):
        # XXX: buy items permission is meant to control whether a user can buy
        #      a specific item. Change check to whether a user is customer
        #      somewhere in the portal, which is semantically the correct way.
        permissions = [VIEW_OWN_ORDERS_PERMISSION]
        super(MyOrdersLink, self).__init__(
            context, view_permissions=permissions)
        self.url = '{}/@@myorders'.format(api.portal.get().absolute_url())


class OrdersLink(ShopNavigationLink):
    """Link for navigating to ``Global Orders`` view.
    """
    order = 10
    cssclass = 'orders'

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(OrdersLink, self).__init__(
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
        self.url = '{}/@@orders'.format(context.absolute_url())


class OrdersInContextLink(ShopNavigationLink):
    """Link for navigating to ``Context Orders`` view.
    """
    title = _('orders_in_context', default=u'Orders in Context')
    order = 11
    cssclass = 'orders'

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(OrdersInContextLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # XXX: catalog query -> IBuyable contained in path
        #      of not, display False
        # Go to appropriate context
        if not IBuyable.providedBy(context) \
                and not IFolder.providedBy(context) \
                and not IPloneSiteRoot.providedBy(context):
            context = context.aq_inner.aq_parent
        self.url = '{}/@@orders'.format(context.absolute_url())


###############################################################################
# bookings related
###############################################################################

class BookingsLink(ShopNavigationLink):
    """Link for navigating to ``Global Bookings`` view.
    """
    order = 21
    cssclass = 'bookings'

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(BookingsLink, self).__init__(
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
        self.url = '{}/@@bookings'.format(context.absolute_url())


class BookingsInContextLink(ShopNavigationLink):
    """Link for navigating to ``Context Bookings`` view.
    """
    title = _('bookings_in_context', default=u'Bookings in Context')
    order = 22
    cssclass = 'bookings'

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(BookingsInContextLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # XXX: catalog query -> IBuyable contained in path
        #      of not, display False
        # Go to appropriate context
        if not IBuyable.providedBy(context) \
                and not IFolder.providedBy(context) \
                and not IPloneSiteRoot.providedBy(context):
            context = context.aq_inner.aq_parent
        self.url = '{}/@@bookings'.format(context.absolute_url())


###############################################################################
# contacts related
###############################################################################

class ContactsLink(ShopNavigationLink):
    """Link for navigating to ``Contacts`` view.
    """
    title = _('contacts', default=u'Contacts')
    order = 23
    cssclass = 'bookings'

    def __init__(self, context):
        permissions = [VIEW_ORDERS_PERMISSION]
        super(ContactsLink, self).__init__(
            context, view_permissions=permissions)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        self.url = '{}/@@contacts'.format(api.portal.get().absolute_url())


###############################################################################
# export related
###############################################################################

class ExportOrdersLink(ShopNavigationLink):
    """Link for navigating to ``Export Orders`` view.
    """
    title = _('exportorders', default=u'Export Orders')
    order = 30
    cssclass = 'export_orders'

    def __init__(self, context):
        permissions = [EXPORT_ORDERS_PERMISSION]
        super(ExportOrdersLink, self).__init__(
            context, view_permissions=permissions)
        self.url = '{}/@@exportorders'.format(api.portal.get().absolute_url())


class ExportOrdersItemLink(ShopNavigationLink):
    """Link for navigating to ``Export Context Orders`` view.
    """
    title = _('exportorders_item', default=u'Export Orders on this Item')
    order = 40
    cssclass = 'export_orders_item'

    def __init__(self, context):
        permissions = [EXPORT_ORDERS_PERMISSION]
        super(ExportOrdersItemLink, self).__init__(
            context, view_permissions=permissions)
        # XXX: catalog query -> IBuyable contained in path
        #      of not, display False
        if IPloneSiteRoot.providedBy(context):
            self.display = False
            return
        self.url = '{}/@@exportorders_contextual'.format(
            self.context.absolute_url()
        )


###############################################################################
# mail templates related
###############################################################################

class MailTemplatesLink(ShopNavigationLink):
    """Link for navigating to ``Mail Templates`` view.
    """
    order = 50
    cssclass = 'mailtemplates'

    def __init__(self, context):
        permissions = [MANAGE_TEAMPLETS_PERMISSION]
        super(MailTemplatesLink, self).__init__(
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
        self.url = '{}/@@mailtemplates'.format(context.absolute_url())


###############################################################################
# discount related
###############################################################################

class CartDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Cart Discount`` view.
    """
    title = _('cart_discount', default=u'Cart Discount')
    order = 60
    cssclass = 'cart_discount'

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(CartDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = ISite.providedBy(context)
        self.url = '{}/@@cart_discount'.format(context.absolute_url())


class CartItemDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Item Discount`` view.
    """
    title = _('item_discount', default=u'Item Discount')
    order = 70
    cssclass = 'item_discount'

    def __init__(self, context):
        permissions = [MANAGE_DISCOUNT_PERMISSION]
        super(CartItemDiscountLink, self).__init__(
            context, view_permissions=permissions)
        if self.display:
            self.display = ISite.providedBy(context) \
                or IDiscountSettingsEnabled.providedBy(context)
        self.url = '{}/@@item_discount'.format(context.absolute_url())


###############################################################################
# control panel related
###############################################################################

class ControlpanelLink(ShopNavigationLink):
    """Link for navigating to ``Shop Controlpanel`` view.
    """
    order = 50
    cssclass = 'controlpanel'

    def __init__(self, context):
        permissions = [MANAGE_SHOP_PERMISSION]
        super(ControlpanelLink, self).__init__(
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
        self.url = '{}/@@shop_controlpanel'.format(context.absolute_url())
