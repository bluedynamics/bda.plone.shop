from zope.interface import Interface 
from zope.interface import directlyProvides 
from zope.interface import noLongerProvides
from Products.Five.browser import BrowserView
from Products.CMFPlone import PloneMessageFactory as _
from ..interfaces import (
    IPotentiallyBuyable,
    IBuyable,
)


class ActionsView(BrowserView):
    
    def enableBuyable(self):
        directlyProvides(self.context, IBuyable)
        self.context.portal_catalog.reindexObject(self.context, 
                                                  idxs=['object_provides'], 
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(
            _(u'Enabled Buyable.'))
        self.request.response.redirect(self.context.absolute_url())

    def disableBuyable(self):
        noLongerProvides(self.context, IBuyable)
        self.context.portal_catalog.reindexObject(self.context, 
                                                  idxs=['object_provides'], 
                                                  update_metadata=1)
        self.context.plone_utils.addPortalMessage(
            _(u'Disabled Buyable.'))
        self.request.response.redirect(self.context.absolute_url())
        
    def isPossibleToEnableBuyable(self):
        return IPotentiallyBuyable.providedBy(self.context) \
               and not IBuyable.providedBy(self.context)
        
    def isPossibleToDisableBuyable(self):
        return IPotentiallyBuyable.providedBy(self.context) \
               and IBuyable.providedBy(self.context)