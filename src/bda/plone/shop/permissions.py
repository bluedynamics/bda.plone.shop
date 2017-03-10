# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles


# view buyable information
ViewBuyableInfo = 'bda.plone.shop: View Buyable Info'
setDefaultRoles(ViewBuyableInfo,
                ('Manager', 'Site Administrator', 'Reviewer',
                 'Editor', 'Customer', 'Authenticated'))


# modify cart
ModifyCart = 'bda.plone.shop: Modify Cart'
setDefaultRoles(ModifyCart,
                ('Manager', 'Site Administrator', 'Customer'))


# change personal information
ChangePersonalInformation = 'bda.plone.shop: Change Personal Information'
setDefaultRoles(ChangePersonalInformation,
                ('Manager', 'Site Administrator', 'Reviewer',
                 'Editor', 'Customer', 'Authenticated'))


# change personal preferences
ChangePersonalPreferences = 'bda.plone.shop: Change Personal Preferences'
setDefaultRoles(ChangePersonalPreferences,
                ('Manager', 'Site Administrator', 'Reviewer', 'Editor'))
