from bda.plone.shop.tests import ShopATFull_ROBOT_TESTING
from bda.plone.shop.tests import ShopDXFull_ROBOT_TESTING
from plone.testing import layered
import robotsuite
import unittest

try:
    from plone.app.testing.interfaces import ROBOT_TEST_LEVEL
except ImportError:
    # don't fail if plone.app.testing < 4.2.4
    ROBOT_TEST_LEVEL = 5


def test_suite():
    suite = unittest.TestSuite()
    suite.level = ROBOT_TEST_LEVEL
    suite.addTests([
        layered(robotsuite.RobotTestSuite('robot'),
                layer=ShopATFull_ROBOT_TESTING),
        layered(robotsuite.RobotTestSuite('robot'),
                layer=ShopDXFull_ROBOT_TESTING),
    ])
    return suite
