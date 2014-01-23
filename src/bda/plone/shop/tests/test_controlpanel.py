import unittest2 as unittest
from . import Shop_INTEGRATION_TESTING
from . import set_browserlayer


class TestControlpanel(unittest.TestCase):
    layer = Shop_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_foo(self):
        self.assertEquals(1, 1)
