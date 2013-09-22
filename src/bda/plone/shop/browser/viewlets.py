from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class BuyableViewlet(ViewletBase):
    """Viewlet rendering buyable controls.
    """

    index = ViewPageTemplateFile('buyable_viewlet.pt')
