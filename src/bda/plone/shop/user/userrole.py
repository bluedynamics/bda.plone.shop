from plone.api import user as apiuser


def add_customer_role(event):
    username = event.principal.getUserName()
    apiuser.grant_roles(username=username, roles=['Customer', ])
