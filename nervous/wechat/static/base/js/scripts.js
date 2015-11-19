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

function displayContent(data, params, container, callback) {
    var main;
    if (typeof container === typeof undefined)
        container = "#main-page";
    main = $(container);
    var anim = true, scroll = true;
    for (var prop in params) {
        if (prop === "anim") anim = params.anim;
        if (prop === "scroll") scroll = params.scroll;
    }
    main.queue(function () {
        main.html(data);

        var final = function () {
            main.css("height", "auto");
            if (typeof callback === "function")
                callback();
        };

        if (anim) {
            var new_height = 0;
            main.children().each(function () {
                new_height += $(this).outerHeight(true);
            });
            if (scroll) {
                var delta_str = $(".main").css("padding-top");
                var delta = parseInt(delta_str.substr(0, delta_str.indexOf("px")), 10);
                var pos = main.position().top + ((container === "#main-page") ? (-delta) : delta);
                $("html, body").delay(50).animate({
                    "scroll-top": pos
                });
            }
            main.delay(50).animate({
                opacity: 1.0,
                height: new_height
            }, final);
        } else {
            final();
        }
        $(this).dequeue();
    });
}

// load page content using ajax
function loadContent(url, params, item_selector, callback) {
    var height = $("#left-column").height();
    var main = $("#main-page");

//    console.log(url);

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

function loadContentOn(container, url, params, load_params, callback) {
//    console.log("on: " + url);
    var main = $(container);

    var anim = false;
    for (var prop in load_params) {
        if (prop === "anim") anim = load_params.anim;
    }
    if (anim === true) {
        main.animate({
            opacity: 0,
            height: 0
        }, 250);
    }

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            displayContent(data, load_params, container);
            initAjaxPage(container);
        },
        error: function (xhr, textStatus, errorThrown) {
            displayContent('\
                <div class="alert alert-danger" role="alert">\
                    <strong>部件载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown
                + xhr.responseText.replace(/\n/g, "<br>") +
                '</div>',
                {anim: true, scroll: true}, container);
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

function loadContentOfItem(item, callback) {
    loadContent($(item).data("url"), {}, item, callback);
}

function handleFormPost(form_selector, post_url, params) {
    /*
     params = {
        success_callback(data):
            function to call when ajax POST returns success,
        error_callback(xhr, textStatus, errorThrown):
            function to call when ajax POST returns error,
        success_msg(data):
            function that returns message to display for success POST
            note that though POST is successful, returned status maybe "error"
     }
     */
    var form = $(form_selector);
    form.ready(function () {
        var msg = form.find(".form-error-msg");
        var msg_text = msg.find("> div");
        var form_groups = $(".form-group");

        var success_callback = function () {
            },
            error_callback = function () {
            },
            success_msg = function (data) {
                var method = "提交";
                if (data.hasOwnProperty("submit_method"))
                    method = data.submit_method === "submit" ? "提交" : "保存";
                if (data.status === "ok") return method + "成功！";

                if (data.hasOwnProperty("error_message"))
                    return data.error_message;
                return "提交出错，请再次检查您填写的信息。"
            };
        if (params.hasOwnProperty("success_callback"))
            success_callback = params.success_callback;
        if (params.hasOwnProperty("error_callback")) {
            success_callback = params.error_callback;
            console.log("own error_callback");
        }
        if (params.hasOwnProperty("success_msg"))
            success_callback = params.success_msg;

        msg.find("button").click(function () {
            msg.fadeOut();
        });
        form_groups.find("input, textarea").focus(function () {
            $(this).parent().removeClass("has-error");
        });

        form.submit(function (event) {
            event.preventDefault();
            form_groups.removeClass("has-error");

            $.ajax({
                type: "POST",
                url: post_url,
                data: form.serialize(),
                success: function (data) {
                    msg.removeClass("alert-danger alert-success");
                    if (data.status === "ok") msg.addClass("alert-success");
                    else msg.addClass("alert-danger");
                    msg_text.html(success_msg(data));
                    msg.fadeIn();

                    if (data.hasOwnProperty("error_field")) {
                        var field = form_groups.has("[name='" + data.error_field + "']");
                        field.addClass("has-error");
                        $.scrollTo(field, {offset: -200});
                    }

                    success_callback(data);
                },
                error: function (xhr, textStatus, errorThrown) {
                    console.log("post error");
                    msg_text.html("提交申请遇到错误：" + textStatus + ": " + errorThrown);
                    console.log(xhr.responseText.substr(0, 500));
                    msg.fadeIn();

                    error_callback(xhr, textStatus, errorThrown);
                }
            });
        });
    });
}

// apply one-time-only animation using animate.css
function animate(item, animation) {
    item.removeClass().addClass("animated " + animation)
        .one("animationend", function () {
            $(this).removeClass("animated " + animation);
        });
}

// pop up an modal for confirmation (substitute for "alert()")
function showConfirmModal(text, callback) {

}

// on document ready
$(function () {

    // bind History.js
    History.Adapter.bind(window, 'statechange', function () {
        var state = History.getState();
//        console.log('statechange: ' + state.url);
        var main = $("#main-page");

        if ($(window).width() < 768) {
//            console.log("mobile");
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

        displayContent(state.data.data, {}, undefined, state.data.callback);
    });

    // configure scrollto.js
    $.extend($.scrollTo.defaults, {
        axis: 'y',
        duration: 250
    });

    // bind toggle left column button (visible in xs)
    var left_column = $("#left-column");
    var column_container = $(".column-container");

    $("#left-column-toggle").click(function (e) {
        e.preventDefault();
        left_column.toggleClass("expanded");
        if (left_column.hasClass("expanded")) {
            var height = Math.max($("body").height(), $(window).height());
            var backdrop = $('<div id="left-column-backdrop"' +
                ' class="modal-backdrop fade visible-xs"' +
                ' style="z-index: 50; height: ' + height + 'px"></div>');
            $("body").append(backdrop);
            setTimeout(function () {
                backdrop.addClass("in");
            }, 100);
            $(backdrop).click(function () {
                left_column.removeClass("expanded");
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
        column_container.animate({
            "scroll-top": 0
        }, "fast");
    });

    // activate fixer for left column
    left_column.fixer({
        gap: 70
    });

    // set page min height according to left column
    var height = left_column.outerHeight(true);
    $("html, body").css("min-height", height);
    $("#main-page").css({
        "min-height": height
    });

    // spinning effect for chevrons
    left_column.find(".column-container > a").each(function () {
        $(this).append('<span class="fa fa-chevron-up pull-right"></span>');
    }).click(function () {
        var chevron = $(this).find("span.fa");
        if (chevron.hasClass("fa-chevron-up")) {
            chevron.removeClass("fa-chevron-up").addClass("fa-chevron-down");
        } else {
            chevron.removeClass("fa-chevron-down").addClass("fa-chevron-up");
        }
    });

    // hide scrolling indicators when reached top or bottom
    left_column.ready(function () {
        var top = left_column.find(".scroll-edge-top"),
            bottom = left_column.find(".scroll-edge-bottom");
        var delta = 100;
        column_container.scroll(function () {
            var scrollPos = column_container.scrollTop(),
                scrollHeight = column_container[0].scrollHeight,
                outerHeight = left_column.outerHeight();
//            console.log(scrollPos, scrollHeight, outerHeight);
            var bottom_opac = 1, top_opac = 1;
            if (scrollPos + delta > scrollHeight - outerHeight)
                bottom_opac = (scrollHeight - outerHeight - scrollPos) / delta;
            if (scrollPos < delta)
                top_opac = scrollPos / delta;
            bottom.css("opacity", bottom_opac);
//            bottom.css("filter", "alpha(opacity=" + bottom_opac + ")");
            top.css("opacity", top_opac);
//            top.css("filter", "alpha(opacity=" + top_opac + ");");
        });
        top.click(function () {
            column_container.animate({
                "scroll-top": 0
            }, "fast");
        });
        bottom.click(function () {
            column_container.animate({
                "scroll-top": column_container[0].scrollHeight - left_column.outerHeight()
            }, "fast");
        });
    });

    initAjaxPage();
});
