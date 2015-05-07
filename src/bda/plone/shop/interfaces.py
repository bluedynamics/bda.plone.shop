from bda.plone.orders.interfaces import IGlobalNotificationText
from bda.plone.orders.interfaces import IItemNotificationText
from bda.plone.orders.interfaces import IOrdersExtensionLayer
from bda.plone.shop import message_factory as _
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform.directives import widget
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import provider

import zope.deferredimport

zope.deferredimport.deprecated(
    "Import from bda.plone.orders.interfaces instead",
    IBuyable='bda.plone.orders:interfaces.IBuyable'
)


class IShopExtensionLayer(IOrdersExtensionLayer):
    """Browser layer for bda.plone.shop
    """


class IPotentiallyBuyable(Interface):
    """Mark item as potentially buyable.

    Considered for providing action in UI.
    """


class IBuyablePeriod(Interface):
    """Define period in which an item is buyable.
    """

    effective = Attribute(u"Buyable effective date")

    expires = Attribute(u"Buyable expires date")


class IShopSettingsProvider(Interface):
    """A marker interface for plone.registry configuration
    interfaces
    """


class IShopSettings(model.Schema):
    """Shop controlpanel schema.
    """

    admin_email = schema.ASCIILine(
        title=_(u"label_admin_email", default=u'Shop Admin E-Mail'),
        description=_(u"help_admin_email", default=u'No typos please....'),
        required=True,
        default=""
    )

    # XXX: change value type to schema.TextLine (needs migration)
    admin_name = schema.ASCIILine(
        title=_(u"label_admin_name", default=u'Shop Admin Name'),
        description=_(u"help_admin_name",
                      default=u'Name used for Shop E-Mails.'),
        required=True,
        default=""
    )

    add_customer_role_to_new_users = schema.Bool(
        title=_(
            u'label_add_customer_role_to_new_users',
            default=u'Add Customer role to new Users'
        ),
        required=False,
        default=True
    )

    # XXX: this is an article setting, move to IShopArticleSettings
    default_item_display_gross = schema.Bool(
        title=_(
            u'label_default_item_display_gross',
            default=u'Display Gross by default'
        ),
        required=False
    )

    currency = schema.Choice(
        title=_(u"label_currency", default="Currency"),
        description=_(
            u"help_currency",
            default=u"Choose the default currency"
        ),
        vocabulary='bda.plone.shop.vocabularies.AvailableCurrenciesVocabulary'
    )

    show_currency = schema.Choice(
        title=_(
            u"label_show_currency",
            default=u"Show the currency for items"
        ),
        description=_(u"help_show_currency", default=u""),
        vocabulary='bda.plone.shop.vocabularies.'
                   'CurrencyDisplayOptionsVocabulary'
    )


@provider(IShopSettingsProvider)
class IShopCartSettings(model.Schema):
    """Shop controlpanel schema for cart settings.
    """

    model.fieldset(
        'cart',
        label=_(u'Cart', default=u'Cart'),
        fields=[
            'hide_cart_if_empty',
            'max_artice_count',
            'disable_max_article',
            'summary_total_only',
            'show_checkout',
            'show_to_cart',
        ],
    )

    hide_cart_if_empty = schema.Bool(
        title=_(u"label_hide_cart_if_empty", default=u"Hide Cart if empty"),
        description=_(
            u"help_hide_cart_if_empty",
            default=u"Hide cart if no items contained"
        ),
        default=False
    )

    max_artice_count = schema.Int(
        title=_(
            u'label_max_artice_count',
            default=u'Maximum number articles in cart'
        ),
        description=_(
            u"help_max_artice_count",
            default=u"Maximum number of articles in cart if disable max "
                    u"article flag set"
        ),
        required=False
    )

    disable_max_article = schema.Bool(
        title=_(u"label_disable_max_article", default=u"Disable max article"),
        description=_(
            u"help_disable_max_article",
            default=u"No total number of items in cart limit"
        ),
        default=True
    )

    summary_total_only = schema.Bool(
        title=_(
            u"label_summary_total_only",
            default=u"Cart Summary total only"
        ),
        description=_(
            u"help_summary_total_only",
            default=u"Show only total value in cart summary"
        ),
        default=False
    )

    show_checkout = schema.Bool(
        title=_(
            u"label_show_checkout",
            default=u"Show checkout link in portlet"
        ),
        description=_(u"help_show_checkout", default=""),
        default=False
    )

    show_to_cart = schema.Bool(
        title=_(
            u"label_show_to_cart",
            default=u"Show link to cart in portlet"
        ),
        description=_(u"help_show_to_cart", default=u""),
        default=True
    )


@provider(IShopSettingsProvider)
class IShopArticleSettings(model.Schema):
    """Shop controlpanel schema for article settings.
    """

    model.fieldset(
        'article',
        label=_(u'Article', default=u'Article'),
        fields=[
            'quantity_units',
            'default_item_net',
            'default_item_quantity_unit',
            'default_item_comment_enabled',
            'default_item_comment_required',
            'default_item_quantity_unit_float',
            'default_item_cart_count_limit',
        ],
    )

    widget('quantity_units', CheckBoxFieldWidget)
    quantity_units = schema.List(
        title=_(
            u"label_quantity_units",
            default=u"Specify quantity units allowed in shop."
        ),
        description=_(
            u"help_quantity_units",
            default=u'Quantity units (what the buyable items are measured in)'
        ),
        required=True,
        missing_value=set(),
        value_type=schema.Choice(
            vocabulary='bda.plone.shop.vocabularies.'
                       'AvailableQuantityUnitVocabulary'
        )
    )

    default_item_quantity_unit = schema.Choice(
        title=_(
            u"label_default_quantity_units",
            default=u"Specify default quantity name."
        ),
        description=_(
            u"help_default_quantity_unit",
            default=u'default measurement'
        ),
        vocabulary='bda.plone.shop.vocabularies.QuantityUnitVocabulary'
    )

    default_item_net = schema.Float(
        title=_(
            u'label_default_item_net',
            default=u'Default Item net price'
        ),
        required=False
    )

    default_item_comment_enabled = schema.Bool(
        title=_(
            u'label_default_item_comment_enabled',
            default='Comment enabled by default'
        ),
        required=False
    )

    default_item_comment_required = schema.Bool(
        title=_(
            u'label_default_item_comment_required',
            default='Comment required by default'
        ),
        required=False
    )

    default_item_quantity_unit_float = schema.Bool(
        title=_(
            u'label_default_item_quantity_unit_float',
            default='Quantity as float as default'
        ),
        required=False
    )

    default_item_cart_count_limit = schema.Float(
        title=_(
            u'label_default_item_cart_count_limit',
            default='Quantity limit of an item in the cart.'
        ),
        required=False
    )


@provider(IShopSettingsProvider)
class IShopShippingSettings(model.Schema):
    """Shop controlpanel schema for article settings.
    """

    model.fieldset(
        'shipping',
        label=_(u'Shipping', default=u'Shipping'),
        fields=[
            'default_shipping_item_shippable',
            'available_shipping_methods',
            'shipping_method',
            'shipping_vat',
            'shipping_limit_from_gross',
            'free_shipping_limit',
            'flat_shipping_cost',
            'item_shipping_cost',
        ],
    )

    default_shipping_item_shippable = schema.Bool(
        title=_(
            u'label_default_shipping_item_shippable',
            default=u'Item Shippable by default'),
        description=_('help_default_shipping_item_shippable',
                      default=u'Flag whether item is shippable by default, '
                              u'i.e. downloads are not')
    )

    available_shipping_methods = schema.List(
        title=_(u"label_available_shipping_methods",
                default=u"Available Shipping Methods"),
        description=_(u"help_available_shipping_methods",
                      default=u"Available shipping methods in checkout"),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            vocabulary='bda.plone.shop.vocabularies.'
                       'AvailableShippingMethodsVocabulary'
        )
    )

    shipping_method = schema.Choice(
        title=_(u"label_shipping_method",
                default=u"Shipping Method"),
        description=_(u"help_shipping_method",
                      default=u"Default shipping method in checkout"),
        vocabulary='bda.plone.shop.vocabularies.'
                   'ShippingMethodsVocabulary'
    )

    shipping_vat = schema.Choice(
        title=_(u"label_shipping_vat", default=u'Shipping VAT'),
        description=_(
            u"help_shipping_vat",
            default=u"VAT used to calculate shipping costs"
        ),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary'
    )

    # default shipping related settings

    free_shipping_limit = schema.Float(
        title=_(u"label_free_shipping_limit", default=u"Free Shipping Limit"),
        description=_(u"help_free_shipping_limit",
                      default=u"Do not add shipping costs to orders "
                              u"with price bigger than limit. If limit "
                              u"applies to gross or net purchase price "
                              u"depends on 'Calculate shipping limit from "
                              u"gross' setting"),
        required=True,
        default=200.0
    )

    shipping_limit_from_gross = schema.Bool(
        title=_(u"label_shipping_limit_from_gross",
                default=u"Calculate shipping limit from gross"),
        description=_(u"help_shipping_limit_from_gross",
                      default=u"If set to False, shipping limit gets "
                              u"calculated from net price instead of gross.")
    )

    flat_shipping_cost = schema.Float(
        title=_(u"label_flat_shipping_cost", default=u"Flat shipping cost"),
        description=_(u"help_flat_shipping_cost",
                      default=u"Net flat shipping cost"),
        required=True,
        default=10.0
    )

    item_shipping_cost = schema.Float(
        title=_(u"label_item_shipping_cost", default=u"Item shipping cost"),
        description=_(u"help_item_shipping_cost",
                      default=u"Net shipping cost per item in cart. If flat "
                              u"shipping cost set and item shipping cost "
                              u"below flat shipping cost, flat shipping cost "
                              u"is used"),
        required=True,
        default=0.0
    )


@provider(IShopSettingsProvider)
class IShopTaxSettings(model.Schema):
    """Shop controlpanel schema for tax settings.
    """

    model.fieldset(
        'tax',
        label=_(u'Tax Settings'),
        fields=[
            'vat',
            'default_item_vat',
        ],
    )

    widget('vat', CheckBoxFieldWidget)
    vat = schema.List(
        title=_(u"label_vat", default=u'VAT in %'),
        description=_(
            u"help_vat",
            default=u"Specify all allowed vat settings"
        ),
        required=True,
        missing_value=set(),
        value_type=schema.Choice(
            vocabulary='bda.plone.shop.vocabularies.AvailableVatVocabulary'
        )
    )

    default_item_vat = schema.Choice(
        title=_(u"label_default_vat", default=u'Default Value added tax name'),
        description=_(
            u"help_default_vat",
            default=u"Specify default vat name"
        ),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary'
    )


class ILanguageAwareTextRow(model.Schema):

    lang = schema.Choice(
        title=_(u'language', default=u'Language'),
        vocabulary='plone.app.vocabularies.SupportedContentLanguages',
        required=False
    )

    text = schema.Text(
        title=_(u'text', default=u'Text'),
        required=False
    )


@provider(IShopSettingsProvider)
class INotificationTextSettings(model.Schema,
                                IGlobalNotificationText,
                                IItemNotificationText):

    model.fieldset(
        'notifications',
        label=_(u'Notifications', default=u'Notifications'),
        fields=[
            'global_order_text',
            'global_overbook_text',
            'order_text',
            'overbook_text',
        ],
    )

    widget('order_text', DataGridFieldFactory)
    order_text = schema.List(
        title=_(
            u"label_site_item_notification_text",
            default=u"Default notification text for items in order "
                    u"confirmation mail"
        ),
        value_type=DictRow(
            title=_(u'order_text', default='Order Text'),
            schema=ILanguageAwareTextRow),
        required=False
    )

    widget('overbook_text', DataGridFieldFactory)
    overbook_text = schema.List(
        title=_(
            u"label_site_item_overbook_notification_text",
            default=u"Default notification text for items in order "
                    u"confirmation mail if item out of stock."
        ),
        value_type=DictRow(
            title=_(u'overbook_text', default='Overbook Text'),
            schema=ILanguageAwareTextRow),
        required=False
    )

    widget('global_order_text', DataGridFieldFactory)
    global_order_text = schema.List(
        title=_(
            u"label_site_global_notification_text",
            default=u"Overall notification text for order confirmation mail"
        ),
        value_type=DictRow(
            title=_(u'order_text', default='Order Text'),
            schema=ILanguageAwareTextRow),
        required=False
    )

    widget('global_overbook_text', DataGridFieldFactory)
    global_overbook_text = schema.List(
        title=_(
            u"label_site_global_overbook_notification_text",
            default=u"Overall notification text for order confirmation mail "
                    u"if order contains items out of stock"
        ),
        value_type=DictRow(
            title=_(u'overbook_text', default='Overbook Text'),
            schema=ILanguageAwareTextRow),
        required=False
    )


class ILanguageAndPaymentAwareTextRow(model.Schema):

    payment = schema.Choice(
        title=_(u'payment', default=u'Payment'),
        vocabulary='bda.plone.shop.vocabularies.PaymentMethodsVocabulary',
        required=False
    )

    lang = schema.Choice(
        title=_(u'language', default=u'Language'),
        vocabulary='plone.app.vocabularies.SupportedContentLanguages',
        required=False
    )

    text = schema.Text(
        title=_(u'text', default=u'Text'),
        required=False
    )


@provider(IShopSettingsProvider)
class IPaymentTextSettings(model.Schema):
    # XXX: rename to IPaymentSettings

    model.fieldset(
        'payment',
        label=_(u'Payment', default=u'Payment'),
        fields=[
            'available_payment_methods',
            'payment_method',
            'skip_payment_if_order_contains_reservations',
            'payment_text',
            'cash_on_delivery_costs',
        ],
    )

    available_payment_methods = schema.List(
        title=_(u"label_available_payment_methods",
                default=u"Available Payment Methods"),
        description=_(u"help_available_payment_methods",
                      default=u"Available payment methods in checkout"),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            vocabulary='bda.plone.shop.vocabularies.'
                       'AvailablePaymentMethodsVocabulary'
        )
    )

    payment_method = schema.Choice(
        title=_(u"label_payment_method",
                default=u"Payment Method"),
        description=_(u"help_payment_method",
                      default=u"Default payment method in checkout"),
        vocabulary='bda.plone.shop.vocabularies.'
                   'PaymentMethodsVocabulary'
    )

    skip_payment_if_order_contains_reservations = schema.Bool(
        title=_(
            u'label_skip_payment_if_order_contains_reservations',
            default=u'Skip Payment if order contains reservations'
        ),
        required=False
    )

    widget('payment_text', DataGridFieldFactory)
    payment_text = schema.List(
        title=_(
            u"label_payment_text",
            default=u"Payment Texts"
        ),
        value_type=DictRow(
            title=_(u'payment_text', default='Payment Text'),
            schema=ILanguageAndPaymentAwareTextRow),
        required=False
    )

    cash_on_delivery_costs = schema.Float(
        title=_(
            u'label_cash_on_delivery_costs',
            default=u'Cash on delivery costs in gross'
        ),
        required=False
    )
