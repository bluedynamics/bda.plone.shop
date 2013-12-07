from bda.plone.shop.interfaces import IShopExtensionLayer
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from zope import schema
from zope.component import adapts
from zope.interface import Interface
from bda.plone.shop import message_factory as _


def validate_accept(value):
    if value is not True:
        return False
    return True


class IAddress(model.Schema):
    model.fieldset('main_address', _('main_address', u'Hauptadresse'),
                   fields=['street', 'zip_code', 'city', 'country', 'phone'])
    model.fieldset('delivery_address',
                   _('delivery_address', u'Zustelladresse'),
                   fields=['delivery_street', 'delivery_zip_code',
                           'delivery_city', 'delivery_country',
                           'delivery_phone'])

    street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=False
    )
    zip_code = schema.TextLine(
        title=_(u'label_zip_code', default=u'Zip Code'),
        description=_(u'help_zip_code', default=u''),
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
        vocabulary='collective.address.CountryVocabulary'
    )
    phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
    )

    delivery_address = schema.Bool(
        title=_(u'label_delivery_address',
                default=u'Delivery address different'),
        description=_(u'help_accept',
                      default=u"Delivery address is different from payment."),
        required=True,
        constraint=validate_accept,
    )

    # Delivery Address
    delivery_name = schema.TextLine(
        title=_(u'label_name', default=u'Name'),
        description=_(u'help_name', default=u''),
        required=False
    )
    delivery_street = schema.TextLine(
        title=_(u'label_street', default=u'Street'),
        description=_(u'help_street', default=u''),
        required=False
    )
    delivery_zip_code = schema.TextLine(
        title=_(u'label_zip_code', default=u'Zip Code'),
        description=_(u'help_zip_code', default=u''),
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
        vocabulary='collective.address.CountryVocabulary'
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



from plone.app.users.browser.account import AccountPanelSchemaAdapter
class UserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IAddress


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
