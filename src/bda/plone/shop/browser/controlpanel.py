from zope.i18nmessageid import MessageFactory
from plone.app.registry.browser import controlpanel
from ..interfaces import IShopSettings, IShopTaxSettings
from z3c.form import group, field

from zope.component import adapts
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.z3cform.fieldsets import extensible

_ = MessageFactory('bda.plone.shop')


class TaxGroup(group.Group):
    """docstring for TaxGroup"""
    label = _(u'label_tax_group', default=u'Tax Settings')
    fields = field.Fields(IShopTaxSettings)


class ShopSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IShopSettings
    label = _(u"Shop settings")
    description = _(u"")


    # groups = (
    # 	TaxGroup,
    # 	)

    def updateFields(self):
        super(ShopSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(ShopSettingsEditForm, self).updateWidgets()

class TaxSettingsExtender(extensible.FormExtender):
    """docstring for TaxSettingsExtender"""
    adapts(Interface, IDefaultBrowserLayer, ShopSettingsEditForm)
    fields = field.Fields(IShopTaxSettings)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        # Add the fields defined in ICommentExtenderFields to the form.
        self.add(IShopTaxSettings, prefix="")
        # Move the website field to the top of the comment form.
        # self.move('website', before='text', prefix="")
        

class ShopSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ShopSettingsEditForm
