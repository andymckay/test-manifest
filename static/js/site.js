$(document).ready(function() {
    $('#validate').bind('submit', function() {
        $.post($('#validate').attr('action'), $('#validate').serialize(),
                function(data) {
                    $('section.output').append($('p', {'text': data}));
                });
        return false;
    });
});
