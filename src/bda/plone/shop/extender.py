from zope.interface import implementer
from zope.component import (
    adapter,
    getUtility,
)
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
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
from bda.plone.cart.interfaces import (
    ICartItemDataProvider,
    ICartItemStock,
)
from .interfaces import (
    IShopExtensionLayer,
    IBuyable,
)


_ = MessageFactory('bda.plone.shop')


def field_value(obj, field_name):
    try:
        acc = obj.getField(field_name).getAccessor(obj)
        return acc()
    except (KeyError, TypeError):
        raise AttributeError


def set_field_value(obj, field_name, value):
    try:
        field = obj.getField(field_name)
        field.set(obj, value)
    except (KeyError, TypeError):
        raise AttributeError


class XStringField(ExtensionField, StringField): pass
class XFloatField(ExtensionField, FloatField): pass
class XBooleanField(ExtensionField, BooleanField): pass


@implementer(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
@adapter(IBuyable)
class ExtenderBase(object):

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
            vocabulary_factory='bda.plone.shop.vocabularies.VatVocabulary',
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
            vocabulary_factory=\
                'bda.plone.shop.vocabularies.QuantityUnitVocabulary',
        ),
    ]


@implementer(ICartItemDataProvider)
@adapter(IBaseObject)
class ATCartItemDataProvider(object):

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
        vocab = getUtility(
            IVocabularyFactory,
            'bda.plone.shop.vocabularies.QuantityUnitVocabulary')(self.context)
        for term in vocab:
            if unit == term.value:
                return term.token


class StockExtender(ExtenderBase):
    """Schema extender for buyable item stock
    """

    layer = IShopExtensionLayer

    fields = [
        XFloatField(
            name='item_available',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_available', u'Item stock available'),
            ),
        ),
        XFloatField(
            name='item_overbook',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_overbook', u'Item stock overbook'),
            ),
        ),
    ]


@implementer(ICartItemStock)
@adapter(IBaseObject)
class ATCartItemStock(object):

    def __init__(self, context):
        self.context = context

    def _get_available(self):
        return field_value(self.context, 'item_available')

    def _set_available(self, value):
        set_field_value(self.context, 'item_available', value)

    available = property(_get_available, _set_available)

    def _get_overbook(self):
        return field_value(self.context, 'item_overbook')

    def _set_overbook(self, value):
        set_field_value(self.context, 'item_overbook', value)

    overbook = property(_get_overbook, _set_overbook)
