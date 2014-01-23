from zope.container.interfaces import IContainer
from zope.interface import directlyProvides
from zope.interface import noLongerProvides
from Products.Five.browser import BrowserView
from bda.plone.orders.interfaces import ISubShop
from ..interfaces import IBuyable
from ..interfaces import IPotentiallyBuyable
from .. import message_factory as _


class EnableDisableFeature(BrowserView):
    FeatureIface = None
    PotentialFeatureIface = None
    enable_message = None
    disable_message = None

    def enableFeature(self):
        directlyProvides(self.context, self.FeatureIface)
        self.context.portal_catalog.reindexObject(self.context,
                                                  idxs=['object_provides'],
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(self.enable_message)
        self.request.response.redirect(self.context.absolute_url())

    def disableFeature(self):
        noLongerProvides(self.context, self.FeatureIface)
        self.context.portal_catalog.reindexObject(self.context,
                                                  idxs=['object_provides'],
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(self.disable_message)
        self.request.response.redirect(self.context.absolute_url())

    def isPossibleToEnableFeature(self):
        return self.PotentialFeatureIface.providedBy(self.context) \
               and not self.FeatureIface.providedBy(self.context)

    def isPossibleToDisableFeature(self):
        return self.PotentialFeatureIface.providedBy(self.context) \
               and self.FeatureIface.providedBy(self.context)


class BuyableAction(EnableDisableFeature):

    FeatureIface = IBuyable
    PotentialFeatureIface = IPotentiallyBuyable
    enable_message = _(u'enabled_buyable', u'Enabled Buyable.')
    disable_message = _(u'disabled_buyable', u'Disabled Buyable.')


class SubShopAction(EnableDisableFeature):

    FeatureIface = ISubShop
    PotentialFeatureIface = IContainer
    enable_message = _(u'enabled_subshop', u'Enabled Subshop.')
    disable_message = _(u'disabled_subshop', u'Disabled Subshop.')
