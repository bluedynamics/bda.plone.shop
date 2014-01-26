==============
bda.plone.shop
==============

Webshop Solution for Plone.


Installation
------------

Depend your instance to ``bda.plone.shop`` and install it as addon
in plone control panel.


Development and testing
-----------------------

Checkout ``bda.plone.shop`` from
``git://github.com/bluedynamics/bda.plone.shop.git`` and run contained buidlout
like so::

    ~$ virtualenv --no-site-packages vpython
    ~$ ./vpython/bin/python bootstrap.py
    ~$ ./bin/buildout

Start instance and create Plone site with shop profile applied.


Enable Content to be buyable
----------------------------

Content which represent buyable items must implement
``bda.plone.shop.interfaces.IBuyable``.

Information related to Buyable items is acquired from content instance via
adapters implementing the following interfaces::

- ``bda.plone.cart.interfaces.ICartItemDataProvider``
- ``bda.plone.cart.interfaces.ICartItemStock``
- ``bda.plone.shipping.interfaces.IShippingItem``
- ``bda.plone.orders.interfaces.INotificationText``

There exists Archetypes and Dexterity related implementations of these
adapters among with related Schema Extenders respective Dexterity Behaviors.


Archetypes
~~~~~~~~~~

The Archetypes related implementation consists of Schema Extenders for each
required interfaces which all are bound to ``IBuyable`` and the corresponding
adapter implementations which are registered for
``Products.Archetypes.BaseObject.BaseObject``.

There exists a content action with which ``IBuyable`` interface can be set
dynamically. To enable this Action content items must implement
``bda.plone.shop.interfaces.IPotentiallyBuyable``.

**Note** This action works for Archetypes based content only::

    <class zcml:condition="installed Products.Archetypes"
           class="Products.Archetypes.BaseObject.BaseObject">
      <implements interface="bda.plone.shop.interfaces.IPotentiallyBuyable" />
    </class>

If Archetypes based content should be immediately buyable without explicit
activation, set ``IBuyable`` interface directly on content class::

    <class zcml:condition="installed Products.Archetypes"
           class="Products.Archetypes.BaseObject.BaseObject">
      <implements interface="bda.plone.shop.interfaces.IBuyable" />
    </class>


Dexterity
~~~~~~~~~

The Dexterity related implementation consists of Behaviors for each
interface. These are:

- ``bda.plone.shop.dx.IBuyableBehavior``
- ``bda.plone.shop.dx.IStockBehavior``
- ``bda.plone.shop.dx.IShippingBehavior``
- ``bda.plone.shop.dx.INotificationTextBehavior``

The corresponding adapter implementations are registered for the referring
behavior interfaces.

The ``IBuyable`` interface gets hooked on content via ``IBuyableBehavior``.

In order to create buyable items with dexterity you need to either create a
portal type via GenericSetup or use the Dexterity TTW Editor to assign the
behaviors to existing content, or create new type(s) TTW from scratch.


Cart item preview images
------------------------

The cart can render preview images for the cart items in case when

    1. the context has a field named ``image``
    2. ``collective.contentleadimage`` is installed (Archetypes only)

You can easily change the preview image rendering by adapting your own cart
items. If you want to change the scale of the image, inherit from the existing
adapter class and change ``preview_scale`` property (example uses the
Archetypes version)::

    >>> from bda.plone.shop.at import ATCartItemPreviewImage
    >>> class MyATCartItemPreviewImage(ATCartItemPreviewImage):
    ...     preview_scale = "my_scale"

To do more complex preview image rendering you can override the ``url``
property (example uses the Dexterity version)::

    >>> from bda.plone.shop.dx import DXCartItemPreviewImage
    >>> class MyDXCartItemPreviewImage(DXCartItemPreviewImage):
    ...     @property
    ...     def url(self):
    ...         # do sophisticated stuff to get your preview image
    ...         return preview_url

Register your adapter via ZCML.

Archetypes::

    <adapter
      for="some.package.IMyATContent"
      factory=".youradater.MyATCartItemPreviewImage" />

Dexterity::

    <adapter
      for="some.package.IMyDXContent"
      factory=".youradater.MyDXCartItemPreviewImage" />


Create translations
-------------------

::

    $ cd src/bda/plone/shop/
    $ ./i18n.sh


Contributors
------------

- Robert Niederreiter (Author)
- Peter Holzer
- Peter Mathis
- Harald Frießnegger
- Espen Moe-Nilssen
- Johannes Raggam
- Jure Cerjak
