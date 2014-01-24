import plone.api as ploneapi
from AccessControl import Unauthorized
from repoze.catalog.query import Any
from repoze.catalog.query import Contains
from repoze.catalog.query import Eq
from souper.soup import get_soup
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.orders.browser.views import OrdersTable
from bda.plone.orders.browser.views import TableData
from ..utils import get_vendor_areas
from .. import message_factory as _


class UserOrdersTable(OrdersTable):
    table_template = ViewPageTemplateFile('templates/table.pt')

    @property
    def current_user(self):
        user = ploneapi.user.get_current()
        if not user:
            return None
        return user.getId()

    @property
    def is_shopadmin(self):
        roles = ploneapi.user.get_roles()
        return 'Manager' in roles or 'Shop Admin' in roles

    @property
    def is_vendor(self):
        perm = 'bda.plone.shop: Manage this shop'
        perms = ploneapi.user.get_permissions(obj=self.context)
        return perm in perms and perms[perm] or False

    @property
    def allow_userfilter(self):
        return self.is_shopadmin or self.is_vendor

    @property
    def url(self):
        return self.request.getURL()

    @property
    def ajaxurl(self):
        userid = self.request.form.get('user')
        userid_qs = userid and '?userid=%s' % userid or ''
        return '%s/%s%s' % (
            self.context.absolute_url(), '@@ordersdata', userid_qs)

    @property
    def columns(self):
        if ploneapi.user.is_anonymous():
            # don't allow this for anonymous users
            raise Unauthorized(
                _('unauthorized_orders_view',
                  default="You have to log in to access the orders view")
            )
        return super(UserOrdersTable, self).columns

    #def render_salaried(self, colname, record):
    #    return record.attrs.get('salaried', 'no')

    #def render_state(self, colname, record):
    #    return record.attrs['state']


class UserOrdersData(UserOrdersTable, TableData):

    def query(self, soup):
        if ploneapi.user.is_anonymous():
            # don't allow this for anonymous users
            raise Unauthorized(
                _('unauthorized_orders_view',
                  default="You have to log in to access the orders view")
            )
        query = None
        manageable_orders = get_allowed_orders(self.context)
        # vendor
        if manageable_orders:
            _query = Any('uid', manageable_orders)
            query = query and query & _query or _query
        # vendor or admin
        if manageable_orders or self.is_shopadmin:
            userid = self.request.form.get('userid')
        # user
        else:
            userid = ploneapi.user.get_current().getId()
        if userid:
            _query = Eq('creator', userid)
            query = query and query & _query or _query
        sort = self.sort()
        term = self.request.form['sSearch'].decode('utf-8')
        if term:
            _query = Contains(self.search_text_index, term)
            query = query and query & _query or _query
        if query:
            res = soup.lazy(query,
                            sort_index=sort['index'],
                            reverse=sort['reverse'],
                            with_size=True)
            length = res.next()
            return length, res
        else:
            return self.all(soup)


def get_allowed_orders(context, vendor=None):
    """Get all orders from bookings related to a shop, as the shop_uid is only
    indexed on bda_plone_orders_bookings soup and not on
    bda_plone_orders_orders.

    If you had a previous version of bda.plone.shop without mutli client
    feature installed, please run the bda.plone.orders "Add shop_uid to booking
    records" upgrade step.

    >>> [it[1].attrs['shop_uid'] for it in soup.data.items()]
    >>> [it.attrs['order_uid'] for it in soup.query(Eq('creator', 'test'))]

    """
    manageable_shops = get_vendor_areas(vendor)
    query = Any('shop_uid', [IUUID(it) for it in manageable_shops])
    soup = get_soup('bda_plone_orders_bookings', context)
    res = soup.query(query)
    order_uids = [it.attrs['order_uid'] for it in res]
    # TODO: make a set of order_uids
    return order_uids
