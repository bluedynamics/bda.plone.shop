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


class IBuyableDataProvider(Interface):
    """Provide information relevant for being buyable.
    """
    net = Attribute(u"Item net price as float")
    
    vat = Attribute(u"Item vat as float")
    
    display_gross = Attribute(u"Flag whether whether to display gross "
                              u"instead of net")
    
    comment_enabled = Attribute(u"Flag whether customer comment can be added "
                                u"when adding buyable to cart")
    
    comment_required = Attribute(u"Flag whether comment input is required in "
                                 u"order to add buyable to cart")
    
    quantity_unit_float = Attribute(u"Flag whether quantity unit value is "
                                    u"allowed as float")
    
    #quantity_label = Attribute(u"Quantity label")