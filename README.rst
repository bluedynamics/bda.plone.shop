==============
bda.plone.shop
==============

Webshop Solution for Plone.


Installation
============

Depend your instance to ``bda.plone.shop`` and install it as addon in plone
control panel.

``bda.plone.shop`` won't work on stock Plone 4.3.x installations because it
requires some packages in more recent versions:

* ``plone.app.workflow`` >= 2.1.8

* ``plone.app.users`` >= 2.0.4

See the Troubleshooting_ section for more information.


Development and testing
=======================

Checkout ``bda.plone.shop`` from
``git://github.com/bluedynamics/bda.plone.shop.git`` and run contained buidlout
like so::

    ~$ virtualenv --no-site-packages vpython
    ~$ ./vpython/bin/python bootstrap.py
    ~$ ./bin/buildout

Start instance and create Plone site with shop profile applied.


Running tests
-------------

If you have run the buildout, you can run all tests like so::

    ./bin/test -s bda.plone.shop

The -t switch allows you to run a specific test file or method. The
``--list-tests`` lists all available tests.

To run the robot tests do::

    ./bin/test --all -s bda.plone.shop -t robot

For development, it might be more convenient to start a test server and run
robot tests individually, like so (-d to start Zope in DEBUG-MODE)::

    ./bin/robot-server bda.plone.shop.tests.ShopDXFull_ROBOT_TESTING -d
    ./bin/robot src/bda/plone/shop/tests/robot/test_shop_orderprocess.robot

To automatically land in the debug shell on test-failure, use::

    ./bin/robot-debug src/bda/plone/shop/tests/robot/test_shop_orderprocess.robot

In the robot test you can place the debug statement to access a robot shell to
try things out.

For more information on this topic visit:
http://developer.plone.org/reference_manuals/external/plone.app.robotframework/happy.html


Enable Content to be buyable
============================

Content which represent buyable items must implement
``bda.plone.orders.interfaces.IBuyable``.

Information related to Buyable items is acquired from content instance via
adapters implementing the following interfaces::

- ``bda.plone.cart.interfaces.ICartItemDataProvider``
- ``bda.plone.cart.interfaces.ICartItemStock``
- ``bda.plone.shipping.interfaces.IShippingItem``
- ``bda.plone.orders.interfaces.IItemNotificationText``
- ``bda.plone.orders.interfaces.IGlobalNotificationText``
- ``bda.plone.orders.interfaces.ITrading``
- ``bda.plone.orders.interfaces.IBuyablePeriod``

There exists Archetypes and Dexterity related implementations of these
adapters among with related Schema Extenders respective Dexterity Behaviors.


Archetypes
----------

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
      <implements interface="bda.plone.orders.interfaces.IBuyable" />
    </class>

Notification related schema extenders can be applied to any Archetypes object
including buyable items, notification text values are aquired until plone root
is reached::

    <adapter
      name="bda.plone.shop.itemnotificationtext"
      for="your.package.IContentInterface"
      factory="bda.plone.shop.at.ItemNotificationTextExtender"
      provides="archetypes.schemaextender.interfaces.IOrderableSchemaExtender" />

    <adapter
      name="bda.plone.shop.globalnotificationtext"
      for="your.package.IContentInterface"
      factory="bda.plone.shop.at.GlobalNotificationTextExtender"
      provides="archetypes.schemaextender.interfaces.IOrderableSchemaExtender" />


Dexterity
---------

The Dexterity related implementation consists of Behaviors for each
interface. These are:

- ``bda.plone.shop.dx.IBuyableBehavior``
- ``bda.plone.shop.dx.IStockBehavior``
- ``bda.plone.shop.dx.IShippingBehavior``
- ``bda.plone.shop.dx.IItemNotificationTextBehavior``
- ``bda.plone.shop.dx.IGlobalNotificationTextBehavior``
- ``bda.plone.shop.dx.ITradingBehavior``
- ``bda.plone.shop.dx.IBuyablePeriodBehavior``

The corresponding adapter implementations are registered for the referring
behavior interfaces.

The ``IBuyable`` interface gets hooked on content via ``IBuyableBehavior``.

In order to create buyable items with dexterity you need to either create a
portal type via GenericSetup or use the Dexterity TTW Editor to assign the
behaviors to existing content, or create new type(s) TTW from scratch.

Notification related behaviors can be applied to any Dexterity object including
buyable items, notification text values are aquired until plone root is
reached.


Cart item preview images
========================

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
===========

In general, custom shop deployments are likely to configure the permission and
role settings according to their use cases.

There exists ``bda.plone.shop.ViewBuyableInfo`` and ``bda.plone.shop.BuyItems``
permission to control what parts of buyable data and controls get exposed to
the user.

Further the permissions ``bda.plone.shop.ChangePersonalInformation`` and
``bda.plone.shop.ChangePersonalPreferences`` are used to control access to
Personal Preferences respective Personal Information pages. By default,
users with role ``Customer`` can access Personal Information only, as it
usually makes no sense to give a customer settings like a preferred editor.


bda.plone.shop.ViewBuyableInfo
------------------------------

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
-----------------------

This permission controls whether a user can actually add this item to shopping
cart. By default, this permission is set for roles:

* Manager
* Site Administrator
* Customer

In order to enable non-customers or anonymous users to buy items, modify
``rolemap.xml`` in your integration package as needed. Be aware that the shop
is basically designed that anonymous users can buy items, but orders related
features like viewing own orders are bound to ``Customer`` role.


Customizing the shop
====================

We know that every web-shop has different needs. This is why ``bda.plone.shop``
has been designed with maximum flexibility in mind.

In general, ``bda.plone.shop`` is customized by either changing settings
in the (always growing) control-panel, or by patching variables/classes.

Integrators might want to add a ``patchShop`` method to the ``initialize``
method of a Zope2 package::

    def initialize(context):
        """Initializer called when used as a Zope 2 product.
        """
        patchShop()

...and make sure it's called at startup time using the zcml::

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:five="http://namespaces.zope.org/five">

      <five:registerPackage package="." initialize=".initialize" />

    </configure>

In ``patchShop`` you typically import constants from ``bda.plone.shop``
related packages and redefine them.::

    def patchShop():
        from bda.plone import cart
        cart.CURRENCY_LITERALS['EUR'] = u'€'

Please see `bda.plone.checkout`_ or `bda.plone.order`_ for information
how to customize the checkout form or the notification emails
respectively.

.. _`bda.plone.checkout`: https://github.com/bluedynamics/bda.plone.checkout

.. _`bda.plone.order`: https://github.com/bluedynamics/bda.plone.order


Troubleshooting
===============

If you're missing widgets in the ``@@item_discount`` form (eg. the Autocomplete
for users or groups), you might want to reinstall (or re-run the GS import
steps) of the ``yafowil.plone`` (see its README__ for more information).

.. __: https://github.com/bluedynamics/yafowil.plone

If the autocomplete widget (in ``@@item_discount``) is not working you can try
to disable
``++resource++yafowil.widget.autocomplete/jquery-ui-1.8.18.autocomplete.min.js``
in ``portal_javascripts``.

In case you're having trouble with the forms, check if you're having
recent versions of ``yafowil`` >= 2.1 and yafowil related packages.


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
- Benjamin Stefaner (benniboy)
