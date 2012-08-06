from plone.indexer import indexer
from Products.Archetypes.interfaces import IBaseObject
from .extender import field_value


@indexer(IBaseObject)
def item_buyable(obj):
    return field_value(obj, 'item_buyable')


@indexer(IBaseObject)
def item_price(obj):
    return field_value(obj, 'item_price')


@indexer(IBaseObject)
def item_vat(obj):
    return float(field_value(obj, 'item_vat'))