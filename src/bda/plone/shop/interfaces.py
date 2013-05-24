from zope.interface import (
    Interface,
    Attribute,
)


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
