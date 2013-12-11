from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IShopExtensionLayer
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from zope import schema
from zope.component import adapts
from zope.interface import Interface


def validate_accept(value):
    if value is not True:
        return False
    return True


class IAddress(model.Schema):
    model.fieldset('main_address', _('main_address', u'Hauptadresse'),
                   fields=['firstname', 'lastname', 'email', 'phone',
                           'company', 'street', 'zip', 'city', 'country',
                           'alternative_delivery'])
    model.fieldset('delivery_address',
                   _('delivery_address', u'Zustelladresse'),
                   fields=['delivery_firstname', 'delivery_lastname',
                           'delivery_company',
                           'delivery_street', 'delivery_zip',
                           'delivery_city', 'delivery_country',
                           'delivery_phone'])
    model.fieldset('legal',
                   _('legal', u'Legal'),
                   fields=['accept', ])

    gender = schema.Choice(
        title=_(u'label_gender', default=u'Gender'),
        description=_(u'help_gender', default=u""),
        required=False,
        vocabulary='bda.plone.shop.vocabularies.GenderVocabulary'
    )
    firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        description=_(u'help_firstname',
                      default=u"Fill in your given name."),
        required=False,
    )
    lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        description=_(u'help_lastname',
                      default=u"Fill in your surname or your family name."),
        required=False,
    )
    company = schema.TextLine(
        title=_(u'label_company', default=u'Company'),
        description=_(u'help_company'),
        required=False,
    )

    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=False
    )
    zip = schema.TextLine(
        title=_(u'label_zip', default=u'Postal Code'),
        description=_(u'help_zip', default=u''),
        required=False
    )
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u""),
        required=False,
    )
    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country', default=u""),
        required=False,
        vocabulary='bda.plone.shop.vocabularies.CountryVocabulary'
    )

    alternative_delivery = schema.Bool(
        title=_(u'label_alternative_delivery',
                default=u'Alternative delivery address'),
        description=_(u'help_alternative_delivery',
                      default=u"Delivery address is different from billing "
                              u"address."),
        required=False,
        constraint=validate_accept,
    )

    # Delivery Address
    delivery_firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        description=_(u'help_firstname',
                      default=u"Fill in your given name."),
        required=False,
    )
    delivery_lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        description=_(u'help_lastname',
                      default=u"Fill in your surname or your family name."),
        required=False,
    )
    delivery_company = schema.TextLine(
        title=_(u'label_company', default=u'Company'),
        description=_(u'help_company',
                      default=u"Company name, if available."),
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
        description=_(u'help_city', default=u""),
        required=False,
    )
    delivery_country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country', default=u""),
        required=False,
        vocabulary='bda.plone.shop.vocabularies.CountryVocabulary'
    )
    delivery_phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
    )

    accept = schema.Bool(
        title=_(u'label_accept', default=u'Accept terms of use'),
        description=_(u'help_accept',
                      default=u"Tick this box to indicate that you have found,"
                      " read and accepted the terms of use for this site. "),
        required=True,
        constraint=validate_accept,
    )


class UserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IAddress

    @property
    def fullname(self):
        first = self._getProperty('firstname')
        last = self._getProperty('lastname')
        return u'%s%s' % (first and first or '',
                          first and last and ' ' or '',
                          last and last or '')


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IAddress)
        fields = fields.omit('accept')  # Users have already accepted.
        self.add(fields, prefix="delivery")


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, RegistrationForm)

    def update(self):
        fields = field.Fields(IAddress)
        self.add(fields, prefix="delivery")


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, AddUserForm)

    def update(self):
        fields = field.Fields(IAddress)
        # management form doesn't need this field
        fields = fields.omit('accept')
        self.add(fields, prefix="delivery")
