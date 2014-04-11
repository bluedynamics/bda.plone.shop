from plone.indexer import indexer
from bda.plone.shop.interfaces import IBuyable


@indexer(IBuyable)
def item_buyable(obj):
    return True
