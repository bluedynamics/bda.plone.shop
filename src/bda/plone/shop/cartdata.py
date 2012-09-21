from decimal import Decimal
from Products.CMFCore.utils import getToolByName
from bda.plone.cart import CartDataProviderBase
from bda.plone.cart.interfaces import ICartItemDataProvider


SUMMARY_TOTAL_ONLY = False

class CartDataProvider(CartDataProviderBase):
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def data_for(self, brain):
        return ICartItemDataProvider(brain.getObject())
    
    def net(self, items):
        cat = self.catalog
        net = Decimal(0)
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = self.data_for(brain[0])
            net += Decimal(str(data.net)) * count
        return net
    
    def vat(self, items):
        cat = self.catalog
        vat = Decimal(0)
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = self.data_for(brain[0])
            vat += (Decimal(str(data.net)) / Decimal(100)) \
                   * Decimal(str(data.vat)) * count
        return vat
    
    def cart_items(self, items):
        cat = self.catalog
        ret = list()
        for uid, count, comment in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            title = brain[0].Title
            data = self.data_for(brain[0])
            price = Decimal(str(data.net)) * count
            if data.display_gross:
                price = price + price / Decimal(100) * Decimal(str(data.vat))
            url = brain[0].getURL()
            description = brain[0].Description
            comment_required = data.comment_required
            quantity_unit_float = data.quantity_unit_float
            ret.append(self.item(uid, title, count, price, url, comment,
                                 description, comment_required,
                                 quantity_unit_float))
        return ret
    
    def validate_set(self, uid):
        return {
            'success': True,
            'error': '',
        }
    
    def validate_count(self, uid, count):
        return {
            'success': True,
            'error': '',
        }
    
    @property
    def disable_max_article(self):
        return True
    
    @property
    def summary_total_only(self):
        return SUMMARY_TOTAL_ONLY
    
    @property
    def checkout_url(self):
        return '%s/@@checkout' % self.context.absolute_url()