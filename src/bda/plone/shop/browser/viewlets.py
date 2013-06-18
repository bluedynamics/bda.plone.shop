# -*- coding: utf-8 -*-
from zope.i18n import translate
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.cart import (
    get_data_provider,
    get_item_data_provider,
    get_item_availability,
)
from bda.plone.cart.browser import DataProviderMixin


class BuyableViewlet(ViewletBase, DataProviderMixin):
    """Vielet rendering buyable information.
    """

    index = ViewPageTemplateFile('buyable.pt')

    @property
    def _cart_data(self):
        return get_data_provider(self.context)

    @property
    def _item_data(self):
        return get_item_data_provider(self.context)

    @property
    def _item_availability(self):
        return get_item_availability(self.context)

    @property
    def availability_signal(self):
        return self._item_availability.signal

    @property
    def availability_details(self):
        return self._item_availability.details

    @property
    def item_addable(self):
        return self._item_availability.addable

    @property
    def currency(self):
        return self._cart_data.currency

    @property
    def item_uid(self):
        return self.context.UID()

    @property
    def item_net(self):
        return self._item_data.net

    @property
    def item_vat(self):
        return self._item_data.vat

    @property
    def item_gross(self):
        return self.item_net + self.item_net / 100 * self.item_vat

    @property
    def display_gross(self):
        return self._item_data.display_gross

    @property
    def comment_enabled(self):
        return self._item_data.comment_enabled

    @property
    def comment_required(self):
        return self._item_data.comment_required

    @property
    def quantity_unit_float(self):
        return self._item_data.quantity_unit_float

    @property
    def quantity_unit(self):
        return translate(self._item_data.quantity_unit, context=self.request)
