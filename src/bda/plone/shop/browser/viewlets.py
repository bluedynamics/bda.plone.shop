# -*- coding: utf-8 -*-
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from plone.app.layout.viewlets.common import ViewletBase
from bda.plone.cart.interfaces import ICartItemDataProvider
from bda.plone.cart.browser import DataProviderMixin


_ = MessageFactory('bda.plone.shop')


class BuyableViewlet(ViewletBase, DataProviderMixin):
    """Vielet rendering buyable information.
    """
    
    @property
    def data(self):
        return ICartItemDataProvider(self.context)
    
    @property
    def currency(self):
        return self.data_provider.currency
    
    @property
    def item_uid(self):
        return self.context.UID()
    
    @property
    def item_net(self):
        return self.data.net
    
    @property
    def item_vat(self):
        return self.data.vat
    
    @property
    def item_gross(self):
        return self.item_net + self.item_net / 100 * self.item_vat
    
    @property
    def display_gross(self):
        return self.data.display_gross
    
    @property
    def comment_enabled(self):
        return self.data.comment_enabled
    
    @property
    def comment_required(self):
        return self.data.comment_required
    
    @property
    def quantity_unit_float(self):
        return self.data.quantity_unit_float
    
    @property
    def quantity_label(self):
        return translate(_(self.data.quantity_label), context=self.request)
