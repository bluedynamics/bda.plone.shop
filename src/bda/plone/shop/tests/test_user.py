# -*- coding: utf-8 -*-
from bda.plone.shop.tests import set_browserlayer
from bda.plone.shop.tests import Shop_INTEGRATION_TESTING
from bda.plone.shop.utils import get_shop_settings

import plone.api
import unittest2 as unittest


class TestUser(unittest.TestCase):
    layer = Shop_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_is_customer(self):
        """Test if a newly created user is granted the "Customer" role.
        """
        self.assertTrue(get_shop_settings().add_customer_role_to_new_users)
        plone.api.user.create(
            email="user@test.com",
            username="testuser",
            password="testuser"
        )
        self.assertTrue(
            'Customer' in plone.api.user.get_roles(username="testuser")
        )
