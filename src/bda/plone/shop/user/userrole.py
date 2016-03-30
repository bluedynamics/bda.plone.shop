from bda.plone.shop.utils import get_shop_settings
from plone.api import user as apiuser


def add_customer_role(event):
    if not get_shop_settings().add_customer_role_to_new_users:
        return
    username = event.principal.getUserName()
    apiuser.grant_roles(username=username, roles=['Customer'])
