from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
from .utils import get_shop_settings, get_shop_tax_settings, get_shop_article_settings


_ = MessageFactory('bda.plone.shop')


def QuantityUnitVocabulary(context):
    settings = get_shop_article_settings()
    if not settings:
        return
    items = []
    for line in settings.quantity_units:
        if not line:
            continue
        line = line.split()
        # XXX: key / value
        items.append((line[0], line[0]))
    return SimpleVocabulary.fromItems(items)


directlyProvides(QuantityUnitVocabulary, IVocabularyFactory)


def VatVocabulary(context):
    settings = get_shop_tax_settings()
    if not settings:
        return
    items = []
    for line in settings.vat:
        if not line:
            continue
        line = line.split()
        items.append((line[0], line[1]))
    return SimpleVocabulary.fromItems(items)


directlyProvides(VatVocabulary, IVocabularyFactory)


def AvailableCurrenciesVocabulary(context):
    items = [
        (_('EUR', default='Euro'), 'EUR'),
        (_('USD', default='US Dollar'), 'USD'),
        (_('INR', default='Indian Rupee'), 'INR'),
        (_('CAD', default='Canadian Dollar'), 'CAD'),
        (_('CHF', default='Swiss Franc'), 'CHF'),
        (_('GBP', default='British Pound Sterling'), 'GBP'),
        (_('AUD', default='Australian Dollar'), 'AUD'),
        (_('NOK', default='Norwegian Krone'), 'NOK'),
        (_('SEK', default='Swedish Krona'), 'SEK'),
        (_('DKK', default='Danish Krone'), 'DKK'),
        (_('YEN', default='Japanese Yen'), 'YEN'),
    ]
    return SimpleVocabulary.fromItems(items)


directlyProvides(AvailableCurrenciesVocabulary, IVocabularyFactory)


def AvailableShippingMethodsVocabulary(context):
    # XXX: from registered IShipping adapters
    items = [
        (_('flat_rate', default='Flat rate'), 'flat_rate'),
    ]
    return SimpleVocabulary.fromItems(items)


directlyProvides(AvailableShippingMethodsVocabulary, IVocabularyFactory)


def CurrencyDisplayOptionsVocabulary(context):
    items = [
        (_('yes', default='Yes'), 'yes'),
        (_('no', default='No'), 'no'),
        (_('symbol', default='Symbol'), 'symbol'),
    ]
    return SimpleVocabulary.fromItems(items)


directlyProvides(CurrencyDisplayOptionsVocabulary, IVocabularyFactory)
