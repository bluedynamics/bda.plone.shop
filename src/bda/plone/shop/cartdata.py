from decimal import Decimal
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    HAS_CLI = True
except:
    HAS_CLI = False
from bda.plone.cart import (
    CartDataProviderBase,
    CartItemPreviewAdapterBase,
)
from bda.plone.cart.interfaces import (
    ICartItemDataProvider,
    ICartItemPreviewImage,
)
from .interfaces import IShopSettings


_ = MessageFactory('bda.plone.shop')


class CartItemCalculator(object):

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


class CartDataProvider(CartItemCalculator, CartDataProviderBase):
    
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IShopSettings)
   
   
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
            quantity_unit = translate(data.quantity_unit, context=self.request)
            preview_image_url = ICartItemPreviewImage(brain[0].getObject()).url
            ret.append(self.item(uid, title, count, price, url, comment,
                                 description, comment_required,
                                 quantity_unit_float, quantity_unit,
                                 preview_image_url))
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
    def shop_show_checkout(self):
        return settings.shop_show_checkout
        
    @property
    def currency(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IShopSettings)
        return settings.shop_currency

    @property
    def shop_show_to_cart(self):
        return settings.shop_show_to_cart
        
    @property
    def shop_show_currency_in_cart(self):
        return settings.shop_show_currency_in_cart

    @property
    def disable_max_article_count(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IShopSettings)
        return settings.disable_max_article_count
        
    @property
    def summary_total_only(self):
        return settings.summary_total_only
        
    @property
    def include_shipping_costs(self):
        return settings.include_shipping_costs
        
    @property
    def shipping_method(self):
        return settings.shipping_method   

    @property
    def checkout_url(self):
        return '%s/@@checkout' % self.context.absolute_url()


class CartItemPreviewImage(CartItemPreviewAdapterBase):

    preview_scale = "tile"

    @property
    def url(self):
        """Get url of preview image:
            1. try to read the 'image' field on the context
            2. try to use collective.contentleadimage
        """
        img_scale = None
        scales = self.context.restrictedTraverse('@@images')
        if self.context.getField("image") is not None:
            img_scale = scales.scale("image", scale=self.preview_scale)
        if img_scale is None and HAS_CLI:
            if self.context.getField(IMAGE_FIELD_NAME) is not None:
                img_scale = scales.scale(IMAGE_FIELD_NAME,
                                         scale=self.preview_scale)
        return img_scale and img_scale.url or ""
