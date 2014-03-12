from bda.plone.shop.tests import ShopATFull_ROBOT_TESTING
from bda.plone.shop.tests import ShopDXFull_ROBOT_TESTING
from plone.app.testing.interfaces import ROBOT_TEST_LEVEL
from plone.testing import layered

import robotsuite
import unittest


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
