from decimal import Decimal
from bda.plone.cart import CURRENCY_LITERALS
from bda.plone.payment.interfaces import IPaymentSettings
from bda.plone.payment.cash_on_delivery import ICashOnDeliverySettings
from bda.plone.shop.utils import format_amount
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_payment_settings
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IPaymentSettings)
@adapter(Interface)
class PaymentSettings(object):

    def __init__(self, context):
        self.context = context

    @property
    def available(self):
        settings = get_shop_payment_settings()
        return settings.available_payment_methods

    @property
    def default(self):
        settings = get_shop_payment_settings()
        return settings.payment_method


@implementer(ICashOnDeliverySettings)
@adapter(Interface)
class CashOnDeliverySettings(object):

    def __init__(self, context):
        self.context = context

    @property
    def currency(self):
        settings = get_shop_settings()
        currency = settings.currency
        show_currency = settings.show_currency
        if show_currency == 'symbol':
            currency = CURRENCY_LITERALS[currency]
        return currency

    @property
    def costs(self):
        try:
            settings = get_shop_payment_settings()
        except KeyError:
            # happens GS profile application if registry entries not present
            # yet
            return Decimal('0')
        costs = settings.cash_on_delivery_costs
        if costs:
            costs = Decimal(str(costs))
        else:
            costs = Decimal('0')
        return format_amount(costs)
