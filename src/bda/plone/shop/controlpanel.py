from .interfaces import IBdaShopSettings
from plone.app.registry.browser import controlpanel

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bda.plone.shop')

class BdaShopSettingsEditForm(controlpanel.RegistryEditForm):

    schema =  IBdaShopSettings
    label = _(u"Shop settings")
    description = _(u"""""")

    def updateFields(self):
        super(BdaShopSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(BdaShopSettingsEditForm, self).updateWidgets()

class BdaShopSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BdaShopSettingsEditForm

