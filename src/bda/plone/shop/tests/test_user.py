import unittest2 as unittest
from . import ShopDX_INTEGRATION_TESTING
from . import set_browserlayer
import plone.api


class TestUser(unittest.TestCase):
    layer = ShopDX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        set_browserlayer(self.request)

    def test_is_customer(self):
        """Test if a newly created user is granted the "Customer" role.
        """
        plone.api.user.create(
            email="user@test.com",
            username="testuser",
            password="testuser"
        )
        self.assertTrue(
            'Customer' in plone.api.user.get_roles(username="testuser")
        )
