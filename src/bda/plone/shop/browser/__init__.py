from plone.app.layout.viewlets.common import ViewletBase


class BuyableViewlet(ViewletBase):
    """Vielet rendering buyable information.
    """
    
    def get_field_value(self, field_name):
        try:
            acc = self.context.getField(field_name).getAccessor(self.context)
            return acc()
        except (KeyError, TypeError):
            return None
    
    @property
    def item_buyable(self):
        return self.get_field_value('item_buyable')
    
    @property
    def item_uid(self):
        return self.context.UID()