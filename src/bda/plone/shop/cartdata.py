from Products.CMFCore.utils import getToolByName
from bda.plone.cart import CartDataProviderBase


class CartDataProvider(CartDataProviderBase):
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def net(self, items):
        cat = self.catalog
        net = 0.0
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            net += brain[0].item_price * count
        return net
    
    def vat(self, items):
        cat = self.catalog
        vat = 0.0
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            vat += (brain[0].item_price / 100.0) * brain[0].item_vat * count
        return vat
    
    def cart_items(self, items):
        cat = self.catalog
        ret = list()
        for uid, count in items:
            brain = cat(UID=uid)
            if not brain:
                continue
            title = brain[0].Title
            price = brain[0].item_price * count
            url = self.context.absolute_url()
            ret.append(self.item(uid, title, count, price, url))
        return ret        
    
    def validate_count(self, uid, count):
        return True
    
    @property
    def disable_max_article(self):
        return True
    
    @property
    def show_summary(self):
        return True
    
    @property
    def summary_total_only(self):
        return False
    
    @property
    def checkout_url(self):
        return '%s/@@checkout' % self.context.absolute_url()