# -*- coding: utf-8 -*-
from bda.plone.orders.interfaces import IBuyable
from plone.indexer import indexer


@indexer(IBuyable)
def item_buyable(obj):
    return True
