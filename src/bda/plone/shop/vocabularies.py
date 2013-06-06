from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('bda.plone.shop')


def VatVocabulary(context):
    items = [
         ( '0%',  '0'), 
         ('10%', '10'), 
         ('20%', '20')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(VatVocabulary, IVocabularyFactory)


def QuantityUnitVocabulary(context):
    items = [
        (_('quantity', default='Quantity'), 'quantity'),
        (_('meter', default='Meter'), 'meter'),
        (_('kilo', default='Kilo'), 'kilo'),
        (_('liter', default='Liter'), 'liter')]
    return SimpleVocabulary.fromItems(items)

directlyProvides(QuantityUnitVocabulary, IVocabularyFactory)
