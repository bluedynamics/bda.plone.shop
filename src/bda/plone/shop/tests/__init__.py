from zope.interface import alsoProvides
from plone.testing import z2
from plone.app.testing import (
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from Products.CMFPlone.utils import getFSVersionTuple
from bda.plone.shop.interfaces import IShopExtensionLayer

try:
    import Products.DateRecurringIndex
    PAC_11 = True
except ImportError:
    PAC_11 = False

if getFSVersionTuple()[0] >= 5:
    PLONE5 = 1
else:
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
        self.loadZCML(package=bda.plone.shop,
                      context=configurationContext)

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
        import Products.ATContentTypes
        self.loadZCML(package=Products.ATContentTypes,
                      context=configurationContext)

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
        # case plone.app.contenttypes > 1.0
        if PAC_11:
            z2.installProduct(app, 'Products.DateRecurringIndex')
        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.contenttypes:default')

    def tearDownZope(self, app):
        # case plone.app.contenttypes > 1.0
        if PAC_11:
            z2.uninstallProduct(app, 'Products.DateRecurringIndex')


ShopDX_FIXTURE = ShopDXLayer()
ShopDX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDX_FIXTURE,),
    name="ShopDX:Integration")
