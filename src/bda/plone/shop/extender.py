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
    StringWidget,
    SelectionWidget,
)
from Products.Archetypes.interfaces import IBaseObject
from bda.plone.cart.interfaces import ICartItemDataProvider
from bda.plone.shop.interfaces import IShopExtensionLayer
from .interfaces import IBuyable


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


VAT_VOCAB = ['10', '20']
QUANTITY_UNIT_VOCAB = [
    ('quantity', _('quantity', 'Quantity')),
    ('meter', _('meter', 'Meter')),
    ('kilo', _('kilo', 'Kilo')),
    ('liter', _('liter', 'Liter')),
]


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
            vocabulary=VAT_VOCAB,
        ),
        XBooleanField(
            name='item_display_gross',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_display_gross', u'Display Gross'),
            ),
            default=False,
        ),
        XBooleanField(
            name='item_comment_enabled',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_enabled', u'Comment enabled'),
            ),
            default=True,
        ),
        XBooleanField(
            name='item_comment_required',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_required', u'Comment required'),
            ),
            default=False,
        ),
        XBooleanField(
            name='item_quantity_unit_float',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_quantity_unit_float',
                        u'Quantity as float'),
            ),
            default=False,
        ),
        XStringField(
            name='item_quantity_unit',
            schemata='Shop',
            widget=SelectionWidget(
                label=_(u'label_item_quantity_unit', u'Quantity unit'),
            ),
            vocabulary=QUANTITY_UNIT_VOCAB,
        ),
    ]


def field_value(obj, field_name):
    try:
        acc = obj.getField(field_name).getAccessor(obj)
        return acc()
    except (KeyError, TypeError):
        raise AttributeError


class ATCartItemDataProvider(object):
    implements(ICartItemDataProvider)
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

    @property
    def comment_enabled(self):
        return field_value(self.context, 'item_comment_enabled')

    @property
    def comment_required(self):
        return field_value(self.context, 'item_comment_required')

    @property
    def quantity_unit_float(self):
        return field_value(self.context, 'item_quantity_unit_float')

    @property
    def quantity_unit(self):
        unit = field_value(self.context, 'item_quantity_unit')
        for key, term in QUANTITY_UNIT_VOCAB:
            if unit == key:
                return term
