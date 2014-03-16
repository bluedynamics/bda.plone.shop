from plone.api import user as apiuser


def add_customer_role(event):
    # XXX: config flag whether to apply customer role to registered user
    username = event.principal.getUserName()
    apiuser.grant_roles(username=username, roles=['Customer'])
