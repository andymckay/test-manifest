$(document).ready(function() {
    $('#validate').bind('submit', function() {
        $.post($('#validate').attr('action'), $('#validate').serialize(),
                function(data) {
                    alert(data);
                });
        return false;
    });
});
