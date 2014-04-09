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


Running tests
~~~~~~~~~~~~~

If you have run the buildout, you can run all tests like so::

    ./bin/test -s bda.plone.shop

The -t switch allows you to run a specific test file or method. The
``--list-tests`` lists all available tests.

To run the robot tests do::

    ./bin/test --all -s bda.plone.shop -t robot

For development, it might be more convenient to start a test server and run
robot tests individually, like so::

    ./bin/robot-server bda.plone.shop.tests.ShopDXFull_ROBOT_TESTING
    ./bin/robot src/bda/plone/shop/tests/robot/test_shop_orderprocess.robot

In the robot test you can place the debug statement to access a robot shell to
try things out.

For more information on this topic visit:
http://developer.plone.org/reference_manuals/external/plone.app.robotframework/happy.html


Enable Content to be buyable
----------------------------

Content which represent buyable items must implement
``bda.plone.shop.interfaces.IBuyable``.

Information related to Buyable items is acquired from content instance via
adapters implementing the following interfaces::

- ``bda.plone.cart.interfaces.ICartItemDataProvider``
- ``bda.plone.cart.interfaces.ICartItemStock``
- ``bda.plone.shipping.interfaces.IShippingItem``
- ``bda.plone.orders.interfaces.IItemNotificationText``
- ``bda.plone.orders.interfaces.IGlobalNotificationText``

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

XXX: AT notification text documentation.


Dexterity
~~~~~~~~~

The Dexterity related implementation consists of Behaviors for each
interface. These are:

- ``bda.plone.shop.dx.IBuyableBehavior``
- ``bda.plone.shop.dx.IStockBehavior``
- ``bda.plone.shop.dx.IShippingBehavior``
- ``bda.plone.shop.dx.IItemNotificationTextBehavior``
- ``bda.plone.shop.dx.IGlobalNotificationTextBehavior``

The corresponding adapter implementations are registered for the referring
behavior interfaces.

The ``IBuyable`` interface gets hooked on content via ``IBuyableBehavior``.

In order to create buyable items with dexterity you need to either create a
portal type via GenericSetup or use the Dexterity TTW Editor to assign the
behaviors to existing content, or create new type(s) TTW from scratch.

Notification related behaviors can be applied to any parent objects of buyable
items as well, notification text values are aquired until plone root is
reached.


Hide/Show viewlets for buyable items
------------------------------------

The bda.plone.shop.buyable viewlet is registered twice for buyable items - once
above the content body and once below. You can control the display via standard
``viewlets.xml`` GenericSetup profile mechanisms or manually via the
``@@manage-viewlets`` on individual buyable items.
If you want to control the viewlets via ``@@manage-viewlets`` for the whole
portal at once, use one of the following links directly (the portlet is not
shown in @@manage-viewlets, if the context is not a buyable item):

- http://YOUR_PORTALS_URL/@@manage-viewlets?show=plone.abovecontentbody%3Abda.plone.shop.buyable
- http://YOUR_PORTALS_URL/@@manage-viewlets?hide=plone.abovecontentbody%3Abda.plone.shop.buyable
- http://YOUR_PORTALS_URL/@@manage-viewlets?show=plone.belowcontentbody%3Abda.plone.shop.buyable
- http://YOUR_PORTALS_URL/@@manage-viewlets?hide=plone.belowcontentbody%3Abda.plone.shop.buyable


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


Permissions
-----------

There exists ``bda.plone.shop.ViewBuyableInfo`` and ``bda.plone.shop.BuyItems``
permission to control what parts of buyable data and controls get exposed to
the user.

In general, custom shop deployments are likely to configure the permission and
role settings according to their use cases.


bda.plone.shop.ViewBuyableInfo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This permission controls whether a user can view basic buyable information.
These are item availability and item price. By default, this permission is set
for roles:

* Manager
* Site Administrator
* Reviewer
* Editor
* Customer
* Authenticated

This permission is also granted to the Authenticated role, to cover the use
case, where authenticated users should see price informations, but not buy
items.

In order to expose buyable information to all visitors by default,
add ``Anonymous`` role via generic setup's ``rolemap.xml`` of your
integration package.


bda.plone.shop.BuyItems
~~~~~~~~~~~~~~~~~~~~~~~

This permission controls whether a user can actually add this item to shopping
cart. By default, this permission is set for roles:

* Manager
* Site Administrator
* Customer

In order to enable non-customers or anonymous users to buy items, modify
``rolemap.xml`` in your integration package as needed. Be aware that the shop
is basically designed that anonymous users can buy items, but orders related
features like viewing own orders are bound to ``Customer`` role.


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
