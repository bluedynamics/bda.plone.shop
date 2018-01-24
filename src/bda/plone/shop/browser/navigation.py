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
from zope.annotation import IAnnotations
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
# interfaces
###############################################################################

class IShopNavigationLink(Interface):
    """Adapter interface for providing shop navigation links.
    """
    id = Attribute(u"Link ID")
    group = Attribute(u"Navigation group ID")
    permission = Attribute(u"Permissions a user must have on context to view "
                           u"this link")
    display = Attribute(u"Flag whether to display this link")
    url = Attribute(u"Target URL of this link")
    title = Attribute(u"Title of this link")
    order = Attribute(u"Order in which this link gets rendered")
    cssclass = Attribute(u"Additional CSS class to render")


class IShopNavigationGroup(Interface):
    """Adapter interface for providing shop navigation groups.
    """
    id = Attribute(u"Group ID")
    title = Attribute(u"Group Title")
    order = Attribute(u"Group rendering order")
    available = Attribute(u"Flag whether group navigation links are available")

    def links():
        """Sorted list of ``IShopNavigationLink`` implementing instances
        related to this group.
        """


class IShopNavigation(Interface):
    """Interface for providing shop navigation API.
    """
    available = Attribute(u"Flag whether navigation links are available")

    def links():
        """Sorted list of ``IShopNavigationLink`` implementing instances
        regardless of group.
        """

    def groups():
        """Sorted list of ``IShopNavigationGroup`` implementing instances.
        """


###############################################################################
# general
###############################################################################

VIEW_OWN_ORDERS = 'bda.plone.orders.ViewOwnOrders'
VIEW_ORDERS = 'bda.plone.orders.ViewOrders'
EXPORT_ORDERS = 'bda.plone.orders.ExportOrders'
MANAGE_TEAMPLETS = 'bda.plone.orders.ManageTemplates'
MANAGE_DISCOUNT = 'bda.plone.discount.ManageDiscount'
MANAGE_SHOP = 'cmf.ManagePortal'


class NavigationItemLookupMixin(object):
    """Mixin for navigation links related item lookup.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def lookup_navigation_items(self, interface):
        """Lookup navigation items by interface.
        """
        cache = IAnnotations(self.request)
        cache_key = 'NavigationItemLookupMixin.lookup_navigation_items.{}'
        cache_key = cache_key.format(interface.__name__)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        def unsorted_items():
            to_adapt = self.context, self.request
            for _, link in getAdapters(to_adapt, interface):
                yield link
        cache[cache_key] = sorted(unsorted_items(), key=attrgetter('order'))
        return cache[cache_key]


@implementer(IShopNavigationLink)
@adapter(Interface, IBrowserRequest)
class ShopNavigationLink(object):
    """Abstract shop navigation link.
    """
    id = None
    group = None
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

    def context_provides(self, context, interfaces=[]):
        """Return flag whether context provides one of the given interfaces.
        """
        for iface in interfaces:
            if iface.providedBy(context):
                return True
        return False

    def acquire_context(self, context, interfaces=[]):
        """Acquire next context parent providing one of the given interfaces.
        """
        if self.context_provides(context, interfaces=interfaces):
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
        return default_page.getDefaultPage() == context.getId()


@implementer(IShopNavigationGroup)
@adapter(Interface, IBrowserRequest)
class ShopNavigationGroup(NavigationItemLookupMixin):
    """Abstract shop navigation group.
    """
    id = None
    title = None
    order = 0

    @property
    def available(self):
        return bool(self.links())

    def links(self):
        for link in self.lookup_navigation_items(IShopNavigationLink):
            if link.display and link.group == self.id:
                yield link


@implementer(IShopNavigation)
class ShopNavigation(NavigationItemLookupMixin):
    """Mixin for shop navigation view.

    Subclass is usually view like and must provide ``context`` and ``request``
    """

    @property
    def available(self):
        return bool(self.links())

    def links(self):
        for link in self.lookup_navigation_items(IShopNavigationLink):
            if link.display:
                yield link

    def groups(self):
        for group in self.lookup_navigation_items(IShopNavigationGroup):
            if group.available:
                yield group


###############################################################################
# orders related
###############################################################################

class OrdersGroup(ShopNavigationGroup):
    id = 'shop_orders_group'
    title = _('orders', default=u'Orders')
    order = 10


class OrdersLink(ShopNavigationLink):
    """Link for navigating to ``Global Orders`` view.
    """
    id = 'shop_orders_link'
    group = 'shop_orders_group'
    permission = VIEW_ORDERS
    order = 10
    cssclass = 'orders'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[IVendor, ISite])
        # call super class constructor
        super(OrdersLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
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
    id = 'shop_orders_in_context_link'
    group = 'shop_orders_group'
    permission = VIEW_ORDERS
    title = _('orders_in_context', default=u'Orders in Context')
    order = 11
    cssclass = 'orders'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(OrdersInContextLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
            return
        # set target URL
        self.url = '{}/@@orders'.format(context.absolute_url())


class OrdersInContainerLink(OrdersInContextLink):
    """Link for navigating to ``Container Orders`` view.
    """
    id = 'shop_orders_in_container_link'
    group = 'shop_orders_group'
    title = _('orders_in_container', default=u'Orders in Container')
    order = 12

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if not self.context_is_default_page(context):
            self.display = False
            return
        # get container
        context = aq_parent(aq_inner(context))
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(OrdersInContainerLink, self).__init__(context, request)


class MyOrdersLink(ShopNavigationLink):
    """Link for navigating to ``My Orders`` view.
    """
    id = 'shop_myorders_link'
    group = 'shop_orders_group'
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

class BookingsGroup(ShopNavigationGroup):
    id = 'shop_bookings_group'
    title = _('bookings', default=u'Bookings')
    order = 20


class BookingsLink(ShopNavigationLink):
    """Link for navigating to ``Global Bookings`` view.
    """
    id = 'shop_bookings_link'
    group = 'shop_bookings_group'
    permission = VIEW_ORDERS
    order = 20
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[IVendor, ISite])
        # call super class constructor
        super(BookingsLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
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
    id = 'shop_bookings_in_context_link'
    group = 'shop_bookings_group'
    permission = VIEW_ORDERS
    title = _('bookings_in_context', default=u'Bookings in Context')
    order = 21
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(BookingsInContextLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
            return
        # set target URL
        self.url = '{}/@@bookings'.format(context.absolute_url())


class BookingsInContainerLink(BookingsInContextLink):
    """Link for navigating to ``Container Bookings`` view.
    """
    id = 'shop_bookings_in_container_link'
    group = 'shop_bookings_group'
    title = _('bookings_in_container', default=u'Bookings in Container')
    order = 22

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if not self.context_is_default_page(context):
            self.display = False
            return
        # get container
        context = aq_parent(aq_inner(context))
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(BookingsInContainerLink, self).__init__(context, request)


###############################################################################
# invoices related
###############################################################################

class InvoicesGroup(ShopNavigationGroup):
    id = 'shop_invoices_group'
    title = _('invoices', default=u'Invoices')
    order = 30


class InvoicesLink(ShopNavigationLink):
    """Link for navigating to ``Global Invoices`` view.
    """
    id = 'shop_invoices_link'
    group = 'shop_invoices_group'
    permission = VIEW_ORDERS
    order = 30
    cssclass = 'invoices'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[IVendor, ISite])
        # call super class constructor
        super(InvoicesLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
        # set title by context interface
        if IPloneSiteRoot.providedBy(context):
            self.title = _('invoices_global', default=u'Invoices (global)')
        elif ISite.providedBy(context):
            self.title = _('invoices_site', default=u'Invoices (site-wide)')
        elif IVendor.providedBy(context):
            self.title = _(
                'invoices_vendor',
                default=u'Invoices (vendor specific)'
            )
        # set target URL
        self.url = '{}/@@invoices'.format(context.absolute_url())


class InvoicesInContextLink(ShopNavigationLink):
    """Link for navigating to ``Context Invoices`` view.
    """
    id = 'shop_invoices_in_context_link'
    group = 'shop_invoices_group'
    permission = VIEW_ORDERS
    title = _('invoices_in_context', default=u'Invoices in Context')
    order = 31
    cssclass = 'invoices'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(InvoicesInContextLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
            return
        # set target URL
        self.url = '{}/@@invoices'.format(context.absolute_url())


class InvoicesInContainerLink(InvoicesInContextLink):
    """Link for navigating to ``Container Invoices`` view.
    """
    id = 'shop_invoices_in_container_link'
    group = 'shop_invoices_group'
    title = _('invoices_in_container', default=u'Invoices in Container')
    order = 32

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if not self.context_is_default_page(context):
            self.display = False
            return
        # get container
        context = aq_parent(aq_inner(context))
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(InvoicesInContainerLink, self).__init__(context, request)


class MyInvoicesLink(ShopNavigationLink):
    """Link for navigating to ``My Invoices`` view.
    """
    id = 'shop_myinvoices_link'
    group = 'shop_invoices_group'
    permission = VIEW_OWN_ORDERS
    title = _('my_invoices', default=u'My Invoices')
    order = 33
    cssclass = 'myinvoices'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(MyInvoicesLink, self).__init__(context, request)
        # set target URL
        self.url = '{}/@@myinvoices'.format(context.absolute_url())


###############################################################################
# contacts related
###############################################################################

class ContactsGroup(ShopNavigationGroup):
    id = 'shop_contacts_group'
    title = _('contacts', default=u'Contacts')
    order = 40


class ContactsLink(ShopNavigationLink):
    """Link for navigating to ``Contacts`` view.
    """
    id = 'shop_contacts_link'
    group = 'shop_contacts_group'
    permission = VIEW_ORDERS
    title = _('contacts', default=u'Contacts')
    order = 40
    cssclass = 'bookings'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[ISite])
        # call super class constructor
        super(ContactsLink, self).__init__(context, request)
        # check if authenticated user is vendor
        if self.display and not get_vendors_for():
            self.display = False
            return
        # set target URL
        self.url = '{}/@@contacts'.format(context.absolute_url())


###############################################################################
# export related
###############################################################################

class ExportGroup(ShopNavigationGroup):
    id = 'shop_export_group'
    title = _('export', default=u'Export')
    order = 50


class ExportOrdersLink(ShopNavigationLink):
    """Link for navigating to ``Export Orders`` view.
    """
    id = 'shop_export_orders_link'
    group = 'shop_export_group'
    permission = EXPORT_ORDERS
    title = _('exportorders', default=u'Export Orders')
    order = 50
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
    id = 'shop_export_orders_in_context_link'
    group = 'shop_export_group'
    permission = EXPORT_ORDERS
    title = _('exportorders_item', default=u'Export Orders on this Item')
    order = 51
    cssclass = 'export_orders_item'

    def __init__(self, context, request):
        # acquire desired context
        interfaces = [IBuyable, IFolder, ISite]
        context = self.acquire_context(context, interfaces=interfaces)
        # skip link if context is site
        if self.context_provides(context, interfaces=[ISite]):
            self.display = False
            return
        # call super class constructor
        super(ExportOrdersInContext, self).__init__(context, request)
        # do not display on site
        if self.display and ISite.providedBy(context):
            self.display = False
            return
        # check if buyables in context
        if self.display and not self.buyables_in_context(context):
            self.display = False
            return
        # set target URL
        self.url = '{}/@@exportorders_contextual'.format(
            context.absolute_url()
        )


class ExportOrdersInContainerLink(ExportOrdersInContext):
    """Link for navigating to ``Export Orders in Container`` view.
    """
    id = 'shop_export_orders_in_container_link'
    group = 'shop_export_group'
    title = _(
        'exportorders_in_container',
        default=u'Export Orders in Container'
    )
    order = 52

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if not self.context_is_default_page(context):
            self.display = False
            return
        # get container
        context = aq_parent(aq_inner(context))
        # skip link if context is site
        if self.context_provides(context, interfaces=[ISite]):
            self.display = False
            return
        # call super class constructor
        super(ExportOrdersInContainerLink, self).__init__(context, request)


###############################################################################
# mail templates related
###############################################################################

class MailTemaplatesGroup(ShopNavigationGroup):
    id = 'shop_mailtemplates_group'
    title = _('mailtemplates', default=u'Mail Templates')
    order = 60


class MailTemplatesLink(ShopNavigationLink):
    """Link for navigating to ``Mail Templates`` view.
    """
    id = 'shop_mail_templates_link'
    group = 'shop_mailtemplates_group'
    permission = MANAGE_TEAMPLETS
    order = 60
    cssclass = 'mailtemplates'

    def __init__(self, context, request):
        # acquire desired context
        context = self.acquire_context(context, interfaces=[IVendor, ISite])
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

class DiscountGroup(ShopNavigationGroup):
    id = 'shop_discount_group'
    title = _('discount', default=u'Discount')
    order = 70


class CartDiscountLink(ShopNavigationLink):
    """Link for navigating to ``Cart Discount`` view.
    """
    id = 'shop_cart_discount_link'
    group = 'shop_discount_group'
    permission = MANAGE_DISCOUNT
    title = _('cart_discount', default=u'Cart Discount')
    order = 70
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
    id = 'shop_item_discount_link'
    group = 'shop_discount_group'
    permission = MANAGE_DISCOUNT
    title = _('item_discount', default=u'Item Discount')
    order = 71
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
    id = 'shop_item_discount_in_container_link'
    group = 'shop_discount_group'
    title = _(
        'item_discount_in_container',
        default=u'Item Discount in Container'
    )
    order = 72

    def __init__(self, context, request):
        # check whether context is default page in folder
        self.request = request
        if not self.context_is_default_page(context):
            self.display = False
            return
        # get container
        context = aq_parent(aq_inner(context))
        # skip link if context is vendor or site
        if self.context_provides(context, interfaces=[IVendor, ISite]):
            self.display = False
            return
        # call super class constructor
        super(CartItemDiscountInContainerLink, self).__init__(context, request)


###############################################################################
# control panel related
###############################################################################

class AdministrationGroup(ShopNavigationGroup):
    id = 'shop_administration_group'
    title = _('administration', default=u'Administration')
    order = 80


class ControlPanelLink(ShopNavigationLink):
    """Link for navigating to ``Shop Control Panel`` view.
    """
    id = 'shop_control_panel_link'
    group = 'shop_administration_group'
    permission = MANAGE_SHOP
    order = 80
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
