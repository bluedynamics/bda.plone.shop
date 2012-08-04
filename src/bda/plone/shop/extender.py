from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from archetypes.schemaextender.interfaces import (
    IOrderableSchemaExtender,
    IBrowserLayerAwareExtender,
)
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.utils import OrderedDict
from Products.Archetypes.public import (
    StringField,
    BooleanField,
    FixedPointField,
    BooleanWidget,
    DecimalWidget,
    SelectionWidget,
)
from Products.Archetypes.interfaces import IBaseObject
from bda.plone.shop.interfaces import IShopExtensionLayer

_ = MessageFactory('bda.plone.shop')


class XStringField(ExtensionField, StringField): pass
class XBooleanField(ExtensionField, BooleanField): pass
class XFixedPointField(ExtensionField, FixedPointField): pass


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
        XBooleanField(
            name='item_buyable',
            schemata='Shop',
            widget=BooleanWidget(
                label=_(u'label_item_buyable', u'Item buyable?'),
            ),
        ),
        XFixedPointField(
            name='item_price',
            schemata='Shop',
            widget=DecimalWidget(
                label=_(u'label_item_price', u'Item price'),
            ),
        ),
        XStringField(
            name='item_vat',
            schemata='Shop',
            widget=SelectionWidget(
                label=_(u'label_item_vat', u'Item VAT (in %)'),
            ),
            vocabulary=['10', '20'],
        ),
    ]