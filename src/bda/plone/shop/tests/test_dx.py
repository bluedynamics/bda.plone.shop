import unittest2 as unittest
from bda.plone.shop.tests import (
    ShopDX_INTEGRATION_TESTING,
    set_browserlayer,
)


class TestDXIntegration(unittest.TestCase):
    layer = ShopDX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_foo(self):
        self.assertEquals(0, 1)
