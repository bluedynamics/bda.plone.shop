# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from bda.plone.cart.cart import CartDataProviderBase
from bda.plone.cart.cartitem import CartItemStateBase
from bda.plone.cart.cartitem import get_item_data_provider
from bda.plone.cart.cartitem import get_item_preview
from bda.plone.cart.cartitem import get_item_state
from bda.plone.cart.cartitem import get_item_stock
from bda.plone.cart.cartitem import remove_item_from_cart
from bda.plone.cart.interfaces import IShippingItem
from bda.plone.shop import message_factory as _
from bda.plone.shop import permissions
from bda.plone.shop.interfaces import IBuyablePeriod
from bda.plone.shop.utils import get_shop_cart_settings
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_shipping_settings
from datetime import datetime
from decimal import Decimal
from plone import api
from zope.component import queryAdapter
from zope.i18n import translate

import warnings


# patch to define intermediate checkout view
CHECKOUT_INTERMEDIATE_VIEW = None


class CartItemCalculator(object):
    """Object for calculating cart item related data.
    """

    def __init__(self, context):
        msg = (
            "The use of ``CartItemCalculator`` is deprecated. "
            "Please use ``bda.plone.cart.get_data_provider`` instead. "
            "This class will be removed as of ``bda.plone.shop`` 1.0. "
        )
        warnings.warn(msg, DeprecationWarning)
        self.context = context

    @property
    def catalog(self):
        return api.portal.get_tool("portal_catalog")

    def item_net(self, item):
        """Net price of item.
        """
        uid, count, _ = item
        try:
            obj = api.content.get(UID=uid)
        except ValueError:
            return Decimal(0)
        data = get_item_data_provider(obj)
        discount_net = data.discount_net(count)
        item_net = Decimal(str(data.net)) - discount_net
        return item_net * count

    def item_vat(self, item):
        """VAT of item.
        """
        uid, count, _ = item
        try:
            obj = api.content.get(UID=uid)
        except ValueError:
            return Decimal(0)
        data = get_item_data_provider(obj)
        discount_net = data.discount_net(count)
        item_net = Decimal(str(data.net)) - discount_net
        return (item_net / Decimal(100)) * Decimal(str(data.vat)) * count

    def item_weight(self, item):
        """Weight of item.
        """
        uid, count, _ = item
        try:
            obj = api.content.get(UID=uid)
        except ValueError:
            return Decimal(0)
        shipping = IShippingItem(obj)
        item_weight = shipping.weight
        if item_weight:
            return Decimal(item_weight) * count
        return Decimal(0)

    def net(self, items):
        """Overall net of items.
        """
        net = Decimal(0)
        for uid, count, unused in items:
            try:
                obj = api.content.get(UID=uid)
            except ValueError:
                continue
            if obj is None:
                continue
            data = get_item_data_provider(obj)
            discount_net = data.discount_net(count)
            item_net = Decimal(str(data.net)) - discount_net
            net += item_net * count
        return net

    def vat(self, items):
        """Overall VAT of items.
        """
        vat = Decimal(0)
        for uid, count, unused in items:
            try:
                obj = api.content.get(UID=uid)
            except ValueError:
                continue
            if obj is None:
                continue
            data = get_item_data_provider(obj)
            discount_net = data.discount_net(count)
            item_net = Decimal(str(data.net)) - discount_net
            vat += (item_net / Decimal(100)) * Decimal(str(data.vat)) * count
        return vat

    def weight(self, items):
        """Overall weight of items.
        """
        weight = Decimal(0)
        for uid, count, unused in items:
            try:
                obj = api.content.get(UID=uid)
            except ValueError:
                continue
            if obj is None:
                continue
            shipping = IShippingItem(obj)
            item_weight = shipping.weight
            if item_weight:
                weight += Decimal(item_weight) * count
        return weight


class CartDataProvider(CartItemCalculator, CartDataProviderBase):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def currency(self):
        return get_shop_settings().currency

    @property
    def hide_cart_if_empty(self):
        return get_shop_cart_settings().hide_cart_if_empty

    @property
    def max_artice_count(self):
        return get_shop_cart_settings().max_artice_count

    @property
    def disable_max_article(self):
        return get_shop_cart_settings().disable_max_article

    @property
    def summary_total_only(self):
        return get_shop_cart_settings().summary_total_only

    @property
    def shipping_method(self):
        settings = get_shop_shipping_settings()
        # read from cookie and return if present and available
        shipping_method = self.request.cookies.get("shipping_method")
        if shipping_method:
            if shipping_method in settings.available_shipping_methods:
                return shipping_method
        # return default shipping method
        return settings.shipping_method

    @property
    def checkout_url(self):
        view_name = '@@checkout'
        # case anonymous user is permitted to perform checkout and intermediate
        # view is defined. can be used to ask user to login before checkout
        if api.user.is_anonymous() and CHECKOUT_INTERMEDIATE_VIEW:
            view_name = CHECKOUT_INTERMEDIATE_VIEW
        return "{0}{1}".format(
            api.portal.get_navigation_root(self.context).absolute_url(),
            view_name
        )

    @property
    def cart_url(self):
        return "%s/@@cart" % self.context.absolute_url()

    @property
    def show_to_cart(self):
        return get_shop_cart_settings().show_to_cart

    @property
    def show_checkout(self):
        return get_shop_cart_settings().show_checkout

    @property
    def show_currency(self):
        return get_shop_settings().show_currency

    def validate_set(self, uid):
        try:
            buyable = api.content.get(UID=uid)
        except ValueError:
            message = _(
                u"buyable_does_not_exist",
                default=u"Buyable item with UID {uuid} does not exist.",
                mapping={"uuid": uid},
            )
            return {"success": False, "error": message, "update": True}
        # check whether user can modify cart
        if not api.user.has_permission(permissions.ModifyCart, obj=buyable):
            remove_item_from_cart(self.request, uid)
            message = _(
                u"permission_not_granted_to_buy_item",
                default=u"Permission to buy ${title} not granted.",
                mapping={"title": buyable.Title()},
            )
            message = translate(message, context=self.request)
            return {"success": False, "error": message, "update": True}
        # check buyable period
        buyable_period = queryAdapter(buyable, IBuyablePeriod)
        if buyable_period:
            now = datetime.now()
            # effective date not reached yet
            effective = buyable_period.effective
            if effective and now < effective:
                remove_item_from_cart(self.request, uid)
                message = _("item_not_buyable_yet", default=u"Item not buyable yet")
                message = translate(message, context=self.request)
                return {"success": False, "error": message, "update": True}
            # expires date exceed
            expires = buyable_period.expires
            if expires and now > expires:
                remove_item_from_cart(self.request, uid)
                message = _("item_no_longer_buyable", default=u"Item no longer buyable")
                message = translate(message, context=self.request)
                return {"success": False, "error": message, "update": True}
        return {"success": True, "error": ""}

    def cart_items(self, items):
        ret = list()
        sm = getSecurityManager()
        for uid, count, comment in items:
            try:
                obj = api.content.get(UID=uid)
            except ValueError:
                remove_item_from_cart(self.request, uid)
                continue
            if obj is None:
                remove_item_from_cart(self.request, uid)
                continue
            if not sm.checkPermission(permissions.ModifyCart, obj):
                remove_item_from_cart(self.request, uid)
                continue
            buyable_period = queryAdapter(obj, IBuyablePeriod)
            if buyable_period:
                now = datetime.now()
                effective = buyable_period.effective
                if effective and now < effective:
                    remove_item_from_cart(self.request, uid)
                    continue
                expires = buyable_period.expires
                if expires and now > expires:
                    remove_item_from_cart(self.request, uid)
                    continue
            data = get_item_data_provider(obj)
            discount_net = data.discount_net(count)
            price = (Decimal(str(data.net)) - discount_net) * count
            discount = discount_net * count
            if data.display_gross:
                price = price + price / Decimal(100) * Decimal(str(data.vat))
                discount = discount + discount / Decimal(100) * Decimal(str(data.vat))
            url = obj.absolute_url()
            quantity_unit = translate(data.quantity_unit, context=self.request)
            item_state = get_item_state(obj, self.request)
            ret.append(
                self.item(
                    uid=uid,
                    title=data.title,
                    count=count,
                    price=price,
                    url=url,
                    comment=comment,
                    description=obj.description,
                    comment_enabled=data.comment_enabled,
                    comment_required=data.comment_required,
                    quantity_unit_float=data.quantity_unit_float,
                    quantity_unit=quantity_unit,
                    preview_image_url=get_item_preview(obj).url,
                    no_longer_available=not item_state.validate_count(count),
                    alert=item_state.alert(count),
                    discount=discount * Decimal(-1) if discount else Decimal(0),
                )
            )
        return ret


class CartItemState(CartItemStateBase):
    # XXX: cart item state needs love how to display item warnings.
    #      only display warning on effected items.

    @property
    def completely_exceeded_alert(self):
        message = _(
            u"alert_item_no_longer_available",
            default=u"No longer available, please " u"remove from cart",
        )
        return translate(message, context=self.request)

    @property
    def some_reservations_alert(self):
        message = _(u"alert_item_some_reserved", default=u"Partly reserved")
        return translate(message, context=self.request)

    def partly_exceeded_alert(self, exceed, quantity_unit):
        message = _(
            u"alert_item_number_exceed",
            default=u"Limit exceed by ${exceed} ${quantity_unit}",
            mapping={"exceed": exceed, "quantity_unit": quantity_unit},
        )
        return translate(message, context=self.request)

    def number_reservations_alert(self, reserved, quantity_unit):
        message = _(
            u"alert_item_number_reserved",
            default=u"${reserved} ${quantity_unit} reserved",
            mapping={"reserved": reserved, "quantity_unit": quantity_unit},
        )
        return translate(message, context=self.request)

    def alert(self, count):
        stock = get_item_stock(self.context)
        # stock not applied
        if stock is None:
            return ""
        available = stock.available
        # no limitation
        if available is None:
            return ""
        reserved = self.reserved
        exceed = self.exceed
        # no reservations and no exceed
        if not reserved and not exceed:
            # no message
            return ""
        item_data = get_item_data_provider(self.context)
        quantity_unit = item_data.quantity_unit
        quantity_unit_float = item_data.quantity_unit_float

        def display_format(num):
            if quantity_unit_float:
                return num
            return int(num)

        # exceed
        if exceed:
            remaining_available = self.remaining_available
            # partly exceeded
            if remaining_available > 0:
                return self.partly_exceeded_alert(display_format(exceed), quantity_unit)
            # completely exceeded
            return self.completely_exceeded_alert
        # reservations
        if reserved:
            aggregated_count = float(self.aggregated_count)
            count = float(count)
            # some reservations message
            if aggregated_count > count:
                return self.some_reservations_alert
            # number reservations message
            else:
                return self.number_reservations_alert(
                    display_format(reserved), quantity_unit
                )
        return ""
