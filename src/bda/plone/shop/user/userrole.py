# -*- coding: utf-8 -*-
from bda.plone.shop.utils import get_shop_settings
from plone.api import user as apiuser
try:
    # Plone 4.3 compatibility: module moved in zope.component 3.11.0 
    from zope.interface.interfaces import ComponentLookupError
except ImportError:
    from zope.component.interfaces import ComponentLookupError


def add_customer_role(event):
    try:
        if not get_shop_settings().add_customer_role_to_new_users:
            return
        username = event.principal.getUserName()
        apiuser.grant_roles(username=username, roles=['Customer'])
    except ComponentLookupError:
        # failing on ``bin/instance adduser`` due to uninitialized registry
        # on startup.
        return
