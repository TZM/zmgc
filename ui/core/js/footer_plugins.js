/* Modernizr 2.5.3 (Custom Build) | MIT & BSD
 * Build: http://www.modernizr.com/download/#-touch-mq-cssclasses-teststyles-prefixes
 */;
window.Modernizr = function (a, b, c) {
    function x(a) {
        j.cssText = a
    }
    function y(a, b) {
        return x(m.join(a + ";") + (b || ""))
    }
    function z(a, b) {
        return typeof a === b
    }
    function A(a, b) {
        return !!~ ("" + a).indexOf(b)
    }
    function B(a, b, d) {
        for (var e in a) {
            var f = b[a[e]];
            if (f !== c) return d === !1 ? a[e] : z(f, "function") ? f.bind(d || b) : f
        }
        return !1
    }
    var d = "2.5.3",
        e = {},
        f = !0,
        g = b.documentElement,
        h = "modernizr",
        i = b.createElement(h),
        j = i.style,
        k, l = {}.toString,
        m = " -webkit- -moz- -o- -ms- ".split(" "),
        n = {},
        o = {},
        p = {},
        q = [],
        r = q.slice,
        s, t = function (a, c, d, e) {
            var f, i, j, k = b.createElement("div"),
                l = b.body,
                m = l ? l : b.createElement("body");
            if (parseInt(d, 10)) while (d--) j = b.createElement("div"), j.id = e ? e[d] : h + (d + 1), k.appendChild(j);
            return f = ["&#173;", "<style>", a, "</style>"].join(""), k.id = h, m.innerHTML += f, m.appendChild(k), l || (m.style.background = "", g.appendChild(m)), i = c(k, a), l ? k.parentNode.removeChild(k) : m.parentNode.removeChild(m), !! i
        },
        u = function (b) {
            var c = a.matchMedia || a.msMatchMedia;
            if (c) return c(b).matches;
            var d;
            return t("@media " + b + " { #" + h + " { position: absolute; } }", function (b) {
                d = (a.getComputedStyle ? getComputedStyle(b, null) : b.currentStyle)["position"] == "absolute"
            }), d
        },
        v = {}.hasOwnProperty,
        w;
    !z(v, "undefined") && !z(v.call, "undefined") ? w = function (a, b) {
        return v.call(a, b)
    } : w = function (a, b) {
        return b in a && z(a.constructor.prototype[b], "undefined")
    }, Function.prototype.bind || (Function.prototype.bind = function (b) {
        var c = this;
        if (typeof c != "function") throw new TypeError;
        var d = r.call(arguments, 1),
            e = function () {
                if (this instanceof e) {
                    var a = function () {};
                    a.prototype = c.prototype;
                    var f = new a,
                        g = c.apply(f, d.concat(r.call(arguments)));
                    return Object(g) === g ? g : f
                }
                return c.apply(b, d.concat(r.call(arguments)))
            };
        return e
    });
    var C = function (c, d) {
            var f = c.join(""),
                g = d.length;
            t(f, function (c, d) {
                var f = b.styleSheets[b.styleSheets.length - 1],
                    h = f ? f.cssRules && f.cssRules[0] ? f.cssRules[0].cssText : f.cssText || "" : "",
                    i = c.childNodes,
                    j = {};
                while (g--) j[i[g].id] = i[g];
                e.touch = "ontouchstart" in a || a.DocumentTouch && b instanceof DocumentTouch || (j.touch && j.touch.offsetTop) === 9
            }, g, d)
        }([, ["@media (", m.join("touch-enabled),("), h, ")", "{#touch{top:9px;position:absolute}}"].join("")], [, "touch"]);
    n.touch = function () {
        return e.touch
    };
    for (var D in n) w(n, D) && (s = D.toLowerCase(), e[s] = n[D](), q.push((e[s] ? "" : "no-") + s));
    return x(""), i = k = null, e._version = d, e._prefixes = m, e.mq = u, e.testStyles = t, g.className = g.className.replace(/(^|\s)no-js(\s|$)/, "$1$2") + (f ? " js " + q.join(" ") : ""), e
}(this, this.document);

/**
 * hoverIntent r6 // 2011.02.26 // jQuery 1.5.1+
 * <http://cherne.net/brian/resources/jquery.hoverIntent.html>
 *
 * @param  f  onMouseOver function || An object with configuration options
 * @param  g  onMouseOut function  || Nothing (use configuration options object)
 * @author    Brian Cherne brian(at)cherne(dot)net
 */ (function ($) {
    $.fn.hoverIntent = function (f, g) {
        var cfg = {
            sensitivity: 7,
            interval: 100,
            timeout: 0
        };
        cfg = $.extend(cfg, g ? {
            over: f,
            out: g
        } : f);
        var cX, cY, pX, pY;
        var track = function (ev) {
                cX = ev.pageX;
                cY = ev.pageY
            };
        var compare = function (ev, ob) {
                ob.hoverIntent_t = clearTimeout(ob.hoverIntent_t);
                if ((Math.abs(pX - cX) + Math.abs(pY - cY)) < cfg.sensitivity) {
                    $(ob).unbind("mousemove", track);
                    ob.hoverIntent_s = 1;
                    return cfg.over.apply(ob, [ev])
                } else {
                    pX = cX;
                    pY = cY;
                    ob.hoverIntent_t = setTimeout(function () {
                        compare(ev, ob)
                    }, cfg.interval)
                }
            };
        var delay = function (ev, ob) {
                ob.hoverIntent_t = clearTimeout(ob.hoverIntent_t);
                ob.hoverIntent_s = 0;
                return cfg.out.apply(ob, [ev])
            };
        var handleHover = function (e) {
                var ev = jQuery.extend({}, e);
                var ob = this;
                if (ob.hoverIntent_t) {
                    ob.hoverIntent_t = clearTimeout(ob.hoverIntent_t)
                }
                if (e.type == "mouseenter") {
                    pX = ev.pageX;
                    pY = ev.pageY;
                    $(ob).bind("mousemove", track);
                    if (ob.hoverIntent_s != 1) {
                        ob.hoverIntent_t = setTimeout(function () {
                            compare(ev, ob)
                        }, cfg.interval)
                    }
                } else {
                    $(ob).unbind("mousemove", track);
                    if (ob.hoverIntent_s == 1) {
                        ob.hoverIntent_t = setTimeout(function () {
                            delay(ev, ob)
                        }, cfg.timeout)
                    }
                }
            };
        return this.bind('mouseenter', handleHover).bind('mouseleave', handleHover)
    }
})(jQuery);
(function (a) {
    function d() {
        a("#social ul li, .tooltip").css({
            opacity: .5
        }).hover(function () {
            a(this).stop().animate({
                opacity: .95
            })
        }, function () {
            a(this).stop().animate({
                opacity: .5
            })
        })
    }
    function c() {
        var b = a(".footer_dropup", this);
        a(b).hide()
    }
    function b() {
        var b = a(".footer_dropup", this);
        a(b).fadeIn(hoverIntentShow);
        a(this).hover(function () {
            a(b).fadeOut(hoverIntentHide)
        })
    }
    a.fn.stickyFooter = function (e) {
        var e = a.extend({
            dropup_speed_show: 300,
            dropup_speed_hide: 200,
            dropup_speed_delay: 200,
            footer_effect: "hover_fade",
            showhidefooter: "hide",
            hide_speed: 1e3,
            hide_delay: 2e3
        }, e);
        return this.each(function () {
            var f = a(this),
                g = a(f).children("li"),
                h = a(g).children(".footer_dropup");
            a(".footer_dropup").css("left", "auto").hide();
            d();
            if (e.footer_click_outside === 1) {
                stickyFooterClickOutside()
            }
            if (Modernizr.touch) {
                a(g).bind("touchstart", function () {
                    var b = a(this);
                    b.siblings().removeClass("active").end().toggleClass("active");
                    b.siblings().find(h).hide(0);
                    b.find(h).delay(e.dropup_speed_delay).show(0).click(function (a) {
                        a.stopPropagation()
                    })
                })
            } else if (e.footer_effect === "hover_fade") {
                hoverIntentEffect = e.footer_effect;
                hoverIntentShow = e.dropup_speed_show;
                hoverIntentHide = e.dropup_speed_hide;
                var i = {
                    sensitivity: 2,
                    interval: 100,
                    over: b,
                    timeout: 200,
                    out: c
                };
                a(g).hoverIntent(i)
            }
            if (e.showhidefooter == "hide") {
                a(f).stop().delay(e.hide_delay).slideToggle(e.hide_speed);
                a("#footer_trigger").toggleClass("trigger_active")
            } else if (e.showhidefooter == "show") {
                a(f).stop().hide().fadeIn(300)
            }
            a("#footer_trigger").live("click", function () {
                a(f).slideToggle(400);
                a("#footer_trigger").toggleClass("trigger_active");
                return false
            })
        })
    }
})(jQuery)