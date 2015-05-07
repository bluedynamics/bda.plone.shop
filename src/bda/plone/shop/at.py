# -*- coding: utf-8 -*-
from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import TextField
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IFieldDefaultProvider
from Products.Archetypes.utils import OrderedDict
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bda.plone.cart import CartItemDataProviderBase
from bda.plone.cart import CartItemPreviewAdapterBase
from bda.plone.cart.interfaces import ICartItemStock
from bda.plone.orders.interfaces import IBuyable
from bda.plone.orders.interfaces import ITrading
from bda.plone.shipping.interfaces import IShippingItem
from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IBuyablePeriod
from bda.plone.shop.interfaces import IShopExtensionLayer
from bda.plone.shop.mailnotify import BubbleGlobalNotificationText
from bda.plone.shop.mailnotify import BubbleItemNotificationText
from bda.plone.shop.utils import get_shop_article_settings
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_shipping_settings
from bda.plone.shop.utils import get_shop_tax_settings
from datetime import datetime
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    HAS_CLI = True
except:
    HAS_CLI = False


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
class XDateTimeField(ExtensionField, DateTimeField): pass


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
def default_item_cart_count_limit(context):
    return lambda: get_shop_article_settings().default_item_cart_count_limit

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
                label=_(u'label_item_net', default=u'Item net price'),
            ),
        ),
        XStringField(
            name='item_vat',
            schemata='Shop',
            widget=SelectionWidget(
                label=_(u'label_item_vat', default=u'Item VAT (in %)'),
            ),
            vocabulary_factory='bda.plone.shop.vocabularies.VatVocabulary',
        ),
        XFloatField(
            name='item_cart_count_limit',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_cart_count_limit',
                        default=u'Max count of this item in cart'),
            ),
        ),
        XBooleanField(
            name='item_display_gross',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_display_gross', default=u'Display Gross'),
            ),
        ),
        XBooleanField(
            name='item_comment_enabled',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_enabled',
                        default=u'Comment enabled'),
            ),
        ),
        XBooleanField(
            name='item_comment_required',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_comment_required',
                        default=u'Comment required'),
            ),
        ),
        XBooleanField(
            name='item_quantity_unit_float',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_quantity_unit_float',
                        default=u'Quantity as float'),
            ),
        ),
        XStringField(
            name='item_quantity_unit',
            schemata='Shop',
            widget=SelectionWidget(
                label=_(u'label_item_quantity_unit', default=u'Quantity unit'),
            ),
            vocabulary_factory=\
                'bda.plone.shop.vocabularies.QuantityUnitVocabulary',
        ),
    ]


@adapter(IBaseObject)
class ATCartItemDataProvider(CartItemDataProviderBase):
    """Accessor Interface
    """

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
    def cart_count_limit(self):
        return field_value(self.context, 'item_cart_count_limit')

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


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_item_display_stock(context):
    return lambda: True


class StockExtender(ExtenderBase):
    """Schema extender for item stock.
    """

    layer = IShopExtensionLayer

    fields = [
        XBooleanField(
            name='item_display_stock',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_item_display_stock',
                        default=u'Display item stock'),
            ),
        ),
        XFloatField(
            name='item_available',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_available',
                        default=u'Item stock available'),
            ),
        ),
        XFloatField(
            name='item_overbook',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_item_overbook',
                        default=u'Item stock overbook'),
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

    @property
    def display(self):
        return field_value(self.context, 'item_display_stock')

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


@implementer(IFieldDefaultProvider)
@adapter(IBuyable)
def default_shipping_item_shippable(context):
    return lambda: get_shop_shipping_settings().default_shipping_item_shippable


class ShippingExtender(ExtenderBase):
    """Schema extender for item shipping.
    """

    layer = IShopExtensionLayer

    fields = [
        XBooleanField(
            name='shipping_item_shippable',
            schemata='Shop',
            widget=BooleanField._properties['widget'](
                label=_(u'label_shipping_item_shippable',
                        default=u'Item Shippable'),
                description=_('help_shipping_item_shippable',
                              default=u'Flag whether item is shippable, i.e. '
                                      u'downloads are not'),
            ),
        ),
        XFloatField(
            name='shipping_item_weight',
            schemata='Shop',
            widget=FloatField._properties['widget'](
                label=_(u'label_shipping_item_weight',
                        default=u'Item Weight'),
            ),
        ),
    ]


@implementer(IShippingItem)
@adapter(IBaseObject)
class ATShippingItem(object):
    """Accessor Interface
    """

    def __init__(self, context):
        self.context = context

    @property
    def shippable(self):
        return field_value(self.context, 'shipping_item_shippable')

    @property
    def weight(self):
        return field_value(self.context, 'shipping_item_weight')


@adapter(IBaseObject)
class ATCartItemPreviewImage(CartItemPreviewAdapterBase):
    """Accessor Interface
    """

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


class ItemNotificationTextExtender(ExtenderBase):
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
                label=_(u'label_item_notification_text',
                        default=u"Notification text for this item in order "
                                u"confirmation mail"),
            ),
        ),
        XTextField(
            name='overbook_text',
            schemata='Shop',
            default_content_type="text/plain",
            allowable_content_types=('text/plain',),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_(u'label_item_overbook_notification_text',
                        default=u"Notification text for this item in order "
                                u"confirmation mail if item out of stock"),
            ),
        ),
    ]


class GlobalNotificationTextExtender(ExtenderBase):
    """Schema extender for global notification text.
    """

    layer = IShopExtensionLayer

    fields = [
        XTextField(
            name='global_order_text',
            schemata='Shop',
            default_content_type="text/plain",
            allowable_content_types=('text/plain',),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_(u'label_item_global_notification_text',
                        default=u"Additional overall notification text for "
                                u"order confirmation mail if this item "
                                u"in cart"),
            ),
        ),
        XTextField(
            name='global_overbook_text',
            schemata='Shop',
            default_content_type="text/plain",
            allowable_content_types=('text/plain',),
            default_output_type="text/plain",
            widget=TextAreaWidget(
                label=_(u'label_item_global_overbook_notification_text',
                        default=u"Additional overall notification text for "
                                u"order confirmation mail if this item "
                                u"in cart and out of stock"),
            ),
        ),
    ]


@adapter(IBaseObject)
class ATItemNotificationText(BubbleItemNotificationText):
    """Accessor Interface
    """

    @property
    def order_text(self):
        text = None
        field = self.context.getField('order_text')
        if field:
            text = field.get(self.context)
        if text:
            return text
        return super(ATItemNotificationText, self).order_text

    @property
    def overbook_text(self):
        text = None
        field = self.context.getField('overbook_text')
        if field:
            text = field.get(self.context)
        if text:
            return text
        return super(ATItemNotificationText, self).overbook_text


@adapter(IBaseObject)
class ATGlobalNotificationText(BubbleGlobalNotificationText):
    """Accessor Interface
    """

    @property
    def order_text(self):
        text = None
        field = self.context.getField('global_order_text')
        if field:
            text = field.get(self.context)
        if text:
            return text
        return super(ATGlobalNotificationText, self).global_order_text

    @property
    def overbook_text(self):
        text = None
        field = self.context.getField('global_overbook_text')
        if field:
            text = field.get(self.context)
        if text:
            return text
        if text:
            return text
        return super(ATGlobalNotificationText, self).global_overbook_text


class BuyablePeriodExtender(ExtenderBase):
    """Schema extender for buyable period.
    """

    layer = IShopExtensionLayer

    fields = [
        XDateTimeField(
            name='buyable_effective',
            schemata='Shop',
            widget=CalendarWidget(
                label=_(u'label_buyable_effective_date',
                        default=u'Buyable effective date'),
            ),
        ),
        XDateTimeField(
            name='buyable_expires',
            schemata='Shop',
            widget=CalendarWidget(
                label=_(u'label_buyable_expiration_date',
                        default=u'Buyable expiration date'),
            ),
        ),
    ]


@implementer(IBuyablePeriod)
@adapter(IBaseObject)
class ATBuyablePeriod(object):

    def __init__(self, context):
        self.context = context

    @property
    def effective(self):
        effective = field_value(self.context, 'buyable_effective')
        if effective:
            effective = datetime.fromtimestamp(effective.timeTime())
        return effective

    @property
    def expires(self):
        expires = field_value(self.context, 'buyable_expires')
        if expires:
            expires = datetime.fromtimestamp(expires.timeTime())
        return expires


class TradingExtender(ExtenderBase):
    """Schema extender for trading information.
    """

    layer = IShopExtensionLayer

    fields = [
        XStringField(
            name='item_number',
            schemata='Shop',
            widget=StringWidget(
                label=_(u'label_item_number', default=u'Item number'),
                description=_(u'help_item_number',
                              default=u'Buyable Item number')
            ),
        ),
        XStringField(
            name='gtin',
            schemata='Shop',
            widget=StringWidget(
                label=_(u'label_gtin', default=u'GTIN'),
                description=_(u'help_gtin',
                              default=u'Global Trade Item Number')
            ),
        ),
    ]


@implementer(ITrading)
@adapter(IBaseObject)
class ATTrading(object):
    """Accessor Interface
    """

    def __init__(self, context):
        self.context = context

    @property
    def item_number(self):
        return field_value(self.context, 'item_number')

    @property
    def gtin(self):
        return field_value(self.context, 'gtin')
