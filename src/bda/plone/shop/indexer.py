from plone.indexer import indexer
from Products.Archetypes.interfaces import IBaseObject


@indexer(IBaseObject)
def item_buyable(obj):
    try:
        acc = obj.getField('item_buyable').getAccessor(obj)
        return acc()
    except (KeyError, TypeError):
        raise AttributeError