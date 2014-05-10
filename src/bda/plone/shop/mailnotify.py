from Acquisition import aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from bda.plone.orders.interfaces import INotificationSettings
from bda.plone.orders.interfaces import IGlobalNotificationText
from bda.plone.orders.interfaces import IItemNotificationText
from bda.plone.orders.interfaces import IPaymentText
from bda.plone.shop.utils import get_shop_settings
from bda.plone.shop.utils import get_shop_notification_settings
from bda.plone.shop.utils import get_shop_payment_settings
from zope.component import adapter
from zope.component import queryAdapter
from zope.component.interfaces import ISite
from zope.interface import implementer
from zope.interface import Interface
from zope.location.interfaces import IContained


@implementer(INotificationSettings)
@adapter(Interface)
class NotificationSettings(object):

    def __init__(self, context):
        self.context = context

    @property
    def admin_email(self):
        props = getToolByName(self.context, 'portal_properties')
        return get_shop_settings().admin_email or \
            props.site_properties.email_from_address

    @property
    def admin_name(self):
        props = getToolByName(self.context, 'portal_properties')
        return get_shop_settings().admin_name or \
            props.site_properties.email_from_name


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


class SiteRegistryNotificationText(object):

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
class RegistryItemNotificationText(SiteRegistryNotificationText,
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
class RegistryGlobalNotificationText(SiteRegistryNotificationText,
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


@implementer(IPaymentText)
@adapter(ISite)
class RegistryPaymentText(object):

    def __init__(self, context):
        self.context = context

    def payment_text(self, payment):
        settings = get_shop_payment_settings()
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        lang = portal_state.language()
        for entry in settings.payment_text:
            if entry['lang'] == lang and entry['payment'] == payment:
                return entry['text']
        return u''
