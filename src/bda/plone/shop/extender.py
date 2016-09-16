# -*- coding: utf-8 -*-
from zope.deprecation import deprecated

import bda.plone.shop.at
import sys


sys.modules['bda.plone.shop.extender'] = deprecated(bda.plone.shop.at, """
``bda.plone.shop.extender`` is deprecated as of ``bda.plone.shop`` 0.4 and
will be removed in ``bda.plone.shop`` 1.0. Use ``bda.plone.shop.at`` instead.
""")
