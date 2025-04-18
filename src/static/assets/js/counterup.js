/*!
 * Modified jquery.counterup.js to use data-value and prevent re-animation
 */
(function (e) {
    "use strict";
    e.fn.counterUp = function (t) {
        var n = e.extend({time: 400, delay: 10}, t);
        return this.each(function () {
            var t = e(this), r = n, i = function () {
                var initialValue = t.data('value') || t.text();
                var e = [], n = r.time / r.delay, i = initialValue.toString();

                i = i.replace(/,/g, "");

                var s = /[0-9]+,[0-9]+/.test(initialValue),
                    o = /^[0-9]+$/.test(i),
                    u = /^[0-9]+\.[0-9]+$/.test(i),
                    a = u ? (i.split(".")[1] || []).length : 0;

                for (var f = n; f >= 1; f--) {
                    var l = parseInt(i / n * f);
                    u && (l = parseFloat(i / n * f).toFixed(a));

                    if (s) {
                        while (/(\d+)(\d{3})/.test(l.toString())) {
                            l = l.toString().replace(/(\d+)(\d{3})/, "$1,$2");
                        }
                    }
                    e.unshift(l);
                }

                t.data("counterup-nums", e);
                t.text("0");

                var c = function () {
                    t.text(t.data("counterup-nums").shift());
                    if (t.data("counterup-nums").length) {
                        setTimeout(t.data("counterup-func"), r.delay);
                    } else {
                        t.data("counterup-nums", null);
                        t.data("counterup-func", null);
                    }
                };

                t.data("counterup-func", c);
                setTimeout(t.data("counterup-func"), r.delay);
            };

            t.waypoint(i, {
                offset: "100%",
                triggerOnce: true
            });
        });
    };
})(jQuery);