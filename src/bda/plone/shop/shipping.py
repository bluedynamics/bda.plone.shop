# -*- coding: utf-8 -*-
from bda.plone.cart import CURRENCY_LITERALS
from bda.plone.cart import cart_item_free_shipping
from bda.plone.cart import cart_item_shippable
from bda.plone.cart import get_data_provider
from bda.plone.shipping import Shipping
from bda.plone.shipping.interfaces import IShippingSettings
from bda.plone.shop import message_factory as _
from bda.plone.shop.utils import format_amount
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_shipping_settings
from decimal import Decimal
from zope.component import adapter
from zope.deprecation import deprecated
from zope.i18nmessageid import Message
from zope.interface import Interface
from zope.interface import implementer


@implementer(IShippingSettings)
@adapter(Interface)
class ShippingSettings(object):

    def __init__(self, context):
        self.context = context

    @property
    def available(self):
        settings = get_shop_shipping_settings()
        return settings.available_shipping_methods

    @property
    def default(self):
        settings = get_shop_shipping_settings()
        return settings.shipping_method


class DefaultShipping(Shipping):
    sid = 'default_shipping'
    label = _('default_shipping', default='Default Shipping')

    @property
    def description(self):
        settings = get_shop_shipping_settings()
        currency = get_shop_settings().currency
        show_currency = get_shop_settings().show_currency
        if show_currency == 'symbol':
            currency = CURRENCY_LITERALS[currency]
        shipping_limit_from_gross = settings.shipping_limit_from_gross
        free_shipping_limit = Decimal(str(settings.free_shipping_limit))
        flat_shipping_cost = Decimal(str(settings.flat_shipping_cost))
        item_shipping_cost = Decimal(str(settings.item_shipping_cost))
        shipping_vat = Decimal(str(settings.shipping_vat))

        def gross(val):
            return format_amount(val + (val / Decimal(100) * shipping_vat))

        # no shipping costs
        if not flat_shipping_cost and not item_shipping_cost:
            return _(u"free_shipping", default=u"Free Shipping")
        # no free shipping limit
        if not free_shipping_limit:
            # flat and item costs defined
            if flat_shipping_cost and item_shipping_cost:
                msg = _(u"no_free_shipping_flat_and_item",
                        default=u"Minimum ${flat} ${currency} or ${item} "
                                u"${currency} per item in cart")
                return Message(msg, mapping={
                    'flat': gross(flat_shipping_cost),
                    'item': gross(item_shipping_cost),
                    'currency': currency,
                })
            # flat costs only
            if flat_shipping_cost and not item_shipping_cost:
                msg = _(u"no_free_shipping_flat_only",
                        default=u"Flat ${flat} ${currency}")
                return Message(msg, mapping={
                    'flat': gross(flat_shipping_cost),
                    'currency': currency,
                })
            # item costs only
            if not flat_shipping_cost and item_shipping_cost:
                msg = _(u"no_free_shipping_item_only",
                        default=u"${item} ${currency} per item in cart")
                return Message(msg, mapping={
                    'item': gross(item_shipping_cost),
                    'currency': currency,
                })
        # free shipping above limit
        # flat and item costs defined
        if flat_shipping_cost and item_shipping_cost:
            # from gross
            if shipping_limit_from_gross:
                msg = _(u"free_shipping_limit_flat_and_item_gross",
                        default=u"Minimum ${flat} ${currency} or "
                                u"${item} ${currency} per item in cart. Free "
                                u"shipping if gross purchase price above "
                                u"${limit} ${currency}")
            # from net
            else:
                msg = _(u"free_shipping_limit_flat_and_item_net",
                        default=u"Minimum ${flat} ${currency} or "
                                u"${item} ${currency} per item in cart. Free "
                                u"shipping if net purchase price above "
                                u"${limit} ${currency}")
            return Message(msg, mapping={
                'flat': gross(flat_shipping_cost),
                'item': gross(item_shipping_cost),
                'limit': format_amount(free_shipping_limit),
                'currency': currency,
            })
        # flat costs only
        if flat_shipping_cost and not item_shipping_cost:
            # from gross
            if shipping_limit_from_gross:
                msg = _(u"free_shipping_limit_flat_only_gross",
                        default=u"Flat ${flat} ${currency}. Free "
                                u"shipping if gross purchase price above "
                                u"${limit} ${currency}")
            # from net
            else:
                msg = _(u"free_shipping_limit_flat_only_net",
                        default=u"Flat ${flat} ${currency}. Free "
                                u"shipping if net purchase price above "
                                u"${limit} ${currency}")
            return Message(msg, mapping={
                'flat': gross(flat_shipping_cost),
                'limit': format_amount(free_shipping_limit),
                'currency': currency,
            })
        # item costs only
        if not flat_shipping_cost and item_shipping_cost:
            # from gross
            if shipping_limit_from_gross:
                msg = _(u"free_shipping_limit_item_only_gross",
                        default=u"${item} ${currency} per item in "
                                u"cart. Free shipping if gross purchase "
                                u"price above ${limit} ${currency}")
            # from net
            else:
                msg = _(u"free_shipping_limit_item_only_net",
                        default=u"${item} ${currency} per item in "
                                u"cart. Free shipping if net purchase "
                                u"price above ${limit} ${currency}")
            return Message(msg, mapping={
                'item': gross(item_shipping_cost),
                'limit': format_amount(free_shipping_limit),
                'currency': currency,
            })

    def net(self, items):
        settings = get_shop_shipping_settings()
        cart_data = get_data_provider(self.context)
        shipping_limit_from_gross = settings.shipping_limit_from_gross
        free_shipping_limit = Decimal(str(settings.free_shipping_limit))
        purchase_price = Decimal(0)
        # calculate shipping from gross
        if shipping_limit_from_gross:
            purchase_price += cart_data.net(items) + cart_data.vat(items)
        # calculate shipping from net
        else:
            purchase_price += cart_data.net(items)
        # purchase price exceeds free shipping limit, no shipping costs
        if free_shipping_limit and purchase_price > free_shipping_limit:
            return Decimal(0)
        flat_shipping_cost = Decimal(str(settings.flat_shipping_cost))
        item_shipping_cost = Decimal(str(settings.item_shipping_cost))
        # flag whether all items have free shipping flag set
        all_items_free_shipping = True
        shipping_costs = Decimal(0)
        # item shipping costs set, calculate for contained cart items
        if item_shipping_cost > Decimal(0):
            for item in items:
                # ignore item if not shippable
                if not cart_item_shippable(self.context, item):
                    continue
                # ignore item if free shipping set
                if cart_item_free_shipping(self.context, item):
                    continue
                # as soon as one item in cart has no free shipping,
                # all_items_free_shipping is False
                all_items_free_shipping = False
                shipping_costs += item_shipping_cost * item[1]
        # calculate flat shipping costs anyway if no item shipping costs
        else:
            all_items_free_shipping = False
        # consider flat shipping cost if set, gets ignored if all items
        # have free shipping set
        if flat_shipping_cost and not all_items_free_shipping:
            # item shipping costs exceed flat shipping costs
            if shipping_costs > flat_shipping_cost:
                return shipping_costs
            # flat shipping costs apply
            return Decimal(flat_shipping_cost)
        # return calculated shipping costs
        return shipping_costs

    def vat(self, items):
        settings = get_shop_shipping_settings()
        shipping_vat = Decimal(str(settings.shipping_vat))
        return self.net(items) / Decimal(100) * shipping_vat


class CashAndCarryShipping(Shipping):
    sid = 'cash_and_carry'
    label = _('cash_and_carry', default='Cash and Carry')

    @property
    def description(self):
        return _('cash_and_carry_descripton',
                 default='Customer picks up goods at dealer\'s place')

    def net(self, items):
        return Decimal('0')

    def vat(self, items):
        return Decimal('0')


###############################################################################
# B/C - will be removed in ``bda.plone.shop`` 1.0
###############################################################################

FREE_SHIPPING_LIMIT = 200
FLAT_SHIPPING_COST = 10


class FlatRate(Shipping):
    sid = 'flat_rate'
    label = _('flat_rate', 'Flat Rate')

    def calculate(self, items):
        cart_data = get_data_provider(self.context)
        limit = FREE_SHIPPING_LIMIT
        if cart_data.net(items) + cart_data.vat(items) > Decimal(limit):
            return Decimal(0)
        return Decimal(FLAT_SHIPPING_COST)


deprecated(
    'FlatRate',
    "'FlatRate' shipping is deprecated as of 'bda.plone.shop' 0.7 and "
    "will be removed in 'bda.plone.shop' 1.0. Use 'DefaultShipping' "
    "instead which provides the same functionality."
)
