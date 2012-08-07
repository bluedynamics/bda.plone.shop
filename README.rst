bda.plone.shop
==============

Create translations
-------------------

::

    cd src/bda/plone/shop/
    
    i18ndude rebuild-pot --pot locales/bda.plone.shop.pot \
        --merge locales/manual.pot --create bda.plone.shop .
    
    i18ndude sync --pot locales/bda.plone.shop.pot \
        locales/de/LC_MESSAGES/bda.plone.shop.po
