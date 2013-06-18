from zope.interface import (
    Interface,
    Attribute,
)
from zope import schema
from zope.i18nmessageid import MessageFactory



from plone.z3cform.fieldsets.group import GroupFactory



_ = MessageFactory('bda.plone.shop')


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


AVAILABLE_CURRENCIES = [
    "EUR", "USD", "INR", "CAD", "CHF", "GBP", "AUD", "NOK", "SEK", "DKK", "YEN",
]

CART_CURRENCIES_ANSWERS = [
    "Yes", "No", "Symbol",
]

AVAILABLE_SHIPPING = [
    "flat_rate",
]

class IShopSettings(Interface):
    """Shop controlpanel schema.
    """

    shop_vat=schema.List(
        title=_(u"Specify all allowed vat settings, one per line. "
                u"The required format is <name> <persentage>"),
        description=_(u"help_shop_vat", default=u'Value added tax in %'),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    shop_admin_email = schema.ASCIILine(
        title=_(u"label_shop_admin_email",
                default=u'Shop admin Email. No typos please....'),
        description=_(u"help_shop_admin_email", default=u''),
        required=True,
        default="")

    shop_currency = schema.Choice(
        title=u"Currency",
        description=u"Choose the default currency",
        values=AVAILABLE_CURRENCIES)
        
    shop_quantity_units=schema.List(
        title=_(u"Specify all allowed quantity settins. "
                u"The required format is <name>. No spaces, please"),
        description=_(u"help_shop_quantity_units", default=u'Quantity units (what the buyable items are measured in)'),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    disable_max_article_count = schema.Bool(
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
        values=AVAILABLE_SHIPPING)

    shop_show_checkout = schema.Bool(
        title=u"Show checkout link in portlet",
        description=u"",
        default=False)

    shop_show_to_cart = schema.Bool(
        title=u"Show link to cart in portlet",
        description=u"",
        default=True)
        
    shop_show_currency_in_cart = schema.Choice(
        title=u"Show the currency for items in portlet",
        description=u"",
        values=CART_CURRENCIES_ANSWERS)
        