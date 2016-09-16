# -*- coding: utf-8 -*-
from bda.plone.shop.setuphandlers import add_plugin
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

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


def install_userproperties_pas_plugin(context):
    pas = api.portal.get_tool(name='acl_users')
    logger.info(add_plugin(pas))
