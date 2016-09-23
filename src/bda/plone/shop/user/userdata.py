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

    model.fieldset('main_address', _('main_address', u'Main Address'),
                   fields=['firstname', 'lastname', 'phone',
                           'company', 'street', 'zip', 'city', 'country',
                           'delivery_alternative_delivery'])

    model.fieldset('delivery_address',
                   _('delivery_address', u'Delivery Address'),
                   fields=['delivery_firstname', 'delivery_lastname',
                           'delivery_company',
                           'delivery_street', 'delivery_zip',
                           'delivery_city', 'delivery_country'])

    model.fieldset('legal',
                   _('legal', u'Legal'),
                   fields=['accept', ])

    # Personal Data
    gender = schema.Choice(
        title=_(u'label_gender', default=u'Gender'),
        description=_(u'help_gender', default=u''),
        required=False,
        vocabulary='bda.plone.shop.vocabularies.GenderVocabulary'
    )

    firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        description=_(u'help_firstname',
                      default=u'Fill in your given name.'),
        required=True,
    )

    lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        description=_(u'help_lastname',
                      default=u'Fill in your surname or your family name.'),
        required=True,
    )

    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Phone'),
        description=_(u'help_phone', default=u''),
        required=True,
    )

    company = schema.TextLine(
        title=_(u'label_company', default=u'Company'),
        description=_(u'help_company', default=u''),
        required=False,
    )

    # Billing Address
    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=True
    )

    zip = schema.TextLine(
        title=_(u'label_zip', default=u'Postal Code'),
        description=_(u'help_zip', default=u''),
        required=True
    )

    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=True,
    )

    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country', default=u''),
        required=True,
        vocabulary='bda.plone.shop.vocabularies.CountryVocabulary'
    )

    # Delivery Address
    delivery_alternative_delivery = schema.Bool(
        title=_(u'label_alternative_delivery',
                default=u'Alternative delivery address'),
        description=_(u'help_alternative_delivery',
                      default=u"Delivery address is different from billing "
                              u"address."),
        required=False,
    )

    delivery_firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        description=_(u'help_firstname',
                      default=u'Fill in your given name.'),
        required=False,
    )

    delivery_lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        description=_(u'help_lastname',
                      default=u'Fill in your surname or your family name.'),
        required=False,
    )

    delivery_company = schema.TextLine(
        title=_(u'label_company', default=u'Company'),
        description=_(u'help_company', default=u''),
        required=False,
    )

    delivery_street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=False
    )

    delivery_zip = schema.TextLine(
        title=_(u'label_zip', default=u'Postal Code'),
        description=_(u'help_zip', default=u''),
        required=False
    )

    delivery_city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=False,
    )

    delivery_country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country', default=u''),
        required=False,
        vocabulary='bda.plone.shop.vocabularies.CountryVocabulary'
    )

    # Terms and Conditions
    accept = schema.Bool(
        title=_(u'label_accept', default=u'Accept terms of use'),
        description=_(u'help_accept',
                      default=u'Tick this box to indicate that you have found,'
                      ' read and accepted the terms of use for this site.'),
        required=False
    )


class UserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = ICustomer


@adapter(Interface, IShopExtensionLayer, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):

    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove('fullname')
        self.remove('location')
        fields = field.Fields(ICustomer)
        fields = fields.omit('accept')  # Users have already accepted.
        self.add(fields, prefix="delivery")


@adapter(Interface, IShopExtensionLayer, RegistrationForm)
class RegistrationPanelExtender(extensible.FormExtender):

    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove('fullname')
        self.remove('location')
        fields = field.Fields(ICustomer)
        self.add(fields, prefix="delivery")


@adapter(Interface, IShopExtensionLayer, AddUserForm)
class AddUserFormExtender(extensible.FormExtender):

    def update(self):
        # Remove fields, where our schema has substitutes
        self.remove('fullname')
        self.remove('location')
        fields = field.Fields(ICustomer)
        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields, prefix="delivery")


@implementer(ICheckoutFormPresets)
@adapter(Interface, IShopExtensionLayer)
class CheckoutFormMemberPresets(object):
    """Adapter to retrieve member presets for checkout form.
    """

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
            parts = field_name.split('.')
            name = parts[-1]
            if 'delivery_address' in parts:
                name = 'delivery_%s' % name
            default = self.member.getProperty(name, UNSET)
        return default
