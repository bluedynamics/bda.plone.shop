from zope.interface import implementer
from zope.component import adapter
from bda.plone.cart.interfaces import ICartItemAvailability
from ..interfaces import IBuyable


@implementer(ICartItemAvailability)
@adapter(IBuyable)
class CartItemAvailability(object):

    def __init__(self, context):
        self.context = context

    def signal(self):
        return 'yellow'

    def details(self):
        return '<strong>hallo</strong>'
