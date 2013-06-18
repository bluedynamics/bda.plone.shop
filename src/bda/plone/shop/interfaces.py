from zope.interface import (
    Interface,
    Attribute,
)
from zope import schema
from zope.i18nmessageid import MessageFactory
from bda.plone.cart.interfaces import ICartItem


_ = MessageFactory('bda.plone.shop')


class IShopExtensionLayer(Interface):
    """Browser layer for bda.plone.shop
    """


class IPotentiallyBuyable(Interface):
    """Mark item as potentially buyable.

    Considered for providing action in UI.
    """


class IBuyable(ICartItem):
    """Marker for buyable item.

    Item is buyable.
    """


class IShopSettings(Interface):
    """Shop controlpanel schema.
    """

    vat = schema.List(
        title=_(u"Specify all allowed vat settings, one per line. "
                u"The required format is <name> <persentage>"),
        description=_(u"help_vat", default=u'Value added tax in %'),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    admin_email = schema.ASCIILine(
        title=_(u"label_admin_email",
                default=u'Shop admin Email. No typos please....'),
        description=_(u"help_admin_email", default=u''),
        required=True,
        default="")

    currency = schema.Choice(
        title=u"Currency",
        description=u"Choose the default currency",
        vocabulary='bda.plone.shop.vocabularies.AvailableCurrenciesVocabulary')

    quantity_units = schema.List(
        title=_(u"Specify all allowed quantity settins. "
                u"The required format is <name>. No spaces, please"),
        description=_(u"help_quantity_units",
                      default=u'Quantity units (what the buyable items are '
                              u'measured in)'),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    disable_max_article = schema.Bool(
        title=u"Disable max article",
        description=u"",
        default=True)

    summary_total_only = schema.Bool(
        title=u"Summary, total only",
        description=u"",
        default=False)

    include_shipping_costs = schema.Bool(
        title=u"Include Shipping Costs",
        description=u"",
        default=True)

    shipping_method = schema.Choice(
        title=u"Shipping Method",
        description=u"",
        vocabulary=\
            'bda.plone.shop.vocabularies.AvailableShippingMethodsVocabulary')

    show_checkout = schema.Bool(
        title=u"Show checkout link in portlet",
        description=u"",
        default=False)

    show_to_cart = schema.Bool(
        title=u"Show link to cart in portlet",
        description=u"",
        default=True)

    show_currency = schema.Choice(
        title=u"Show the currency for items",
        description=u"",
        vocabulary=\
            'bda.plone.shop.vocabularies.CurrencyDisplayOptionsVocabulary')
