from zope.interface import Interface, Attribute


class IShopExtensionLayer(Interface):
    """Browser layer for bda.plone.shop
    """


class IPotentiallyBuyable(Interface):
    """Mark item as potentially buyable.
    
    Considered for providing action in UI.
    """


class IBuyable(Interface):
    """Marker for buyable item.
    
    Item is buyable.
    """


class IBuyableAdapter(Interface):
    """Provide information relevant for being buyable.
    """
    price = Attribute(u"Item price as float")
    
    vat = Attribute(u"Item vat as float")
    
    vat_included = Attribute(u"Flag whether VAT is included")