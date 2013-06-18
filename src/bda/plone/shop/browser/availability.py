from zope.interface import implementer
from zope.component import adapter
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from bda.plone.cart.interfaces import (
    ICartItemAvailability,
    ICartItemStock,
)
from ..interfaces import IBuyable


CRITICAL_LIMIT = 5


@implementer(ICartItemAvailability)
@adapter(IBuyable)
class CartItemAvailability(object):
    """Default cart item availability display behavior
    """

    details_template = PageTemplateFile('availability_details.pt')

    def __init__(self, context):
        self.context = context

    @property
    def _stock(self):
        return ICartItemStock(self.context)

    @property
    def _available(self):
        return self._stock.available

    @property
    def _overbook(self):
        return self._stock.overbook

    def addable(self):
        return True

    def signal(self):
        return 'yellow'

    def details(self):
        return self.details_template(self)
