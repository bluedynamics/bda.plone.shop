# -*- coding:utf-8 -*-
from Products.CMFPlone import interfaces as Plone
from Products.CMFQuickInstallerTool import interfaces as QuickInstaller
from zope.interface import implementer


@implementer(Plone.INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return ['bda.plone.shop:install-base',
                ]


@implementer(QuickInstaller.INonInstallable)
class HiddenProducts(object):

    def getNonInstallableProducts(self):
        """Do not show on QuickInstaller's list of installable products."""
        return ['bda.plone.shop:install-base',
                ]
