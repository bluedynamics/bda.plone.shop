from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    HAS_CLI = True
except:
    HAS_CLI = False
from bda.plone.cart import CartItemPreviewAdapterBase
from bda.plone.cart.interfaces import ICartItemDataProvider
from bda.plone.cart.interfaces import ICartItemStock
from bda.plone.orders.interfaces import INotificationText
from bda.plone.shipping.interfaces import IShippingItem
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IFieldDefaultProvider
from Products.Archetypes.utils import OrderedDict
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from . import message_factory as _
from .interfaces import IBuyable
from .interfaces import IShopExtensionLayer
from .notificationtext import BubbleNotificationText
from .utils import get_shop_article_settings
from .utils import get_shop_settings
from .utils import get_shop_tax_settings


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
class XTextField(ExtensionField, TextField): pass


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


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_net(context):
    return lambda: get_shop_article_settings().default_item_net


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_vat(context):
    return lambda: get_shop_tax_settings().default_item_vat


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_display_gross(context):
    return lambda: get_shop_settings().default_item_display_gross


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def item_comment_enabled(context):
    return lambda: get_shop_article_settings().default_item_comment_enabled


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_comment_required(context):
    return lambda: get_shop_article_settings().default_item_comment_required


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_quantity_unit_float(context):
    return lambda: get_shop_article_settings().default_item_quantity_unit_float


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_quantity_unit(context):
    return lambda: get_shop_article_settings().default_item_quantity_unit


class BuyableExtender(ExtenderBase):
    """Schema extender for buyable items.
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
        ),
        XBooleanField(
            name='item_comment_enabled',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_enabled', u'Comment enabled'),
            ),
        ),
        XBooleanField(
            name='item_comment_required',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_required', u'Comment required'),
            ),
        ),
        XBooleanField(
            name='item_quantity_unit_float',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_quantity_unit_float',
                        u'Quantity as float'),
            ),
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
                return term.title


class StockExtender(ExtenderBase):
    """Schema extender for item stock.
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
    """Accessor Interface
    """

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


class ShippingExtender(ExtenderBase):
    """Schema extender for item shipping.
    """

    layer = IShopExtensionLayer

    fields = [
        XFloatField(
            name='shipping_item_weight',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_shipping_item_weight', u'Item Weight'),
            ),
        ),
    ]


@implementer(IShippingItem)
@adapter(IBaseObject)
class ATShippingItem(object):

    def __init__(self, context):
        self.context = context

    @property
    def weight(self):
        return field_value(self.context, 'shipping_item_weight')


@adapter(IBaseObject)
class ATCartItemPreviewImage(CartItemPreviewAdapterBase):
    preview_scale = "tile"

    @property
    def url(self):
        """Get url of preview image:
            1. try to read the 'image' field on the context
            2. try to use collective.contentleadimage
        """
        img_scale = None
        scales = self.context.restrictedTraverse('@@images')
        if self.context.getField("image") is not None:
            img_scale = scales.scale("image", scale=self.preview_scale)
        if img_scale is None and HAS_CLI:
            if self.context.getField(IMAGE_FIELD_NAME) is not None:
                img_scale = scales.scale(IMAGE_FIELD_NAME,
                                         scale=self.preview_scale)
        return img_scale and img_scale.url or ""


class NotificationTextExtender(ExtenderBase):
    """Schema extender for notification text.
    """

    layer = IShopExtensionLayer

    fields = [
        XTextField(
            name='order_text',
            schemata='Shop',
            default_content_type="text/plain",
            allowable_content_types=('text/plain',),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_(
                    u'label_order_notification_text',
                    u'Order Notification Text'
                ),
            ),
        ),
        XTextField(
            name='overbook_text',
            schemata='Shop',
            default_content_type="text/plain",
            allowable_content_types=('text/plain',),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_(
                    u'label_overbook_notification_text',
                    u'Overbooked Notification Text'
                ),
            ),
        ),
    ]


@adapter(IBaseObject)
class ATNotificationText(BubbleNotificationText):

    @property
    def order_text(self):
        order_text = self.context.getField('order_text').get(self.context)
        if order_text:
            return order_text
        return super(ATNotificationText, self).order_text

    @property
    def overbook_text(self):
        overbook_text = self.context.getField('overbook_text').get(self.context)
        if overbook_text:
            return overbook_text
        return super(ATNotificationText, self).overbook_text
