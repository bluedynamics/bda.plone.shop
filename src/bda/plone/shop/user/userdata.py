# -*- coding: utf-8 -*-
from bda.plone.checkout.interfaces import ICheckoutFormPresets
from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IShopExtensionLayer
from node.utils import UNSET
from plone import api
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import AddUserForm
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class ICustomer(model.Schema):

    model.fieldset(
        "main_address",
        _("main_address", "Main Address"),
        fields=[
            "firstname",
            "lastname",
            "phone",
            "company",
            "street",
            "zip",
            "city",
            "country",
            "delivery_alternative_delivery",
        ],
    )

    model.fieldset(
        "delivery_address",
        _("delivery_address", "Delivery Address"),
        fields=[
            "delivery_firstname",
            "delivery_lastname",
            "delivery_company",
            "delivery_street",
            "delivery_zip",
            "delivery_city",
            "delivery_country",
        ],
    )

    model.fieldset("legal", _("legal", "Legal"), fields=["accept"])

    # Personal Data
    gender = schema.Choice(
        title=_("label_gender", default="Gender"),
        description=_("help_gender", default=""),
        required=False,
        vocabulary="bda.plone.shop.vocabularies.GenderVocabulary",
    )

    firstname = schema.TextLine(
        title=_("label_firstname", default="First name"),
        description=_("help_firstname", default="Fill in your given name."),
        required=True,
    )

    lastname = schema.TextLine(
        title=_("label_lastname", default="Last name"),
        description=_(
            "help_lastname", default="Fill in your surname or your family name."
        ),
        required=True,
    )

    phone = schema.TextLine(
        title=_("label_phone", default="Phone"),
        description=_("help_phone", default=""),
        required=True,
    )

    company = schema.TextLine(
        title=_("label_company", default="Company"),
        description=_("help_company", default=""),
        required=False,
    )

    # Billing Address
    street = schema.TextLine(
        title=_("label_street", default="Street"),
        description=_("help_street", default=""),
        required=True,
    )

    zip = schema.TextLine(
        title=_("label_zip", default="Postal Code"),
        description=_("help_zip", default=""),
        required=True,
    )

    city = schema.TextLine(
        title=_("label_city", default="City"),
        description=_("help_city", default=""),
        required=True,
    )

    country = schema.Choice(
        title=_("label_country", default="Country"),
        description=_("help_country", default=""),
        required=True,
        vocabulary="bda.plone.shop.vocabularies.CountryVocabulary",
    )

    # Delivery Address
    delivery_alternative_delivery = schema.Bool(
        title=_("label_alternative_delivery", default="Alternative delivery address"),
        description=_(
            "help_alternative_delivery",
            default="Delivery address is different from billing " "address.",
        ),
        required=False,
    )

    delivery_firstname = schema.TextLine(
        title=_("label_firstname", default="First name"),
        description=_("help_firstname", default="Fill in your given name."),
        required=False,
    )

    delivery_lastname = schema.TextLine(
        title=_("label_lastname", default="Last name"),
        description=_(
            "help_lastname", default="Fill in your surname or your family name."
        ),
        required=False,
    )

    delivery_company = schema.TextLine(
        title=_("label_company", default="Company"),
        description=_("help_company", default=""),
        required=False,
    )

    delivery_street = schema.TextLine(
        title=_("label_street", default="Street"),
        description=_("help_street", default=""),
        required=False,
    )

    delivery_zip = schema.TextLine(
        title=_("label_zip", default="Postal Code"),
        description=_("help_zip", default=""),
        required=False,
    )

    delivery_city = schema.TextLine(
        title=_("label_city", default="City"),
        description=_("help_city", default=""),
        required=False,
    )

    delivery_country = schema.Choice(
        title=_("label_country", default="Country"),
        description=_("help_country", default=""),
        required=False,
        vocabulary="bda.plone.shop.vocabularies.CountryVocabulary",
    )

    # Terms and Conditions
    accept = schema.Bool(
        title=_("label_accept", default="Accept terms of use"),
        description=_(
            "help_accept",
            default="Tick this box to indicate that you have found,"
            " read and accepted the terms of use for this site.",
        ),
        required=False,
    )


class UserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = ICustomer


@adapter(Interface, IShopExtensionLayer, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):
    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove("fullname")
        self.remove("location")
        fields = field.Fields(ICustomer)
        fields = fields.omit("accept")  # Users have already accepted.
        self.add(fields, prefix="delivery")


@adapter(Interface, IShopExtensionLayer, RegistrationForm)
class RegistrationPanelExtender(extensible.FormExtender):
    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove("fullname")
        self.remove("location")
        fields = field.Fields(ICustomer)
        self.add(fields, prefix="delivery")


@adapter(Interface, IShopExtensionLayer, AddUserForm)
class AddUserFormExtender(extensible.FormExtender):
    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove("fullname")
        self.remove("location")
        fields = field.Fields(ICustomer)
        # management form doesn't need this field
        fields = fields.omit("accept")
        self.add(fields, prefix="delivery")


@implementer(ICheckoutFormPresets)
@adapter(Interface, IShopExtensionLayer)
class CheckoutFormMemberPresets(object):
    """Adapter to retrieve member presets for checkout form."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        if api.user.is_anonymous():
            self.member = None
        else:
            self.member = api.user.get_current()

    def get_value(self, field_name):
        default = UNSET
        if self.member:
            parts = field_name.split(".")
            name = parts[-1]
            if "delivery_address" in parts:
                name = "delivery_%s" % name
            default = self.member.getProperty(name, UNSET)
        return default
