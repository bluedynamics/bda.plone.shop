TESTING SHOP WORKFLOW

Two users order some items in different vendor areas

Each vendor should onle see the items in the orders, for which he has vendor
rights. Admin should see all.

*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***


*** Test Cases ***

Scenario: Two users order some items in different vendor areas

# SETUP

  Given a site owner

  When Admin enables vendor area on folder_1
  Then Vendor area is enabled
  When Admin adds user vendor1 to Vendors on folder_1
  Then User is added as Vendor

  When Admin enables vendor area on folder_2
  Then Vendor area is enabled
  When Admin adds user vendor2 to Vendors on folder_2
  Then User is added as Vendor


# ORDERS

  Given a user customer1
  When adding item_11 in folder_1 to cart
  Then item number 1 in cart should have quantity 1
  When adding item_11 in folder_1 to cart
  Then item number 1 in cart should have quantity 2
  When adding item_12 in folder_1 to cart
  Then item number 2 in cart should have quantity 1
  When adding item_21 in folder_2 to cart
  Then item number 3 in cart should have quantity 1
  When adding item_22 in folder_2 to cart
  Then item number 4 in cart should have quantity 1
  When Checkout Order customer1
  Then Order should be placed

  When checking myorders
  Then customer Pfister sees own but not Poppins orders
  When checking order details
  Then customer sees email mister@pfister.com and own bookings item_11 and item_22

  Given a user customer2
  When editing personal information for customer2
  When adding item_21 in folder_2 to cart
  Then item number 1 in cart should have quantity 1
  When adding item_21 in folder_2 to cart
  Then item number 1 in cart should have quantity 2
  When adding item_22 in folder_2 to cart
  Then item number 2 in cart should have quantity 1
  When Checkout Order customer2
  Then Order should be placed

  When checking myorders
  Then customer Poppins sees own but not Pfister orders
  When checking order details
  Then customer sees email marry@poppins.com and own bookings item_21 and item_22


# VENDORS

  Given a user vendor1
  When checking orders
  Then vendor1 sees allowed orders
  When vendor1 checking customer1 order details
  Then vendor1 sees customer1 allowed bookings

  Given a user vendor2
  When checking orders
  Then vendor2 sees allowed orders
  When vendor2 checking customer1 order details
  Then vendor2 sees customer1 allowed bookings
  When vendor2 checking customer2 order details
  Then vendor2 sees customer2 allowed bookings

  Given a site owner
  When checking orders
  Then admin sees all orders
  When admin checking customer1 order details
  Then admin sees customer1 all bookings
  When admin checking customer2 order details
  Then admin sees customer2 all bookings


*** Keywords ***

# Given

a site owner
  Log out
  Login as site owner

a user ${user}
  Log out
  Log In  ${user}  ${user}


# When

Admin enables vendor area on ${path}
  Go to  ${PLONE_URL}/${path}
  Location Should Be  ${PLONE_URL}/${path}
  Click Element  css=#plone-contentmenu-actions dt a
  Click Link  css=#plone-contentmenu-actions-enableVendor

Admin adds user ${user} to Vendors on ${path}
  Go to  ${PLONE_URL}/${path}/@@sharing
  Page Should Contain  Sharing for
  Input Text  id=sharing-user-group-search  ${user}
  Select Checkbox  css=td[title='${user}'] ~ td input[name='entries.role_Vendor:records']
  Click Button  id=sharing-save-button

adding ${item} in ${path} to cart
  Go To  ${PLONE_URL}/${path}/${item}
  Sleep  500ms  # wait for ajax request to finish
  Sleep  1s  # wait for ajax request to succeed
  Click Link  css=.add_cart_item

item number ${pos} in cart should have quantity ${num}
  Sleep  500ms  # wait for ajax request to succeed
  Wait Until Page Contains Element  css=#cart li.cart_item:nth-of-type(${pos})
  Textfield Value Should Be  css=#cart li.cart_item:nth-of-type(${pos}) .cart_item_count  ${num}

Checkout Order customer1
  Click Link  css=.go_to_cart_action
  Click Link  css=.cart_checkout_button
  Input Text  css=#input-checkout-personal_data-firstname  Mister
  Input Text  css=#input-checkout-personal_data-lastname  Pfister
  Input Text  css=#input-checkout-personal_data-email  mister@pfister.com
  Input Text  css=#input-checkout-personal_data-phone  +1234567890
  Input Text  css=#input-checkout-billing_address-street  Mister Pfisterstrasse
  Input Text  css=#input-checkout-billing_address-zip  1234
  Input Text  css=#input-checkout-billing_address-city  megacity
  Select From List By Value  css=#input-checkout-billing_address-country  040
  Select Radio Button  checkout.payment_selection.payment  cash
  Click Button  css=#input-checkout-next
  Page Should Contain  Your Order
  Page Should Contain Element  css=.cart_item.cart_overview+.cart_item.cart_overview+.cart_item.cart_overview+.cart_item.cart_overview
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Contain  Pfisterstrasse
  Page Should Contain  Cash
  Select Checkbox  css=#input-checkout-accept_terms_and_conditions-accept
  Click Button  css=#input-checkout-finish


editing personal information for customer2
  Go To  ${PLONE_URL}/@@personal-information
  Input Text  css=#form-widgets-firstname  Marry
  Input Text  css=#form-widgets-lastname  Poppins
  Input Text  css=#form-widgets-email  marry@poppins.com
  Input Text  css=#form-widgets-phone  +123
  Input Text  css=#form-widgets-street  Galaxy North
  Input Text  css=#form-widgets-zip  9999
  Input Text  css=#form-widgets-city  high in the sky
  Select From List By Value  css=#form-widgets-country  040
  Click Button  css=#form-buttons-save

Checkout Order customer2
  Click Link  css=#portaltab-index_html a
  Click Link  css=.go_to_cart_action
  Click Link  css=.cart_checkout_button
  Textfield Value Should Be  css=#input-checkout-personal_data-firstname  Marry
  Textfield Value Should Be  css=#input-checkout-personal_data-lastname  Poppins
  Textfield Value Should Be  css=#input-checkout-personal_data-phone  +123
  Textfield Value Should Be  css=#input-checkout-billing_address-street  Galaxy North
  Textfield Value Should Be  css=#input-checkout-billing_address-zip  9999
  Textfield Value Should Be  css=#input-checkout-billing_address-city  high in the sky
  List Selection Should Be  css=#input-checkout-billing_address-country  040
  Select Radio Button  checkout.payment_selection.payment  cash
  Click Button  css=#input-checkout-next
  Page Should Contain  Your Order
  Page Should Contain Element  css=.cart_item.cart_overview+.cart_item.cart_overview
  Page Should Contain  Marry
  Page Should Contain  Poppins
  Page Should Contain  high in the sky
  Page Should Contain  Cash
  Select Checkbox  css=#input-checkout-accept_terms_and_conditions-accept
  Click Button  css=#input-checkout-finish

checking myorders
  Click Link  css=.portlet .myorders a

checking orders
  Click Link  css=.portletShopAdmin li.orders a

checking order details
  Click Link  css=#bdaploneorders tr:nth-of-type(1) a.contenttype-document[title="View Order"]


vendor1 checking customer1 order details
  # These selectors are quite weak. but the table doesn't offer better.
  Click Link  css=#bdaploneorders tr:nth-of-type(1) a.contenttype-document[title="View Order"]

vendor2 checking customer1 order details
  # These selectors are quite weak. but the table doesn't offer better.
  Click Link  css=#bdaploneorders tr:nth-of-type(2) a.contenttype-document[title="View Order"]

vendor2 checking customer2 order details
  # These selectors are quite weak. but the table doesn't offer better.
  Click Link  css=#bdaploneorders tr:nth-of-type(1) a.contenttype-document[title="View Order"]

admin checking customer1 order details
  # These selectors are quite weak. but the table doesn't offer better.
  Click Link  css=#bdaploneorders tr:nth-of-type(2) a.contenttype-document[title="View Order"]

admin checking customer2 order details
  # These selectors are quite weak. but the table doesn't offer better.
  Click Link  css=#bdaploneorders tr:nth-of-type(1) a.contenttype-document[title="View Order"]



# Then

Vendor area is enabled
  Page Should Contain  Enabled Vendor

User is added as Vendor
  Page Should Contain  Changes saved

Order should be placed
  Page Should Contain  Order Received

customer ${customer_lastname} sees own but not ${other_lastname} orders
  Page Should Contain  ${customer_lastname}
  Page Should Not Contain  ${other_lastname}


customer sees email ${email} and own bookings ${item1} and ${item2}
  Page Should Contain  Order Details
  Page Should Contain  ${email}
  Page Should Contain  ${item1}
  Page Should Contain  ${item2}


vendor1 sees allowed orders
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Not Contain  Marry
  Page Should Not Contain  Poppins

vendor1 sees customer1 allowed bookings
  Page Should Contain  Order Details
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Contain  item_11
  Page Should Contain  item_12
  Page Should Not Contain  item_21
  Page Should Not Contain  item_22


vendor2 sees allowed orders
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Contain  Marry
  Page Should Contain  Poppins

vendor2 sees customer1 allowed bookings
  Page Should Contain  Order Details
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Not Contain  item_11
  Page Should Not Contain  item_12
  Page Should Contain  item_21
  Page Should Contain  item_22

vendor2 sees customer2 allowed bookings
  Page Should Contain  Order Details
  Page Should Contain  Marry
  Page Should Contain  Poppins
  Page Should Not Contain  item_11
  Page Should Not Contain  item_12
  Page Should Contain  item_21
  Page Should Contain  item_22


admin sees all orders
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Contain  Marry
  Page Should Contain  Poppins

admin sees customer1 all bookings
  Page Should Contain  Order Details
  Page Should Contain  Mister
  Page Should Contain  Pfister
  Page Should Contain  item_11
  Page Should Contain  item_12
  Page Should Contain  item_21
  Page Should Contain  item_22

admin sees customer2 all bookings
  Page Should Contain  Order Details
  Page Should Contain  Marry
  Page Should Contain  Poppins
  Page Should Not Contain  item_11
  Page Should Not Contain  item_12
  Page Should Contain  item_21
  Page Should Contain  item_22
