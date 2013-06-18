(function($) {

    $(document).ready(function() {
        $('div.availability').bind('mouseover', function() {
            var details = $('div.availability_details', $(this).parents());
            if (!details.is(":visible")) {
                details.show();
            }
        });
        $('div.availability').bind('mouseout', function() {
            var details = $('div.availability_details', $(this).parents());
            if (details.is(":visible")) {
                details.hide();
            }
        });
    });

})(jQuery);
