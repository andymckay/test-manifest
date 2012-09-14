$(document).ready(function() {
    $('button.action').bind('click', function() {
        var $elem = $(this);
        var $form = $elem.closest('form');
        $.post($elem.attr('data-dest'), $form.serialize(),
                function(data) {
                    data.each(function(index) {
                        $('section.output').append('<pre>' + this + '</pre>');
                    });
                });
        return false;
    });
});
