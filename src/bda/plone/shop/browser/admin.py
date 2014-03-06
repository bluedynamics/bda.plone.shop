from zope.interface import implementer
from zope.security import checkPermission
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from bda.plone.orders.interfaces import IVendor
from .. import message_factory as _

import plone.api


class IShopAdminPortlet(IPortletDataProvider):
    """A portlet rendering shop admin links.
    """


@implementer(IShopAdminPortlet)
class ShopAdminAssignment(base.Assignment):
    title = _(u'shop_admin', default=u'Shop Administration')


class ShopAdminRenderer(base.Renderer):
    render = ViewPageTemplateFile('admin.pt')

    @property
    def show(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    @property
    def current_user(self):
        return plone.api.user.get_current().getId()

    @property
    def display_mailtemplates_link(self):
        return IPloneSiteRoot.providedBy(self.context) \
            or IVendor.providedBy(self.context)


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()
