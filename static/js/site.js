$(document).ready(function() {
    $('button.action').bind('click', function() {
        var $elem = $(this);
        var $form = $elem.closest('form');
        $.post($elem.attr('data-dest'), $form.serialize(),
                function(data) {
                    jQuery.each(data, function(index, value) {
                        $('section.output').append('<pre>' + value + '</pre>');
                    });
                });
        return false;
    });
});
