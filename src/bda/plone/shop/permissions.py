from Products.CMFCore.permissions import setDefaultRoles


BuyItems = 'bda.plone.shop: Buy Items'
setDefaultRoles(BuyItems,
                ('Manager', 'Site Administrator', 'Customer'))
