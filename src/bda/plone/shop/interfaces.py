# -*- coding: utf-8 -*-
from bda.plone.orders.interfaces import IGlobalNotificationText
from bda.plone.orders.interfaces import IItemNotificationText
from bda.plone.orders.interfaces import IOrdersExtensionLayer
from bda.plone.shop import message_factory as _
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from decimal import Decimal
from plone.autoform.directives import widget
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import provider

import zope.deferredimport


zope.deferredimport.deprecated(
    "Import from bda.plone.orders.interfaces instead",
    IBuyable="bda.plone.orders:interfaces.IBuyable",
)


class IShopExtensionLayer(IOrdersExtensionLayer):
    """Browser layer for bda.plone.shop"""


class IPotentiallyBuyable(Interface):
    """Mark item as potentially buyable.

    Considered for providing action in UI.
    """


class IBuyablePeriod(Interface):
    """Define period in which an item is buyable."""

    effective = Attribute("Buyable effective date")

    expires = Attribute("Buyable expires date")


class IShopSettingsProvider(Interface):
    """A marker interface for plone.registry configuration
    interfaces
    """


class IShopSettings(model.Schema):
    """Shop controlpanel schema."""

    admin_email = schema.ASCIILine(
        title=_("label_admin_email", default="Shop Admin E-Mail"),
        description=_("help_admin_email", default="No typos please...."),
        required=True,
        default="",
    )

    # XXX: change value type to schema.TextLine (needs migration)
    admin_name = schema.ASCIILine(
        title=_("label_admin_name", default="Shop Admin Name"),
        description=_("help_admin_name", default="Name used for Shop E-Mails."),
        required=True,
        default="",
    )

    add_customer_role_to_new_users = schema.Bool(
        title=_(
            "label_add_customer_role_to_new_users",
            default="Add Customer role to new Users",
        ),
        required=False,
        default=True,
    )

    # XXX: this is an article setting, move to IShopArticleSettings
    default_item_display_gross = schema.Bool(
        title=_("label_default_item_display_gross", default="Display Gross by default"),
        required=False,
        default=False,
    )

    currency = schema.Choice(
        title=_("label_currency", default="Currency"),
        description=_("help_currency", default="Choose the default currency"),
        vocabulary="bda.plone.shop.vocabularies.AvailableCurrenciesVocabulary",
        default="EUR",
    )

    show_currency = schema.Choice(
        title=_("label_show_currency", default="Show the currency for items"),
        description=_("help_show_currency", default=""),
        vocabulary="bda.plone.shop.vocabularies.CurrencyDisplayOptionsVocabulary",
        default="symbol",
    )


@provider(IShopSettingsProvider)
class IShopCartSettings(model.Schema):
    """Shop controlpanel schema for cart settings."""

    model.fieldset(
        "cart",
        label=_("Cart", default="Cart"),
        fields=[
            "hide_cart_if_empty",
            "max_artice_count",
            "disable_max_article",
            "summary_total_only",
            "show_checkout",
            "show_to_cart",
        ],
    )

    hide_cart_if_empty = schema.Bool(
        title=_("label_hide_cart_if_empty", default="Hide Cart if empty"),
        description=_(
            "help_hide_cart_if_empty", default="Hide cart if no items contained"
        ),
        default=False,
        required=False,
    )

    max_artice_count = schema.Int(
        title=_("label_max_artice_count", default="Maximum number articles in cart"),
        description=_(
            "help_max_artice_count",
            default="Maximum number of articles in cart if disable max "
            "article flag set",
        ),
        required=False,
        default=5,
    )

    disable_max_article = schema.Bool(
        title=_("label_disable_max_article", default="Disable max article"),
        description=_(
            "help_disable_max_article",
            default="No total number of items in cart limit",
        ),
        default=True,
        required=False,
    )

    summary_total_only = schema.Bool(
        title=_("label_summary_total_only", default="Cart Summary total only"),
        description=_(
            "help_summary_total_only", default="Show only total value in cart summary"
        ),
        default=False,
        required=False,
    )

    show_checkout = schema.Bool(
        title=_("label_show_checkout", default="Show checkout link in portlet"),
        description=_("help_show_checkout", default=""),
        default=False,
        required=False,
    )

    show_to_cart = schema.Bool(
        title=_("label_show_to_cart", default="Show link to cart in portlet"),
        description=_("help_show_to_cart", default=""),
        default=True,
        required=False,
    )


@provider(IShopSettingsProvider)
class IShopArticleSettings(model.Schema):
    """Shop controlpanel schema for article settings."""

    model.fieldset(
        "article",
        label=_("Article", default="Article"),
        fields=[
            "quantity_units",
            "default_item_net",
            "default_item_quantity_unit",
            "default_item_comment_enabled",
            "default_item_comment_required",
            "default_item_quantity_unit_float",
            "default_item_cart_count_limit",
            "default_item_stock_warning_threshold",
        ],
    )

    widget("quantity_units", CheckBoxFieldWidget)
    quantity_units = schema.List(
        title=_(
            "label_quantity_units", default="Specify quantity units allowed in shop."
        ),
        description=_(
            "help_quantity_units",
            default="Quantity units (what the buyable items are measured in)",
        ),
        required=False,
        missing_value=set(["quantity"]),
        value_type=schema.Choice(
            vocabulary="bda.plone.shop.vocabularies.AvailableQuantityUnitVocabulary"
        ),
    )

    default_item_quantity_unit = schema.Choice(
        title=_(
            "label_default_quantity_units", default="Specify default quantity name."
        ),
        description=_("help_default_quantity_unit", default="default measurement"),
        vocabulary="bda.plone.shop.vocabularies.QuantityUnitVocabulary",
    )

    default_item_net = schema.Decimal(
        title=_("label_default_item_net", default="Default Item net price"),
        required=False,
        default=Decimal("10.0"),
    )

    default_item_comment_enabled = schema.Bool(
        title=_(
            "label_default_item_comment_enabled", default="Comment enabled by default"
        ),
        required=False,
        default=True,
    )

    default_item_comment_required = schema.Bool(
        title=_(
            "label_default_item_comment_required",
            default="Comment required by default",
        ),
        required=False,
        default=False,
    )

    default_item_quantity_unit_float = schema.Bool(
        title=_(
            "label_default_item_quantity_unit_float",
            default="Quantity as float as default",
        ),
        required=False,
        default=False,
    )

    default_item_cart_count_limit = schema.Decimal(
        title=_(
            "label_default_item_cart_count_limit",
            default="Quantity limit of an item in the cart.",
        ),
        required=False,
    )

    default_item_stock_warning_threshold = schema.Decimal(
        title=_(
            "label_default_item_stock_warning_threshold",
            default="Item stock warning threshold.",
        ),
        description=_(
            "help_default_item_stock_warning_threshold",
            default="Shop administrator will be notified if stock is less "
            "than the specified threshold.",
        ),
        required=False,
    )


@provider(IShopSettingsProvider)
class IShopShippingSettings(model.Schema):
    """Shop controlpanel schema for article settings."""

    model.fieldset(
        "shipping",
        label=_("Shipping", default="Shipping"),
        fields=[
            "default_shipping_item_shippable",
            "available_shipping_methods",
            "shipping_method",
            "shipping_vat",
            "shipping_limit_from_gross",
            "free_shipping_limit",
            "flat_shipping_cost",
            "item_shipping_cost",
        ],
    )

    default_shipping_item_shippable = schema.Bool(
        title=_(
            "label_default_shipping_item_shippable",
            default="Item Shippable by default",
        ),
        description=_(
            "help_default_shipping_item_shippable",
            default="Flag whether item is shippable by default, "
            "i.e. downloads are not",
        ),
        required=False,
        default=True,
    )

    available_shipping_methods = schema.List(
        title=_(
            "label_available_shipping_methods", default="Available Shipping Methods"
        ),
        description=_(
            "help_available_shipping_methods",
            default="Available shipping methods in checkout",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            vocabulary="bda.plone.shop.vocabularies."
            "AvailableShippingMethodsVocabulary"
        ),
    )

    shipping_method = schema.Choice(
        title=_("label_shipping_method", default="Shipping Method"),
        description=_(
            "help_shipping_method", default="Default shipping method in checkout"
        ),
        vocabulary="bda.plone.shop.vocabularies.ShippingMethodsVocabulary",
        default="default_shipping",
    )

    shipping_vat = schema.Choice(
        title=_("label_shipping_vat", default="Shipping VAT"),
        description=_(
            "help_shipping_vat", default="VAT used to calculate shipping costs"
        ),
        vocabulary="bda.plone.shop.vocabularies.VatVocabulary",
        default="20",
    )

    # default shipping related settings

    free_shipping_limit = schema.Decimal(
        title=_("label_free_shipping_limit", default="Free Shipping Limit"),
        description=_(
            "help_free_shipping_limit",
            default="Do not add shipping costs to orders "
            "with price bigger than limit. If limit "
            "applies to gross or net purchase price "
            "depends on 'Calculate shipping limit from "
            "gross' setting",
        ),
        required=True,
        default=Decimal("200.0"),
    )

    shipping_limit_from_gross = schema.Bool(
        title=_(
            "label_shipping_limit_from_gross",
            default="Calculate shipping limit from gross",
        ),
        description=_(
            "help_shipping_limit_from_gross",
            default="If set to False, shipping limit gets "
            "calculated from net price instead of gross.",
        ),
        required=False,
        default=True,
    )

    flat_shipping_cost = schema.Decimal(
        title=_("label_flat_shipping_cost", default="Flat shipping cost"),
        description=_("help_flat_shipping_cost", default="Net flat shipping cost"),
        required=True,
        default=Decimal("10.0"),
    )

    item_shipping_cost = schema.Decimal(
        title=_("label_item_shipping_cost", default="Item shipping cost"),
        description=_(
            "help_item_shipping_cost",
            default="Net shipping cost per item in cart. If flat "
            "shipping cost set and item shipping cost "
            "below flat shipping cost, flat shipping cost "
            "is used",
        ),
        required=True,
        default=Decimal("0.0"),
    )


@provider(IShopSettingsProvider)
class IShopTaxSettings(model.Schema):
    """Shop controlpanel schema for tax settings."""

    model.fieldset("tax", label=_("Tax Settings"), fields=["vat", "default_item_vat"])

    widget("vat", CheckBoxFieldWidget)
    vat = schema.List(
        title=_("label_vat", default="VAT in %"),
        description=_("help_vat", default="Specify all allowed vat settings"),
        required=False,
        missing_value=set([0]),
        value_type=schema.Choice(
            vocabulary="bda.plone.shop.vocabularies.AvailableVatVocabulary"
        ),
    )

    default_item_vat = schema.Choice(
        title=_("label_default_vat", default="Default Value added tax name"),
        description=_("help_default_vat", default="Specify default vat name"),
        vocabulary="bda.plone.shop.vocabularies.VatVocabulary",
        default="20",
    )


class ILanguageAwareTextRow(model.Schema):

    lang = schema.Choice(
        title=_("language", default="Language"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        required=False,
    )

    text = schema.Text(title=_("text", default="Text"), required=False)


@provider(IShopSettingsProvider)
class INotificationTextSettings(
    model.Schema, IGlobalNotificationText, IItemNotificationText
):

    model.fieldset(
        "notifications",
        label=_("Notifications", default="Notifications"),
        fields=[
            "global_order_text",
            "global_overbook_text",
            "order_text",
            "overbook_text",
        ],
    )

    widget("order_text", DataGridFieldFactory)
    order_text = schema.List(
        title=_(
            "label_site_item_notification_text",
            default="Default notification text for items in order confirmation mail",
        ),
        value_type=DictRow(
            title=_("order_text", default="Order Text"), schema=ILanguageAwareTextRow
        ),
        required=False,
    )

    widget("overbook_text", DataGridFieldFactory)
    overbook_text = schema.List(
        title=_(
            "label_site_item_overbook_notification_text",
            default="Default notification text for items in order "
            "confirmation mail if item out of stock.",
        ),
        value_type=DictRow(
            title=_("overbook_text", default="Overbook Text"),
            schema=ILanguageAwareTextRow,
        ),
        required=False,
    )

    widget("global_order_text", DataGridFieldFactory)
    global_order_text = schema.List(
        title=_(
            "label_site_global_notification_text",
            default="Overall notification text for order confirmation mail",
        ),
        value_type=DictRow(
            title=_("order_text", default="Order Text"), schema=ILanguageAwareTextRow
        ),
        required=False,
    )

    widget("global_overbook_text", DataGridFieldFactory)
    global_overbook_text = schema.List(
        title=_(
            "label_site_global_overbook_notification_text",
            default="Overall notification text for order confirmation mail "
            "if order contains items out of stock",
        ),
        value_type=DictRow(
            title=_("overbook_text", default="Overbook Text"),
            schema=ILanguageAwareTextRow,
        ),
        required=False,
    )


@provider(IShopSettingsProvider)
class IInvoiceSettings(model.Schema):
    """Global invoice settings."""

    model.fieldset(
        "invoice",
        label=_("Invoice", default="Invoice"),
        fields=[
            "default_invoice_company",
            "default_invoice_companyadd",
            "default_invoice_firstname",
            "default_invoice_lastname",
            "default_invoice_street",
            "default_invoice_zip",
            "default_invoice_city",
            "default_invoice_country",
            "default_invoice_phone",
            "default_invoice_email",
            "default_invoice_web",
            "default_invoice_iban",
            "default_invoice_bic",
        ],
    )

    default_invoice_company = schema.TextLine(
        title=_("label_company", default="Company"),
        description=_(
            "help_invoice_company", default="Company name of invoice sender."
        ),
        required=False,
    )

    default_invoice_companyadd = schema.TextLine(
        title=_("label_companyadd", default="Company additional"),
        description=_(
            "help_invoice_companyadd",
            default="Optional additional line displayed under company name",
        ),
        required=False,
    )

    default_invoice_firstname = schema.TextLine(
        title=_("label_firstname", default="First name"),
        description=_("help_invoice_firstname", default="Given name of invoice sender"),
        required=False,
    )

    default_invoice_lastname = schema.TextLine(
        title=_("label_lastname", default="Last name"),
        description=_("help_invoice_lastname", default="Last name of invoice sender"),
        required=False,
    )

    default_invoice_street = schema.TextLine(
        title=_("label_street", default="Street"),
        description=_("help_invoice_street", default="Street of invoice sender"),
        required=False,
    )

    default_invoice_zip = schema.TextLine(
        title=_("label_zip", default="Postal Code"),
        description=_("help_invoice_zip", default="Postal code of invoice sender"),
        required=False,
    )

    default_invoice_city = schema.TextLine(
        title=_("label_city", default="City"),
        description=_("help_invoice_city", default="City of invoice sender"),
        required=False,
    )

    default_invoice_country = schema.Choice(
        title=_("label_country", default="Country"),
        description=_("help_invoice_country", default="Country of invoice sender"),
        required=False,
        vocabulary="bda.plone.shop.vocabularies.CountryVocabulary",
        default="040",
    )

    default_invoice_phone = schema.TextLine(
        title=_("label_phone", default="Phone"),
        description=_(
            "help_invoice_phone", default="Optional phone number of invoice sender"
        ),
        required=False,
    )

    default_invoice_email = schema.TextLine(
        title=_("label_email", default="Email address"),
        description=_(
            "help_invoice_email", default="Optional email address of invoice sender"
        ),
        required=False,
    )

    default_invoice_web = schema.TextLine(
        title=_("label_web", default="Web address"),
        description=_(
            "help_invoice_web", default="Optional web address of invoice sender"
        ),
        required=False,
    )

    default_invoice_iban = schema.TextLine(
        title=_("label_iban", default="IBAN"),
        description=_(
            "help_invoice_iban", default="Invoice sender banking account IBAN"
        ),
        required=False,
    )

    default_invoice_bic = schema.TextLine(
        title=_("label_bic", default="BIC"),
        description=_("help_invoice_bic", default="Invoice sender banking account BIC"),
        required=False,
    )


class ILanguageAndPaymentAwareTextRow(model.Schema):

    payment = schema.Choice(
        title=_("payment", default="Payment"),
        vocabulary="bda.plone.shop.vocabularies.PaymentMethodsVocabulary",
        required=False,
    )

    lang = schema.Choice(
        title=_("language", default="Language"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        required=False,
    )

    text = schema.Text(title=_("text", default="Text"), required=False)


@provider(IShopSettingsProvider)
class IPaymentTextSettings(model.Schema):
    # XXX: rename to IPaymentSettings

    model.fieldset(
        "payment",
        label=_("Payment", default="Payment"),
        fields=[
            "available_payment_methods",
            "payment_method",
            "skip_payment_if_order_contains_reservations",
            "payment_text",
            "cash_on_delivery_costs",
        ],
    )

    available_payment_methods = schema.List(
        title=_("label_available_payment_methods", default="Available Payment Methods"),
        description=_(
            "help_available_payment_methods",
            default="Available payment methods in checkout",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            vocabulary="bda.plone.shop.vocabularies."
            "AvailablePaymentMethodsVocabulary"
        ),
    )

    payment_method = schema.Choice(
        title=_("label_payment_method", default="Payment Method"),
        description=_(
            "help_payment_method", default="Default payment method in checkout"
        ),
        vocabulary="bda.plone.shop.vocabularies.PaymentMethodsVocabulary",
        default="invoice",
    )

    skip_payment_if_order_contains_reservations = schema.Bool(
        title=_(
            "label_skip_payment_if_order_contains_reservations",
            default="Skip Payment if order contains reservations",
        ),
        required=False,
    )

    widget("payment_text", DataGridFieldFactory)
    payment_text = schema.List(
        title=_("label_payment_text", default="Payment Texts"),
        value_type=DictRow(
            title=_("payment_text", default="Payment Text"),
            schema=ILanguageAndPaymentAwareTextRow,
        ),
        required=False,
    )

    cash_on_delivery_costs = schema.Decimal(
        title=_(
            "label_cash_on_delivery_costs", default="Cash on delivery costs in gross"
        ),
        required=False,
        default=Decimal("9.9"),
    )
