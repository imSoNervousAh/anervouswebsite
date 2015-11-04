// deal with csrf tokens when using ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })
});


// load page content using ajax
function loadContent(url, params, item, callback) {
    var height = $("#left-column").height();
    var main = $("#main-page");

    console.log(url);

    main.animate({
        opacity: 0,
        height: height
    }, 250);
    $(".left-column-item").removeClass("active");
    if (typeof item !== typeof undefined) {
        item.addClass("active");
    }

    var show = function (data) {
        main.queue(function () {
            main.html(data);
            var new_height = 0;
            main.children().each(function () {
                new_height += $(this).outerHeight(true);
            });
            $("html, body").delay(60).animate({
                "scroll-top": 0
            });
            main.delay(50).animate({
                opacity: 1.0,
                height: new_height
            }, function () {
                main.css("height", "auto");
                if (typeof callback !== typeof undefined)
                    callback();
            });
            $(this).dequeue();
        });
    };

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            show(data);
        },
        error: function (xhr, textStatus, errorThrown) {
            show('\
                <div class="alert alert-danger" role="alert">\
                    <strong>页面载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown + xhr.responseText +
                '</div>'
            );
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

function loadContentOn(url, params, container, callback) {
    console.log(url);
    var main = $(container);

    main.animate({
        opacity: 0,
        height: 0
    }, 250);

    var show = function (data) {
        main.queue(function () {
            main.html(data);
            var new_height = 0;
            main.children().each(function () {
                new_height += $(this).outerHeight(true);
            });
            /*            $("html, body").delay(60).animate({
             "scroll-top": main.offset().top
             });
             */
            main.delay(50).animate({
                opacity: 1.0,
                height: new_height
            }, function () {
                main.css("height", "auto");
                if (typeof callback !== typeof undefined)
                    callback();
            });
            $(this).dequeue();
        });
    };

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            show(data);
        },
        error: function (xhr, textStatus, errorThrown) {
            show('\
                <div class="alert alert-danger" role="alert">\
                    <strong>部件载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown + xhr.responseText +
                '</div>'
            );
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

function loadContentOfItem(item, callback) {
    loadContent($(item).data("url"), {}, $(item), callback);
}

// apply one-time-only animation using animate.css
function animate(item, animation) {
    item.removeClass().addClass("animated " + animation)
        .one("animationend", function () {
            $(this).removeClass("animated " + animation);
        });
}

// on document ready
$(function () {
    $(".left-column-item").click(function () {
        if (!$(this).hasClass("active")) {
            loadContentOfItem(this);
        }
    });

    var height = $("#left-column").height();
    $("#main-page").css({
        "min-height": height
    });

    var itemSel = $("#main-page > #first-page-indicator").data("first-page");
    if (typeof itemSel !== typeof undefined) {
        loadContentOfItem(itemSel);
    }
});
