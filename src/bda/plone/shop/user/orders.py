from AccessControl import Unauthorized
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bda.plone.orders import message_factory as _bpo
from bda.plone.orders.browser.views import OrdersTable
from bda.plone.orders.browser.views import TableData
from bda.plone.orders.browser.views import Translate
from bda.plone.shop import message_factory as _
from repoze.catalog.query import Contains
from repoze.catalog.query import Any
from repoze.catalog.query import Eq
from yafowil.utils import Tag
import plone.api as ploneapi
from plone.uuid.interfaces import IUUID
from bda.plone.shop.utils import get_vendor_shops


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
        return 'Shop Admin' in ploneapi.user.get_roles()

    @property
    def is_vendor(self):
        perm = 'bda.plone.shop: View vendor orders'
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
        return [{
            'id': 'actions',
            'label': _bpo('actions', 'Actions'),
            'renderer': self.render_order_actions,
        }, {
            'id': 'created',
            'label': _bpo('date', 'Date'),
            'renderer': self.render_dt,
        }, {
            'id': 'personal_data.lastname',
            'label': _bpo('lastname', 'Last Name'),
        }, {
            'id': 'personal_data.firstname',
            'label': _bpo('firstname', 'First Name'),
        }, {
            'id': 'billing_address.city',
            'label': _bpo('city', 'City'),
        }, {
            'id': 'salaried',
            'label': _bpo('salaried', 'Salaried'),
            'renderer': self.render_salaried,
        }, {
            'id': 'state',
            'label': _bpo('state', 'State'),
            'renderer': self.render_state,
        }]

    def render_order_actions(self, colname, record):
        tag = Tag(Translate(self.request))
        target = '%s?uid=%s' % (self.context.absolute_url(),
                                str(record.attrs['uid']))
        link_attrs = {
            'ajax:bind': 'click',
            'ajax:target': target,
            'ajax:overlay': 'order',
            'class_': 'contenttype-document',
            'href': '',
            'title': _bpo('view_order', 'View Order'),
        }
        return tag('a', '&nbsp', **link_attrs)

    def render_salaried(self, colname, record):
        return record.attrs.get('salaried', 'no')

    def render_state(self, colname, record):
        return record.attrs['state']


class UserOrdersData(UserOrdersTable, TableData):
    soup_name = 'bda_plone_orders_orders'
    search_text_index = 'text'

    def query(self, soup):

        if ploneapi.user.is_anonymous():
            # don't allow this for anonymous users
            raise Unauthorized(
                _('unauthorized_orders_view',
                  default="You have to log in to access the orders view")
            )

        query = None

        manageable_shops = get_vendor_shops()
        if manageable_shops:
            # CASE VENDOR
            _query = Any('shop_uid', [IUUID(it) for it in manageable_shops])
            query = query and query & _query or _query

        if manageable_shops or self.is_shopadmin:
            # CASE VENDOR OR ADMIN
            userid = self.request.form.get('userid')
        else:
            # CASE USER
            userid = ploneapi.user.get_current().getId()

        if userid:
            _query = Eq('creator', userid)
            query = query and query & _query or _query

        sort = self.sort()
        term = self.request.form['sSearch'].decode('utf-8')
        if term:
            _query = Contains(self.search_text_index, term)
            query = query and query & _query or _query

        print query
        if query:
            res = soup.lazy(query,
                            sort_index=sort['index'],
                            reverse=sort['reverse'],
                            with_size=True)
            length = res.next()
            return length, res
        else:
            return self.all(soup)
