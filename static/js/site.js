$(document).ready(function() {
    function auth_show() {
        $('#auth-get').removeClass('hidden');
        $('#auth-show').addClass('hidden');
        $('#auth').removeClass('hidden');
    }

    function auth_hide() {
        $('#auth-get').addClass('hidden');
        $('#auth-show').removeClass('hidden');
        $('#auth').addClass('hidden');
    }

    if (window.localStorage.getItem('key-secret')) {
        var vals = window.localStorage.getItem('key-secret').split('|');
        $('input#id_key')[0].value = vals[0];
        $('input#id_secret')[0].value = vals[1];
        auth_hide();
    }

    $('button.action').bind('click', function() {
        var $elem = $(this);
        var $form = $elem.closest('form');
        var $target = $('section.output');
        if ($('input#id_key')[0].value && $('input#id_secret')[0].value) {
            window.localStorage.setItem('key-secret',
                    $('input#id_key')[0].value + '|' +
                    $('input#id_secret')[0].value);
            auth_hide();
        }
        $form.ajaxError(
            function(event, request, settings) {
                $target.append('<div class="alert alert-error">Error occurred</div>');
            }
        );
        $.post($elem.attr('data-dest'), $form.serialize(),
                function(data) {
                    $.each(data, function() {
                        var type = this.error ? 'alert-error' : '';
                        $target.append('<div class="alert ' + type + '">' +
                                       '<b>Action:</b> ' + this.action + '<br/>' +
                                       '<b>URL:</b> ' + this.url + '<br/>' +
                                       '<b>Status:</b> ' + this.status + '</b></div>');
                        $target.append('<pre>' + JSON.stringify(this.result) + '</pre>');
                    });
                }, 'json');
        return false;
    });
    $('#clear').bind('click', function() {
        $('section.output').children().remove();
        return false;
    });
    $('#auth-show').bind('click', function() {
        auth_show();
        return false;
    });
});
