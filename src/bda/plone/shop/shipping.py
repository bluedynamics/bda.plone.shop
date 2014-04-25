from bda.plone.shipping import Shipping
from bda.plone.shop import message_factory as _
from bda.plone.shop.cartdata import CartItemCalculator
from bda.plone.shop.utils import get_shop_shipping_settings
from decimal import Decimal
from zope.deprecation import deprecated


class ShippingBase(Shipping):
    """Abstract shipping.
    """

    @property
    def settings(self):
        return get_shop_shipping_settings()

    @property
    def available(self):
        return self.sid in self.settings.available_shipping_methods

    @property
    def default(self):
        return self.sid == self.settings.shipping_method


class DefaultShipping(ShippingBase, CartItemCalculator):
    sid = 'default_shipping'
    label = _('default_shipping', 'Default Shipping')

    def calculate(self, items):
        """XXX: calculation from net price. Currently shipping gets calculated
        from gross only.
        """
        settings = self.settings
        free_shipping_limit = Decimal(settings.free_shipping_limit)
        # cart price exceeds free shipping limit, no shipping costs
        if self.net(items) + self.vat(items) > free_shipping_limit:
            return Decimal(0)
        flat_shipping_cost = Decimal(settings.flat_shipping_cost)
        item_shipping_cost = Decimal(settings.item_shipping_cost)
        shipping_costs = Decimal(0)
        # item shipping costs set, calculate for contained cart items
        if item_shipping_cost > Decimal(0):
            for item in items:
                shipping_costs += self.item_net(item) + self.item_vat(item)
        # item shipping costs exceed flat shipping costs
        if shipping_costs > flat_shipping_cost:
            return shipping_costs
        # flat shipping costs apply
        return Decimal(flat_shipping_cost)


###############################################################################
# B/C - will be removed in ``bda.plone.shop`` 1.0
###############################################################################

FREE_SHIPPING_LIMIT = 200
FLAT_SHIPPING_COST = 10


class FlatRate(ShippingBase, CartItemCalculator):
    sid = 'flat_rate'
    label = _('flat_rate', 'Flat Rate')

    def calculate(self, items):
        if self.net(items) + self.vat(items) > Decimal(FREE_SHIPPING_LIMIT):
            return Decimal(0)
        return Decimal(FLAT_SHIPPING_COST)


deprecated('FlatRate', """``FlatRate`` shipping is deprecated as of
``bda.plone.shop`` 0.7 and will be removed in ``bda.plone.shop`` 1.0. Use
``DefaultShipping`` instead which provides the same functionality.""")
