from .interfaces import IBdaShopConfiguration
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapts, getUtility
from zope.formlib.form import FormFields
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

_ = MessageFactory('bda.plone.shop')


class BdaShopControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IBdaShopConfiguration)
        
    def __init__(self, context):
        super(BdaShopControlPanelAdapter, self).__init__(context)
        self.context = getUtility(IRegistry).forInterface(self.schema, prefix=self.schema_prefix)
        
    shop_currency = ProxyFieldProperty(IBdaShopConfiguration['shop_currency'])
    shop_admin_email = ProxyFieldProperty(IBdaShopConfiguration['shop_admin_email'])
    shop_vat = ProxyFieldProperty(IBdaShopConfiguration['shop_vat'])
    
    

class BdaShopControlPanel(ControlPanelForm):
    form_fields = FormFields(IBdaShopConfiguration)
    label = _(u"BdaShopControlPanel configuration.")
    description = _(u'Settings to configure BdaShopControlPanel.')
    form_name = _(u'BdaShopControlPanelsettings')
    #def _on_save(self, data=None):
    #    pass


