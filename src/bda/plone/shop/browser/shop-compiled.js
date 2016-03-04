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


function createCookie(name,value,days) {
    var date,
        expires;

    if (days) {
        date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        expires = "; expires="+date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = name+"="+escape(value)+expires+"; path=/;";
}

function readCookie(name) {
    var nameEQ = name + "=",
        ca = document.cookie.split(';'),
        i,
        c;

    for(i=0;i < ca.length;i=i+1) {
        c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return unescape(c.substring(nameEQ.length,c.length));
        }
    }
    return null;
}
