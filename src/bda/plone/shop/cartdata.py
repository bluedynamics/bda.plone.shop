from decimal import Decimal
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from Products.CMFCore.utils import getToolByName
from bda.plone.shipping.interfaces import IShippingItem
from bda.plone.cart import (
    readcookie,
    extractitems,
    aggregate_cart_item_count,
    get_item_data_provider,
    get_item_stock,
    get_item_state,
    get_item_preview,
    CartDataProviderBase,
    CartItemStateBase,
)
from .utils import (
    get_shop_settings,
    get_shop_cart_settings,
    get_shop_shipping_settings,
)


_ = MessageFactory('bda.plone.shop')


class CartItemCalculator(object):

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def net(self, items):
        cat = self.catalog
        net = Decimal(0)
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = get_item_data_provider(brain[0].getObject())
            net += Decimal(str(data.net)) * count
        return net

    def vat(self, items):
        cat = self.catalog
        vat = Decimal(0)
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = get_item_data_provider(brain[0].getObject())
            vat += (Decimal(str(data.net)) / Decimal(100)) \
                   * Decimal(str(data.vat)) * count
        return vat

    def weight(self, items):
        cat = self.catalog
        weight = Decimal(0)
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            shipping = IShippingItem(brain[0].getObject())
            item_weight = shipping.weight
            if item_weight:
                weight += Decimal(item_weight) * count
        return weight


class CartDataProvider(CartItemCalculator, CartDataProviderBase):

    def cart_items(self, items):
        cat = self.catalog
        ret = list()
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            brain = brain[0]
            obj = brain.getObject()
            title = brain.Title
            data = get_item_data_provider(obj)
            price = Decimal(str(data.net)) * count
            if data.display_gross:
                price = price + price / Decimal(100) * Decimal(str(data.vat))
            url = brain.getURL()
            description = brain.Description
            comment_required = data.comment_required
            quantity_unit_float = data.quantity_unit_float
            quantity_unit = translate(data.quantity_unit, context=self.request)
            preview_image_url = get_item_preview(obj).url
            item_state = get_item_state(obj, self.request)
            no_longer_available = not item_state.validate_count(count)
            alert = item_state.alert(count)
            item = self.item(
                uid, title, count, price, url, comment, description,
                comment_required, quantity_unit_float, quantity_unit,
                preview_image_url, no_longer_available, alert)
            ret.append(item)
        return ret

    @property
    def currency(self):
        return get_shop_settings().currency

    @property
    def show_checkout(self):
        return get_shop_cart_settings().show_checkout

    @property
    def show_to_cart(self):
        return get_shop_cart_settings().show_to_cart

    @property
    def show_currency(self):
        return get_shop_settings().show_currency

    @property
    def disable_max_article(self):
        return get_shop_cart_settings().disable_max_article

    @property
    def summary_total_only(self):
        return get_shop_cart_settings().summary_total_only

    @property
    def include_shipping_costs(self):
        return get_shop_shipping_settings().include_shipping_costs

    @property
    def shipping_method(self):
        return get_shop_shipping_settings().shipping_method

    @property
    def checkout_url(self):
        return '%s/@@checkout' % self.context.absolute_url()


class CartItemState(CartItemStateBase):

    @property
    def completely_exceeded_alert(self):
        message = _(u'alert_item_no_longer_available',
                    default=u'No longer available, please '
                            u'remove from cart')
        return translate(message, context=self.request)

    @property
    def some_reservations_alert(self):
        message = _(u'alert_item_some_reserved',
                    default=u'Partly reserved')
        return translate(message, context=self.request)

    def partly_exceeded_alert(self, exceed, quantity_unit):
        message = _(u'alert_item_number_exceed',
                    default=u'Limit exceed by ${exceed} ${quantity_unit}',
                    mapping={'exceed': exceed,
                             'quantity_unit': quantity_unit})
        return translate(message, context=self.request)

    def number_reservations_alert(self, reserved, quantity_unit):
        message = _(u'alert_item_number_reserved',
                    default=u'${reserved} ${quantity_unit} reserved',
                    mapping={'reserved': reserved,
                             'quantity_unit': quantity_unit})
        return translate(message, context=self.request)

    def alert(self, count):
        stock = get_item_stock(self.context)
        available = stock.available
        # no limitation
        if available is None:
            return ''
        reserved = self.reserved
        exceed = self.exceed
        # no reservations and no exceed
        if not reserved and not exceed:
            # no message
            return ''
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
                return self.partly_exceeded_alert(
                    display_format(exceed), quantity_unit)
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
                    display_format(reserved), quantity_unit)
        return ''
