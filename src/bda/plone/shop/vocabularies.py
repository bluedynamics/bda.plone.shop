from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory

from bda.plone.shop.interfaces import IBdaShopSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

_ = MessageFactory('bda.plone.shop')


#def OldVatVocabulary(context):
#    items = [
#         ( '0%',  '0'), 
#         ('10%', '10'), 
#         ('20%', '20'),
#         ('25%', '25')]
#    return SimpleVocabulary.fromItems(items)

#directlyProvides(VatVocabulary, IVocabularyFactory)


def QuantityUnitVocabulary(context):
    items = [
        (_('quantity', default='Quantity'), 'quantity'),
        (_('meter', default='Meter'), 'meter'),
        (_('kilo', default='Kilo'), 'kilo'),
        (_('liter', default='Liter'), 'liter')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(QuantityUnitVocabulary, IVocabularyFactory)


def VatVocabulary(context):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IBdaShopSettings)
    if settings is None:
        return None
    vat_settings = settings.shop_vat
    vat_alternatives = []
    for line in vat_settings:
        if line:
            line = line.split()
            alternative = (line[0], line[1])
            #convert to int?
            vat_alternatives.append(alternative)
            
    return SimpleVocabulary.fromItems(vat_alternatives)

directlyProvides(VatVocabulary, IVocabularyFactory)
