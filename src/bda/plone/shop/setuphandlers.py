# -*- coding:utf-8 -*-
from bda.plone.shop.user.properties import PAS_ID
from bda.plone.shop.user.properties import UserPropertiesPASPlugin
from plone import api
from plone.base.interfaces import INonInstallable
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from zope.globalrequest import getRequest
from zope.interface import implementer

import logging


PAS_TITLE = "bda.plone.shop plugin"


logger = logging.getLogger("bda.plone.shop")


def add_plugin(pas, plugin_id=PAS_ID):
    """
    Install and activate bda.plone.shop user properties PAS plugin
    """
    # Skip if already installed (activation is assumed).
    installed = pas.objectIds()
    if plugin_id in installed:
        return PAS_TITLE + " already installed."

    # Install the plugin
    plugin = UserPropertiesPASPlugin(plugin_id, title=PAS_TITLE)
    pas._setObject(plugin_id, plugin)

    # get plugin acquisition wrapped
    plugin = pas[plugin.getId()]

    # Activate the Plugin
    pas.plugins.activatePlugin(IPropertiesPlugin, plugin.getId())

    return PAS_TITLE + " installed."


def remove_plugin(pas, plugin_id=PAS_ID):
    """
    Deactivate and uninstall bda.plone.shop user properties PAS plugin
    """

    # Skip if already uninstalled (deactivation is assumed).
    installed = pas.objectIds()
    if plugin_id not in installed:
        return PAS_TITLE + " not installed."

    plugin = UserPropertiesPASPlugin(plugin_id, title=PAS_TITLE)

    # get plugin acquisition wrapped
    plugin = pas[plugin.getId()]

    # Deactivate the plugin
    pas.plugins.deactivatePlugin(IPropertiesPlugin, plugin.getId())

    # And finaly uninstall it
    pas._delObject(plugin_id, plugin)

    return PAS_TITLE + " uninstalled."


def install(context):
    """
    Install the PAS plugin.
    """
    pas = api.portal.get_tool(name="acl_users")
    logger.info(add_plugin(pas))


def uninstall(context):
    """
    Remove dependencies
    """
    installer = api.content.get_view(
        name="installer",
        context=api.portal.get(),
        request=getRequest(),
    )

    for dep in [
        "bda.plone.ajax",
        "bda.plone.cart",
        "bda.plone.checkout",
        "bda.plone.discount",
        "bda.plone.orders",
        "bda.plone.payment",
        "collective.js.datatables",
        "souper.plone",
        "yafowil.plone",
    ]:
        installer.uninstall_product(dep)

    pas = api.portal.get_tool(name="acl_users")
    logger.info(remove_plugin(pas))


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["bda.plone.shop:uninstall"]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return [
            "bda.plone.cart",
            "bda.plone.checkout",
            "bda.plone.discount",
            "bda.plone.orders",
            "bda.plone.payment",
            "bda.plone.shop.upgrades",
        ]
