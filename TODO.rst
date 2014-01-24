TESTCASES
=========

- directly call @@checkout on item with empty cart -> redirect to item.
- anonymous @@checkout
- member @@checkout with @@personal-information filled out
- member @@checkout with no @@personal-information filled out

- create member, check if it's in Customer role


rnixx
-----

- darf anon benutzer einkaufen?
- darf anon benutzer preise sehen?


@@orders
--------

- perm. checks in code. eine view.
- req. parameter mit username.

- export auch angepasst

- enable vendor action

- vendor_uid ===> context uid ===> index in soup von booking.
        if no vendor set, use Plone Site uid /

- XXX: folder mit FTI vendor

- XXX: buyable uid


should orders be canceled on smtperrors?
----------------------------------------
2014-01-14 14:28:41 ERROR MailDataManager {'admin@admin.admin': (450, '4.1.2 <admin@admin.admin>: Recipient address rejected: Domain not found')}
Traceback (most recent call last):
  File "/home/thet-data/dotfiles-thet/home/.buildout/eggs/Products.CMFPlone-4.3.2-py2.7.egg/Products/CMFPlone/patches/sendmail.py", line 12, in _catch
    return func(*args, **kwargs)
  File "/home/thet-data/dotfiles-thet/home/.buildout/eggs/zope.sendmail-3.7.5-py2.7.egg/zope/sendmail/mailer.py", line 77, in send
    connection.sendmail(fromaddr, toaddrs, message)
  File "/usr/lib64/python2.7/smtplib.py", line 734, in sendmail
    raise SMTPRecipientsRefused(senderrs)
SMTPRecipientsRefused: {'admin@admin.admin': (450, '4.1.2 <admin@admin.admin>: Recipient address rejected: Domain not found')}


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
