from zope.interface import implementer
from zope.component import adapter
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from bda.plone.cart import CartItemAvailabilityBase
from bda.plone.cart.interfaces import (
    ICartItemAvailability,
    ICartItemStock,
)
from ..interfaces import IBuyable


class CartItemAvailability(CartItemAvailabilityBase):
    details_template = PageTemplateFile('availability_details.pt')

    def details(self):
        return self.details_template(view=self)
