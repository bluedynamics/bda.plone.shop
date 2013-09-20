#!/bin/sh
#
# Shell script to manage .po files.
#
# Run this file in the folder main __init__.py of product
#
# E.g. if your product is yourproduct.name
# you run this file in yourproduct.name/yourproduct/name
#
#
# Copyright 2009 Twinapex Research http://www.twinapex.com
#

# Assume the product name is the current folder name
CURRENT_PATH=`pwd`
CATALOGNAME="bda.plone.shop"

# List of languages
LANGUAGES="en de fr it"

# Create locales folder structure for languages
install -d locales
for lang in $LANGUAGES; do
    install -d locales/$lang/LC_MESSAGES
done

# Assume i18ndude is installed with buildout
# and this script is run under src/ folder with two nested namespaces in the package name (like collective.bla)
I18NDUDE=../../../../bin/i18ndude
#I18NDUDE=../../../../../../bin/i18ndude

if test ! -e $I18NDUDE; then
        echo "You must install i18ndude with buildout"
        echo "See http://svn.plone.org/svn/collective/collective.developermanual/trunk/source/i18n/localization.txt"
        exit
fi

#
# Do we need to merge manual PO entries from a file called manual.pot.
# this option is later passed to i18ndude
# 
if test -e locales/manual.pot; then
        echo "Manual PO entries detected"
        MERGE="--merge locales/manual.pot"
else
        echo "No manual PO entries detected"
        MERGE=""
fi

# Rebuild .pot
$I18NDUDE rebuild-pot --pot locales/$CATALOGNAME.pot $MERGE --create $CATALOGNAME .


# Compile po files
for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do

    if test -d $lang/LC_MESSAGES; then

        PO=$lang/LC_MESSAGES/${CATALOGNAME}.po

        # Create po file if not exists
        touch $PO

        # Sync po file
        echo "Syncing $PO"
        $I18NDUDE sync --pot locales/$CATALOGNAME.pot $PO


        # Plone 3.3 and onwards do not need manual .po -> .mo compilation,
        # but it will happen on start up if you have
        # registered the locales directory in ZCML
        # For more info see http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4
    
        # Compile .po to .mo
        # MO=$lang/LC_MESSAGES/${CATALOGNAME}.mo
        # echo "Compiling $MO"
        # msgfmt -o $MO $lang/LC_MESSAGES/${CATALOGNAME}.po
    fi
done
