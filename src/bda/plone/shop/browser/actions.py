from zope.container.interfaces import IContainer
from zope.interface import directlyProvides
from zope.interface import noLongerProvides
from Products.Five.browser import BrowserView
from bda.plone.orders.interfaces import IVendor
from bda.plone.orders import permissions
from bda.plone.shop.interfaces import IBuyable
from bda.plone.shop.interfaces import IPotentiallyBuyable
from bda.plone.shop import message_factory as _


class EnableDisableFeature(BrowserView):
    feature_iface = None
    potential_feature_iface = None
    enable_message = None
    disable_message = None

    def enableFeature(self):
        directlyProvides(self.context, self.feature_iface)
        self.context.portal_catalog.reindexObject(self.context,
                                                  idxs=['object_provides'],
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(self.enable_message)
        self.request.response.redirect(self.context.absolute_url())

    def disableFeature(self):
        noLongerProvides(self.context, self.feature_iface)
        self.context.portal_catalog.reindexObject(self.context,
                                                  idxs=['object_provides'],
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(self.disable_message)
        self.request.response.redirect(self.context.absolute_url())

    def isPossibleToEnableFeature(self):
        return self.potential_feature_iface.providedBy(self.context) \
               and not self.feature_iface.providedBy(self.context)

    def isPossibleToDisableFeature(self):
        return self.potential_feature_iface.providedBy(self.context) \
               and self.feature_iface.providedBy(self.context)


class BuyableAction(EnableDisableFeature):
    feature_iface = IBuyable
    potential_feature_iface = IPotentiallyBuyable
    enable_message = _(u'enabled_buyable', u'Enabled Buyable.')
    disable_message = _(u'disabled_buyable', u'Disabled Buyable.')


class VendorAction(EnableDisableFeature):
    feature_iface = IVendor
    potential_feature_iface = IContainer
    enable_message = _(u'enabled_vendor', u'Enabled Vendor.')
    disable_message = _(u'disabled_vendor', u'Disabled Vendor.')

    def enableFeature(self):
        self.context.manage_permission(
            permissions.DelegateVendorRole,
            roles=['Manager', 'Site Administrator'],
            acquire=0)
        super(VendorAction, self).enableFeature()

    def disableFeature(self):
        self.context.manage_permission(
            permissions.DelegateVendorRole, roles=[], acquire=0)
        super(VendorAction, self).disableFeature()
