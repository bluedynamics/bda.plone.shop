from decimal import Decimal
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from bda.plone.shop.interfaces import IShopArticleSettings
from bda.plone.shop.interfaces import IShopCartSettings
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopShippingSettings
from bda.plone.shop.interfaces import IShopTaxSettings
from bda.plone.shop.interfaces import INotificationTextSettings
from bda.plone.shop.interfaces import IPaymentTextSettings


def format_amount(val):
    val = val.quantize(Decimal('1.00'))
    if bool(val % 2):
        return str(val).replace('.', ',')
    return str(val.quantize(Decimal('1'))) + ',-'


def get_shop_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IShopSettings)


def get_shop_tax_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IShopTaxSettings)


def get_shop_article_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IShopArticleSettings)


def get_shop_cart_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IShopCartSettings)


def get_shop_shipping_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IShopShippingSettings)


def get_shop_notification_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(INotificationTextSettings)


def get_shop_payment_settings():
    reg = getUtility(IRegistry)
    return reg.forInterface(IPaymentTextSettings)
