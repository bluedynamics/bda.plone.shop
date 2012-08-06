from plone.indexer import indexer
from Products.Archetypes.interfaces import IBaseObject
from .interfaces import IBuyable
from .extender import field_value


@indexer(IBuyable)
def item_buyable(obj):
    return True


@indexer(IBuyable)
def item_price(obj):
    price = field_value(obj, 'item_price')
    if not price:
        return 0
    return price


@indexer(IBuyable)
def item_vat(obj):
    try:
        return float(field_value(obj, 'item_vat'))
    except ValueError:
        return 0