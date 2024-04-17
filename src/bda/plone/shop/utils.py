# -*- coding: utf-8 -*-
from bda.plone.shop.interfaces import IInvoiceSettings
from bda.plone.shop.interfaces import INotificationTextSettings
from bda.plone.shop.interfaces import IPaymentTextSettings
from bda.plone.shop.interfaces import IShopArticleSettings
from bda.plone.shop.interfaces import IShopCartSettings
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopShippingSettings
from bda.plone.shop.interfaces import IShopTaxSettings
from decimal import Decimal
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def format_amount(val):
    val = val.quantize(Decimal("1.00"))
    if bool(val % 2):
        return str(val).replace(".", ",")
    return str(val.quantize(Decimal("1"))) + ",-"


def get_shop_settings():
    return getUtility(IRegistry).forInterface(IShopSettings, check=False)


def get_shop_tax_settings():
    return getUtility(IRegistry).forInterface(IShopTaxSettings, check=False)


def get_shop_article_settings():
    return getUtility(IRegistry).forInterface(IShopArticleSettings, check=False)


def get_shop_cart_settings():
    return getUtility(IRegistry).forInterface(IShopCartSettings, check=False)


def get_shop_shipping_settings():
    return getUtility(IRegistry).forInterface(IShopShippingSettings, check=False)


def get_shop_notification_settings():
    return getUtility(IRegistry).forInterface(INotificationTextSettings, check=False)


def get_shop_invoice_settings():
    return getUtility(IRegistry).forInterface(IInvoiceSettings, check=False)


def get_shop_payment_settings():
    return getUtility(IRegistry).forInterface(IPaymentTextSettings, check=False)
