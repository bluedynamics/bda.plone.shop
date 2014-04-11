from decimal import Decimal
from bda.plone.shipping import FlatRate as FlatRateBase
from bda.plone.shop.cartdata import CartItemCalculator


FREE_SHIPPING_LIMIT = 200
FLAT_SHIPPING_COST = 10


class FlatRate(FlatRateBase, CartItemCalculator):

    def calculate(self, items):
        if self.net(items) + self.vat(items) > Decimal(FREE_SHIPPING_LIMIT):
            return Decimal(0)
        return Decimal(FLAT_SHIPPING_COST)
