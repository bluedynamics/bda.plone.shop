*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***


*** Test Cases ***

Scenario: Two users order some items in different vendor areas
  Given a site owner

  When Admin enables vendor area on folder_1
  Then Vendor area is enabled
  When Admin adds user vendor1 to Vendors on folder_1
  Then User is added as Vendor

  When Admin enables vendor area on folder_2
  Then Vendor area is enabled
  When Admin adds user vendor2 to Vendors on folder_2
  Then User is added as Vendor

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

  debug




*** Keywords ***

# Given

a site owner
  Enable autologin as  Manager

a user ${user}
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
  Input Text  id=sharing-user-group-search  vendor1
  Select Checkbox  css=td[title='vendor1']+td+td+td input[name='entries.role_Vendor:records']
  Click Button  id=sharing-save-button

adding ${item} in ${path} to cart
  Go To  ${PLONE_URL}/${path}/${item}
  Click Link  css=.add_cart_item

item number ${pos} in cart should have quantity ${num}
  Sleep  1s  # wait for ajax request to succeed
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




# Then

Vendor area is enabled
  Page Should Contain  Enabled Vendor

User is added as Vendor
  Page Should Contain  Changes saved

Order should be placed
  Page Should Contain  Order Received

