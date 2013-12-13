from bda.plone.orders.browser.views import OrdersData
from repoze.catalog.query import Contains
from repoze.catalog.query import Eq
from plone.api import user as apiuser


class UserOrdersData(OrdersData):

    def query(self, soup):
        user = apiuser.get_current()
        sort = self.sort()
        term = self.request.form['sSearch'].decode('utf-8')
        if term:
            res = soup.lazy(Contains(self.search_text_index, term) &
                            Eq('creator', user.getUserName()),
                            sort_index=sort['index'],
                            reverse=sort['reverse'],
                            with_size=True)
            length = res.next()
            return length, res
        return self.all(soup)
