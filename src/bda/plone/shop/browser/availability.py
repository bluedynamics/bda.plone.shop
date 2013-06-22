from zope.i18nmessageid import MessageFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.cart import CartItemAvailabilityBase


_ = MessageFactory('bda.plone.shop')


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

    @property
    def full_available_message(self):
        # XXX: quantity unit float
        message = _(u'full_available_message',
                    default=u'${available} items(s) available.',
                    mapping={'available': self.available})
        return message

    @property
    def critical_available_message(self):
        # XXX: quantity unit float
        message = _(u'critical_available_message',
                    default=u'Just ${available} items(s) left.',
                    mapping={'available': self.available})
        return message

    @property
    def overbook_available_message(self):
        # XXX: quantity unit float
        state = get_item_state(self.context, self.request)
        reservable = self.stock.overbook - state.reserved
        message = _(u'overbook_available_message',
                    default=u'Item is sold out. You can pre-order '
                            u'${reservable} items. As soon as item is '
                            u'available again, it gets delivered.',
                    mapping={'reservable': reservable})
        return message
