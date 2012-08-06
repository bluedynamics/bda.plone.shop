from zope.interface import Interface, Attribute


class IShopExtensionLayer(Interface):
    """Browser layer for bda.plone.shop
    """


class IBuyable(Interface):
    """Interface for buyable item.
    """
    price = Attribute(u"Item price as float")
    
    vat = Attribute(u"Item vat as float")
    
    vat_included = Attribute(u"Flag whether VAT is included")