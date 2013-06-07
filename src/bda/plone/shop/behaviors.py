from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides, implements
from zope.component import getUtility, adapts
from zope.schema.interfaces import IVocabularyFactory
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from bda.plone.cart.interfaces import ICartItemDataProvider


_ = MessageFactory('bda.plone.shop')


class IBuyableBehavior(model.Schema):
    """ Basic event schema.
    """

    model.fieldset('shop',
            label=u"Shop",
            fields=['item_net', 'item_vat', 'item_display_gross', 'item_comment_enabled', 'item_comment_required', 'item_quantity_unit_float', 'item_quantity_unit']
        )

    item_net = schema.Float(
        title = _(u'label_item_net', default=u'Item net price'),
        required = False
        )

    item_vat = schema.Choice(
        title = _(u'label_item_vat', default=u'Item VAT (in %)'),
        vocabulary='bda.plone.shop.vocabularies.VatVocabulary',
        required = False
        )

    item_display_gross = schema.Bool(
        title = _(u'label_item_display_gross', default=u'Display Gross'),
        required = False
        )

    item_comment_enabled = schema.Bool(
        title = _(u'label_item_comment_enabled', default='Comment enabled'),
        required = False
        )

    item_comment_required = schema.Bool(
        title = _(u'label_item_comment_required', default='Comment required'),
        required = False
        )

    item_quantity_unit_float = schema.Bool(
        title = _(u'label_item_quantity_unit_float', default='Quantity as float'),
        required = False
        )

    item_quantity_unit = schema.Choice(
        title = _(u'label_item_quantity_unit', default='Quantity unit'),
        vocabulary='bda.plone.shop.vocabularies.QuantityUnitVocabulary',
        required = False
        )


# Mark these interfaces as form field providers
alsoProvides(IBuyableBehavior, IFormFieldProvider)


class DXCartItemDataProvider(object):
    implements(ICartItemDataProvider)
    adapts(IDexterityContent)

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
                return term.token