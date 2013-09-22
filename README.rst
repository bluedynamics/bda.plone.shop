==============
bda.plone.shop
==============

Webshop Solution for Plone.


Installation
============

Depend your instance to ``bda.plone.shop`` and install it as addon
in plone control panel.


Development and testing
=======================

Checkout ``bda.plone.shop`` from
``git://github.com/bluedynamics/bda.plone.shop.git`` and run contained buidlout
like so::

    ~$ virtualenv --no-site-packages vpython
    ~$ ./vpython/bin/python bootstrap.py
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


Cart item preview images
========================

The cart can render preview images for the cart items in case when

    1. the context has a field named "image"
    2. ``collective.contentleadimage`` is installed (Archetypes only)

You can easily change the preview image rendering by adapting your own cart
items. If you want to change the scale of the image, inherit from the existing
adapter class and change ``preview_scale`` property (example uses the
Archetypes version)::

    >>> from bda.plone.shop.at import ATCartItemPreviewImage
    >>> class MyATCartItemPreviewImage(ATCartItemPreviewImage):
    ...     preview_scale = "my_scale"

to do more complex preview image rendering you can override the ``url``
property (example uses the Dexterity version)::

    >>> from bda.plone.shop.dx import DXCartItemPreviewImage
    >>> class MyDXCartItemPreviewImage(DXCartItemPreviewImage):
    ...     @property
    ...     def url(self):
    ...         # do sophisticated stuff to get your preview image
    ...         return preview_url

Register your adapter in ``configure.zcml``::

    <adapter
      for="some.package.IMyATContent"
      factory=".youradater.MyATCartItemPreviewImage" />

respective::

    <adapter
      for="some.package.IMyDXContent"
      factory=".youradater.MyDXCartItemPreviewImage" />


Create translations
===================

::
    $ cd src/bda/plone/shop/
    $ ./i18n.sh


Contributors
============

- Robert Niederreiter (Author)
- Peter Holzer
- Peter Mathis
- Harald Frießnegger
- Espen Moe-Nilssen
- Johannes Raggam
- Jure Cerjak
