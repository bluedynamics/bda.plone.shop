# -*- coding: utf-8 -*-
from bda.plone.shop.setuphandlers import add_plugin
from pkg_resources import parse_version
from plone import api
from plone.api import env
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
import logging

HAS_PLONE5 = parse_version(env.plone_version()) >= parse_version('5.0b2')
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


def remove_old_resources(context):
    """ Remove old resources for Plone 5"""

    portal_css = getToolByName(context, 'portal_css')
    old_css = ('++resource++bda.plone.cart.css',
               '++resource++bda.plone.checkout.css',
               '++resource++bda.plone.discount.css',
               '++resource++bda.plone.orders.css',
               '++resource++bda.plone.orders_print.css',
               '++resource++bda.plone.payment.css',
               '++resource++bda.plone.shop.css',)
    for css in old_css:
        portal_css.unregisterResource(css)
        logger.info('Removed old resource: {0}'.format(css))

    portal_js = getToolByName(context, 'portal_javascripts')
    old_js = ('++resource++bda.plone.cart.js',
              '@@bda.plone.cart.translations.js',
              '++resource++bda.plone.checkout.js',
              '++resource++bda.plone.discount.js',
              '++resource++qrcode.js',
              '++resource++bda.plone.orders.js',
              '++resource++bda.plone.shop.js',)
    for js in old_js:
        portal_js.unregisterResource(js)
        logger.info('Removed old resource: {0}'.format(js))
