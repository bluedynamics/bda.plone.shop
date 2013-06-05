==============
bda.plone.shop
==============


Installation
============

Depend your instance to ``bda.plone.shop`` and install it as addon
in plone control panel.


Development and testing
=======================

Checkout ``bda.plone.shop`` from
``git://github.com/bluedynamics/bda.plone.shop.git`` and run contained buidlout
like so::

    ~$ python bootstrap.py -v 1.7
    ~$ ./bin/buildout

Enyble some object to be either potentialy buyable or buyable as described
below.

Start instance and create plone site with shop profile applied.


Enable Content to be buyable
============================

Archtypes Content which represent buyable items must implement
``bda.plone.shop.interfaces.IBuyable``. Shop related schema extension is
bound to this interface.

There exists a content action with which ``IBuyable`` interface can be set
dynamically. To enable this Action content items must implement
``bda.plone.shop.interfaces.IPotentiallyBuyable``.

See ``bda.plone.shop:configure.zcml`` for examples.


Create translations
===================

::
    $ cd src/bda/plone/payment/
    $ ./i18n.sh


Contributors
============

- Robert Niederreiter, Author

- Harald Frießnegger, Webmeisterei GmbH
