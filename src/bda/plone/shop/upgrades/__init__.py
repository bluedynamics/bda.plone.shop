from zope.component import getUtility
from plone.registry.interfaces import IRegistry

import logging

logger = logging.getLogger('bda.plone.shop UPGRADE')


def update_notification_text_registry_entries(ctx=None):
    # XXX
    registry = getUtility(IRegistry)
    key = 'bda.plone.shop.interfaces.INotificationTextSettings.order_text'
    del registry.records[key]
    key = 'bda.plone.shop.interfaces.INotificationTextSettings.overbook_text'
    del registry.records[key]
    key = 'bda.plone.shop.interfaces.IPaymentTextSettings.payment_text'
    del registry.records[key]
