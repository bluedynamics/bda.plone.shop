from Products.CMFCore.utils import getToolByName
from bda.plone.cart import CartDataProviderBase
from .interfaces import IBuyableDataProvider


class CartDataProvider(CartDataProviderBase):
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def data_for(self, brain):
        return IBuyableDataProvider(brain.getObject())
    
    def net(self, items):
        cat = self.catalog
        net = 0.0
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = self.data_for(brain[0])
            net += data.net * count
        return net
    
    def vat(self, items):
        cat = self.catalog
        vat = 0.0
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            data = self.data_for(brain[0])
            vat += (data.net / 100.0) * data.vat * count
        return vat
    
    def cart_items(self, items):
        cat = self.catalog
        ret = list()
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            title = brain[0].Title
            data = self.data_for(brain[0])
            price = data.net * count
            if data.display_gross:
                price = price + price / 100 * data.vat
            url = brain[0].getURL()
            description = brain[0].Description
            ret.append(self.item(uid, title, count, price, url, description))
        return ret
    
    def validate_count(self, uid, count):
        return True
    
    @property
    def disable_max_article(self):
        return True
    
    @property
    def summary_total_only(self):
        return False
    
    @property
    def checkout_url(self):
        return '%s/@@checkout' % self.context.absolute_url()