# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Products.Five import BrowserView
from bda.plone.cart import get_data_provider
from bda.plone.cart import get_item_availability
from bda.plone.cart import get_item_data_provider
from bda.plone.cart.browser import DataProviderMixin
from bda.plone.shop import permissions
from bda.plone.shop.interfaces import IBuyablePeriod
from datetime import datetime
from decimal import Decimal
from plone.uuid.interfaces import IUUID
from zope.component import queryAdapter
from zope.i18n import translate


class BuyableControls(BrowserView, DataProviderMixin):

    @property
    def _cart_data(self):
        return get_data_provider(self.context, self.request)

    @property
    def _item_data(self):
        return get_item_data_provider(self.context)

    @property
    def _item_availability(self):
        return get_item_availability(self.context, self.request)

    @property
    def can_view_buyable_info(self):
        sm = getSecurityManager()
        return sm.checkPermission(permissions.ViewBuyableInfo, self.context)

    @property
    def can_buy_items(self):
        buyable_period = queryAdapter(self.context, IBuyablePeriod)
        if buyable_period:
            now = datetime.now()
            effective = buyable_period.effective
            if effective and now <= effective:
                return False
            expires = buyable_period.expires
            if expires and now >= expires:
                return False
        sm = getSecurityManager()
        return sm.checkPermission(permissions.BuyItems, self.context)

    @property
    def show_available(self):
        return self._item_availability.display

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
        return IUUID(self.context)

    @property
    def item_vat(self):
        vat = self._item_data.vat
        if vat % 2 != 0:
            return Decimal(vat).quantize(Decimal('1.0'))
        return Decimal(vat)

    @property
    def item_net_original(self):
        return Decimal(self._item_data.net)

    @property
    def item_net(self):
        return Decimal(self._item_data.net) - \
            self._item_data.discount_net(Decimal(1))

    @property
    def item_gross_original(self):
        net = self.item_net_original
        return net + net / Decimal(100) * self.item_vat

    @property
    def item_gross(self):
        net = self.item_net
        return net + net / Decimal(100) * self.item_vat

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

    def not_eq(self, v_1, v_2):
        return v_1.quantize(Decimal('1.000')) != v_2.quantize(Decimal('1.000'))

    def __call__(self, *args):
        if '_' in self.request.form:
            self.request.response.setHeader('X-Theme-Disabled', 'True')
        return super(BuyableControls, self).__call__()
