from decimal import Decimal
from bda.plone.shipping import FlatRate as FlatRateBase
from .cartdata import CartItemCalculator
from .utils import get_shop_shipping_settings

from . import message_factory as _

class FlatRate(FlatRateBase, CartItemCalculator):

    def calculate(self, items):
        flat_shipping_minimum =  get_shop_shipping_settings().flat_shipping_minimum
        flat_shipping_limit   =  get_shop_shipping_settings().flat_shipping_limit
        
        if self.net(items) + self.vat(items) > Decimal(flat_shipping_limit):
                return Decimal(0)
        return Decimal(flat_shipping_minimum)
        
        
class ItemRate(FlatRateBase, CartItemCalculator):
	sid = 'item_rate'
	label = _('item_rate', 'Item Rate')
	available = True
	default = False
	
	def calculate(self, items):
		flat_shipping_minimum =  get_shop_shipping_settings().flat_shipping_minimum
		flat_shipping_limit   =  get_shop_shipping_settings().flat_shipping_limit
		flat_shipping_cost    =  get_shop_shipping_settings().item_shipping_cost
		
		if self.net(items) + self.vat(items) > Decimal(flat_shipping_limit):
			return Decimal(0)
		if flat_shipping_minimum > Decimal(flat_shipping_cost * self.item_count(items)):
		    return Decimal(flat_shipping_minimum)
		return Decimal(flat_shipping_cost * self.item_count(items))
