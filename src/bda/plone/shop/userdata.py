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


class IDeliveryAddress(model.Schema):
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
    delivery_country = schema.TextLine(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country', default=u""),
        required=False,
        )
    delivery_phone = schema.TextLine(
        title=_(u'label_phone', default=u'Telephone number'),
        description=_(u'help_phone',
                      default=u"Leave your phone number so we can reach you."),
        required=False,
        )


from plone.app.users.browser.account import AccountPanelSchemaAdapter
class UserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IDeliveryAddress


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IDeliveryAddress)
        self.add(fields, prefix="delivery")


class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, RegistrationForm)

    def update(self):
        fields = field.Fields(IDeliveryAddress)
        self.add(fields, prefix="delivery")


class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IShopExtensionLayer, AddUserForm)

    def update(self):
        fields = field.Fields(IDeliveryAddress)
        self.add(fields, prefix="delivery")
