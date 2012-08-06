from plone.indexer import indexer
from .interfaces import IBuyable


@indexer(IBuyable)
def item_buyable(obj):
    return True