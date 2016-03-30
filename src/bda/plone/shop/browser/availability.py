# -*- coding: utf-8 -*-
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.cart import CartItemAvailabilityBase
from bda.plone.cart import get_item_data_provider
from bda.plone.cart import get_item_delivery
from bda.plone.cart import get_item_state
from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IBuyablePeriod
from datetime import datetime
from zope.component import queryAdapter


class CartItemAvailability(CartItemAvailabilityBase):
    details_template = ViewPageTemplateFile('availability_details.pt')

    def details(self):
        return self.details_template(self)

    @property
    def within_buyable_period(self):
        buyable_period = queryAdapter(self.context, IBuyablePeriod)
        # no buyable period defined, always buyable
        if not buyable_period:
            return True
        now = datetime.now()
        effective = buyable_period.effective
        # effective date not reached yet
        if effective and effective >= now:
            return False
        expires = buyable_period.expires
        # expires date already reached
        if expires and expires <= now:
            return False
        return True

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
    def delivery_duration(self):
        return get_item_delivery(self.context).delivery_duration

    @property
    def purchasable_until(self):
        expires = queryAdapter(self.context, IBuyablePeriod).expires
        return bool(expires) and self.addable

    @property
    def not_effective_yet(self):
        effective = queryAdapter(self.context, IBuyablePeriod).effective
        now = datetime.now()
        return effective and effective >= now or False

    @property
    def already_expired(self):
        expires = queryAdapter(self.context, IBuyablePeriod).expires
        now = datetime.now()
        return expires and expires <= now or False

    @property
    def full_available_message(self):
        available = self.available
        if available is None:
            available = ''
        else:
            if not get_item_data_provider(self.context).quantity_unit_float:
                available = int(available)
        message = _(u'full_available_message',
                    default=u'${available} items(s) available.',
                    mapping={'available': available})
        return message

    @property
    def critical_available_message(self):
        available = self.available
        if not get_item_data_provider(self.context).quantity_unit_float:
            available = int(available)
        message = _(u'critical_available_message',
                    default=u'Just ${available} items(s) left.',
                    mapping={'available': available})
        return message

    @property
    def overbook_available_message(self):
        state = get_item_state(self.context, self.request)
        overbook = self.stock.overbook
        if overbook is None:
            reservable = ''
        else:
            reservable = overbook - state.reserved
            if not get_item_data_provider(self.context).quantity_unit_float:
                reservable = int(reservable)
        message = _(u'overbook_available_message',
                    default=u'Item is sold out. You can pre-order '
                            u'${reservable} items. As soon as item is '
                            u'available again, it gets delivered.',
                    mapping={'reservable': reservable})
        return message

    @property
    def purchasable_until_message(self):
        date = ulocalized_time(
            queryAdapter(self.context, IBuyablePeriod).expires,
            long_format=1,
            context=self.context,
            request=self.request,
        )
        message = _(u'purchasable_until_message',
                    default=u'Item is purchasable until ${date}',
                    mapping={'date': date})
        return message

    @property
    def purchasable_as_of_message(self):
        date = ulocalized_time(
            queryAdapter(self.context, IBuyablePeriod).effective,
            long_format=1,
            context=self.context,
            request=self.request,
        )
        message = _(u'purchasable_as_of_message',
                    default=u'Item is purchasable as of ${date}',
                    mapping={'date': date})
        return message
