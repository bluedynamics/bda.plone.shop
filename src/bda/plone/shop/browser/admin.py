# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.shop import message_factory as _
from bda.plone.shop.browser.navigation import ShopNavigation
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implementer

import pkg_resources


if pkg_resources.get_distribution("Products.CMFPlone").version > '4.99':
    PLONE5 = 1
else:
    PLONE5 = 0


class IShopAdminPortlet(IPortletDataProvider):
    """A portlet rendering shop portlet links.
    """


@implementer(IShopAdminPortlet)
class ShopAdminAssignment(base.Assignment):
    title = _(u'shop_portlet', default=u'Shop Portlet')


class ShopAdminRenderer(base.Renderer, ShopNavigation):
    if PLONE5:
        render = ViewPageTemplateFile('admin_p5.pt')
    else:
        render = ViewPageTemplateFile('admin_p4.pt')


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()
