from zope.component import getUtility
from zope.interface import alsoProvides
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from plone.app.testing import (
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from bda.plone.shop.interfaces import IShopExtensionLayer
try:
    from plone.app.upgrade import v50
    PLONE5 = 1
except ImportError:
    PLONE5 = 0


def set_browserlayer(request):
    """Set the BrowserLayer for the request.

    We have to set the browserlayer manually, since importing the profile alone
    doesn't do it in tests.
    """
    alsoProvides(request, IShopExtensionLayer)


class ShopLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bda.plone.shop
        self.loadZCML(package=bda.plone.shop, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'bda.plone.shop:default')

    def tearDownZope(self, app):
        pass


Shop_FIXTURE = ShopLayer()
Shop_INTEGRATION_TESTING = IntegrationTesting(
    bases=(Shop_FIXTURE,),
    name="Shop:Integration")


class ShopATLayer(PloneSandboxLayer):
    defaultBases = (Shop_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # XXX: provide AT shop item
        pass

    def setUpPloneSite(self, portal):
        if PLONE5:
            self.applyProfile(portal, 'Products.ATContentTypes:default')


ShopAT_FIXTURE = ShopATLayer()
ShopAT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopAT_FIXTURE,),
    name="ShopAT:Integration")


class ShopDXLayer(PloneSandboxLayer):
    defaultBases = (Shop_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.contenttypes:default')


ShopDX_FIXTURE = ShopDXLayer()
ShopDX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDX_FIXTURE,),
    name="ShopDX:Integration")
