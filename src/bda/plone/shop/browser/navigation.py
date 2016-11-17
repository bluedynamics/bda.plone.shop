# -*- coding: utf-8 -*-
from Acquisition import aq_inner
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
from zope.component import getMultiAdapter
from zope.component.interfaces import ISite
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.security import checkPermission


###############################################################################
# general
###############################################################################

VIEW_OWN_ORDERS = 'bda.plone.orders.ViewOwnOrders'
VIEW_ORDERS = 'bda.plone.orders.ViewOrders'
EXPORT_ORDERS = 'bda.plone.orders.ExportOrders'
MANAGE_TEAMPLETS = 'bda.plone.orders.ManageTemplates'
MANAGE_DISCOUNT = 'bda.plone.discount.ManageDiscount'
MANAGE_SHOP = 'cmf.ManagePortal'


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
@adapter(Interface, IBrowserRequest)
class ShopNavigationLink(object):
    """Abstract shop navigation link.
    """
    permission = None
    display = False
    url = None
    title = None
    order = 0
    cssclass = None

    def __init__(self, context, request):
        """Initialize shop navigation link. Set ``self.display`` based on
        a permission check on context against ``self.permission``
        """
        self.context = context
        self.request = request
        if self.permission is not None:
            self.display = checkPermission(self.permission, self.context)

    def acquire_context(self, context, interfaces=[]):
        """Acquire next context parent providing one of the given interfaces.
        """
        for iface in interfaces:
            if iface.providedBy(context):
                return context
        return self.acquire_context(aq_parent(context), interfaces=interfaces)

    def buyables_in_context(self, context):
        """Return flag whether context contains buyables.
        """
        catalog = api.portal.get_tool("portal_catalog")
        path = '/'.join(context.getPhysicalPath())
        brains = catalog(path=path, object_provides=IBuyable.__identifier__)
        for _ in brains:
            return True
        return False

    def context_is_default_page(self, context):
        """Return flag whether given context is default page in it's container.
        """
        context = aq_inner(context)
        container = aq_parent(context)
        to_adapt = container, self.request
        default_page = getMultiAdapter(to_adapt, name='default_page')
        return default_page.getDefaultPage() is context


class ShopNavigation(object):
    """Mixin for shop navigation view.

    Subclass is usually view like and must provide ``context`` and ``request``
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
            to_adapt = self.context, self.request
            for _, link in getAdapters(to_adapt, IShopNavigationLink):
                if link.display:
                    yield link
        return sorted(unsorted_links(), key=attrgetter('order'))


###############################################################################
# orders related
###############################################################################

class OrdersLink(ShopNavigationLink):
    """Link for navigating to ``Global Orders`` view.
    """
    permission = VIEW_ORDERS
    order = 10
    cssclass = 'orders'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite, IVendor])
        # call super class constructor
        super(OrdersLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # set title by context interface
        if IPloneSiteRoot.providedBy(context):
            self.title = _('orders_global', default=u'Orders (global)')
        elif ISite.providedBy(context):
            self.title = _('orders_site', default=u'Orders (site-wide)')
        elif IVendor.providedBy(context):
            self.title = _(
                'orders_vendor',
                default=u'Orders (vendor specific)'
            )
        # set target URL
        self.url = '{}/@@orders'.format(context.absolute_url())


class OrdersInContextLink(ShopNavigationLink):
    """Link for navigating to ``Context Orders`` view.
    """
    permission = VIEW_ORDERS
    title = _('orders_in_context', default=u'Orders in Context')
    order = 11
    cssclass = 'orders'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # call super class constructor
        super(OrdersInContextLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
        # set target URL
        self.url = '{}/@@orders'.format(context.absolute_url())


class OrdersInContainerLink(OrdersInContextLink):
    """Link for navigating to ``Container Orders`` view.
    """
    title = _('orders_in_container', default=u'Orders in Container')
    order = 12

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if self.context_is_default_page(context):
            context = aq_parent(aq_inner(context))
        else:
            self.display = False
            return
        # call super class constructor
        super(OrdersInContextLink, self).__init__(context, request)


class MyOrdersLink(ShopNavigationLink):
    """Link for navigating to ``My Orders`` view.
    """
    permission = VIEW_OWN_ORDERS
    title = _('my_orders', default=u'My Orders')
    order = 13
    cssclass = 'myorders'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(MyOrdersLink, self).__init__(context, request)
        # set target URL
        self.url = '{}/@@myorders'.format(context.absolute_url())


###############################################################################
# bookings related
###############################################################################

class BookingsLink(ShopNavigationLink):
    """Link for navigating to ``Global Bookings`` view.
    """
    permission = VIEW_ORDERS
    order = 20
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite, IVendor])
        # call super class constructor
        super(BookingsLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # set title by context interface
        if IPloneSiteRoot.providedBy(context):
            self.title = _('bookings_global', default=u'Bookings (global)')
        elif ISite.providedBy(context):
            self.title = _('bookings_site', default=u'Bookings (site-wide)')
        elif IVendor.providedBy(context):
            self.title = _(
                'bookings_vendor',
                default=u'Bookings (vendor specific)'
            )
        # set target URL
        self.url = '{}/@@bookings'.format(context.absolute_url())


class BookingsInContextLink(ShopNavigationLink):
    """Link for navigating to ``Context Bookings`` view.
    """
    permission = VIEW_ORDERS
    title = _('bookings_in_context', default=u'Bookings in Context')
    order = 21
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # call super class constructor
        super(BookingsInContextLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
        # set target URL
        self.url = '{}/@@bookings'.format(context.absolute_url())


class BookingsInContainerLink(BookingsInContextLink):
    """Link for navigating to ``Container Bookings`` view.
    """
    title = _('bookings_in_container', default=u'Bookings in Container')
    order = 22

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if self.context_is_default_page(context):
            context = aq_parent(aq_inner(context))
        else:
            self.display = False
            return
        # call super class constructor
        super(BookingsInContainerLink, self).__init__(context, request)


###############################################################################
# contacts related
###############################################################################

class ContactsLink(ShopNavigationLink):
    """Link for navigating to ``Contacts`` view.
    """
    permission = VIEW_ORDERS
    title = _('contacts', default=u'Contacts')
    order = 30
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(ContactsLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
        # set target URL
        self.url = '{}/@@contacts'.format(context.absolute_url())


###############################################################################
# export related
###############################################################################

class ExportOrdersLink(ShopNavigationLink):
    """Link for navigating to ``Export Orders`` view.
    """
    permission = EXPORT_ORDERS
    title = _('exportorders', default=u'Export Orders')
    order = 40
    cssclass = 'export_orders'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(ExportOrdersLink, self).__init__(context, request)
        # set target URL
        self.url = '{}/@@exportorders'.format(context.absolute_url())


class ExportOrdersInContext(ShopNavigationLink):
    """Link for navigating to ``Export Context Orders`` view.
    """
    permission = EXPORT_ORDERS
    title = _('exportorders_item', default=u'Export Orders on this Item')
    order = 41
    cssclass = 'export_orders_item'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # call super class constructor
        super(ExportOrdersInContext, self).__init__(context, request)
        # do not display on site
        if self.display and ISite.providedBy(context):
            self.display = False
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
        # set target URL
        self.url = '{}/@@exportorders_contextual'.format(
            context.absolute_url()
        )


class ExportOrdersInContainerLink(ExportOrdersInContext):
    """Link for navigating to ``Export Orders in Container`` view.
    """
    title = _(
        'exportorders_in_container',
        default=u'Export Orders in Container'
    )
    order = 42

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if self.context_is_default_page(context):
            context = aq_parent(aq_inner(context))
        else:
            self.display = False
            return
        # call super class constructor
        super(ExportOrdersInContainerLink, self).__init__(context, request)


###############################################################################
# mail templates related
###############################################################################

class MailTemplatesLink(ShopNavigationLink):
    """Link for navigating to ``Mail Templates`` view.
    """
    permission = MANAGE_TEAMPLETS
    order = 50
    cssclass = 'mailtemplates'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite, IVendor])
        # call super class constructor
        super(MailTemplatesLink, self).__init__(context, request)
        # set title by context interface
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
        # set target URL
        self.url = '{}/@@mailtemplates'.format(context.absolute_url())


###############################################################################
# discount related
###############################################################################

class CartDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Cart Discount`` view.
    """
    permission = MANAGE_DISCOUNT
    title = _('cart_discount', default=u'Cart Discount')
    order = 60
    cssclass = 'cart_discount'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(CartDiscountLink, self).__init__(context, request)
        # set target URL
        self.url = '{}/@@cart_discount'.format(context.absolute_url())


class CartItemDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Item Discount`` view.
    """
    permission = MANAGE_DISCOUNT
    title = _('item_discount', default=u'Item Discount')
    order = 61
    cssclass = 'item_discount'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # call super class constructor
        super(CartItemDiscountLink, self).__init__(context, request)
        # check whether context is site or discount settings are enabled on
        # context
        if self.display:
            self.display = ISite.providedBy(context) \
                or IDiscountSettingsEnabled.providedBy(context)
        # set target URL
        self.url = '{}/@@item_discount'.format(context.absolute_url())


class CartItemDiscountInContainerLink(CartItemDiscountLink):
    """Link for navigating to ``Item Discount in Container`` view.
    """
    title = _(
        'item_discount_in_container',
        default=u'Item Discount in Container'
    )
    order = 62

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if self.context_is_default_page(context):
            context = aq_parent(aq_inner(context))
        else:
            self.display = False
            return
        # call super class constructor
        super(CartItemDiscountInContainerLink, self).__init__(context, request)


###############################################################################
# control panel related
###############################################################################

class ControlPanelLink(ShopNavigationLink):
    """Link for navigating to ``Shop Control Panel`` view.
    """
    permission = MANAGE_SHOP
    order = 70
    cssclass = 'controlpanel'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(ControlPanelLink, self).__init__(context, request)
        # set title by context interface
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
        # set target URL
        self.url = '{}/@@shop_controlpanel'.format(context.absolute_url())
