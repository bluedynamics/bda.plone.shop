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
    permission = Attribute(u"Permissions a user must have on contextto view "
                           u"this link")
    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Target URL of this link")
    title = Attribute(u"Title of this link")
    order = Attribute(u"Order in which this link gets rendered")
    cssclass = Attribute(u"Additional CSS class to render")


@implementer(IShopNavigationLink)
@adapter(Interface)
class ShopNavigationLink(object):
    """Abstract shop navigation link.
    """
    permission = None
    display = True
    url = None
    title = None
    order = 0
    cssclass = None

    def __init__(self, context):
        self.context = context
        if self.permission is not None:
            self.display = checkPermission(self.permission, self.context)


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
    permission = VIEW_OWN_ORDERS_PERMISSION
    title = _('my_orders', default=u'My Orders')
    order = 20
    cssclass = 'myorders'

    def __init__(self, context):
        super(MyOrdersLink, self).__init__(context)
        self.url = '{}/@@myorders'.format(api.portal.get().absolute_url())


class OrdersLink(ShopNavigationLink):
    """Link for navigating to ``Global Orders`` view.
    """
    permission = VIEW_ORDERS_PERMISSION
    order = 10
    cssclass = 'orders'

    def __init__(self, context):
        super(OrdersLink, self).__init__(context)
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
    permission = VIEW_ORDERS_PERMISSION
    title = _('orders_in_context', default=u'Orders in Context')
    order = 11
    cssclass = 'orders'

    def __init__(self, context):
        super(OrdersInContextLink, self).__init__(context)
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
    permission = VIEW_ORDERS_PERMISSION
    order = 21
    cssclass = 'bookings'

    def __init__(self, context):
        super(BookingsLink, self).__init__(context)
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
    permission = VIEW_ORDERS_PERMISSION
    title = _('bookings_in_context', default=u'Bookings in Context')
    order = 22
    cssclass = 'bookings'

    def __init__(self, context):
        super(BookingsInContextLink, self).__init__(context)
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
    permission = VIEW_ORDERS_PERMISSION
    title = _('contacts', default=u'Contacts')
    order = 23
    cssclass = 'bookings'

    def __init__(self, context):
        super(ContactsLink, self).__init__(context)
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
    permission = EXPORT_ORDERS_PERMISSION
    title = _('exportorders', default=u'Export Orders')
    order = 30
    cssclass = 'export_orders'

    def __init__(self, context):
        super(ExportOrdersLink, self).__init__(context)
        self.url = '{}/@@exportorders'.format(api.portal.get().absolute_url())


class ExportOrdersItemLink(ShopNavigationLink):
    """Link for navigating to ``Export Context Orders`` view.
    """
    permission = EXPORT_ORDERS_PERMISSION
    title = _('exportorders_item', default=u'Export Orders on this Item')
    order = 40
    cssclass = 'export_orders_item'

    def __init__(self, context):
        super(ExportOrdersItemLink, self).__init__(context)
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
    permission = MANAGE_TEAMPLETS_PERMISSION
    order = 50
    cssclass = 'mailtemplates'

    def __init__(self, context):
        super(MailTemplatesLink, self).__init__(context)
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
    permission = MANAGE_DISCOUNT_PERMISSION
    title = _('cart_discount', default=u'Cart Discount')
    order = 60
    cssclass = 'cart_discount'

    def __init__(self, context):
        super(CartDiscountLink, self).__init__(context)
        if self.display:
            self.display = ISite.providedBy(context)
        self.url = '{}/@@cart_discount'.format(context.absolute_url())


class CartItemDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Item Discount`` view.
    """
    permission = MANAGE_DISCOUNT_PERMISSION
    title = _('item_discount', default=u'Item Discount')
    order = 70
    cssclass = 'item_discount'

    def __init__(self, context):
        super(CartItemDiscountLink, self).__init__(context)
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
    permission = MANAGE_SHOP_PERMISSION
    order = 50
    cssclass = 'controlpanel'

    def __init__(self, context):
        super(ControlpanelLink, self).__init__(context)
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
