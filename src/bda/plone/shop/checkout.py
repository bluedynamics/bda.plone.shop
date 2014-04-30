from bda.plone.checkout.interfaces import ICheckoutSettings
from bda.plone.orders.interfaces import STATE_RESERVED
from bda.plone.orders.interfaces import STATE_MIXED
from bda.plone.orders.common import OrderData
from bda.plone.shop.utils import get_shop_payment_settings
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ICheckoutSettings)
@adapter(Interface)
class CheckoutSettings(object):

    def __init__(self, context):
        self.context = context

    def skip_payment(self, uid):
        settings = get_shop_payment_settings()
        order_data = OrderData(self.context, uid=uid)
        # no order payment method, skip
        if order_data.order.attrs['payment_method'] == 'no_payment':
            return True
        # if payment should be skipped if order contains reservations and
        # order contains reservations, skip
        if settings.skip_payment_if_order_contains_reservations:
            if order_data.state in (STATE_RESERVED, STATE_MIXED):
                return True
        return False

    def skip_payment_redirect_url(self, uid):
        base = '%s/@@order_done?uid=%s'
        return base % (self.context.absolute_url(), self.order.attrs['uid'])
