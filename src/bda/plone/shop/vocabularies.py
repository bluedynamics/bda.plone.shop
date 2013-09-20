from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import (
    SimpleVocabulary,
    SimpleTerm,
)
from zope.i18nmessageid import MessageFactory
from .utils import (
    get_shop_settings,
    get_shop_tax_settings,
    get_shop_article_settings,
)


_ = MessageFactory('bda.plone.shop')


# This are the overall avaiable quantity units which then can be reduced in
# control panel. If you need to provide more quantity units add it here or
# patch this vocab
AVAILABLE_QUANTITY_UNITS = {
    'quantity': _('quantity', default='Quantity'),
    'meter': _('meter', default='Meter'),
    'kilo': _('kilo', default='Kilo'),
    'liter': _('liter', default='Liter'),
}


def AvailableQuantityUnitVocabulary(context):
    # vocab is used in shop settings control panel
    items = AVAILABLE_QUANTITY_UNITS.items()
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(AvailableQuantityUnitVocabulary, IVocabularyFactory)


def QuantityUnitVocabulary(context):
    # vocab is used for buyable items
    settings = get_shop_article_settings()
    if not settings:
        return
    terms = []
    for quantity_unit in settings.quantity_units:
        title = AVAILABLE_QUANTITY_UNITS.get(quantity_unit, quantity_unit)
        terms.append(SimpleTerm(value=quantity_unit, title=title))
    return SimpleVocabulary(terms)


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
        ('EUR', _('EUR', default='Euro')),
        ('USD', _('USD', default='US Dollar')),
        ('INR', _('INR', default='Indian Rupee')),
        ('CAD', _('CAD', default='Canadian Dollar')),
        ('CHF', _('CHF', default='Swiss Franc')),
        ('GBP', _('GBP', default='British Pound Sterling')),
        ('AUD', _('AUD', default='Australian Dollar')),
        ('NOK', _('NOK', default='Norwegian Krone')),
        ('SEK', _('SEK', default='Swedish Krona')),
        ('DKK', _('DKK', default='Danish Krone')),
        ('YEN', _('YEN', default='Japanese Yen')),
    ]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(AvailableCurrenciesVocabulary, IVocabularyFactory)


def AvailableShippingMethodsVocabulary(context):
    # XXX: from registered IShipping adapters
    items = [
        ('flat_rate', _('flat_rate', default='Flat rate')),
    ]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(AvailableShippingMethodsVocabulary, IVocabularyFactory)


def CurrencyDisplayOptionsVocabulary(context):
    items = [
        ('yes', _('yes', default='Yes')),
        ('no', _('no', default='No')),
        ('symbol', _('symbol', default='Symbol')),
    ]
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(CurrencyDisplayOptionsVocabulary, IVocabularyFactory)
