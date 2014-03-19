from .utils import get_shop_notification_settings
from Acquisition import aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from bda.plone.orders.interfaces import IGlobalNotificationText
from bda.plone.orders.interfaces import IItemNotificationText
from zope.component import adapter
from zope.component import queryAdapter
from zope.interface import implementer
from zope.location.interfaces import IContained


@implementer(IItemNotificationText)
@adapter(IContained)
class BubbleItemNotificationText(object):

    def __init__(self, context):
        self.context = context

    @property
    def order_text(self):
        parent = queryAdapter(aq_parent(self.context), IItemNotificationText)
        if parent:
            return parent.order_text
        return ''

    @property
    def overbook_text(self):
        parent = queryAdapter(aq_parent(self.context), IItemNotificationText)
        if parent:
            return parent.overbook_text
        return ''


@implementer(IGlobalNotificationText)
@adapter(IContained)
class BubbleGlobalNotificationText(object):

    def __init__(self, context):
        self.context = context

    @property
    def global_order_text(self):
        parent = queryAdapter(aq_parent(self.context), IGlobalNotificationText)
        if parent:
            return parent.global_order_text
        return ''

    @property
    def global_overbook_text(self):
        parent = queryAdapter(aq_parent(self.context), IGlobalNotificationText)
        if parent:
            return parent.global_overbook_text
        return ''


class BaseRegistryNotificationText(object):

    def __init__(self, context):
        self.context = context

    def _lookup_text(self, field):
        settings = get_shop_notification_settings()
        enum = getattr(settings, field)
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        lang = portal_state.language()
        for entry in enum:
            if entry['lang'] == lang:
                return entry['text']


@adapter(ISiteRoot)
class RegistryItemNotificationText(BaseRegistryNotificationText,
                                   BubbleItemNotificationText):

    @property
    def order_text(self):
        text = self._lookup_text('order_text')
        if text:
            return text
        return super(RegistryItemNotificationText, self).order_text

    @property
    def overbook_text(self):
        text = self._lookup_text('overbook_text')
        if text:
            return text
        return super(RegistryItemNotificationText, self).overbook_text


@adapter(ISiteRoot)
class RegistryGlobalNotificationText(BaseRegistryNotificationText,
                                     BubbleGlobalNotificationText):

    @property
    def order_text(self):
        text = self._lookup_text('global_order_text')
        if text:
            return text
        return super(RegistryGlobalNotificationText, self).global_order_text

    @property
    def overbook_text(self):
        text = self._lookup_text('global_overbook_text')
        if text:
            return text
        return super(RegistryGlobalNotificationText, self).global_overbook_text
