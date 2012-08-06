from plone.indexer import indexer
from Products.Archetypes.interfaces import IBaseObject


def field_value(obj, field_name):
    try:
        acc = obj.getField(field_name).getAccessor(obj)
        return acc()
    except (KeyError, TypeError):
        raise AttributeError


@indexer(IBaseObject)
def item_buyable(obj):
    return field_value('item_buyable')


@indexer(IBaseObject)
def item_price(obj):
    return field_value('item_price')


@indexer(IBaseObject)
def item_vat(obj):
    return field_value('item_vat')