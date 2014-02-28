from Acquisition import aq_parent
from bda.plone.orders.interfaces import INotificationText
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import adapter
from zope.component import queryAdapter
from zope.interface import implementer
from zope.location.interfaces import IContained
from .utils import get_shop_notification_settings


@implementer(INotificationText)
@adapter(IContained)
class BubbleNotificationText(object):

    @property
    def order_text(self):
        parent = queryAdapter(aq_parent(self.context), INotificationText)
        if parent:
            return parent.order_text

    @property
    def overbook_text(self):
        parent = queryAdapter(aq_parent(self.context), INotificationText)
        if parent:
            return parent.overbook_text


@adapter(ISiteRoot)
class RegistryNotificationText(BubbleNotificationText):

    def lookup_text(self, enum):
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        lang = portal_state.language()
        for entry in enum:
            if entry['lang'] == lang:
                return entry['text']

    @property
    def order_text(self):
        settings = get_shop_notification_settings()
        order_text = self.lookup_text(settings.order_text)
        if order_text:
            return order_text
        return super(RegistryNotificationText, self).order_text

    @property
    def overbook_text(self):
        settings = get_shop_notification_settings()
        overbook_text = self.lookup_text(settings.overbook_text)
        if overbook_text:
            return overbook_text
        return super(RegistryNotificationText, self).overbook_text
