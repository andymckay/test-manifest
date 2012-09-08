$(document).ready(function() {
    $('#validate').submit(function() {
        $.post($('#validate').attr('action'), $('#validate').serialize(),
                function(data) {
                    alert(data)
                });
    });
});
