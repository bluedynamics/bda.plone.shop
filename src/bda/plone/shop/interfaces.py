from zope.interface import (
    Interface,
    Attribute,
)

from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bda.plone.shop')


class IShopExtensionLayer(Interface):
    """Browser layer for bda.plone.shop
    """


class IPotentiallyBuyable(Interface):
    """Mark item as potentially buyable.

    Considered for providing action in UI.
    """


class IBuyable(Interface):
    """Marker for buyable item.

    Item is buyable.
    """

class IBdaShopSettings(Interface):
    """This interface defines the configlet (the control panel)."""
    
    shop_vat = schema.Int(title=_(u"label_shop_vat", default=u'VAT'),
                        description=_(u"help_shop_vat", default=u'Value added tax in %'),
                        required=True,
                        default=20)                         

    shop_admin_email = schema.ASCIILine(title=_(u"label_shop_admin_email", default=u'Shop admin Email. No typos please....'),
                              description=_(u"help_shop_admin_email", default=u''),
                              required=True,
                              default="")     
                              
    shop_currency = schema.Choice(title=u"Currency", 
                                   description=u"Choose the default currency", 
                                   values=["EUR", "USD", "INR", "CAD", "CHF", "GBP", "AUD", "NOK", "SEK", "DKK"], 
                                   default='EUR')

    shop_show_checkout = schema.Bool(title=u"Show checkout link in portlet", 
                                   description=u"", 
                                   default=False)

    shop_show_to_cart = schema.Bool(title=u"Show link to cart in portlet", 
                                   description=u"", 
                                   default=True)