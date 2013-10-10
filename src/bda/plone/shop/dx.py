from zope import schema
from zope.interface import (
    implementer,
    alsoProvides,
    provider,
)
from zope.component import (
    adapter,
    getUtility,
)
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import (
    IVocabularyFactory,
    IContextAwareDefaultFactory,
)
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from bda.plone.shipping.interfaces import IShippingItem
from bda.plone.cart.interfaces import (
    ICartItemDataProvider,
    ICartItemStock,
)
from bda.plone.cart import CartItemPreviewAdapterBase
from .interfaces import IBuyable
from .utils import (
    get_shop_settings,
    get_shop_article_settings,
    get_shop_tax_settings,
)


_ = MessageFactory('bda.plone.shop')


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
def default_item_quantity_unit(context):
    return get_shop_article_settings().default_item_quantity_unit


class IBuyableBehavior(model.Schema, IBuyable):
    """Buyable behavior.
    """

    model.fieldset('shop',
            label=u"Shop",
            fields=['item_net',
                    'item_vat',
                    'item_display_gross',
                    'item_comment_enabled',
                    'item_comment_required',
                    'item_quantity_unit_float',
                    'item_quantity_unit'])

    item_net = schema.Float(
        title=_(u'label_item_net', default=u'Item net price'),
        required=False,
        defaultFactory=default_item_net)

    item_vat = schema.Choice(
        title=_(u'label_item_vat', default=u'Item VAT (in %)'),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary',
        required=False,
        defaultFactory=default_item_vat)

    item_display_gross = schema.Bool(
        title=_(u'label_item_display_gross', default=u'Display Gross'),
        required=False,
        defaultFactory=default_item_display_gross)

    item_comment_enabled = schema.Bool(
        title=_(u'label_item_comment_enabled', default='Comment enabled'),
        required=False,
        defaultFactory=item_comment_enabled)

    item_comment_required = schema.Bool(
        title=_(u'label_item_comment_required', default='Comment required'),
        required=False,
        defaultFactory=default_item_comment_required)

    item_quantity_unit_float = schema.Bool(
        title=_(u'label_item_quantity_unit_float', default='Quantity as float'),
        required=False,
        defaultFactory=default_item_quantity_unit_float)

    item_quantity_unit = schema.Choice(
        title=_(u'label_item_quantity_unit', default='Quantity unit'),
        vocabulary='bda.plone.shop.vocabularies.QuantityUnitVocabulary',
        required=False,
        defaultFactory=default_item_quantity_unit)


alsoProvides(IBuyableBehavior, IFormFieldProvider)


@implementer(ICartItemDataProvider)
@adapter(IDexterityContent)
class DXCartItemDataProvider(object):

    def __init__(self, context):
        self.context = context

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


class IStockBehavior(model.Schema):
    """Stock behavior.
    """

    model.fieldset('shop',
            label=u"Shop",
            fields=['item_available', 'item_overbook'])

    item_available = schema.Float(
        title=_(u'label_item_available', default=u'Item stock available'),
        required=False)

    item_overbook = schema.Float(
        title=_(u'label_item_overbook', default=u'Item stock overbook'),
        required=False)


alsoProvides(IStockBehavior, IFormFieldProvider)


@implementer(ICartItemStock)
@adapter(IDexterityContent)
class DXCartItemStock(object):

    def __init__(self, context):
        self.context = context

    def _get_available(self):
        return self.context.item_available

    def _set_available(self, value):
        self.context.item_available = value

    available = property(_get_available, _set_available)

    def _get_overbook(self):
        return self.context.item_overbook

    def _set_overbook(self, value):
        self.context.item_overbook = value

    overbook = property(_get_overbook, _set_overbook)


class IShippingBehavior(model.Schema):
    """Shipping behavior.
    """

    model.fieldset('shop',
            label=u"Shop",
            fields=['shipping_item_weight'])

    shipping_item_weight = schema.Float(
        title=_(u'label_shipping_item_weight', default=u'Item Weight'),
        required=False)


alsoProvides(IShippingBehavior, IFormFieldProvider)


@implementer(IShippingItem)
@adapter(IDexterityContent)
class DXShippingItem(object):

    def __init__(self, context):
        self.context = context

    @property
    def weight(self):
        return self.context.shipping_item_weight


@adapter(IDexterityContent)
class DXCartItemPreviewImage(CartItemPreviewAdapterBase):
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
