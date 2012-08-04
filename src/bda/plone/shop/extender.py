from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from archetypes.schemaextender.interfaces import (
    IOrderableSchemaExtender,
    IBrowserLayerAwareExtender,
)
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.utils import OrderedDict
from Products.Archetypes.public import TextField
from Products.Archetypes.interfaces import IBaseObject
from bda.plone.shop.interfaces import IShopExtensionLayer

_ = MessageFactory('bda.plone.shop')


class XTextField(ExtensionField, TextField):
    pass


class ExtenderBase(object):
    
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    adapts(IBaseObject)
    
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
    
    def getOrder(self, original):
        neworder = OrderedDict()
        keys = original.keys()
        last = keys.pop()
        keys.insert(1, last)
        for schemata in keys:
            neworder[schemata] = original[schemata]
        return neworder


class BuyableExtender(ExtenderBase):
    """Schema extender for buyable contents
    """
    
    layer = IShopExtensionLayer

    fields = [
        XTextField(
            name='fooooooooo',
            schemata='Buyable',
        ),
    ]