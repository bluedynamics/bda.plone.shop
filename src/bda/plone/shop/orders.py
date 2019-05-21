# -*- coding: utf-8 -*-
from bda.plone.orders.interfaces import IInvoiceSender
from bda.plone.shop.utils import get_shop_invoice_settings
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IInvoiceSender)
@adapter(Interface)
class InvoiceSender(object):
    def __init__(self, context):
        self.context = context

    @property
    def company(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_company

    @property
    def companyadd(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_companyadd

    @property
    def firstname(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_firstname

    @property
    def lastname(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_lastname

    @property
    def street(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_street

    @property
    def zip(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_zip

    @property
    def city(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_city

    @property
    def country(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_country

    @property
    def phone(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_phone

    @property
    def email(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_email

    @property
    def web(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_web

    @property
    def iban(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_iban

    @property
    def bic(self):
        settings = get_shop_invoice_settings()
        return settings.default_invoice_bic
