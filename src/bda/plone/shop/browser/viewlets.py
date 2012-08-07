# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase
from ..interfaces import IBuyableDataProvider


class BuyableViewlet(ViewletBase):
    """Vielet rendering buyable information.
    """
    
    @property
    def data(self):
        return IBuyableDataProvider(self.context)
    
    @property
    def currency(self):
        return '€'
    
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