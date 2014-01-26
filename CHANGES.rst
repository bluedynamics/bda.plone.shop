Changelog
=========

0.5dev
------

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
