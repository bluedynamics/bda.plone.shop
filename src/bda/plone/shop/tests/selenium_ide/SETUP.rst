Requirements in order to run this tests
=======================================

* Plone site running on ``localhost:8080/Plone``
* Portal language set to english
* Configured and working mail host
* Selenium IDE installed and running (2.5.0 at time of writing this tests)

Order of test files in selenium IDE:

* dx_configure_shop_settings
* dx_create_ct
* dx_create_content
* dx_do_orders
* dx_set_item_stock
* dx_delete_content
* dx_delete_ct
