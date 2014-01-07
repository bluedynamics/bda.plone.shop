TESTCASES
=========

- directly call @@checkout on item with empty cart -> redirect to item.
- anonymous @@checkout
- member @@checkout with @@personal-information filled out
- member @@checkout with no @@personal-information filled out

- create member, check if it's in Customer role



implementiert der robert:
- darf anon benutzer einkaufen?
- darf anon benutzer preise sehen?




@@orders
- perm. checks in code. eine view.
- req. parameter mit username.

--- export auch angepasst

-- enable vendor action
--- vendor_uid ===> context uid ===> index in soup von booking.
        if no vendor set, use Plone Site uid / 


XXX--- folder mit FTI vendor

XXX--- buyable uid



Mandantenfähigkeit
==================

- USt spezifika, nicht implementieren, ATM
  - über shop settings adapter...

- mandant soll nur für ihn bestimmte bestellungen sehen. wie?
  - mandanten spezifische shop einstellungen?
  - mandant-typ? shop-typ?
  - mandant-permission auf context, alle bestellungen innerhalb dieses pfads?


- usecase - user bestellt bei verschiedenen mandanten.
  - unterschiedliche carts?
  - oder zusammengefasste bestellung?



