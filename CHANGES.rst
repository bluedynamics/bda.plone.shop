Changelog
=========

2.0.dev0 (unreleased)
---------------------

- Fix availability details pop-up
  [petri]

- Refactor buyable.[py|pt] for localized number output and better Decimal usage.
  Also use Python expressions for performance.
  [jensens]

- Use Decimal field for net price and cast to Decimal (for old values) in accessor.
  [jensens]

- provide information wether a comment is enabled or not on cartitem data.
  [jensens]

- Take buyable period for availability signal into account.
  [jensens]

- Mark buyable dl if comments are enabled or not to ease styling.
  [jensens]

- Localized number input for count.
  [jensens]

- No longer support for z3c.autoinclude.
  [jensens]

- Add more available units.
  [jensens]

- Make invoice fields optional
  [agitator]

- Code style black.
  [jensens]

- Fix import for latest cart/shipping changes.
  [jensens]

- Python 2/3 compatibility
  [agitator]

- Update version and classifiers - 2.x targets Plone 5.1/5.2 without Archetypes
  [agitator]

- migration: fixed an edgecase when upgrading old shop installations
  [petschki]


1.0a1 (unreleased)
------------------

- Replace unittest2 with unittest
  [llisa123]

- Use userschema.xml to extend shop specific user data for Plone 5.
  [agitator]

- Add invoice settings.
  [rnix]

- Some CSS fixes for shop settings in plone 5.
  [rnix]

- Fix failing ``bin/instance adduser`` in Plone due to not initialized registry on startup.
  Fixes: #100.
  [thet]

- Add metadata columns for ``item_net``, ``item_buyable_start`` and ``item_buyable_end``.
  This way, they can be displayed in the table view of collection results.
  [thet]

- Hide empty toolbar categories
  [agitator]

- Deliver discount in cart item data.
  [rnix]

- Rename ``bda.plone.shop: Buy Items`` permission to
  ``bda.plone.shop: Modify Cart``.
  [rnix]

- Added buyable_controls to summary_view via override of plone.app.contentypes
  [agitator]

- Use ``ICartDataProvider`` adapter lookup instead of ``CartItemCalculator``
  directly in shipping calculation to ensure possible custom implementation
  to take effect.
  [rnix]

- Deprecate use of ``bda.plone.shop.cartdata.CartItemCalculator``.
  [rnix]

- Fix error if item from cart cookie not found.
  [rnix]

- Fix display of currency in buyable viewlet based on shop settings
  [agitator]

- Implement ``IShippingItem.free_shipping`` for AT and DX. Consider this flag
  in conjunction with item shipping costs in ``DefaultShipping``.
  [rnix]

- Do not add shop admin portlet assignment on install in Plone 5
  [rnix]

- Implement shop navigation menu for Plone 5 toolbar.
  [rnix]

- Move shop portlet related link implementations to
  ``bda.plone.shop.browser.navigation``.
  [rnix]

- use MwSt. instead of Ust. in german
  [agitator]

- Overhaul code: use plone.api and zca decorators
  [jensens]

- Fix: Do not raise AttributeError if admin email or name were not yet set.
  [jensens]

- Add upgrade step for ``default_item_stock_warning_threshold`` setting.
  [thet]

- Add ``default_item_stock_warning_threshold`` setting for
  ``default_item_minimum_stock`` property from ``bda.plone.orders``.
  [andreesg]

- Behavior registration:
  Remove superfluos 'for' and give behaviors short names.
  [jensens]

- Add a PlonePAS Plugin for computed user properties.
  [pcdummy]

- Plone 5 Update, use separate styles/less.
  [agitator]

- Shop Portlet: Use appropriate context (Vendor, Site or Plone Site Root) also
  for Orders and Bookings views.
  [thet]

- Shop Portlet: Use appropriate context for "orders in context", like it's done
  for "bookings in context". Avoids calling this view on default pages.
  [thet]

- Shop Portlet: Add Shop Controlpanel admin link, linking to ISite or
  IPloneSiteRoot. If lineage.registry is installed, the shop settings can also
  be set on subsite level.
  [thet]

- Always show the mailtemplate link in the shop portlet, but link to the
  correct context. Rename i18n messages to reflect, if context is on a IVendor
  object (vendor), on a ISite (site-wide) or on a IPloneSiteRoot (global).
  [thet]

- Resolve JSHint errors and warnings.
  [thet]

- Fix: ``buyable_period`` was started one minute after the given time.
  [jensens]

- Separate AT and DX zcml registrations into own files for a better overview.
  [thet]

- Disable adapter for deprecated ``FlatRate`` shipping.
  [jensens]

- Change imports of IBuyable to bda.plone.orders - get rid of deprecation
  messages
  [jensens]

- Added two views to the admin portlet in which bookings are displayed
  and can be grouped by the buyers email adress or the buyable uid.
  Both views support daterange filtering and text index support.
  The ``Bookings`` view gets called on the portal root and the
  ``Bookings in Context`` returns all bookings data on the corresponding
  context it is called.
  [benniboy]

- Moved IBuyable to bda.plone.orders to avoid circular dependencies.
  [benniboy]

- Consider buyable effective and expires dates in availability details and
  display appropriate messages.
  [rnix]

- Change userdata adapters to named adapters, so other adapters can
  additionally extend the functionality.
  [thet]

- Added default_item_cart_count_limit to control panel defaults.
  Don't forget to run the update step.
  [agitator]

- Display status messages when modifying cart data via buyable viewlet
  [rnix]

- Add swiss VAT rates
  [rnix]

- Do not show 'Export Orders on this Item' on Plone Site Root
  [jensens]

- Use Products.statusmessages for displaying portal status messages when
  enabling or disabling Buyable or Vendor features.
  [thet]


0.9
---

- Add "Cash and Carry" shipping.
  [rnix]

- To enable and disable features on contexts (like vendor areas), don't use
  ``directlyProvides`` and erase all other directly provided interfaces, but
  use ``alsoProvides``. That's needed for collective.lineage sites to work
  after a vendor area was activated on them.
  [thet]


0.8
---

- Protect the ``@@myorders`` link in ``portlets.ShopAdmin`` portlet with the
  ``bda.plone.orders.ViewOwnOrders`` permission.
  [thet]

- Remove validation constraint for "Accept terms and conditions" flag in
  user information. The validation only applies at checkout time.
  [rnix]

- Do not fail in ``CashOnDeliverySettings.costs`` if
  ``IPaymentTextSettings.cash_on_delivery_costs`` not present yet.
  [rnix]

- Introduce ``bda.plone.shop.utils.format_amount``.
  [rnix]

- Add ``IPaymentTextSettings.cash_on_delivery_costs`` setting.
  [rnix]

- Add ``cash_in_advance`` and ``cash_on_delivery`` values to
  ``IPaymentTextSettings.available_payment_methods``.
  [rnix]

- Format currency values in default shipping messages.
  [rnix]


0.7
---

- Skip Shop portlet entirely if no shop links for user available.
  [rnix]

- Check for ``bda.plone.orders.ExportOrders`` permission in
  ``ShopPortletExportOrdersLink`` and ``ShopPortletExportOrdersItemLink``.
  [rnix]

- Bind ``dashboard`` user action to
  ``bda.plone.shop.ChangePersonalPreferences`` permission.
  [rnix]

- Format ``actions.xml`` to make action translations work properly. GS Profile
  application required.
  [rnix]

- Introcuce ``IShopSettings.add_customer_role_to_new_users`` and consider in
  principal created event subscriber.
  [rnix]

- Introduce "Personal Information" user action and adopt "Personal Preferences"
  user action in order to get displayed for permitted users only.
  [rnix]

- Introduce ``bda.plone.shop.ChangePersonalInformation`` and
  ``bda.plone.shop.ChangePersonalPreferences`` permissions and bind
  ``personal-preferences`` and ``personal-information`` views to shop layer
  and these permissions.
  [rnix]

- Check whether shipping method stored on cookie is available (any longer).
  [rnix]

- Implement ``bda.plone.orders.interfaces.ITrading`` for DX and AT.
  [rnix]

- Register ``mailnotify.RegistryPaymentText`` for
  ``zope.component.interfaces.ISite`` instead of
  ``Products.CMFCore.interfaces.ISiteRoot``.
  [rnix]

- Check against order total value instead of payment method in
  ``CheckoutSettings.skip_payment``.
  [rnix]

- Add ``cartdata.CartDataProvider.max_artice_count``.
  [rnix]

- Remove ``cartdata.CartDataProvider.include_shipping_costs``, it's implemented
  now on base class.
  [rnix]

- Remove ``IShopShippingSettings.include_shipping_costs``, flag gets calculated
  now from ``IShippingItem.shippable``. **Note** - Do not forget to run GS
  upgrade step ``4 to 5`` and adopt your integration package SG profile if
  necessary.
  [rnix]

- Introduce ``IShopShippingSettings.default_shipping_item_shippable`` and use
  as default for ``IShippingItem.shippable``.
  [rnix]

- Implement ``bda.plone.shipping.interfaces.IShippingItem.shippable`` and
  consider at appropriate places.
  [rnix]

- Implement ``bda.plone.checkout.interfaces.ICheckoutSettings`` at
  ``bda.plone.shop.checkout.CheckoutSettings``.
  [rnix]

- Implement ``bda.plone.shipping.interfaces.IShippingSettings`` at
  ``bda.plone.shop.shipping.ShippingSettings`` using
  ``bda.plone.shop.interfaces.IShopShippingSettings`` controlpanel settings.
  [rnix]

- Implement ``bda.plone.payment.interfaces.IPaymentSettings`` at
  ``bda.plone.shop.payment.PaymentSettings`` using
  ``bda.plone.shop.interfaces.IPaymentTextSettings`` controlpanel settings.
  [rnix]

- Add ``available_payment_methods``, ``payment_method`` and
  ``skip_payment_if_order_contains_reservations`` to
  ``bda.plone.shop.interfaces.IPaymentTextSettings`` and provide GS upgrade
  step.
  [rnix]

- Rename ``bda.plone.shop.vocabularies.PaymentVocabulary`` to
  ``bda.plone.shop.vocabularies.PaymentMethodsVocabulary``.
  [rnix]

- Implement ``bda.plone.orders.interfaces.IPaymentText`` at
  ``bda.plone.shop.mailnotify.RegistryPaymentText``.
  [rnix]

- Add admin portlet link for ``@@exportorders_contextual`` to export orders on
  this item.
  [thet]

- Implement ``bda.plone.orders.interfaces.INotificationSettings`` in
  ``bda.plone.shop.mailnotify``.
  [rnix]

- Rename ``bda.plone.shop.notificationtext`` to ``bda.plone.shop.mailnotify``.
  [rnix]

- Add ``Shop Admin Name`` to control panel setting.
  [fRiSi]

- Consider shipping method from cookie in cart data provider if present.
  [rnix]

- Extend ``CartItemCalculator`` by ``item_net``, ``item_vat`` and
  ``item_weight`` functions.
  [rnix]

- Add ``DefaultShipping`` and corresponding control panel settings. GS upgrade
  2_to_3 must be applied.
  [rnix]

- Deprecate ``FlatRate`` shipping.
  [rnix]

- Adopt shipping implementation to ``bda.plone.shipping`` >= 0.4.
  [rnix]

- Fix displaying of discounted price. Original price only gets displayed if
  it deferrs from discounted one.
  [rnix]

- Add documentation for customizing and installation.
  [fRiSi]


0.6
---

- Display original price and discounted price in buyable controls if discount
  for item applies.
  [rnix]

- Let CartDataProvider get the cart items title via an ICartItemDataProvider
  accessor to allow customizations. This can be used to give more context on
  the cart item, e.g. for a buyable within another content item.
  [thet]


0.5
---

- Introduce ``IBuyablePeriod`` interface, Implement for AT and DX and include
  checks in buyable controls and cart validation.
  [rnix]

- Implement ``validate_set`` on cart data provider.
  [rnix]

- Change browser view and adapter regitrations from IPloneSiteRoot to
  `zope.component.interfaces.ISite`. That's needed for Lineage compatibility.
  [thet]

- Integrate ``cart_count_limit`` property of cart item data interface.
  [rnix]

- Integrate ``hide_cart_if_empty`` property of cart data interface.
  [rnix]

- Implement ``display`` property of stock interface and consider it in buyable
  controls.
  [rnix]

- Changed markup and styles for the buyable_controls template, which is used
  for the buyable viewlet.
  [thet]

- Create a show_available property for buyable_controls. When set to True, as
  by default, the available information is shown for each buyable. This can be
  turned off in a customized buyable class for shared stock buyables.
  [thet]

- Remove buyable viewlet class, as it did not have any customization in it.
  This should not break backwards compatibility.
  [thet]

- Stick to ``AccessControl`` directly for checking buyable controls
  permissions. ``<SpecialUser 'Anonymous User'>`` instance returned by
  ``plone.api.user.get_current()`` not provides ``checkPermission`` function,
  which makes it useless.

- Introduce ``bda.plone.shop.ViewBuyableInfo`` and ``bda.plone.shop.BuyItems``
  permissions and consider in buyable controls. Now it can be controlled
  whether users can see item pricing and whether they can buy items.
  [rnix]

- Don't register ``bda.plone.shop.buyable`` viewlet for ``IBelowContentBody``
  but only for ``IAboveContentBody`` to avoid displaying it twice. Integrators
  should register it differently if they want to display the viewlet somewhere
  else.
  [thet]

- Integrate discount related stuff.
  [rnix]

- Set ``bda.plone.orders.permissions.DelegateVendorRole`` permission for
  ``Site Administrator`` and ``Manager`` roles in
  ``bda.plone.shop.browser.actions.VendorAction``.
  [rnix]

- Refactor Shop portlet and introduce
  ``bda.plone.shop.browser.admin.IShopPortletLink`` which can be used to hook
  up links to the shop portlet.
  [rnix, thet]

- Implement ``bda.plone.orders.IPaymentText``
  [rnix, jensens]

- Implement ``bda.plone.orders.I[Item|Global]NotificationText``
  [rnix, jensens]

- Allow portal member to store billing and delivery address information and use
  these as defaults for the checkout process.
  [thet]

- Fix BrowserLayer order precedence.
  [thet]


0.4
---

- Deprecate ``bda.plone.shop.extender`` and ``bda.plone.shop.behaviors``.
  [rnix]

- Obtain available shipping methods by listing registered adapters.
  [fRiSi]

- Take number in account when calculating weight.
  [fRiSi]


0.3
---

- Add weight calculation in ``bda.plone.shop.cartdata.CartItemCalculator``.
  [rnix]

- Display ``delivery_duration`` in availability details if defined.
  [rnix]

- Consider ``quantity_unit_float`` in ``CartItemAvailability`` implementation.
  [rnix]

- Implement ``bda.plone.shipping.IShippingItem`` for Dexterity and Archetypes.
  [rnix]

- Add controlpanel icon.
  [rnix]

- Set browserlayer for browser resources.
  [rnix]


0.2
---

- Vocabulary and controlpanel improvements.
  [rnix]

- Control panel now displays with several field sets.
  [hpeter]

- Refactor control panel by splitting up to several configuration interfaces.
  [hpeter]

- Add controlpanel.
  [espenmn]

- Extend AT and DX implementations by stock related interfaces.
  [rnix]

- Implement cart contracts for Dexterity and Archetypes.
  [rnix]

- No longer set ``bda.plone.shop.interfaces.IPotentiallyBuyable`` on all
  archetypes objects by default. Must be done in integration package.
  [rnix]

- Add adapter for cart item preview images.
  [petschki]

- Allow the shop administration portlet in the left column too.
  (fixes #2)
  [fRiSi]

0.1
---

- initial work
  [rnix]
