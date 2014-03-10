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

  debug

*** Keywords ***

# Given

a site owner
  Enable autologin as  Manager


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


# Then

Vendor area is enabled
  Page Should Contain  Enabled Vendor

User is added as Vendor
  Page Should Contain  Changes saved

