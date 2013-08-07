from zope.interface import Interface
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

    admin_email = schema.ASCIILine(
        title=_(u"label_admin_email", default=u'Shop Admin E-Mail'),
        description=_(u"help_admin_email",
                      default=u'No typos please....'),
        required=True,
        default="")

    quantity_units = schema.List(
        title=_(u"label_quantity_units",
                default=u"Specify all allowed quantity settings. "
                        u"The required format is <name>. No spaces, please"),
        description=_(u"help_quantity_units",
                      default=u'Quantity units (what the buyable items are '
                              u'measured in)'),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    disable_max_article = schema.Bool(
        title=_(u"label_disable_max_article", default=u"Disable max article"),
        description=_(u"help_disable_max_article",
                      default=u"No total number of items in cart limit"),
        default=True)

    summary_total_only = schema.Bool(
        title=_(u"label_summary_total_only",
                default=u"Cart Summary total only"),
        description=_(u"help_summary_total_only",
                      default=u"Show only total value in cart summary"),
        default=False)

    include_shipping_costs = schema.Bool(
        title=_(u"label_include_shipping_costs",
                default=u"Include Shipping Costs"),
        description=_(u"help_include_shipping_costs",
                      default=u""),
        default=True)

    shipping_method = schema.Choice(
        title=_(u"label_shipping_method", default=u"Shipping Method"),
        description=_(u"help_shipping_method", default=u""),
        vocabulary=\
            'bda.plone.shop.vocabularies.AvailableShippingMethodsVocabulary')

    show_checkout = schema.Bool(
        title=_(u"label_show_checkout",
                default=u"Show checkout link in portlet"),
        description=_(u"help_show_checkout", default=""),
        default=False)

    show_to_cart = schema.Bool(
        title=_(u"label_show_to_cart",
                default=u"Show link to cart in portlet"),
        description=_(u"help_show_to_cart", default=u""),
        default=True)  

    show_currency = schema.Choice(
        title=_(u"label_show_currency", default=u"Show the currency for items"),
        description=_(u"help_show_currency", default=u""),
        vocabulary=\
            'bda.plone.shop.vocabularies.CurrencyDisplayOptionsVocabulary')

    currency = schema.Choice(
        title=_(u"label_currency", default="Currency"),
        description=_(u"help_currency",
                      default=u"Choose the default currency"),
        vocabulary='bda.plone.shop.vocabularies.AvailableCurrenciesVocabulary')

    default_item_net = schema.Float(
        title=_(u'label_default_item_net', default=u'Default Item net price'),
        required=False)

    default_item_quantity_unit = schema.Choice(
        title=_(u"label_default_quantity_units",
                default=u"Specify default quantity name."),
        description=_(u"help_default_quantity_unit",
                      default=u'default measurement'),
        vocabulary='bda.plone.shop.vocabularies.QuantityUnitVocabulary')

    default_item_display_gross = schema.Bool(
        title=_(u'label_default_item_display_gross',
                default=u'Display Gross by default'),
        required=False)

    default_item_comment_enabled = schema.Bool(
        title=_(u'label_default_item_comment_enabled',
                default='Comment enabled by default'),
        required=False)

    default_item_comment_required = schema.Bool(
        title=_(u'label_default_item_comment_required',
                default='Comment required by default'),
        required=False)

    default_item_quantity_unit_float = schema.Bool(
        title=_(u'label_default_item_quantity_unit_float',
                default='Quantity as float as default'),
        required=False)

class IShopTaxSettings(Interface):
    """Shop controlpanel schema.
    """

    vat = schema.List(
        title=_(u"label_vat", default=u'Value added tax in %'),
        description=_(u"help_vat",
                      default=u"Specify all allowed vat settings, one per "
                              u"line. Format is <name> <percentage>"),
        required=True,
        value_type=schema.TextLine(),
        default=[])

    default_item_vat = schema.Choice(
        title=_(u"label_default_vat", default=u'Default Value added tax name'),
        description=_(u"help_default_vat",
                      default=u"Specify default vat name"),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary')

