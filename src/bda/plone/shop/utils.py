from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from .interfaces import IShopSettings


def get_shop_settings():
    return getUtility(IRegistry).forInterface(IShopSettings)
