# -*- coding: utf-8 -*-
from bda.plone.cart import get_item_data_provider
from bda.plone.orders.interfaces import IBuyable
from bda.plone.shop.interfaces import IBuyablePeriod
from decimal import Decimal
from plone.indexer import indexer
from zope.component import queryAdapter


@indexer(IBuyable)
def item_buyable(obj):
    return True


@indexer(IBuyable)
def item_net(obj):
    item_data = get_item_data_provider(obj)
    return Decimal(item_data.net)


@indexer(IBuyable)
def item_buyable_start(obj):
    buyable_period = queryAdapter(obj, IBuyablePeriod)
    if not buyable_period or not buyable_period.effective:
        raise AttributeError
    return buyable_period.effective


@indexer(IBuyable)
def item_buyable_end(obj):
    buyable_period = queryAdapter(obj, IBuyablePeriod)
    if not buyable_period or not buyable_period.expires:
        raise AttributeError
    return buyable_period.expires
