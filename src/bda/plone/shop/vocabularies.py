from zope.interface import directlyProvides
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
from plone.registry.interfaces import IRegistry
from .interfaces import IShopSettings


_ = MessageFactory('bda.plone.shop')


def QuantityUnitVocabulary(context):
    settings = getUtility(IRegistry).forInterface(IShopSettings)
    if not settings:
        return
    items = []
    for line in settings.shop_quantity_units:
        if not line:
            continue
        line = line.split()
        # XXX: key / value
        items.append((line[0], line[0]))
    return SimpleVocabulary.fromItems(items)


directlyProvides(QuantityUnitVocabulary, IVocabularyFactory)


def VatVocabulary(context):
    settings = getUtility(IRegistry).forInterface(IShopSettings)
    if not settings:
        return
    items = []
    for line in settings.shop_vat:
        if not line:
            continue
        line = line.split()
        items.append((line[0], line[1]))
    return SimpleVocabulary.fromItems(items)


directlyProvides(VatVocabulary, IVocabularyFactory)
