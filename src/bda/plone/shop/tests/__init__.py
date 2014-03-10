from Products.CMFPlone.utils import getFSVersionTuple
from bda.plone.shop.interfaces import IShopExtensionLayer
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing import z2
from zope.interface import alsoProvides

import plone.api


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
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:default')


ShopDX_FIXTURE = ShopDXLayer()
ShopDX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDX_FIXTURE,),
    name="ShopDX:Integration")
ShopDX_ROBOT_TESTING = FunctionalTesting(
    bases=(
        ShopDX_FIXTURE,
        AUTOLOGIN_LIBRARY_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="ShopDX:Robot")


class ShopDXFullLayer(PloneSandboxLayer):
    defaultBases = (ShopDX_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.DateRecurringIndex')  # prepare

        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes,
                      context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.contenttypes:default')

        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Create test content
        crc = plone.api.content.create
        crc(container=portal, type='Folder', id='folder_1')
        crc(container=portal['folder_1'], type='Document', id='item_11')
        crc(container=portal['folder_1'], type='Document', id='item_12')

        crc(container=portal, type='Folder', id='folder_2')
        crc(container=portal['folder_2'], type='Document', id='item_21')
        crc(container=portal['folder_2'], type='Document', id='item_22')

        # Create test users
        cru = plone.api.user.create
        cru(email="c1@test.com", username="customer1", password="customer1")
        cru(email="c2@test.com", username="customer2", password="customer2")
        cru(email="v1@test.com", username="vendor1", password="vendor1")
        cru(email="vendor2@test.com", username="vendor2", password="vendor2")


ShopDXFull_FIXTURE = ShopDXFullLayer()
ShopDXFull_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDXFull_FIXTURE,),
    name="ShopDX:Integration")
ShopDXFull_ROBOT_TESTING = FunctionalTesting(
    bases=(
        ShopDXFull_FIXTURE,
        AUTOLOGIN_LIBRARY_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="ShopDXFull:Robot")
