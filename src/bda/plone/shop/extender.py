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
    FloatField,
    BooleanField,
    SelectionWidget,
)
from Products.Archetypes.interfaces import IBaseObject
from bda.plone.shop.interfaces import IShopExtensionLayer
from .interfaces import (
    IBuyable,
    IBuyableDataProvider,
)


_ = MessageFactory('bda.plone.shop')


class XStringField(ExtensionField, StringField): pass
class XFloatField(ExtensionField, FloatField): pass
class XBooleanField(ExtensionField, BooleanField): pass


class ExtenderBase(object):
    
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    adapts(IBuyable)
    
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
        XFloatField(
            name='item_net',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_net', u'Item net price'),
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
        XBooleanField(
            name='item_display_gross',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_display_gross', u'Display Gross'),
            ),
            default=False,
        ),
    ]


def field_value(obj, field_name):
    try:
        acc = obj.getField(field_name).getAccessor(obj)
        return acc()
    except (KeyError, TypeError):
        raise AttributeError


class ATBuyableDataProvider(object):
    implements(IBuyableDataProvider)
    adapts(IBaseObject)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def net(self):
        val = field_value(self.context, 'item_net')
        if not val:
            return 0.0
        return float(val)
    
    @property
    def vat(self):
        val = field_value(self.context, 'item_vat')
        if not val:
            return 0.0
        return float(val)
    
    @property
    def display_gross(self):
        return field_value(self.context, 'item_display_gross')