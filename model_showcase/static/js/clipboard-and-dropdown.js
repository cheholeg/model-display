$(document).ready(function() {
    $('.dropdown-menu').click(function(e) {
        e.stopPropagation();
    });

    $('.word-for-copy').each(function () {
        var text = $(this).data('text') || $(this).text();
        var $button = $('<button />', {
            class: "copy-btn fa-regular fa-copy",
            click: function (e) {
                navigator.clipboard.writeText(text).then(function () {
                    var $notification = $('<div>').addClass('copyNotification').html('Скопировано!');
                    var btnPosition = $(e.target).position();
                    var btnCenterY = btnPosition.top;
                    $notification.css({
                        'top': btnCenterY,
                        'left': btnPosition.left + $(e.target).outerWidth() + 10
                    });
                    $notification.insertAfter($(e.target));
                    $notification.show();
                    setTimeout(function () {
                        $notification.remove();
                    }, 1000);
                })
            }
        });
        $(this).append($button);
    });
});
