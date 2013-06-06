from .interfaces import IBdaShopSettings
from plone.app.registry.browser import controlpanel

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bda.plone.shop')

class BdaShopSettingsEditForm(controlpanel.RegistryEditForm):

    schema =  IBdaShopSettings
    label = _(u"Shop settings")
    description = _(u"""""")
    
    #shop_currency = ProxyFieldProperty(IBdaShopConfiguration['shop_currency'])
    #shop_admin_email = ProxyFieldProperty(IBdaShopConfiguration['shop_admin_email'])
    #shop_vat = ProxyFieldProperty(IBdaShopConfiguration['shop_vat'])

    def updateFields(self):
        super(BdaShopSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(BdaShopSettingsEditForm, self).updateWidgets()

class BdaShopSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = BdaShopSettingsEditForm



    

#registry = getUtility(IRegistry)
#Now we fetch the AkismetSetting registry
# something like this
#from bda.plone.shop.interfaces import IBdaShopSettings
#settings = registry.forInterface(IBdaShopSettings)