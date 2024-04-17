# -*- coding: utf-8 -*-
from bda.plone.shop.tests import set_browserlayer
from bda.plone.shop.tests import ShopDX_INTEGRATION_TESTING

import unittest


class TestDXIntegration(unittest.TestCase):
    layer = ShopDX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        set_browserlayer(self.request)

    def test_foo(self):
        self.assertEqual(1, 1)
