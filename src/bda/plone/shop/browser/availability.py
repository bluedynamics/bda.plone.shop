from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.cart import CartItemAvailabilityBase


class CartItemAvailability(CartItemAvailabilityBase):
    details_template = ViewPageTemplateFile('availability_details.pt')

    def details(self):
        return self.details_template(self)

    @property
    def not_available(self):
        return not self.addable

    @property
    def full_available(self):
        available = self.available
        if available is None:
            return True
        return available > self.critical_limit

    @property
    def critical_available(self):
        available = self.available
        if available is None:
            return False
        return available > 0 and available <= self.critical_limit

    @property
    def overbook_available(self):
        available = self.available
        if available is None or available > 0:
            return False
        overbook = self.overbook
        if overbook is None:
            return True
        return available > self.overbook * -1
