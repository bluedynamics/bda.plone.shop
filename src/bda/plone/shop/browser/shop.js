/*jslint browser: true*/
/*global $, jQuery, plone, require*/

if(require === undefined){
  require = function(reqs, torun){
    'use strict';
    return torun(window.jQuery);
  }
}

require([
    'jquery',
    'bdajax'
], function($){
    'use strict';

    var binder = function(context) {
        $('div.availability', context).unbind('mouseover')
                                      .bind('mouseover', function() {
            var details = $('div.availability_details', $(this));
            if (!details.is(":visible")) {
                details.show();
            }
        });
        $('div.availability', context).unbind('mouseout')
                                      .bind('mouseout', function() {
            var details = $('div.availability_details', $(this));
            if (details.is(":visible")) {
                details.hide();
            }
        });
    };
    if (bdajax !== undefined) {
        $.extend(bdajax.binders, {
            buyable_controls_binder: binder
        });
    }
    binder(document);

});
