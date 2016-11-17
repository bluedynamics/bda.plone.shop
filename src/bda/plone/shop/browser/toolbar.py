# -*- coding: utf-8 -*-
from bda.plone.shop import message_factory as _
from bda.plone.shop.browser.navigation import ShopNavigation
from plone.app.contentmenu.interfaces import IActionsMenu
from plone.app.contentmenu.interfaces import IActionsSubMenuItem
from plone.app.contentmenu.menu import BrowserMenu
from plone.app.contentmenu.menu import BrowserSubMenuItem
from zope.interface import implementer


@implementer(IActionsSubMenuItem)
class ShopSubMenuItem(BrowserSubMenuItem):
    title = _('shop', default=u'Shop')
    submenuId = 'shop_toolbar_menu'
    extra = {
        'id': 'shop_toolbar_menu',
        'li_class': 'plonetoolbar-shop_toolbar_menu'
    }
    order = 70

    @property
    def action(self):
        return self.context.absolute_url()

    def available(self):
        return ShopNavigation(self.context, self.request).available

    def selected(self):
        return False


@implementer(IActionsMenu)
class ShopMenu(BrowserMenu):

    def menu_item(self, id_, title, url, cssclass, seperator):
        return {
            'title': title,
            'description': '',
            'action': url,
            'selected': False,
            'icons': None,
            'extra': {
                'id': id_,
                'separator': seperator,
                'class': cssclass
            },
            'submenu': None
        }

    def getMenuItems(self, context, request):
        navigation = ShopNavigation(context, request)
        items = list()
        for group in navigation.groups():
            items.append(self.menu_item(
                group.id,
                group.title,
                None,
                None,
                'actionSeparator'
            ))
            for link in group.links():
                items.append(self.menu_item(
                    link.id,
                    link.title,
                    link.url,
                    link.cssclass,
                    None
                ))
        return items
