from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

_ = MessageFactory('bda.plone.shop')


class IShopAdminPortlet(IPortletDataProvider):
    """A portlet rendering shop admin links.
    """


class ShopAdminAssignment(base.Assignment):
    implements(IShopAdminPortlet)
    title = _(u'shop_admin', default=u'Shop Administration')


class ShopAdminRenderer(base.Renderer):
    render = ViewPageTemplateFile('admin.pt')
    
    @property
    def show(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)


class ShopAdminAddForm(base.NullAddForm):

    def create(self):
        return ShopAdminAssignment()