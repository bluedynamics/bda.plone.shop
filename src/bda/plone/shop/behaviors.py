from plone.supermodel import model
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('bda.plone.shop')

class IBuyableBehavior(model.Schema):
    """ Basic event schema.
    """

    bla = schema.TextLine(
        title = _(u'label_bla', default=u'Bla'),
        description = _(u'help_bla',
                        default=u'bla bla bla ...'),
        required = True
        )
