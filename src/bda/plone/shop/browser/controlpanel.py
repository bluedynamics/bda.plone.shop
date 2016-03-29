# -*- coding: utf-8 -*-
from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IShopSettings
from bda.plone.shop.interfaces import IShopSettingsProvider
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.interface import alsoProvides


class ContextProxy(object):

    def __init__(self, interfaces):
        self.__interfaces = interfaces
        alsoProvides(self, *interfaces)

    def __setattr__(self, name, value):
        if name.startswith('__') or name.startswith('_ContextProxy__'):
            return object.__setattr__(self, name, value)

        registry = getUtility(IRegistry)
        for interface in self.__interfaces:
            proxy = registry.forInterface(interface)
            try:
                getattr(proxy, name)
            except AttributeError:
                pass
            else:
                return setattr(proxy, name, value)
        raise AttributeError(name)

    def __getattr__(self, name):
        if name.startswith('__') or name.startswith('_ContextProxy__'):
            return object.__getattr__(self, name)

        registry = getUtility(IRegistry)
        for interface in self.__interfaces:
            proxy = registry.forInterface(interface)
            try:
                return getattr(proxy, name)
            except AttributeError:
                pass

        raise AttributeError(name)


class ShopSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IShopSettings
    label = _(u"Shop settings")
    description = _(u"")

    def getContent(self):
        interfaces = [self.schema]
        interfaces.extend(self.additionalSchemata)
        return ContextProxy(interfaces)

    @property
    def additionalSchemata(self):
        registry = getUtility(IRegistry)
        interface_names = set(record.interfaceName for record
                              in registry.records.values())

        for name in interface_names:
            if not name:
                continue

            interface = None
            try:
                interface = resolve(name)
            except ImportError:
                # In case of leftover registry entries of uninstalled Products
                continue

            if IShopSettingsProvider.providedBy(interface):
                yield interface

    def updateFields(self):
        super(ShopSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(ShopSettingsEditForm, self).updateWidgets()


class ShopSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ShopSettingsEditForm
