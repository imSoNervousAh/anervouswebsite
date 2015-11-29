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
    });

    // handle global ajaxError
    $(document).ajaxError(function (e, jqXHR, ajaxSettings, thrownError) {
        if (jqXHR.status == '403') {
            window.location = '/login';
        }
    });
});

var __manualStateChange = false;
var transTimeFast = 150,
    transTime = 300;

function displayContent(data, params, container, callback) {
    var main;
    if (typeof container === "undefined")
        container = "#main-page";
    main = $(container);
    var anim = true, scroll = true;
    if (typeof params !== "undefined") {
        for (var prop in params) {
            if (prop === "anim") anim = params.anim;
            if (prop === "scroll") scroll = params.scroll;
        }
    }

    if (anim && main.css("opacity") > 0) {
        main.animate({
            opacity: 0
        }, transTimeFast);
    } else {
        main.css("opacity", 0);
    }

    main.queue(function () {
        main.html(data);

        var final = function () {
            main.css({
                height: "auto",
                opacity: 1
            });
            if (typeof callback === "function")
                callback();
        };

        if (anim) {
            var new_height = 0;
            main.children().each(function () {
                var $this = $(this);
                if ($this.prop("tagName").toLowerCase() === "script"
                    || $this.css("display") === "none") return;
                new_height += $this.outerHeight(true);
            });
            new_height = Math.max(new_height, removePx(main.css("min-height")));
            if (scroll) {
                var delta_str = $(".main").css("padding-top");
                var delta = parseInt(delta_str.substr(0, delta_str.indexOf("px")), 10);
                var pos = main.position().top + ((container === "#main-page") ? (-delta) : delta);
                $("html, body").stop(true).delay(50).animate({
                    "scroll-top": pos
                }, transTime);
            }
            main.delay(50).animate({
                opacity: 1.0,
                height: new_height
            }, transTime, final);
        } else {
            final();
        }
        $(this).dequeue();
    });
}

// load page content using ajax
function loadContent(url, params, item_selector, load_params, callback) {
    var main = $("#main-page");

    var replace = false, anim = true;
    if (typeof load_params != "undefined") {
        if (load_params.hasOwnProperty("replace"))
            replace = load_params["replace"];
        if (load_params.hasOwnProperty("anim"))
            anim = load_params["anim"];
    }

//    console.log(url);
    main.stop(true);
    if (anim) {
        main.animate({
            opacity: 0,
            height: main.height()
        }, transTimeFast);
    } else {
        main.css("height", main.height());
    }
    $(".left-column-item").removeClass("active");
    if (typeof item_selector !== "undefined") {
        var item = $(item_selector);
        if (typeof item !== "undefined") {
            $(item).addClass("active");
        }
    }

    var loadSpinnerTimer;
    loadSpinnerTimer = setTimeout(function () {
        main.animate({
            opacity: 50,
            height: 100
        }, transTimeFast);
        main.html('\
            <div style="width: 100%; text-align: center;">\
                <span class="fa fa-spinner fa-pulse fa-4x"></span>\
            </div>');
    }, 1000);

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            clearTimeout(loadSpinnerTimer);
            __manualStateChange = true;
            var state = {
                data: data,
                params: load_params,
                item: item_selector,
                rand: Math.random(),
                callback: callback
            };
            if (replace) {
                History.replaceState(state, document.title, url);
            } else {
                History.pushState(state, document.title, url);
            }
            initAjaxPage("#main-page");
            loadComplete();
        },
        error: function (xhr, textStatus, errorThrown) {
            clearTimeout(loadSpinnerTimer);
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
        $(".ajax-link").unbind().click(function () {
            loadContent($(this).data("url"));
        });
    });
}

function loadContentOn(container, url, params, load_params, callback) {
//    console.log("on: " + url);
    $(".main").css("height", "auto");
    var main = container;

    var anim = false;
    for (var prop in load_params) {
        if (prop === "anim") anim = load_params.anim;
    }
    if (anim === true) {
        main.animate({
            opacity: 0,
            height: 0
        }, transTimeFast);
    }

    var loadSpinnerTimer;
    loadSpinnerTimer = setTimeout(function () {
        main.animate({
            opacity: 30,
            height: 100
        }, transTimeFast);
        if (main.prop("tagName") == "TBODY") {
            main.html('\
                <tr style="background-color: white;"><td colspan="10000">\
                    <p></p>\
                    <p style="text-align: center">\
                        <span class="fa fa-spinner fa-pulse fa-2x"></span>\
                    </p>\
                </td></tr>');
        } else {
            main.html('\
                <div style="width: 100%; text-align: center;">\
                    <span class="fa fa-spinner fa-pulse fa-3x"></span>\
                </div>');
        }
    }, 1000);

    $.ajax({
        type: "GET",
        url: url,
        data: params,
        success: function (data) {
            clearTimeout(loadSpinnerTimer);
            displayContent(data, load_params, container, function () {
                if (typeof callback === "function")
                    callback();
                initAjaxPage(container);
                loadComplete();
            });
        },
        error: function (xhr, textStatus, errorThrown) {
            clearTimeout(loadSpinnerTimer);
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

function loadContentOfItem(item, load_params, callback) {
    loadContent($(item).data("url"), {}, item, load_params, callback);
}

function removePx(str) {
    if (typeof str === "number") return str;
    return parseInt(str.substr(0, str.length - 2));
}

function handleFormPost(form_selector, post_url, params) {
    /*
     params = {
        success_callback(data):
            Function to call when ajax POST returns success.
        error_callback(xhr, textStatus, errorThrown):
            Function to call when ajax POST returns error.
        success_msg(data):
            Function that returns message to display for success POST.
            Note that though POST is successful, returned status maybe "error".
            If returned message is empty, then the acutal message displayed
                would be generated using "native_success_msg'. To override this
                behavior, return "#no_message#" instead of empty string.
     }
     */
    var form = $(form_selector);
    form.ready(function () {
        var msg = form.find(".form-error-msg");
        var msg_text = msg.find("> div");
        var form_groups = form.find(".form-group");

        var method_input = form.find(".form-method");
        form.find(".form-btn").click(function () {
            method_input.attr("value", $(this).attr("value"));
        });
        form_groups.not(form_groups.has("span.help-block.with-errors"))
            .append('<span class="help-block with-errors"></span>');

        var native_success_msg = function (data) {
            if (data.status === "ok") return "#no_message#";
            if (data.status === "error") {
                if (data.hasOwnProperty("error_messages"))
                    return "#no_message#";
                if (data.hasOwnProperty("error_message"))
                    return data.error_message;
            }
            return "提交出错，请再次检查您填写的信息。"
        };

        var success_callback = $.noop,
            error_callback = $.noop,
            success_msg = native_success_msg,
            before_submit = $.noop;
        if (params.hasOwnProperty("success_callback"))
            success_callback = params.success_callback;
        if (params.hasOwnProperty("error_callback"))
            error_callback = params.error_callback;
        if (params.hasOwnProperty("success_msg"))
            success_msg = params.success_msg;
        if (params.hasOwnProperty("before_submit"))
            before_submit = params.before_submit;

        form_groups.find("input, textarea").focus(function () {
            $(this).parent().removeClass("has-error");
            msg.fadeOut();
        });

        form.submit(function (event) {
            before_submit(event);
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
                    var message = success_msg(data);
                    if (message === "") message = native_success_msg(data);
                    if (message !== "" && message !== "#no_message#") {
                        msg_text.html(message);
                        msg.fadeIn();
                    } else {
                        msg.fadeOut();
                    }

                    if (data.hasOwnProperty("error_messages")) {
                        var pos = -1;
                        for (var field_name in data.error_messages) {
                            var field = form_groups.has("[name='" + field_name + "']");
                            field.addClass("has-error");
                            field.find("span").html(data.error_messages[field_name]);
                            var top = field.position().top;
                            if (pos === -1 || pos > top) pos = top;
                        }

                        if ($("html, body").css("scroll-top") > pos) {
                            $("html, body").animate({
                                "scroll-top": pos
                            }, "fast");
                        }
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

// refresh certain parts of page after (re)load
function loadComplete() {
    // refresh badges with data-source
    $(".badge").each(function () {
        var $this = $(this),
            url = $this.data("source");
        if (typeof url === "undefined") return;
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $this.html(data.toString());
            }
        })
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
function showConfirmModal(title, message, one_button, callback) {
    var raw_html_begin = '\
    <div class="modal fade" id="confirm-modal" tabindex="-1" role="dialog" aria-labelledby="modal-label">\
        <div class="modal-dialog modal-sm" role="document">\
            <div class="modal-content">\
                <div class="modal-header">\
                    <h4 style="font-size: 19px;" class="modal-title" id="modal-label">\
                        <!-- title -->\
                    </h4>\
                </div>\
                <div class="modal-body" style="text-align: center;">\
                    <!-- message -->\
                </div>\
                <div id="modal-click-buttons" class="modal-footer">';

    var raw_html_end = '\
                </div>\
            </div>\
        </div>\
    </div>';
    var no_button = '<button id="modal-no-button" class="btn btn-danger" data-dismiss="modal">取消</button>'
    var yes_button = '<button id="modal-yes-button" class="btn btn-success" data-dismiss="modal">确认</button>'

    if (one_button === undefined || one_button === false) raw_html_begin += no_button;
    raw_html_begin += yes_button;
    $("body").append(raw_html_begin + raw_html_end);
    var modal = $("#confirm-modal");

    modal.find(".modal-header > h4").html(title);
    modal.find(".modal-body").html(message);
    modal.find("#modal-yes-button").click(callback);

    modal.on("hidden.bs.modal", function () {
        modal.remove();
    });
    modal.modal();

    resizeComponents();
    loadComplete();
}

function showModal(url, id) {
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            $("body").append(data);
            var modal = $("#" + id);

            modal.on("hidden.bs.modal", function () {
                modal.remove();
            });
            modal.modal();

            resizeComponents();
            loadComplete();
        },
        error: function (xhr, textStatus, errorThrown) {
            displayContent('\
                <div class="alert alert-danger" role="alert">\
                    <strong>部件载入出错。</strong>\
                    错误信息：' +
                textStatus + ": " + xhr.status + " " + errorThrown
                + xhr.responseText.replace(/\n/g, "<br>") +
                '</div>',
                {anim: true, scroll: true});
            console.log(xhr.responseText.substr(0, 500));
        }
    });
}

// call a function for a number of times with same time delta
function callRepeated(callback, cycles, time) {
    var wrapper = function (x) {
        if (x > 0) {
            callback();
            setTimeout(function () {
                wrapper(x - 1);
            }, time);
        }
    };
    wrapper(cycles);
}

function initLeftColumn() {
    // bind toggle left column button (visible in xs)
    var body = $("body"),
        left_column = $("#left-column"),
        column_container = $(".column-container");

    $("#left-column-toggle").click(function (e) {
        e.preventDefault();
        left_column.toggleClass("expanded");
        if (left_column.hasClass("expanded")) {
            var height = Math.max(body.height(), $(window).height());
            var backdrop = $('<div id="left-column-backdrop"' +
                ' class="modal-backdrop fade visible-xs"' +
                ' style="z-index: 50; height: ' + height + 'px"></div>');
            body.append(backdrop);
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

    // spinning effect for chevrons
    var arrow_type = "angle-double",
        arrow_up = "fa-" + arrow_type + "-up",
        arrow_down = "fa-" + arrow_type + "-down";
    left_column.find(".column-container > a").each(function () {
        $(this).append('<span class="fa ' + arrow_up + ' pull-right"></span>');
    }).click(function () {
        var chevron = $(this).find("span.fa"),
            target = $($(this).data("target"));
        setTimeout(function () {
            if (!target.hasClass("in")) {
                chevron.removeClass(arrow_up).addClass(arrow_down);
            } else {
                chevron.removeClass(arrow_down).addClass(arrow_up);
            }
        }, 500);
    });

    // hide scrolling indicators when reached top or bottom
    left_column.ready(function () {
        var top = left_column.find(".scroll-edge-top"),
            top_chevron = top.find("span"),
            bottom = left_column.find(".scroll-edge-bottom"),
            bottom_chevron = bottom.find("span");
        var delta = 100;
        column_container.scroll(function () {
            var scrollPos = column_container.scrollTop(),
                scrollHeight = column_container[0].scrollHeight,
                outerHeight = left_column.outerHeight();

//            console.log(scrollPos, scrollHeight, outerHeight);
            var bottom_space = delta, top_space = delta;
            if (scrollPos + delta > scrollHeight - outerHeight)
                bottom_space = (scrollHeight - outerHeight - scrollPos);
            if (scrollPos < delta)
                top_space = scrollPos;
            bottom_chevron.css("opacity", bottom_space / delta);
            top_chevron.css("opacity", top_space / delta);

            if (bottom_space === 0) bottom.stop(true).fadeOut(150);
            else bottom.stop(true).fadeIn(150);
            if (top_space === 0) top.stop(true).fadeOut(150);
            else top.stop(true).fadeIn(150);
        });
        top.css("opacity", "");
        bottom.css("opacity", "");
        top.fadeOut(0);
        bottom.fadeOut(0);
        column_container.scroll();
        column_container.find("> a").click(function () {
            callRepeated(function () {
                $(window).scroll();
                column_container.scroll();
            }, 40, 10);
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
        gap: removePx($(".main").css("padding-top"))
    });
}

function resizeComponents() {
    var left_column = $("#left-column");
    // set page min height according to left column
    var height = left_column.outerHeight(true);
    $("html, body").css("min-height", height);
    $("#main-page").css({
        "min-height": height
    });
    $(".column-container").scroll();

    var backdrop = $(".modal-backdrop");
    if (typeof backdrop !== "undefined") {
        var backdrop_height = Math.max($("body").height(), $(window).height());
        backdrop.height(backdrop_height);
    }
}

function drawCharts(selected_charts) {
    var load_status = $(".tab-content").data("loading");
    var charts = $(".tab-pane object");
    if (typeof selected_charts !== "undefined")
        charts = selected_charts;
    if (typeof charts !== "undefined") {
        var active_container = $(".tab-pane.active object");
        var chart_height = active_container.height(), chart_width = active_container.width();
        charts.each(function () {
            var $this = $(this);
            $this.ready(function () {
                var json = $this.data("json");
                if (load_status !== true && json !== "") {
                    charts.html("");
                    renderChart("#" + $this.attr("id"), $this.data("type"), $this.data("json"), {
                        width: chart_width,
                        height: chart_height
                    });
                }
            });
        });
    }
}

// on document ready
$(function () {
    // bind History.js
    $(window).unbind('statechange');
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

        if (__manualStateChange) {
            __manualStateChange = false;
            displayContent(state.data.data, state.data.params, undefined, function () {
                if (typeof state.data.callback === "function")
                    state.data.callback();
                initAjaxPage("#main-page");
                loadComplete();
            });
        } else {
            main.stop(true).animate({
                opacity: 0,
                height: main.height()
            }, transTimeFast);
            $(".left-column-item").removeClass("active");
            if (state.data.item != false) {
                var item = $(state.data.item);
                if (typeof item != typeof undefined) {
                    $(item).addClass("active");
                }
            }
            displayContent(state.data.data, {}, undefined, function () {
                if (typeof state.data.callback === "function")
                    state.data.callback();
                initAjaxPage("#main-page");
                loadComplete();
            });
        }
    });

    $(window).on('resize', resizeComponents);

    var resizeTimer;
    $(window).on('resize', function (e) {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            // resize end
            drawCharts();
        }, transTimeFast);
    });

    initLeftColumn();

    initAjaxPage();

    loadComplete();
});
