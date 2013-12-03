from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import (
    SimpleVocabulary,
    SimpleTerm,
)
from .utils import (
    get_shop_settings,
    get_shop_tax_settings,
    get_shop_article_settings,
)
from bda.plone.shipping import Shippings
from bda.plone.shop import message_factory as _


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


# This are the overall avaiable VAT values which then can be reduced in
# control panel. If you need to provide more vat values add it here or
# patch this vocab
AVAILABLE_VAT_VALUES = {
    '0': '0%',
    '10': '10%',
    '20': '20%',
    '25': '25%',
}


def AvailableVatVocabulary(context):
    # vocab is used in shop settings control panel
    items = AVAILABLE_VAT_VALUES.items()
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(AvailableVatVocabulary, IVocabularyFactory)


def VatVocabulary(context):
    # vocab is used for buyable items
    settings = get_shop_tax_settings()
    if not settings:
        return
    terms = []
    if settings.vat:
        for vat in settings.vat:
            title = AVAILABLE_VAT_VALUES.get(vat, vat)
            terms.append(SimpleTerm(value=vat, title=title))
    return SimpleVocabulary(terms)


directlyProvides(VatVocabulary, IVocabularyFactory)


# This are the overall avaiable currency values available in
# control panel. If you need to provide more currencies add it here or
# patch this vocab
AVAILABLE_CURRENCIES = {
    'EUR': _('EUR', default='Euro'),
    'USD': _('USD', default='US Dollar'),
    'INR': _('INR', default='Indian Rupee'),
    'CAD': _('CAD', default='Canadian Dollar'),
    'CHF': _('CHF', default='Swiss Franc'),
    'GBP': _('GBP', default='British Pound Sterling'),
    'AUD': _('AUD', default='Australian Dollar'),
    'NOK': _('NOK', default='Norwegian Krone'),
    'SEK': _('SEK', default='Swedish Krona'),
    'DKK': _('DKK', default='Danish Krone'),
    'YEN': _('YEN', default='Japanese Yen'),
}


def AvailableCurrenciesVocabulary(context):
    items = AVAILABLE_CURRENCIES.items()
    return SimpleVocabulary([SimpleTerm(value=k, title=v) for k, v in items])


directlyProvides(AvailableCurrenciesVocabulary, IVocabularyFactory)


def AvailableShippingMethodsVocabulary(context):
    items = Shippings(context).vocab
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
