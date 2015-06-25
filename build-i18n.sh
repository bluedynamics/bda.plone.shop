#!/bin/sh
# Make sure, i18ndude is in your path.
I18NDUDE=i18ndude
I18NPATH=src/bda/plone/shop
DOMAIN=bda.plone.shop
$I18NDUDE rebuild-pot --pot $I18NPATH/locales/$DOMAIN.pot --create $DOMAIN $I18NPATH
$I18NDUDE sync --pot $I18NPATH/locales/$DOMAIN.pot $I18NPATH/locales/*/LC_MESSAGES/$DOMAIN.po
