from bda.plone.payment.interfaces import IPaymentSettings
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
