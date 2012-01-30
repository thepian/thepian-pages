// Knockout JavaScript library v1.2.1
// (c) Steven Sanderson - http://knockoutjs.com/
// License: MIT (http://www.opensource.org/licenses/mit-license.php)
(function (window, undefined) {
    function c(e) {
        throw e;
    }
    var m = void 0,
        o = null,
        p = window.ko = {};
    p.b = function (e, d) {
        for (var b = e.split("."), a = window, f = 0; f < b.length - 1; f++) a = a[b[f]];
        a[b[b.length - 1]] = d
    };
    p.i = function (e, d, b) {
        e[d] = b
    };
    p.a = new function () {
        function e(a, b) {
            if (a.tagName != "INPUT" || !a.type) return !1;
            if (b.toLowerCase() != "click") return !1;
            var d = a.type.toLowerCase();
            return d == "checkbox" || d == "radio"
        }
        var d = /^(\s|\u00A0)+|(\s|\u00A0)+$/g,
            b = /MSIE 6/i.test(navigator.userAgent),
            a = /MSIE 7/i.test(navigator.userAgent),
            f = {},
            h = {};
        f[/Firefox\/2/i.test(navigator.userAgent) ? "KeyboardEvent" : "UIEvents"] = ["keyup", "keydown", "keypress"];
        f.MouseEvents = ["click", "dblclick", "mousedown", "mouseup", "mousemove", "mouseover", "mouseout", "mouseenter", "mouseleave"];
        for (var g in f) {
            var i = f[g];
            if (i.length) for (var k = 0, j = i.length; k < j; k++) h[i[k]] = g
        }
        return {
            ca: ["authenticity_token", /^__RequestVerificationToken(_.*)?$/],
            g: function (a, b) {
                for (var d = 0, e = a.length; d < e; d++) b(a[d])
            },
            h: function (a, b) {
                if (typeof a.indexOf == "function") return a.indexOf(b);
                for (var d = 0, e = a.length; d < e; d++) if (a[d] === b) return d;
                return -1
            },
            xa: function (a, b, d) {
                for (var e = 0, f = a.length; e < f; e++) if (b.call(d, a[e])) return a[e];
                return o
            },
            N: function (a, b) {
                var d = p.a.h(a, b);
                d >= 0 && a.splice(d, 1)
            },
            L: function (a) {
                for (var a = a || [], b = [], d = 0, e = a.length; d < e; d++) p.a.h(b, a[d]) < 0 && b.push(a[d]);
                return b
            },
            M: function (a, b) {
                for (var a = a || [], d = [], e = 0, f = a.length; e < f; e++) d.push(b(a[e]));
                return d
            },
            K: function (a, b) {
                for (var a = a || [], d = [], e = 0, f = a.length; e < f; e++) b(a[e]) && d.push(a[e]);
                return d
            },
            u: function (a, b) {
                for (var d = 0, e = b.length; d < e; d++) a.push(b[d])
            },
            Q: function (a) {
                for (; a.firstChild;) p.removeNode(a.firstChild)
            },
            Xa: function (a, b) {
                p.a.Q(a);
                b && p.a.g(b, function (b) {
                    a.appendChild(b)
                })
            },
            ka: function (a, b) {
                var d = a.nodeType ? [a] : a;
                if (d.length > 0) {
                    for (var e = d[0], f = e.parentNode, h = 0, g = b.length; h < g; h++) f.insertBefore(b[h], e);
                    h = 0;
                    for (g = d.length; h < g; h++) p.removeNode(d[h])
                }
            },
            ma: function (a, b) {
                navigator.userAgent.indexOf("MSIE 6") >= 0 ? a.setAttribute("selected", b) : a.selected = b
            },
            da: function (a, b) {
                if (!a || a.nodeType != 1) return [];
                var d = [];
                a.getAttribute(b) !== o && d.push(a);
                for (var e = a.getElementsByTagName("*"), f = 0, h = e.length; f < h; f++) e[f].getAttribute(b) !== o && d.push(e[f]);
                return d
            },
            k: function (a) {
                return (a || "").replace(d, "")
            },
            ab: function (a, b) {
                for (var d = [], e = (a || "").split(b), f = 0, h = e.length; f < h; f++) {
                    var g = p.a.k(e[f]);
                    g !== "" && d.push(g)
                }
                return d
            },
            Za: function (a, b) {
                a = a || "";
                if (b.length > a.length) return !1;
                return a.substring(0, b.length) === b
            },
            Ha: function (a, b) {
                if (b === m) return (new Function("return " + a))();
                return (new Function("sc", "with(sc) { return (" + a + ") }"))(b)
            },
            Fa: function (a, b) {
                if (b.compareDocumentPosition) return (b.compareDocumentPosition(a) & 16) == 16;
                for (; a != o;) {
                    if (a == b) return !0;
                    a = a.parentNode
                }
                return !1
            },
            P: function (a) {
                return p.a.Fa(a, document)
            },
            t: function (a, b, d) {
                if (typeof jQuery != "undefined") {
                    if (e(a, b)) var f = d,
                        d = function (a, b) {
                            var d = this.checked;
                            if (b) this.checked = b.Aa !== !0;
                            f.call(this, a);
                            this.checked = d
                        };
                    jQuery(a).bind(b, d)
                } else typeof a.addEventListener == "function" ? a.addEventListener(b, d, !1) : typeof a.attachEvent != "undefined" ? a.attachEvent("on" + b, function (b) {
                    d.call(a, b)
                }) : c(Error("Browser doesn't support addEventListener or attachEvent"))
            },
            qa: function (a, b) {
                (!a || !a.nodeType) && c(Error("element must be a DOM node when calling triggerEvent"));
                if (typeof jQuery != "undefined") {
                    var d = [];
                    e(a, b) && d.push({
                        Aa: a.checked
                    });
                    jQuery(a).trigger(b, d)
                } else if (typeof document.createEvent == "function") typeof a.dispatchEvent == "function" ? (d = document.createEvent(h[b] || "HTMLEvents"), d.initEvent(b, !0, !0, window, 0, 0, 0, 0, 0, !1, !1, !1, !1, 0, a), a.dispatchEvent(d)) : c(Error("The supplied element doesn't support dispatchEvent"));
                else if (typeof a.fireEvent != "undefined") {
                    if (b == "click" && a.tagName == "INPUT" && (a.type.toLowerCase() == "checkbox" || a.type.toLowerCase() == "radio")) a.checked = a.checked !== !0;
                    a.fireEvent("on" + b)
                } else c(Error("Browser doesn't support triggering events"))
            },
            d: function (a) {
                return p.C(a) ? a() : a
            },
            Ea: function (a, b) {
                return p.a.h((a.className || "").split(/\s+/), b) >= 0
            },
            pa: function (a, b, d) {
                var e = p.a.Ea(a, b);
                if (d && !e) a.className = (a.className || "") + " " + b;
                else if (e && !d) {
                    for (var d = (a.className || "").split(/\s+/), e = "", f = 0; f < d.length; f++) d[f] != b && (e += d[f] + " ");
                    a.className = p.a.k(e)
                }
            },
            Ua: function (a, b) {
                for (var a = p.a.d(a), b = p.a.d(b), d = [], e = a; e <= b; e++) d.push(e);
                return d
            },
            U: function (a) {
                for (var b = [], d = 0, e = a.length; d < e; d++) b.push(a[d]);
                return b
            },
            S: b,
            Ma: a,
            ea: function (a, b) {
                for (var d = p.a.U(a.getElementsByTagName("INPUT")).concat(p.a.U(a.getElementsByTagName("TEXTAREA"))), e = typeof b == "string" ?
                function (a) {
                    return a.name === b
                } : function (a) {
                    return b.test(a.name)
                }, f = [], h = d.length - 1; h >= 0; h--) e(d[h]) && f.push(d[h]);
                return f
            },
            F: function (a) {
                if (typeof a == "string" && (a = p.a.k(a))) {
                    if (window.JSON && window.JSON.parse) return window.JSON.parse(a);
                    return (new Function("return " + a))()
                }
                return o
            },
            Y: function (a) {
                (typeof JSON == "undefined" || typeof JSON.stringify == "undefined") && c(Error("Cannot find JSON.stringify(). Some browsers (e.g., IE < 8) don't support it natively, but you can overcome this by adding a script reference to json2.js, downloadable from http://www.json.org/json2.js"));
                return JSON.stringify(p.a.d(a))
            },
            Ta: function (a, b, d) {
                var d = d || {},
                    e = d.params || {},
                    f = d.includeFields || this.ca,
                    h = a;
                if (typeof a == "object" && a.tagName == "FORM") for (var h = a.action, g = f.length - 1; g >= 0; g--) for (var i = p.a.ea(a, f[g]), k = i.length - 1; k >= 0; k--) e[i[k].name] = i[k].value;
                var b = p.a.d(b),
                    j = document.createElement("FORM");
                j.style.display = "none";
                j.action = h;
                j.method = "post";
                for (var u in b) a = document.createElement("INPUT"), a.name = u, a.value = p.a.Y(p.a.d(b[u])), j.appendChild(a);
                for (u in e) a = document.createElement("INPUT"), a.name = u, a.value = e[u], j.appendChild(a);
                document.body.appendChild(j);
                d.submitter ? d.submitter(j) : j.submit();
                setTimeout(function () {
                    j.parentNode.removeChild(j)
                }, 0)
            }
        }
    };
    p.b("ko.utils", p.a);
    p.b("ko.utils.arrayForEach", p.a.g);
    p.b("ko.utils.arrayFirst", p.a.xa);
    p.b("ko.utils.arrayFilter", p.a.K);
    p.b("ko.utils.arrayGetDistinctValues", p.a.L);
    p.b("ko.utils.arrayIndexOf", p.a.h);
    p.b("ko.utils.arrayMap", p.a.M);
    p.b("ko.utils.arrayPushAll", p.a.u);
    p.b("ko.utils.arrayRemoveItem", p.a.N);
    p.b("ko.utils.fieldsIncludedWithJsonPost", p.a.ca);
    p.b("ko.utils.getElementsHavingAttribute", p.a.da);
    p.b("ko.utils.getFormFields", p.a.ea);
    p.b("ko.utils.postJson", p.a.Ta);
    p.b("ko.utils.parseJson", p.a.F);
    p.b("ko.utils.registerEventHandler", p.a.t);
    p.b("ko.utils.stringifyJson", p.a.Y);
    p.b("ko.utils.range", p.a.Ua);
    p.b("ko.utils.toggleDomNodeCssClass", p.a.pa);
    p.b("ko.utils.triggerEvent", p.a.qa);
    p.b("ko.utils.unwrapObservable", p.a.d);
    Function.prototype.bind || (Function.prototype.bind = function (e) {
        var d = this,
            b = Array.prototype.slice.call(arguments),
            e = b.shift();
        return function () {
            return d.apply(e, b.concat(Array.prototype.slice.call(arguments)))
        }
    });
    p.a.e = new function () {
        var e = 0,
            d = "__ko__" + (new Date).getTime(),
            b = {};
        return {
            get: function (a, b) {
                var d = p.a.e.getAll(a, !1);
                return d === m ? m : d[b]
            },
            set: function (a, b, d) {
                d === m && p.a.e.getAll(a, !1) === m || (p.a.e.getAll(a, !0)[b] = d)
            },
            getAll: function (a, f) {
                var h = a[d];
                if (!h) {
                    if (!f) return;
                    h = a[d] = "ko" + e++;
                    b[h] = {}
                }
                return b[h]
            },
            clear: function (a) {
                var e = a[d];
                e && (delete b[e], a[d] = o)
            }
        }
    };
    p.a.p = new function () {
        function e(a, d) {
            var e = p.a.e.get(a, b);
            e === m && d && (e = [], p.a.e.set(a, b, e));
            return e
        }
        function d(a) {
            var b = e(a, !1);
            if (b) for (var b = b.slice(0), d = 0; d < b.length; d++) b[d](a);
            p.a.e.clear(a);
            typeof jQuery == "function" && typeof jQuery.cleanData == "function" && jQuery.cleanData([a])
        }
        var b = "__ko_domNodeDisposal__" + (new Date).getTime();
        return {
            ba: function (a, b) {
                typeof b != "function" && c(Error("Callback must be a function"));
                e(a, !0).push(b)
            },
            ja: function (a, d) {
                var h = e(a, !1);
                h && (p.a.N(h, d), h.length == 0 && p.a.e.set(a, b, m))
            },
            v: function (a) {
                if (!(a.nodeType != 1 && a.nodeType != 9)) {
                    d(a);
                    var b = [];
                    p.a.u(b, a.getElementsByTagName("*"));
                    for (var a = 0, e = b.length; a < e; a++) d(b[a])
                }
            },
            removeNode: function (a) {
                p.v(a);
                a.parentNode && a.parentNode.removeChild(a)
            }
        }
    };
    p.v = p.a.p.v;
    p.removeNode = p.a.p.removeNode;
    p.b("ko.cleanNode", p.v);
    p.b("ko.removeNode", p.removeNode);
    p.b("ko.utils.domNodeDisposal", p.a.p);
    p.b("ko.utils.domNodeDisposal.addDisposeCallback", p.a.p.ba);
    p.b("ko.utils.domNodeDisposal.removeDisposeCallback", p.a.p.ja);
    p.a.Sa = function (e) {
        if (typeof jQuery != "undefined") e = jQuery.clean([e]);
        else {
            var d = p.a.k(e).toLowerCase(),
                b = document.createElement("div"),
                d = d.match(/^<(thead|tbody|tfoot)/) && [1, "<table>", "</table>"] || !d.indexOf("<tr") && [2, "<table><tbody>", "</tbody></table>"] || (!d.indexOf("<td") || !d.indexOf("<th")) && [3, "<table><tbody><tr>", "</tr></tbody></table>"] || [0, "", ""];
            for (b.innerHTML = d[1] + e + d[2]; d[0]--;) b = b.lastChild;
            e = p.a.U(b.childNodes)
        }
        return e
    };
    p.a.Ya = function (e, d) {
        p.a.Q(e);
        if (d !== o && d !== m) if (typeof d != "string" && (d = d.toString()), typeof jQuery != "undefined") jQuery(e).html(d);
        else for (var b = p.a.Sa(d), a = 0; a < b.length; a++) e.appendChild(b[a])
    };
    p.l = function () {
        function e() {
            return ((1 + Math.random()) * 4294967296 | 0).toString(16).substring(1)
        }
        function d(a, b) {
            if (a) if (a.nodeType == 8) {
                var e = p.l.ha(a.nodeValue);
                e != o && b.push({
                    Da: a,
                    Pa: e
                })
            } else if (a.nodeType == 1) for (var e = 0, g = a.childNodes, i = g.length; e < i; e++) d(g[e], b)
        }
        var b = {};
        return {
            V: function (a) {
                typeof a != "function" && c(Error("You can only pass a function to ko.memoization.memoize()"));
                var d = e() + e();
                b[d] = a;
                return "<\!--[ko_memo:" + d + "]--\>"
            },
            ra: function (a, d) {
                var e = b[a];
                e === m && c(Error("Couldn't find any memo with ID " + a + ". Perhaps it's already been unmemoized."));
                try {
                    return e.apply(o, d || []), !0
                } finally {
                    delete b[a]
                }
            },
            sa: function (a, b) {
                var e = [];
                d(a, e);
                for (var g = 0, i = e.length; g < i; g++) {
                    var k = e[g].Da,
                        j = [k];
                    b && p.a.u(j, b);
                    p.l.ra(e[g].Pa, j);
                    k.nodeValue = "";
                    k.parentNode && k.parentNode.removeChild(k)
                }
            },
            ha: function (a) {
                return (a = a.match(/^\[ko_memo\:(.*?)\]$/)) ? a[1] : o
            }
        }
    }();
    p.b("ko.memoization", p.l);
    p.b("ko.memoization.memoize", p.l.V);
    p.b("ko.memoization.unmemoize", p.l.ra);
    p.b("ko.memoization.parseMemoText", p.l.ha);
    p.b("ko.memoization.unmemoizeDomNodeAndDescendants", p.l.sa);
    p.$a = function (e, d) {
        this.za = e;
        this.n = function () {
            this.La = !0;
            d()
        }.bind(this);
        p.i(this, "dispose", this.n)
    };
    p.Z = function () {
        var e = [];
        this.$ = function (d, b) {
            var a = b ? d.bind(b) : d,
                f = new p.$a(a, function () {
                    p.a.N(e, f)
                });
            e.push(f);
            return f
        };
        this.z = function (d) {
            p.a.g(e.slice(0), function (b) {
                b && b.La !== !0 && b.za(d)
            })
        };
        this.Ja = function () {
            return e.length
        };
        p.i(this, "subscribe", this.$);
        p.i(this, "notifySubscribers", this.z);
        p.i(this, "getSubscriptionsCount", this.Ja)
    };
    p.ga = function (e) {
        return typeof e.$ == "function" && typeof e.z == "function"
    };
    p.b("ko.subscribable", p.Z);
    p.b("ko.isSubscribable", p.ga);
    p.A = function () {
        var e = [];
        return {
            ya: function () {
                e.push([])
            },
            end: function () {
                return e.pop()
            },
            ia: function (d) {
                p.ga(d) || c("Only subscribable things can act as dependencies");
                e.length > 0 && e[e.length - 1].push(d)
            }
        }
    }();
    var x = {
        undefined: !0,
        "boolean": !0,
        number: !0,
        string: !0
    };

    function y(e, d) {
        return e === o || typeof e in x ? e === d : !1
    }
    p.s = function (e) {
        function d() {
            if (arguments.length > 0) {
                if (!d.equalityComparer || !d.equalityComparer(b, arguments[0])) b = arguments[0], d.z(b);
                return this
            } else return p.A.ia(d), b
        }
        var b = e;
        d.o = p.s;
        d.H = function () {
            d.z(b)
        };
        d.equalityComparer = y;
        p.Z.call(d);
        p.i(d, "valueHasMutated", d.H);
        return d
    };
    p.C = function (e) {
        if (e === o || e === m || e.o === m) return !1;
        if (e.o === p.s) return !0;
        return p.C(e.o)
    };
    p.D = function (e) {
        if (typeof e == "function" && e.o === p.s) return !0;
        if (typeof e == "function" && e.o === p.j && e.Ka) return !0;
        return !1
    };
    p.b("ko.observable", p.s);
    p.b("ko.isObservable", p.C);
    p.b("ko.isWriteableObservable", p.D);
    p.Ra = function (e) {
        arguments.length == 0 && (e = []);
        e !== o && e !== m && !("length" in e) && c(Error("The argument passed when initializing an observable array must be an array, or null, or undefined."));
        var d = new p.s(e);
        p.a.g(["pop", "push", "reverse", "shift", "sort", "splice", "unshift"], function (b) {
            d[b] = function () {
                var a = d(),
                    a = a[b].apply(a, arguments);
                d.H();
                return a
            }
        });
        p.a.g(["slice"], function (b) {
            d[b] = function () {
                var a = d();
                return a[b].apply(a, arguments)
            }
        });
        d.remove = function (b) {
            for (var a = d(), e = [], h = [], g = typeof b == "function" ? b : function (a) {
                    return a === b
                }, i = 0, k = a.length; i < k; i++) {
                var j = a[i];
                g(j) ? h.push(j) : e.push(j)
            }
            d(e);
            return h
        };
        d.Va = function (b) {
            if (b === m) {
                var a = d();
                d([]);
                return a
            }
            if (!b) return [];
            return d.remove(function (a) {
                return p.a.h(b, a) >= 0
            })
        };
        d.O = function (b) {
            for (var a = d(), e = typeof b == "function" ? b : function (a) {
                    return a === b
                }, h = a.length - 1; h >= 0; h--) e(a[h]) && (a[h]._destroy = !0);
            d.H()
        };
        d.Ca = function (b) {
            if (b === m) return d.O(function () {
                return !0
            });
            if (!b) return [];
            return d.O(function (a) {
                return p.a.h(b, a) >= 0
            })
        };
        d.indexOf = function (b) {
            var a = d();
            return p.a.h(a, b)
        };
        d.replace = function (b, a) {
            var e = d.indexOf(b);
            e >= 0 && (d()[e] = a, d.H())
        };
        p.i(d, "remove", d.remove);
        p.i(d, "removeAll", d.Va);
        p.i(d, "destroy", d.O);
        p.i(d, "destroyAll", d.Ca);
        p.i(d, "indexOf", d.indexOf);
        return d
    };
    p.b("ko.observableArray", p.Ra);
    p.j = function (e, d, b) {
        function a() {
            p.a.g(n, function (a) {
                a.n()
            });
            n = []
        }
        function f(b) {
            a();
            p.a.g(b, function (a) {
                n.push(a.$(h))
            })
        }
        function h() {
            if (k && typeof b.disposeWhen == "function" && b.disposeWhen()) g.n();
            else {
                try {
                    p.A.ya(), i = b.owner ? b.read.call(b.owner) : b.read()
                } finally {
                    var a = p.a.L(p.A.end());
                    f(a)
                }
                g.z(i);
                k = !0
            }
        }
        function g() {
            if (arguments.length > 0) if (typeof b.write === "function") {
                var a = arguments[0];
                b.owner ? b.write.call(b.owner, a) : b.write(a)
            } else c("Cannot write a value to a dependentObservable unless you specify a 'write' option. If you wish to read the current value, don't pass any parameters.");
            else return k || h(), p.A.ia(g), i
        }
        var i, k = !1;
        e && typeof e == "object" ? b = e : (b = b || {}, b.read = e || b.read, b.owner = d || b.owner);
        typeof b.read != "function" && c("Pass a function that returns the value of the dependentObservable");
        var j = typeof b.disposeWhenNodeIsRemoved == "object" ? b.disposeWhenNodeIsRemoved : o,
            l = o;
        if (j) {
            l = function () {
                g.n()
            };
            p.a.p.ba(j, l);
            var q = b.disposeWhen;
            b.disposeWhen = function () {
                return !p.a.P(j) || typeof q == "function" && q()
            }
        }
        var n = [];
        g.o = p.j;
        g.Ia = function () {
            return n.length
        };
        g.Ka = typeof b.write === "function";
        g.n = function () {
            j && p.a.p.ja(j, l);
            a()
        };
        p.Z.call(g);
        b.deferEvaluation !== !0 && h();
        p.i(g, "dispose", g.n);
        p.i(g, "getDependenciesCount", g.Ia);
        return g
    };
    p.j.o = p.s;
    p.b("ko.dependentObservable", p.j);
    (function () {
        function e(a, f, h) {
            h = h || new b;
            a = f(a);
            if (!(typeof a == "object" && a !== o && a !== m)) return a;
            var g = a instanceof Array ? [] : {};
            h.save(a, g);
            d(a, function (b) {
                var d = f(a[b]);
                switch (typeof d) {
                case "boolean":
                case "number":
                case "string":
                case "function":
                    g[b] = d;
                    break;
                case "object":
                case "undefined":
                    var j = h.get(d);
                    g[b] = j !== m ? j : e(d, f, h)
                }
            });
            return g
        }
        function d(a, b) {
            if (a instanceof Array) for (var d = 0; d < a.length; d++) b(d);
            else for (d in a) b(d)
        }
        function b() {
            var a = [],
                b = [];
            this.save = function (d, e) {
                var i = p.a.h(a, d);
                i >= 0 ? b[i] = e : (a.push(d), b.push(e))
            };
            this.get = function (d) {
                d = p.a.h(a, d);
                return d >= 0 ? b[d] : m
            }
        }
        p.oa = function (a) {
            arguments.length == 0 && c(Error("When calling ko.toJS, pass the object you want to convert."));
            return e(a, function (a) {
                for (var b = 0; p.C(a) && b < 10; b++) a = a();
                return a
            })
        };
        p.toJSON = function (a) {
            a = p.oa(a);
            return p.a.Y(a)
        }
    })();
    p.b("ko.toJS", p.oa);
    p.b("ko.toJSON", p.toJSON);
    p.f = {
        m: function (e) {
            if (e.tagName == "OPTION") {
                if (e.__ko__hasDomDataOptionValue__ === !0) return p.a.e.get(e, p.c.options.W);
                return e.getAttribute("value")
            } else return e.tagName == "SELECT" ? e.selectedIndex >= 0 ? p.f.m(e.options[e.selectedIndex]) : m : e.value
        },
        I: function (e, d) {
            if (e.tagName == "OPTION") switch (typeof d) {
            case "string":
            case "number":
                p.a.e.set(e, p.c.options.W, m);
                "__ko__hasDomDataOptionValue__" in e && delete e.__ko__hasDomDataOptionValue__;
                e.value = d;
                break;
            default:
                p.a.e.set(e, p.c.options.W, d), e.__ko__hasDomDataOptionValue__ = !0, e.value = ""
            } else if (e.tagName == "SELECT") for (var b = e.options.length - 1; b >= 0; b--) {
                if (p.f.m(e.options[b]) == d) {
                    e.selectedIndex = b;
                    break
                }
            } else {
                if (d === o || d === m) d = "";
                e.value = d
            }
        }
    };
    p.b("ko.selectExtensions", p.f);
    p.b("ko.selectExtensions.readValue", p.f.m);
    p.b("ko.selectExtensions.writeValue", p.f.I);
    p.r = function () {
        function e(a, b) {
            return a.replace(d, function (a, d) {
                return b[d]
            })
        }
        var d = /\[ko_token_(\d+)\]/g,
            b = /^[\_$a-z][\_$a-z0-9]*(\[.*?\])*(\.[\_$a-z][\_$a-z0-9]*(\[.*?\])*)*$/i,
            a = ["true", "false"];
        return {
            F: function (a) {
                a = p.a.k(a);
                if (a.length < 3) return {};
                for (var b = [], d = o, i, k = a.charAt(0) == "{" ? 1 : 0; k < a.length; k++) {
                    var j = a.charAt(k);
                    if (d === o) switch (j) {
                    case '"':
                    case "'":
                    case "/":
                        d = k;
                        i = j;
                        break;
                    case "{":
                        d = k;
                        i = "}";
                        break;
                    case "[":
                        d = k, i = "]"
                    } else if (j == i) {
                        j = a.substring(d, k + 1);
                        b.push(j);
                        var l = "[ko_token_" + (b.length - 1) + "]",
                            a = a.substring(0, d) + l + a.substring(k + 1);
                        k -= j.length - l.length;
                        d = o
                    }
                }
                d = {};
                a = a.split(",");
                i = 0;
                for (k = a.length; i < k; i++) {
                    var l = a[i],
                        q = l.indexOf(":");
                    q > 0 && q < l.length - 1 && (j = p.a.k(l.substring(0, q)), l = p.a.k(l.substring(q + 1)), j.charAt(0) == "{" && (j = j.substring(1)), l.charAt(l.length - 1) == "}" && (l = l.substring(0, l.length - 1)), j = p.a.k(e(j, b)), l = p.a.k(e(l, b)), d[j] = l)
                }
                return d
            },
            R: function (d) {
                var e = p.r.F(d),
                    g = [],
                    i;
                for (i in e) {
                    var k = e[i],
                        j;
                    j = k;
                    j = p.a.h(a, p.a.k(j).toLowerCase()) >= 0 ? !1 : j.match(b) !== o;
                    j && (g.length > 0 && g.push(", "), g.push(i + " : function(__ko_value) { " + k + " = __ko_value; }"))
                }
                g.length > 0 && (d = d + ", '_ko_property_writers' : { " + g.join("") + " } ");
                return d
            }
        }
    }();
    p.b("ko.jsonExpressionRewriting", p.r);
    p.b("ko.jsonExpressionRewriting.parseJson", p.r.F);
    p.b("ko.jsonExpressionRewriting.insertPropertyAccessorsIntoJson", p.r.R);
    p.c = {};
    p.J = function (e, d, b, a) {
        function f(a) {
            return function () {
                return i[a]
            }
        }
        function h() {
            return i
        }
        var g = !0,
            a = a || "data-bind",
            i;
        new p.j(function () {
            var k;
            if (!(k = typeof d == "function" ? d() : d)) {
                var j = e.getAttribute(a);
                try {
                    var l = " { " + p.r.R(j) + " } ";
                    k = p.a.Ha(l, b === o ? window : b)
                } catch (q) {
                    c(Error("Unable to parse binding attribute.\nMessage: " + q + ";\nAttribute value: " + j))
                }
            }
            i = k;
            if (g) for (var n in i) p.c[n] && typeof p.c[n].init == "function" && (0, p.c[n].init)(e, f(n), h, b);
            for (n in i) p.c[n] && typeof p.c[n].update == "function" && (0, p.c[n].update)(e, f(n), h, b)
        }, o, {
            disposeWhenNodeIsRemoved: e
        });
        g = !1
    };
    p.ua = function (e, d) {
        d && d.nodeType == m && c(Error("ko.applyBindings: first parameter should be your view model; second parameter should be a DOM node (note: this is a breaking change since KO version 1.05)"));
        var d = d || window.document.body,
            b = p.a.da(d, "data-bind");
        p.a.g(b, function (a) {
            p.J(a, o, e)
        })
    };
    p.b("ko.bindingHandlers", p.c);
    p.b("ko.applyBindings", p.ua);
    p.b("ko.applyBindingsToNode", p.J);
    p.a.g(["click"], function (e) {
        p.c[e] = {
            init: function (d, b, a, f) {
                return p.c.event.init.call(this, d, function () {
                    var a = {};
                    a[e] = b();
                    return a
                }, a, f)
            }
        }
    });
    p.c.event = {
        init: function (e, d, b, a) {
            var f = d() || {},
                h;
            for (h in f)(function () {
                var f = h;
                typeof f == "string" && p.a.t(e, f, function (e) {
                    var h, j = d()[f];
                    if (j) {
                        var l = b();
                        try {
                            h = j.apply(a, arguments)
                        } finally {
                            if (h !== !0) e.preventDefault ? e.preventDefault() : e.returnValue = !1
                        }
                        if (l[f + "Bubble"] === !1) e.cancelBubble = !0, e.stopPropagation && e.stopPropagation()
                    }
                })
            })()
        }
    };
    p.c.submit = {
        init: function (e, d, b, a) {
            typeof d() != "function" && c(Error("The value for a submit binding must be a function to invoke on submit"));
            p.a.t(e, "submit", function (b) {
                var h, g = d();
                try {
                    h = g.call(a, e)
                } finally {
                    if (h !== !0) b.preventDefault ? b.preventDefault() : b.returnValue = !1
                }
            })
        }
    };
    p.c.visible = {
        update: function (e, d) {
            var b = p.a.d(d()),
                a = e.style.display != "none";
            if (b && !a) e.style.display = "";
            else if (!b && a) e.style.display = "none"
        }
    };
    p.c.enable = {
        update: function (e, d) {
            var b = p.a.d(d());
            if (b && e.disabled) e.removeAttribute("disabled");
            else if (!b && !e.disabled) e.disabled = !0
        }
    };
    p.c.disable = {
        update: function (e, d) {
            p.c.enable.update(e, function () {
                return !p.a.d(d())
            })
        }
    };
    p.c.value = {
        init: function (e, d, b) {
            var a = ["change"],
                f = b().valueUpdate;
            f && (typeof f == "string" && (f = [f]), p.a.u(a, f), a = p.a.L(a));
            p.a.g(a, function (a) {
                var f = !1;
                p.a.Za(a, "after") && (f = !0, a = a.substring(5));
                var i = f ?
                function (a) {
                    setTimeout(a, 0)
                } : function (a) {
                    a()
                };
                p.a.t(e, a, function () {
                    i(function () {
                        var a = d(),
                            f = p.f.m(e);
                        p.D(a) ? a(f) : (a = b(), a._ko_property_writers && a._ko_property_writers.value && a._ko_property_writers.value(f))
                    })
                })
            })
        },
        update: function (e, d) {
            var b = p.a.d(d()),
                a = p.f.m(e),
                f = b != a;
            b === 0 && a !== 0 && a !== "0" && (f = !0);
            f && (a = function () {
                p.f.I(e, b)
            }, a(), e.tagName == "SELECT" && setTimeout(a, 0));
            e.tagName == "SELECT" && (a = p.f.m(e), a !== b && p.a.qa(e, "change"))
        }
    };
    p.c.options = {
        update: function (e, d, b) {
            e.tagName != "SELECT" && c(Error("options binding applies only to SELECT elements"));
            var a = p.a.M(p.a.K(e.childNodes, function (a) {
                return a.tagName && a.tagName == "OPTION" && a.selected
            }), function (a) {
                return p.f.m(a) || a.innerText || a.textContent
            }),
                f = e.scrollTop,
                h = p.a.d(d());
            p.a.Q(e);
            if (h) {
                var g = b();
                typeof h.length != "number" && (h = [h]);
                if (g.optionsCaption) {
                    var i = document.createElement("OPTION");
                    i.innerHTML = g.optionsCaption;
                    p.f.I(i, m);
                    e.appendChild(i)
                }
                b = 0;
                for (d = h.length; b < d; b++) {
                    var i = document.createElement("OPTION"),
                        k = typeof g.optionsValue == "string" ? h[b][g.optionsValue] : h[b],
                        k = p.a.d(k);
                    p.f.I(i, k);
                    var j = g.optionsText;
                    optionText = typeof j == "function" ? j(h[b]) : typeof j == "string" ? h[b][j] : k;
                    if (optionText === o || optionText === m) optionText = "";
                    optionText = p.a.d(optionText).toString();
                    typeof i.innerText == "string" ? i.innerText = optionText : i.textContent = optionText;
                    e.appendChild(i)
                }
                h = e.getElementsByTagName("OPTION");
                b = g = 0;
                for (d = h.length; b < d; b++) p.a.h(a, p.f.m(h[b])) >= 0 && (p.a.ma(h[b], !0), g++);
                if (f) e.scrollTop = f
            }
        }
    };
    p.c.options.W = "__ko.bindingHandlers.options.optionValueDomData__";
    p.c.selectedOptions = {
        fa: function (e) {
            for (var d = [], e = e.childNodes, b = 0, a = e.length; b < a; b++) {
                var f = e[b];
                f.tagName == "OPTION" && f.selected && d.push(p.f.m(f))
            }
            return d
        },
        init: function (e, d, b) {
            p.a.t(e, "change", function () {
                var a = d();
                p.D(a) ? a(p.c.selectedOptions.fa(this)) : (a = b(), a._ko_property_writers && a._ko_property_writers.value && a._ko_property_writers.value(p.c.selectedOptions.fa(this)))
            })
        },
        update: function (e, d) {
            e.tagName != "SELECT" && c(Error("values binding applies only to SELECT elements"));
            var b = p.a.d(d());
            if (b && typeof b.length == "number") for (var a = e.childNodes, f = 0, h = a.length; f < h; f++) {
                var g = a[f];
                g.tagName == "OPTION" && p.a.ma(g, p.a.h(b, p.f.m(g)) >= 0)
            }
        }
    };
    p.c.text = {
        update: function (e, d) {
            var b = p.a.d(d());
            if (b === o || b === m) b = "";
            typeof e.innerText == "string" ? e.innerText = b : e.textContent = b
        }
    };
    p.c.html = {
        update: function (e, d) {
            var b = p.a.d(d());
            p.a.Ya(e, b)
        }
    };
    p.c.css = {
        update: function (e, d) {
            var b = p.a.d(d() || {}),
                a;
            for (a in b) if (typeof a == "string") {
                var f = p.a.d(b[a]);
                p.a.pa(e, a, f)
            }
        }
    };
    p.c.style = {
        update: function (e, d) {
            var b = p.a.d(d() || {}),
                a;
            for (a in b) if (typeof a == "string") {
                var f = p.a.d(b[a]);
                e.style[a] = f || ""
            }
        }
    };
    p.c.uniqueName = {
        init: function (e, d) {
            if (d()) e.name = "ko_unique_" + ++p.c.uniqueName.Ba, p.a.S && e.mergeAttributes(document.createElement("<input name='" + e.name + "'/>"), !1)
        }
    };
    p.c.uniqueName.Ba = 0;
    p.c.checked = {
        init: function (e, d, b) {
            p.a.t(e, "click", function () {
                var a;
                if (e.type == "checkbox") a = e.checked;
                else if (e.type == "radio" && e.checked) a = e.value;
                else return;
                var f = d();
                e.type == "checkbox" && p.a.d(f) instanceof Array ? (a = p.a.h(p.a.d(f), e.value), e.checked && a < 0 ? f.push(e.value) : !e.checked && a >= 0 && f.splice(a, 1)) : p.D(f) ? f() !== a && f(a) : (f = b(), f._ko_property_writers && f._ko_property_writers.checked && f._ko_property_writers.checked(a))
            });
            e.type == "radio" && !e.name && p.c.uniqueName.init(e, function () {
                return !0
            })
        },
        update: function (e, d) {
            var b = p.a.d(d());
            if (e.type == "checkbox") e.checked = b instanceof Array ? p.a.h(b, e.value) >= 0 : b, b && p.a.S && e.mergeAttributes(document.createElement("<input type='checkbox' checked='checked' />"), !1);
            else if (e.type == "radio") e.checked = e.value == b, e.value == b && (p.a.S || p.a.Ma) && e.mergeAttributes(document.createElement("<input type='radio' checked='checked' />"), !1)
        }
    };
    p.c.attr = {
        update: function (e, d) {
            var b = p.a.d(d()) || {},
                a;
            for (a in b) if (typeof a == "string") {
                var f = p.a.d(b[a]);
                f === !1 || f === o || f === m ? e.removeAttribute(a) : e.setAttribute(a, f.toString())
            }
        }
    };
    p.aa = function () {
        this.renderTemplate = function () {
            c("Override renderTemplate in your ko.templateEngine subclass")
        };
        this.isTemplateRewritten = function () {
            c("Override isTemplateRewritten in your ko.templateEngine subclass")
        };
        this.rewriteTemplate = function () {
            c("Override rewriteTemplate in your ko.templateEngine subclass")
        };
        this.createJavaScriptEvaluatorBlock = function () {
            c("Override createJavaScriptEvaluatorBlock in your ko.templateEngine subclass")
        }
    };
    p.b("ko.templateEngine", p.aa);
    p.G = function () {
        var e = /(<[a-z]+\d*(\s+(?!data-bind=)[a-z0-9\-]+(=(\"[^\"]*\"|\'[^\']*\'))?)*\s+)data-bind=(["'])([\s\S]*?)\5/gi;
        return {
            Ga: function (d, b) {
                b.isTemplateRewritten(d) || b.rewriteTemplate(d, function (a) {
                    return p.G.Qa(a, b)
                })
            },
            Qa: function (d, b) {
                return d.replace(e, function (a, d, e, g, i, k, j) {
                    a = p.r.R(j);
                    return b.createJavaScriptEvaluatorBlock("ko.templateRewriting.applyMemoizedBindingsToNextSibling(function() {                     return (function() { return { " + a + " } })()                 })") + d
                })
            },
            va: function (d) {
                return p.l.V(function (b, a) {
                    b.nextSibling && p.J(b.nextSibling, d, a)
                })
            }
        }
    }();
    p.b("ko.templateRewriting", p.G);
    p.b("ko.templateRewriting.applyMemoizedBindingsToNextSibling", p.G.va);
    (function () {
        function e(b, a, e, h, g) {
            var i = p.a.d(h),
                g = g || {},
                k = g.templateEngine || d;
            p.G.Ga(e, k);
            e = k.renderTemplate(e, i, g);
            (typeof e.length != "number" || e.length > 0 && typeof e[0].nodeType != "number") && c("Template engine must return an array of DOM nodes");
            e && p.a.g(e, function (a) {
                p.l.sa(a, [h])
            });
            switch (a) {
            case "replaceChildren":
                p.a.Xa(b, e);
                break;
            case "replaceNode":
                p.a.ka(b, e);
                break;
            case "ignoreTargetNode":
                break;
            default:
                c(Error("Unknown renderMode: " + a))
            }
            g.afterRender && g.afterRender(e, h);
            return e
        }
        var d;
        p.na = function (b) {
            b != m && !(b instanceof p.aa) && c("templateEngine must inherit from ko.templateEngine");
            d = b
        };
        p.X = function (b, a, f, h, g) {
            f = f || {};
            (f.templateEngine || d) == m && c("Set a template engine before calling renderTemplate");
            g = g || "replaceChildren";
            if (h) {
                var i = h.nodeType ? h : h.length > 0 ? h[0] : o;
                return new p.j(function () {
                    var d = typeof b == "function" ? b(a) : b,
                        d = e(h, g, d, a, f);
                    g == "replaceNode" && (h = d, i = h.nodeType ? h : h.length > 0 ? h[0] : o)
                }, o, {
                    disposeWhen: function () {
                        return !i || !p.a.P(i)
                    },
                    disposeWhenNodeIsRemoved: i && g == "replaceNode" ? i.parentNode : i
                })
            } else return p.l.V(function (d) {
                p.X(b, a, f, d, "replaceNode")
            })
        };
        p.Wa = function (b, a, d, h) {
            return new p.j(function () {
                var g = p.a.d(a) || [];
                typeof g.length == "undefined" && (g = [g]);
                g = p.a.K(g, function (a) {
                    return d.includeDestroyed || !a._destroy
                });
                p.a.la(h, g, function (a) {
                    var g = typeof b == "function" ? b(a) : b;
                    return e(o, "ignoreTargetNode", g, a, d)
                }, d)
            }, o, {
                disposeWhenNodeIsRemoved: h
            })
        };
        p.c.template = {
            update: function (b, a, d, e) {
                a = p.a.d(a());
                d = typeof a == "string" ? a : a.name;
                if (typeof a.foreach != "undefined") e = p.Wa(d, a.foreach || [], {
                    templateOptions: a.templateOptions,
                    afterAdd: a.afterAdd,
                    beforeRemove: a.beforeRemove,
                    includeDestroyed: a.includeDestroyed,
                    afterRender: a.afterRender
                }, b);
                else var g = a.data,
                    e = p.X(d, typeof g == "undefined" ? e : g, {
                        templateOptions: a.templateOptions,
                        afterRender: a.afterRender
                    }, b);
                (a = p.a.e.get(b, "__ko__templateSubscriptionDomDataKey__")) && typeof a.n == "function" && a.n();
                p.a.e.set(b, "__ko__templateSubscriptionDomDataKey__", e)
            }
        }
    })();
    p.b("ko.setTemplateEngine", p.na);
    p.b("ko.renderTemplate", p.X);
    p.a.w = function (e, d, b) {
        if (b === m) return p.a.w(e, d, 1) || p.a.w(e, d, 10) || p.a.w(e, d, Number.MAX_VALUE);
        else {
            for (var e = e || [], d = d || [], a = e, f = d, h = [], g = 0; g <= f.length; g++) h[g] = [];
            for (var g = 0, i = Math.min(a.length, b); g <= i; g++) h[0][g] = g;
            g = 1;
            for (i = Math.min(f.length, b); g <= i; g++) h[g][0] = g;
            for (var i = a.length, k, j = f.length, g = 1; g <= i; g++) {
                var l = Math.min(j, g + b);
                for (k = Math.max(1, g - b); k <= l; k++) h[k][g] = a[g - 1] === f[k - 1] ? h[k - 1][g - 1] : Math.min(h[k - 1][g] === m ? Number.MAX_VALUE : h[k - 1][g] + 1, h[k][g - 1] === m ? Number.MAX_VALUE : h[k][g - 1] + 1)
            }
            b = e.length;
            a = d.length;
            f = [];
            g = h[a][b];
            if (g === m) h = o;
            else {
                for (; b > 0 || a > 0;) {
                    i = h[a][b];
                    k = a > 0 ? h[a - 1][b] : g + 1;
                    j = b > 0 ? h[a][b - 1] : g + 1;
                    l = a > 0 && b > 0 ? h[a - 1][b - 1] : g + 1;
                    if (k === m || k < i - 1) k = g + 1;
                    if (j === m || j < i - 1) j = g + 1;
                    l < i - 1 && (l = g + 1);
                    k <= j && k < l ? (f.push({
                        status: "added",
                        value: d[a - 1]
                    }), a--) : (j < k && j < l ? f.push({
                        status: "deleted",
                        value: e[b - 1]
                    }) : (f.push({
                        status: "retained",
                        value: e[b - 1]
                    }), a--), b--)
                }
                h = f.reverse()
            }
            return h
        }
    };
    p.b("ko.utils.compareArrays", p.a.w);
    (function () {
        function e(d, b, a) {
            var e = [],
                d = p.j(function () {
                    var d = b(a) || [];
                    e.length > 0 && p.a.ka(e, d);
                    e.splice(0, e.length);
                    p.a.u(e, d)
                }, o, {
                    disposeWhenNodeIsRemoved: d,
                    disposeWhen: function () {
                        return e.length == 0 || !p.a.P(e[0])
                    }
                });
            return {
                Oa: e,
                j: d
            }
        }
        p.a.la = function (d, b, a, f) {
            for (var b = b || [], f = f || {}, h = p.a.e.get(d, "setDomNodeChildrenFromArrayMapping_lastMappingResult") === m, g = p.a.e.get(d, "setDomNodeChildrenFromArrayMapping_lastMappingResult") || [], i = p.a.M(g, function (a) {
                return a.wa
            }), k = p.a.w(i, b), b = [], j = 0, l = [], i = [], q = o, n = 0, v = k.length; n < v; n++) switch (k[n].status) {
            case "retained":
                var r = g[j];
                b.push(r);
                r.B.length > 0 && (q = r.B[r.B.length - 1]);
                j++;
                break;
            case "deleted":
                g[j].j.n();
                p.a.g(g[j].B, function (a) {
                    l.push({
                        element: a,
                        index: n,
                        value: k[n].value
                    });
                    q = a
                });
                j++;
                break;
            case "added":
                var s = e(d, a, k[n].value),
                    r = s.Oa;
                b.push({
                    wa: k[n].value,
                    B: r,
                    j: s.j
                });
                for (var s = 0, w = r.length; s < w; s++) {
                    var t = r[s];
                    i.push({
                        element: t,
                        index: n,
                        value: k[n].value
                    });
                    q == o ? d.firstChild ? d.insertBefore(t, d.firstChild) : d.appendChild(t) : q.nextSibling ? d.insertBefore(t, q.nextSibling) : d.appendChild(t);
                    q = t
                }
            }
            p.a.g(l, function (a) {
                p.v(a.element)
            });
            a = !1;
            if (!h) {
                if (f.afterAdd) for (n = 0; n < i.length; n++) f.afterAdd(i[n].element, i[n].index, i[n].value);
                if (f.beforeRemove) {
                    for (n = 0; n < l.length; n++) f.beforeRemove(l[n].element, l[n].index, l[n].value);
                    a = !0
                }
            }
            a || p.a.g(l, function (a) {
                a.element.parentNode && a.element.parentNode.removeChild(a.element)
            });
            p.a.e.set(d, "setDomNodeChildrenFromArrayMapping_lastMappingResult", b)
        }
    })();
    p.b("ko.utils.setDomNodeChildrenFromArrayMapping", p.a.la);
    p.T = function () {
        this.q = function () {
            if (typeof jQuery == "undefined" || !jQuery.tmpl) return 0;
            if (jQuery.tmpl.tag) {
                if (jQuery.tmpl.tag.tmpl && jQuery.tmpl.tag.tmpl.open && jQuery.tmpl.tag.tmpl.open.toString().indexOf("__") >= 0) return 3;
                return 2
            }
            return 1
        }();
        this.getTemplateNode = function (d) {
            var b = caplin.services.HTMLResourceService.getHTMLTemplate(d);
            b == o && c(Error("Cannot find template with ID=" + d));
            return b
        };
        var e = RegExp("__ko_apos__", "g");
        this.renderTemplate = function (d, b, a) {
            a = a || {};
            this.q == 0 && c(Error("jquery.tmpl not detected.\nTo use KO's default template engine, reference jQuery and jquery.tmpl. See Knockout installation documentation for more details."));
            if (this.q == 1) return d = '<script type="text/html">' + this.getTemplateNode(d).text + "<\/script>", b = jQuery.tmpl(d, b)[0].text.replace(e, "'"), jQuery.clean([b], document);
            if (!(d in jQuery.template)) {
                var f = this.getTemplateNode(d).text;
                jQuery.template(d, f)
            }
            b = [b];
            b = jQuery.tmpl(d, b, a.templateOptions);
            b.appendTo(document.createElement("div"));
            jQuery.fragments = {};
            return b
        };
        this.isTemplateRewritten = function (d) {
            if (d in jQuery.template) return !0;
            return this.getTemplateNode(d).Na === !0
        };
        this.rewriteTemplate = function (d, b) {
            var a = this.getTemplateNode(d),
                e = b(a.text);
            this.q == 1 && (e = p.a.k(e), e = e.replace(/([\s\S]*?)(\${[\s\S]*?}|{{[\=a-z][\s\S]*?}}|$)/g, function (a, b, d) {
                return b.replace(/\'/g, "__ko_apos__") + d
            }));
            a.text = e;
            a.Na = !0
        };
        this.createJavaScriptEvaluatorBlock = function (d) {
            if (this.q == 1) return "{{= " + d + "}}";
            return "{{ko_code ((function() { return " + d + " })()) }}"
        };
        this.ta = function (d, b) {
            document.write("<script type='text/html' id='" + d + "'>" + b + "<\/script>")
        };
        p.i(this, "addTemplate", this.ta);
        this.q > 1 && (jQuery.tmpl.tag.ko_code = {
            open: (this.q < 3 ? "_" : "__") + ".push($1 || '');"
        })
    };
    p.T.prototype = new p.aa;
    p.na(new p.T);
    p.b("ko.jqueryTmplTemplateEngine", p.T);
})(window);