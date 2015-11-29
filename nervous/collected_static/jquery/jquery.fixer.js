/*!
 * jquery.fixer.js 0.0.3 - https://github.com/yckart/jquery.fixer.js
 * Fix elements as `position:sticky` do.
 *
 *
 * Copyright (c) 2013 Yannick Albert (http://yckart.com/) | @yckart
 * Licensed under the MIT license (http://www.opensource.org/licenses/mit-license.php).
 * 2013/07/02
 **/

// Modifications (bug fixes) are made

;(function ($, window) {

    var $win = $(window);
    var defaults = {
        gap: 0,
        horizontal: false,
        isFixed: $.noop
    };

    var supportSticky = function (elem) {
        var prefixes = ['', '-webkit-', '-moz-', '-ms-', '-o-'], prefix;
        while (prefix = prefixes.pop()) {
            elem.style.cssText = 'position:' + prefix + 'sticky';
            if (elem.style.position !== '') return true;
        }
        return false;
    };

    $.fn.fixer = function (options) {
        options = $.extend(defaults, options);  // originally didn't work
        var hori = options.horizontal,
            cssPos = hori ? 'left' : 'top';

        return this.each(function () {
            var style = this.style,
                $this = $(this),
                $parent = $this.parent();

            /*
            if (supportSticky(this)) {
                style[cssPos] = options.gap + 'px';
                return;
            }
            */
            $win.on('scroll', function () {

                // Added: tweak for small windows
                if ($win.width() < 768) {
                    style.position = "fixed";
                    style[cssPos] = "";
                    return ;
                }

                var scrollPos = $win[hori ? 'scrollLeft' : 'scrollTop'](),
                    elemSize = $this[hori ? 'outerWidth' : 'outerHeight'](),
                    parentPos = $parent.offset()[cssPos],
                    parentSize = $parent[hori ? 'outerWidth' : 'outerHeight']();
                parentSize = Math.max(parentSize, elemSize);

                if (scrollPos >= parentPos - options.gap && (parentSize + parentPos - options.gap) >= (scrollPos + elemSize)) {
                    style.position = 'fixed';
                    style[cssPos] = options.gap + 'px';
                    options.isFixed();
                } else if (scrollPos < parentPos - options.gap) {
                    style.position = 'absolute';
                    style[cssPos] = options.gap + 'px';
                } else {
                    style.position = 'absolute';
                    style[cssPos] = (parentSize - elemSize + options.gap) + 'px';
                }
            }).resize();
        });
    };

}(jQuery, this));
