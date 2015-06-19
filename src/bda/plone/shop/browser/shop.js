/* jslint browser: true */
/* global jQuery, bdajax */
(function($, bdajax) {
    "use strict";

    $(document).ready(function() {
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

})(jQuery, bdajax);
