from bda.plone.shop import permissions  # nopep8
from bda.plone.shop.user.properties import UserPropertiesPASPlugin
from Products.PluggableAuthService.PluggableAuthService import \
    registerMultiPlugin
from zope.i18nmessageid import MessageFactory


message_factory = MessageFactory('bda.plone.shop')


def initialize(context):
    """
    Initializer called when used as a Zope 2 product.
    """
    # Add to PAS menu
    registerMultiPlugin(UserPropertiesPASPlugin.meta_type)