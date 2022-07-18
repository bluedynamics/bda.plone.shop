# -*- coding: utf-8 -*-
from bda.plone.shop.interfaces import IShopExtensionLayer
from plone.app.robotframework.testing import MOCK_MAILHOST_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing import z2
from zope.component import getUtility
from zope.interface import alsoProvides

import plone.api


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
        self.applyProfile(portal, "bda.plone.shop:default")

    def tearDownZope(self, app):
        pass


Shop_FIXTURE = ShopLayer()
Shop_INTEGRATION_TESTING = IntegrationTesting(
    bases=(Shop_FIXTURE,), name="Shop:Integration"
)


class ShopDXLayer(PloneSandboxLayer):
    defaultBases = (Shop_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "plone.app.dexterity:default")


ShopDX_FIXTURE = ShopDXLayer()
ShopDX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDX_FIXTURE,), name="ShopDX:Integration"
)
ShopDX_ROBOT_TESTING = FunctionalTesting(
    bases=(MOCK_MAILHOST_FIXTURE, ShopDX_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ShopDX:Robot",
)


class ShopFullLayerBase(PloneSandboxLayer):
    def setup_content(self, portal):
        portal.portal_workflow.setDefaultChain("one_state_workflow")

        setRoles(portal, TEST_USER_ID, ["Manager"])

        login(portal, TEST_USER_NAME)

        # Create test content
        crc = plone.api.content.create
        crc(container=portal, type="Folder", id="folder_1")
        crc(
            container=portal["folder_1"], type="Document", id="item_11", title="item_11"
        )
        crc(
            container=portal["folder_1"], type="Document", id="item_12", title="item_12"
        )

        crc(container=portal, type="Folder", id="folder_2")
        crc(
            container=portal["folder_2"], type="Document", id="item_21", title="item_21"
        )
        crc(
            container=portal["folder_2"], type="Document", id="item_22", title="item_22"
        )

        # Create test users
        cru = plone.api.user.create
        cru(email="c1@test.com", username="customer1", password="customer1")
        cru(email="c2@test.com", username="customer2", password="customer2")
        cru(email="v1@test.com", username="vendor1", password="vendor1")
        cru(email="vendor2@test.com", username="vendor2", password="vendor2")

        logout()


class ShopDXFullLayer(ShopFullLayerBase):
    defaultBases = (ShopDX_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, "Products.DateRecurringIndex")  # still needed

        import plone.app.contenttypes

        self.loadZCML(package=plone.app.contenttypes, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "plone.app.contenttypes:default")

        # Make Documents buyable by adding necessary behaviors to the FTI
        getUtility(IDexterityFTI, name="Document").behaviors += (
            "bda.plone.shop.dx.IBuyableBehavior",
            "bda.plone.shop.dx.IStockBehavior",
            "bda.plone.shop.dx.IShippingBehavior",
            "bda.plone.shop.dx.ITradingBehavior",
        )

        self.setup_content(portal)


ShopDXFull_FIXTURE = ShopDXFullLayer()
ShopDXFull_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ShopDXFull_FIXTURE,), name="ShopDX:Integration"
)
ShopDXFull_ROBOT_TESTING = FunctionalTesting(
    bases=(MOCK_MAILHOST_FIXTURE, ShopDXFull_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ShopDXFull:Robot",
)
