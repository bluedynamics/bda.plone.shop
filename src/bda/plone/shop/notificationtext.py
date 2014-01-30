from bda.plone.orders.interfaces import INotificationText
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import adapter
from zope.interface import implementer
from zope.location.interfaces import IContained

@implementer(INotificationText)
@adapter(IContained)
class BubbleNotificationText(object):

    @property
    def order_text(self):
        parent = queryAdapter(
            aq_parent(self.context),
            INotificationTextBehaviour
        )
        if parent:
            return parent.order_text

    @property
    def overbook_text(self):
        parent = queryAdapter(
            aq_parent(self.context),
            INotificationTextBehaviour
        )
        if parent:
            return parent.overbook_text


@implementer(INotificationText)
@adapter(ISiteRoot)
class RegistryNotificationText(BubbleNotificationText):

    @property
    def order_text(self):
        registry = getUtility(IRegistry)
        name = 'bda.plone.orders.interfaces.INotificationText.order_text'
        order_text = registry.records.get(name, None)
        if order_text:
            return order_text
        return super(RegistryNotificationText, self).order_text

    @property
    def overbook_text(self):
        registry = getUtility(IRegistry)
        name = 'bda.plone.orders.interfaces.INotificationText.overbook_text'
        order_text = registry.records.get(name, None)
        if overbook_text:
            return overbook_text
        return super(RegistryNotificationText, self).overbook_text
