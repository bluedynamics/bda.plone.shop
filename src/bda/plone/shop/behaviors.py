import sys
import bda.plone.shop.dx
from zope.deprecation import deprecated
sys.modules['bda.plone.shop.behaviors'] = deprecated(bda.plone.shop.dx, """
``bda.plone.shop.behaviors`` is deprecated as of ``bda.plone.shop`` 0.4 and
will be removed in ``bda.plone.shop`` 1.0. Use ``bda.plone.shop.dx`` instead.
""")
