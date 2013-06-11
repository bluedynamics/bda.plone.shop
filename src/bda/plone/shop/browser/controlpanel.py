from zope.i18nmessageid import MessageFactory
from plone.app.registry.browser import controlpanel
from ..interfaces import IShopSettings


_ = MessageFactory('bda.plone.shop')


class ShopSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IShopSettings
    label = _(u"Shop settings")
    description = _(u"")

    def updateFields(self):
        super(ShopSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(ShopSettingsEditForm, self).updateWidgets()


class ShopSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ShopSettingsEditForm
