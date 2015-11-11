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

var __manualStateChange = false;

function displayContent(data, callback) {
    var main = $("#main-page");
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
            if (typeof callback === "function")
                callback();
        });
        $(this).dequeue();
    });
}

// load page content using ajax
function loadContent(url, params, item_selector, callback) {
    var height = $("#left-column").height();
    var main = $("#main-page");

    console.log(url);

    main.animate({
        opacity: 0,
        height: height
    }, 250);
    $(".left-column-item").removeClass("active");
    if (item_selector != false) {
        var item = $(item_selector);
        if (typeof item != typeof undefined) {
            $(item).addClass("active");
        }
    }

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            __manualStateChange = true;
            History.pushState({
                data: data,
                item: item_selector,
                callback: callback
            }, null, url);
            initAjaxPage("#main-page");
        },
        error: function (xhr, textStatus, errorThrown) {
            displayContent('\
                <div class="alert alert-danger" role="alert">\
                    <strong>页面载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown +
                xhr.responseText.replace(/\n/g, "<br>") +
                '</div>'
            );
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

function initAjaxPage(container) {
    $(container).ready(function () {
        $(".ajax-link").click(function () {
            loadContent($(this).data("url"));
        })
    });
}

function loadContentOn(url, params, container, callback) {
    console.log("on: " + url);
    var main = $(container);
    /*
     main.animate({
     opacity: 0,
     height: 0
     }, 250);
     */
    var show = function (data) {
        main.queue(function () {
            main.html(data);
            if (typeof callback === "function")
                callback();
            /*
             var new_height = 0;
             main.children().each(function () {
             new_height += $(this).outerHeight(true);
             });

             $("html, body").delay(60).animate({
             "scroll-top": main.offset().top
             });

             main.delay(50).animate({
             opacity: 1.0,
             height: new_height
             }, function () {
             main.css("height", "auto");
             if (typeof callback === "function")
             callback();
             });
             */
            $(this).dequeue();
        });
    };

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            show(data);
            initAjaxPage(container);
        },
        error: function (xhr, textStatus, errorThrown) {
            show('\
                <div class="alert alert-danger" role="alert">\
                    <strong>部件载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown
                + xhr.responseText.replace(/\n/g, "<br>") +
                '</div>'
            );
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

function loadContentOfItem(item, callback) {
    loadContent($(item).data("url"), {}, item, callback);
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
    // bind History.js
    History.Adapter.bind(window, 'statechange', function () {
        var state = History.getState();
        console.log('statechange: ' + state.url);
        var main = $("#main-page");

        if ($(window).width() < 768) {
            console.log("mobile");
            $("#left-column").removeClass("expanded");
            var backdrop = $("#left-column-backdrop");
            backdrop.removeClass("in");
            setTimeout(function () {
                backdrop.remove();
            }, 500);
        }

        if (!__manualStateChange) {
            var height = $("#left-column").height();
            main.animate({
                opacity: 0,
                height: height
            }, 250);
            $(".left-column-item").removeClass("active");
            if (state.data.item != false) {
                var item = $(state.data.item);
                if (typeof item != typeof undefined) {
                    $(item).addClass("active");
                }
            }
        } else {
            __manualStateChange = false;
        }

        displayContent(state.data.data, state.data.callback);
    });

    // bind toggle left column button (visible in xs)
    $("#left-column-toggle").click(function (e) {
        e.preventDefault();
        var left = $("#left-column");
        left.toggleClass("expanded");
        if (left.hasClass("expanded")) {
            var height = max($("body").height(), $(window).height());
            var backdrop = $('<div id="left-column-backdrop"' +
                ' class="modal-backdrop fade visible-xs"' +
                ' style="height:' + height.toString() + 'px"></div>');
            $("body").append(backdrop);
            setTimeout(function () {
                backdrop.addClass("in");
            }, 100);
            $(backdrop).click(function () {
                $("#left-column").removeClass("expanded");
                backdrop.removeClass("in");
                setTimeout(function () {
                    backdrop.remove();
                }, 500);
            });
        } else {
            var backdrop = $("#left-column-backdrop");
            backdrop.removeClass("in");
            setTimeout(function () {
                backdrop.remove();
            }, 500);
        }
    });

    // bind left column items to ajax calls
    $(".left-column-item").click(function () {
        if (!$(this).hasClass("active")) {
            loadContentOfItem("#" + this.id);
        }
    });
    $(".fake-link-scroll").click(function (e) {
        e.preventDefault();
        $("html, body").animate({
            "scroll-top": 0
        }, "fast");
    });

    // set page min height according to left column
    var height = $("#left-column").outerHeight(true);
    $("#main-page").css({
        "min-height": height
    });

    initAjaxPage();
});
