# -*- coding: utf-8 -*-
from bda.plone.cart import CartItemDataProviderBase
from bda.plone.cart import CartItemPreviewAdapterBase
from bda.plone.cart.interfaces import ICartItemStock
from bda.plone.orders.interfaces import IBuyable
from bda.plone.orders.interfaces import ITrading
from bda.plone.shipping.interfaces import IShippingItem
from bda.plone.shop import message_factory as _
from bda.plone.shop.interfaces import IBuyablePeriod
from bda.plone.shop.mailnotify import BubbleGlobalNotificationText
from bda.plone.shop.mailnotify import BubbleItemNotificationText
from bda.plone.shop.utils import get_shop_article_settings
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_shipping_settings
from bda.plone.shop.utils import get_shop_tax_settings
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.interfaces import IVocabularyFactory


@provider(IContextAwareDefaultFactory)
def default_item_net(context):
    return get_shop_article_settings().default_item_net


@provider(IContextAwareDefaultFactory)
def default_item_vat(context):
    return get_shop_tax_settings().default_item_vat


@provider(IContextAwareDefaultFactory)
def default_item_display_gross(context):
    return get_shop_settings().default_item_display_gross


@provider(IContextAwareDefaultFactory)
def item_comment_enabled(context):
    return get_shop_article_settings().default_item_comment_enabled


@provider(IContextAwareDefaultFactory)
def default_item_comment_required(context):
    return get_shop_article_settings().default_item_comment_required


@provider(IContextAwareDefaultFactory)
def default_item_quantity_unit_float(context):
    return get_shop_article_settings().default_item_quantity_unit_float


@provider(IContextAwareDefaultFactory)
def default_item_cart_count_limit(context):
    return get_shop_article_settings().default_item_cart_count_limit


@provider(IContextAwareDefaultFactory)
def default_item_quantity_unit(context):
    return get_shop_article_settings().default_item_quantity_unit


@provider(IFormFieldProvider)
class IBuyableBehavior(model.Schema, IBuyable):
    """Buyable behavior.
    """

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'item_net',
            'item_vat',
            'item_cart_count_limit',
            'item_display_gross',
            'item_comment_enabled',
            'item_comment_required',
            'item_quantity_unit_float',
            'item_quantity_unit'
        ]
    )

    item_net = schema.Float(
        title=_(u'label_item_net', default=u'Item net price'),
        required=False,
        defaultFactory=default_item_net
    )

    item_vat = schema.Choice(
        title=_(u'label_item_vat', default=u'Item VAT (in %)'),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary',
        required=False,
        defaultFactory=default_item_vat
    )

    item_cart_count_limit = schema.Float(
        title=_(u'label_item_cart_count_limit',
                default=u'Max count of this item in cart'),
        required=False,
        defaultFactory=default_item_cart_count_limit
    )

    item_display_gross = schema.Bool(
        title=_(u'label_item_display_gross', default=u'Display Gross'),
        required=False,
        defaultFactory=default_item_display_gross
    )

    item_comment_enabled = schema.Bool(
        title=_(u'label_item_comment_enabled', default='Comment enabled'),
        required=False,
        defaultFactory=item_comment_enabled
    )

    item_comment_required = schema.Bool(
        title=_(u'label_item_comment_required', default='Comment required'),
        required=False,
        defaultFactory=default_item_comment_required
    )

    item_quantity_unit_float = schema.Bool(
        title=_(
            u'label_item_quantity_unit_float', default='Quantity as float'),
        required=False,
        defaultFactory=default_item_quantity_unit_float
    )

    item_quantity_unit = schema.Choice(
        title=_(u'label_item_quantity_unit', default='Quantity unit'),
        vocabulary='bda.plone.shop.vocabularies.QuantityUnitVocabulary',
        required=False,
        defaultFactory=default_item_quantity_unit
    )


@adapter(IBuyableBehavior)
class DXCartItemDataProvider(CartItemDataProviderBase):
    """Accessor Interface
    """

    @property
    def net(self):
        val = self.context.item_net
        if not val:
            return 0.0
        return float(val)

    @property
    def vat(self):
        val = self.context.item_vat
        if not val:
            return 0.0
        return float(val)

    @property
    def cart_count_limit(self):
        return self.context.item_cart_count_limit

    @property
    def display_gross(self):
        return self.context.item_display_gross

    @property
    def comment_enabled(self):
        return self.context.item_comment_enabled

    @property
    def comment_required(self):
        return self.context.item_comment_required

    @property
    def quantity_unit_float(self):
        return self.context.item_quantity_unit_float

    @property
    def quantity_unit(self):
        unit = self.context.item_quantity_unit
        vocab = getUtility(
            IVocabularyFactory,
            'bda.plone.shop.vocabularies.QuantityUnitVocabulary')(self.context)
        for term in vocab:
            if unit == term.value:
                return term.title


@provider(IContextAwareDefaultFactory)
def default_item_display_stock(context):
    return True


@provider(IFormFieldProvider)
class IStockBehavior(model.Schema):
    """Stock behavior.
    """

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=['item_display_stock', 'item_available', 'item_overbook']
    )

    item_display_stock = schema.Bool(
        title=_(u'label_item_display_stock', default=u'Display item stock'),
        required=False,
        defaultFactory=default_item_display_stock
    )

    item_available = schema.Float(
        title=_(u'label_item_available', default=u'Item stock available'),
        required=False
    )

    item_overbook = schema.Float(
        title=_(u'label_item_overbook', default=u'Item stock overbook'),
        required=False
    )


@implementer(ICartItemStock)
@adapter(IStockBehavior)
class DXCartItemStock(object):
    """Accessor Interface
    """

    def __init__(self, context):
        self.context = context

    @property
    def display(self):
        return self.context.item_display_stock

    @property
    def available(self):
        return self.context.item_available

    @available.setter
    def available(self, value):
        self.context.item_available = value

    @property
    def overbook(self):
        return self.context.item_overbook

    @overbook.setter
    def overbook(self, value):
        self.context.item_overbook = value


@provider(IContextAwareDefaultFactory)
def default_shipping_item_shippable(context):
    return get_shop_shipping_settings().default_shipping_item_shippable


@provider(IFormFieldProvider)
class IShippingBehavior(model.Schema):
    """Shipping behavior.
    """

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'shipping_item_shippable',
            'shipping_item_weight'
        ]
    )

    shipping_item_shippable = schema.Bool(
        title=_(u'label_shipping_item_shippable', default=u'Item Shippable'),
        description=_('help_shipping_item_shippable',
                      default=u'Flag whether item is shippable, i.e. '
                              u'downloads are not'),
        defaultFactory=default_shipping_item_shippable
    )

    shipping_item_weight = schema.Float(
        title=_(u'label_shipping_item_weight', default=u'Item Weight'),
        required=False
    )


@implementer(IShippingItem)
@adapter(IShippingBehavior)
class DXShippingItem(object):
    """Accessor Interface
    """

    def __init__(self, context):
        self.context = context

    @property
    def shippable(self):
        return self.context.shipping_item_shippable

    @property
    def weight(self):
        return self.context.shipping_item_weight


@adapter(IDexterityContent)
class DXCartItemPreviewImage(CartItemPreviewAdapterBase):
    """Accessor Interface
    """

    preview_scale = "tile"

    @property
    def url(self):
        """Get url of preview image by trying to read the 'image' field on the
        context.
        """
        img_scale = None
        if hasattr(self.context, 'image'):
            scales = self.context.restrictedTraverse('@@images')
            img_scale = scales.scale("image", scale=self.preview_scale)
        return img_scale and img_scale.url or ""


@provider(IFormFieldProvider)
class IItemNotificationTextBehavior(model.Schema):

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'order_text',
            'overbook_text'])

    order_text = schema.Text(
        title=_(
            u"label_item_notification_text",
            default=u"Notification text for this item in order confirmation "
                    u"mail"
        ),
        required=False
    )

    overbook_text = schema.Text(
        title=_(
            u"label_item_overbook_notification_text",
            default=u"Notification text for this item in order confirmation "
                    u"mail if item out of stock"
        ),
        required=False
    )


@provider(IFormFieldProvider)
class IGlobalNotificationTextBehavior(model.Schema):

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'global_order_text',
            'global_overbook_text'])

    global_order_text = schema.Text(
        title=_(
            u"label_item_global_notification_text",
            default=u"Additional overall notification text for order "
                    u"confirmation mail if this item in cart"
        ),
        required=False
    )

    global_overbook_text = schema.Text(
        title=_(
            u"label_item_global_overbook_notification_text",
            default=u"Additional overall notification text for order "
                    u"confirmation mail if this item in cart and out of stock"
        ),
        required=False
    )


@adapter(IItemNotificationTextBehavior)
class DXItemNotificationText(BubbleItemNotificationText):
    """Accessor Interface
    """

    @property
    def order_text(self):
        if self.context.order_text:
            return self.context.order_text
        return super(DXItemNotificationText, self).order_text

    @property
    def overbook_text(self):
        if self.context.overbook_text:
            return self.context.overbook_text
        return super(DXItemNotificationText, self).overbook_text


@adapter(IGlobalNotificationTextBehavior)
class DXGlobalNotificationText(BubbleGlobalNotificationText):
    """Accessor Interface
    """

    @property
    def global_order_text(self):
        if self.context.global_order_text:
            return self.context.global_order_text
        return super(DXGlobalNotificationText, self).global_order_text

    @property
    def global_overbook_text(self):
        if self.context.global_overbook_text:
            return self.context.global_overbook_text
        return super(DXGlobalNotificationText, self).global_overbook_text


@provider(IFormFieldProvider)
class IBuyablePeriodBehavior(model.Schema):
    """Buyable period behavior.
    """

    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'buyable_effective',
            'buyable_expires'
        ]
    )

    buyable_effective = schema.Datetime(
        title=_(u'label_buyable_effective_date',
                default=u'Buyable effective date'),
        required=False
    )

    buyable_expires = schema.Datetime(
        title=_(u'label_buyable_expiration_date',
                default=u'Buyable expiration date'),
        required=False
    )


@implementer(IBuyablePeriod)
@adapter(IBuyablePeriodBehavior)
class DXBuyablePeriod(object):

    def __init__(self, context):
        self.context = context

    @property
    def effective(self):
        return self.context.buyable_effective

    @property
    def expires(self):
        return self.context.buyable_expires


@provider(IFormFieldProvider)
class ITradingBehavior(model.Schema):
    """Trading behavior.
    """
    model.fieldset(
        'shop',
        label=u"Shop",
        fields=[
            'item_number',
            'gtin',
        ]
    )

    item_number = schema.TextLine(
        title=_(u'label_item_number', default=u'Item number'),
        description=_(u'help_item_number',
                      default=u'Buyable Item number'),
        required=False)

    gtin = schema.TextLine(
        title=_(u'label_gtin', default=u'GTIN'),
        description=_(u'help_gtin',
                      default=u'Global Trade Item Number'),
        required=False)


@implementer(ITrading)
@adapter(ITradingBehavior)
class DXTrading(object):

    def __init__(self, context):
        self.context = context

    @property
    def item_number(self):
        return self.context.item_number

    @property
    def gtin(self):
        return self.context.gtin
