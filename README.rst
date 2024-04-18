bda.plone.shop
==============

E-commerce solution for `Plone <http://plone.com>`_

.. image:: https://github.com/bluedynamics/bda.plone.shop/actions/workflows/main.yml/badge.svg
    :target: https://github.com/bluedynamics/bda.plone.shop/actions/workflows/main.yml

.. image:: https://black.readthedocs.io/en/stable/_static/pypi.svg
    :target: https://pypi.org/project/black/


Installation
------------

Depend your instance to ``bda.plone.shop`` and install it as addon in plone
control panel.


Development and testing
-----------------------

Checkout ``bda.plone.shop`` from
``git://github.com/bluedynamics/bda.plone.shop.git`` and run::

    ~$ make install

This installs all dependencies with ``mxdev`` and prepares scripts for
running tests.


Running tests
~~~~~~~~~~~~~

If you have run the buildout, you can run all tests like so::

    ~$ make test-ignore-warnings

To run the robot tests do::

    ./venv/bin/zope-testrunner --auto-color --auto-progress --test-path=./src --all

For development, it might be more convenient to start a test server and run
robot tests individually, like so (-d to start Zope in DEBUG-MODE)::

    ./venv/bin/robot-server bda.plone.shop.tests.ShopDXFull_ROBOT_TESTING -d
    ./venv/bin/robot src/bda/plone/shop/tests/robot/test_shop_orderprocess.robot

To automatically land in the debug shell on test-failure, use::

    ./venv/bin/robot-debug src/bda/plone/shop/tests/robot/test_shop_orderprocess.robot

In the robot test you can place the debug statement to access a robot shell to
try things out.

For more information on this topic visit:
https://docs.plone.org/external/plone.app.robotframework/docs/source/happy.html


Enable Content to be buyable
----------------------------

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

There exists implementations of these adapters among with related Dexterity Behaviors.

For Plone 5 'Summary View' is overriden for folders and collections to show your
buyables with controls to add them into the cart.


Dexterity Behaviors
~~~~~~~~~~~~~~~~~~~

The Dexterity related implementation consists of Behaviors for each interface.
These are (shortname in brackets):

- ``bda.plone.shop.dx.IBuyableBehavior`` (``bda.shop.buyable``)
- ``bda.plone.shop.dx.IStockBehavior`` (``bda.shop.stock``)
- ``bda.plone.shop.dx.IShippingBehavior`` (``bda.shop.shipping``)
- ``bda.plone.shop.dx.IItemNotificationTextBehavior`` (``bda.shop.notificationtext.item``)
- ``bda.plone.shop.dx.IGlobalNotificationTextBehavior`` (``bda.shop.notificationtext.global``)
- ``bda.plone.shop.dx.ITradingBehavior`` (``bda.shop.trading``)
- ``bda.plone.shop.dx.IBuyablePeriodBehavior`` (``bda.shop.buyableperiod``)

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
------------------------

The cart can render preview images for the cart items in case when the context
has a field named ``image``

You can change the preview image rendering by adapting your own cart items.
If you want to change the scale of the image, inherit from the existing
adapter class and change ``preview_scale`` property::

    >>> from bda.plone.shop.dx import DXCartItemPreviewImage
    >>> class MyDXCartItemPreviewImage(DXCartItemPreviewImage):
    ...     preview_scale = "my_scale"

To do more complex preview image rendering you can override the ``url``
property::

    >>> class MyDXCartItemPreviewImage(DXCartItemPreviewImage):
    ...     @property
    ...     def url(self):
    ...         # do sophisticated stuff to get your preview image
    ...         return preview_url

Register your adapter via ZCML::

    <adapter
      for="some.package.IMyDXContent"
      factory=".youradater.MyDXCartItemPreviewImage" />


Permissions
-----------

In general, custom shop deployments are likely to configure the permission and
role settings according to their use cases.

There exists ``bda.plone.shop.ViewBuyableInfo`` and
``bda.plone.shop.ModifyCart`` permission to control what parts of buyable data
and controls get exposed to the user.

Further the permissions ``bda.plone.shop.ChangePersonalInformation`` and
``bda.plone.shop.ChangePersonalPreferences`` are used to control access to
Personal Preferences respective Personal Information pages. By default,
users with role ``Customer`` can access Personal Information only, as it
usually makes no sense to give a customer settings like a preferred editor.


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


bda.plone.shop.ModifyCart
~~~~~~~~~~~~~~~~~~~~~~~~~

This permission controls whether a user can actually add or update this item to
shopping cart. By default, this permission is set for roles:

* Manager
* Site Administrator
* Customer

In order to enable non-customers or anonymous users to mofify the cart, edit
``rolemap.xml`` in your integration package as needed. Be aware that the shop
is basically designed that anonymous users can buy items, but orders related
features like viewing own orders are bound to ``Customer`` role.


Customizing the shop
--------------------

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
---------------

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
-------------------

::

    $ cd src/bda/plone/shop/
    $ ./i18n.sh


Backward incompatible changes
-----------------------------

1.0a1
~~~~~

* ``bda.plone.shop: Buy Items`` permission has been renamed to
  ``bda.plone.shop: Modify Cart``. If you have custom ``rolemap.xml`` in your
  GS profiles using this permission, or you use this permission somewhere in
  your code, you need to update your customizations.


Upgrade to Plone 5
------------------

If you upgrade to Plone 5, you have to run the upgrade step
``Remove old JS and CSS resources for Plone 5`` manually to remove the old
registration of resources.


Contributors
------------

We'd be happy to see forks and pull-requests to improve this program.
Professional support is offered by the maintainers and some of the authors.


Maintainers
~~~~~~~~~~~

- Robert Niederreiter
- Peter Holzer
- Jens Klein

Contact: `dev@bluedynamics.com <mailto:dev@bluedynamics.com>`_


Authors
~~~~~~~

- Robert Niederreiter (Author)
- Peter Holzer
- Peter Mathis
- Harald Frießnegger
- Espen Moe-Nilssen
- Johannes Raggam
- Jure Cerjak
- Benjamin Stefaner
- Jens Klein
