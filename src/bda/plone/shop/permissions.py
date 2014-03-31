from Products.CMFCore.permissions import setDefaultRoles


# view buyable information
ViewBuyableInfo = 'bda.plone.shop: View Buyable Info'
setDefaultRoles(ViewBuyableInfo,
                ('Manager', 'Site Administrator', 'Reviewer',
                 'Editor', 'Customer', 'Authenticated'))

# buy items
BuyItems = 'bda.plone.shop: Buy Items'
setDefaultRoles(BuyItems,
                ('Manager', 'Site Administrator', 'Customer'))
