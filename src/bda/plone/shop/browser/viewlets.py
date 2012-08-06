# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase
from ..interfaces import IBuyableDataProvider


class BuyableViewlet(ViewletBase):
    """Vielet rendering buyable information.
    """
    
    @property
    def item_uid(self):
        return self.context.UID()
    
    @property
    def data(self):
        return IBuyableDataProvider(self.context)
    
    @property
    def item_price(self):
        return self.data.price
    
    @property
    def item_vat(self):
        return self.data.vat