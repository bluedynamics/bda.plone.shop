from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from .interfaces import IShopArticleSettings
from .interfaces import IShopCartSettings
from .interfaces import IShopSettings
from .interfaces import IShopShippingSettings
from .interfaces import IShopTaxSettings
from .interfaces import INotificationTextSettings
from .interfaces import IPaymentTextSettings


def get_shop_settings():
    return getUtility(IRegistry).forInterface(IShopSettings)


def get_shop_tax_settings():
    return getUtility(IRegistry).forInterface(IShopTaxSettings)


def get_shop_article_settings():
    return getUtility(IRegistry).forInterface(IShopArticleSettings)


def get_shop_cart_settings():
    return getUtility(IRegistry).forInterface(IShopCartSettings)


def get_shop_shipping_settings():
    return getUtility(IRegistry).forInterface(IShopShippingSettings)


def get_shop_notification_settings():
    return getUtility(IRegistry).forInterface(INotificationTextSettings)


def get_shop_payment_settings():
    return getUtility(IRegistry).forInterface(IPaymentTextSettings)
