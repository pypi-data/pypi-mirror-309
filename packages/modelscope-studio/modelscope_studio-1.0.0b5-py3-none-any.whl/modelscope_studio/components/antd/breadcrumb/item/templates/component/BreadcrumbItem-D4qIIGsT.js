import { g as Fe, b as Ne } from "./Index-DuycbnPt.js";
const x = window.ms_globals.React, Ke = window.ms_globals.React.forwardRef, Le = window.ms_globals.React.useRef, Ae = window.ms_globals.React.useState, Me = window.ms_globals.React.useEffect, qe = window.ms_globals.ReactDOM.createPortal;
function Be(e) {
  return e === void 0;
}
function k() {
}
function Te(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ze(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return k;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function w(e) {
  let t;
  return ze(e, (n) => t = n)(), t;
}
const I = [];
function h(e, t = k) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function s(l) {
    if (Te(e, l) && (e = l, n)) {
      const u = !I.length;
      for (const a of r)
        a[1](), I.push(a, e);
      if (u) {
        for (let a = 0; a < I.length; a += 2)
          I[a][0](I[a + 1]);
        I.length = 0;
      }
    }
  }
  function o(l) {
    s(l(e));
  }
  function i(l, u = k) {
    const a = [l, u];
    return r.add(a), r.size === 1 && (n = t(s, o) || k), l(e), () => {
      r.delete(a), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: s,
    update: o,
    subscribe: i
  };
}
const {
  getContext: De,
  setContext: Nt
} = window.__gradio__svelte__internal, Ue = "$$ms-gr-loading-status-key";
function We() {
  const e = window.ms_globals.loadingKey++, t = De(Ue);
  return (n) => {
    if (!t)
      return;
    const {
      loadingStatusMap: r,
      options: s
    } = t, {
      generating: o,
      error: i
    } = w(s);
    (n == null ? void 0 : n.status) === "pending" || i && (n == null ? void 0 : n.status) === "error" || (o && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: l
    }) => (l.set(e, n), {
      map: l
    })) : r.update(({
      map: l
    }) => (l.delete(e), {
      map: l
    }));
  };
}
const {
  getContext: U,
  setContext: E
} = window.__gradio__svelte__internal, Ge = "$$ms-gr-slots-key";
function He() {
  const e = h({});
  return E(Ge, e);
}
const Je = "$$ms-gr-render-slot-context-key";
function Ye() {
  const e = E(Je, h({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const Qe = "$$ms-gr-context-key";
function L(e) {
  return Be(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Ie = "$$ms-gr-sub-index-context-key";
function Xe() {
  return U(Ie) || null;
}
function he(e) {
  return E(Ie, e);
}
function Ze(e, t, n) {
  var m, p;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Ee(), s = et({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = Xe();
  typeof o == "number" && he(void 0);
  const i = We();
  typeof e._internal.subIndex == "number" && he(e._internal.subIndex), r && r.subscribe((c) => {
    s.slotKey.set(c);
  }), Ve();
  const l = U(Qe), u = ((m = w(l)) == null ? void 0 : m.as_item) || e.as_item, a = L(l ? u ? ((p = w(l)) == null ? void 0 : p[u]) || {} : w(l) || {} : {}), f = (c, _) => c ? Fe({
    ...c,
    ..._ || {}
  }, t) : void 0, g = h({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...a,
    restProps: f(e.restProps, a),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: _
    } = w(g);
    _ && (c = c == null ? void 0 : c[_]), c = L(c), g.update((b) => ({
      ...b,
      ...c || {},
      restProps: f(b.restProps, c)
    }));
  }), [g, (c) => {
    var b, P;
    const _ = L(c.as_item ? ((b = w(l)) == null ? void 0 : b[c.as_item]) || {} : w(l) || {});
    return i((P = c.restProps) == null ? void 0 : P.loading_status), g.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      ..._,
      restProps: f(c.restProps, _),
      originalRestProps: c.restProps
    });
  }]) : [g, (c) => {
    var _;
    i((_ = c.restProps) == null ? void 0 : _.loading_status), g.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      restProps: f(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const Ce = "$$ms-gr-slot-key";
function Ve() {
  E(Ce, h(void 0));
}
function Ee() {
  return U(Ce);
}
const $e = "$$ms-gr-component-slot-context-key";
function et({
  slot: e,
  index: t,
  subIndex: n
}) {
  return E($e, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(n)
  });
}
function tt(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function nt(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Re = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var rt = x, ot = Symbol.for("react.element"), st = Symbol.for("react.fragment"), it = Object.prototype.hasOwnProperty, lt = rt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ct = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Se(e, t, n) {
  var r, s = {}, o = null, i = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (r in t) it.call(t, r) && !ct.hasOwnProperty(r) && (s[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: ot,
    type: e,
    key: o,
    ref: i,
    props: s,
    _owner: lt.current
  };
}
N.Fragment = st;
N.jsx = Se;
N.jsxs = Se;
Re.exports = N;
var M = Re.exports;
const ut = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function dt(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return typeof r == "number" && !ut.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function q(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(qe(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: x.Children.toArray(e._reactElement.props.children).map((s) => {
        if (x.isValidElement(s) && s.props.__slot__) {
          const {
            portals: o,
            clonedElement: i
          } = q(s.props.el);
          return x.cloneElement(s, {
            ...s.props,
            el: i,
            children: [...x.Children.toArray(s.props.children), ...o]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: i,
      type: l,
      useCapture: u
    }) => {
      n.addEventListener(l, i, u);
    });
  });
  const r = Array.from(e.childNodes);
  for (let s = 0; s < r.length; s++) {
    const o = r[s];
    if (o.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = q(o);
      t.push(...l), n.appendChild(i);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function at(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const B = Ke(({
  slot: e,
  clone: t,
  className: n,
  style: r
}, s) => {
  const o = Le(), [i, l] = Ae([]);
  return Me(() => {
    var g;
    if (!o.current || !e)
      return;
    let u = e;
    function a() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), at(s, m), n && m.classList.add(...n.split(" ")), r) {
        const p = dt(r);
        Object.keys(p).forEach((c) => {
          m.style[c] = p[c];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let m = function() {
        var _;
        const {
          portals: p,
          clonedElement: c
        } = q(e);
        u = c, l(p), u.style.display = "contents", a(), (_ = o.current) == null || _.appendChild(u);
      };
      m(), f = new window.MutationObserver(() => {
        var p, c;
        (p = o.current) != null && p.contains(u) && ((c = o.current) == null || c.removeChild(u)), m();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", a(), (g = o.current) == null || g.appendChild(u);
    return () => {
      var m, p;
      u.style.display = "", (m = o.current) != null && m.contains(u) && ((p = o.current) == null || p.removeChild(u)), f == null || f.disconnect();
    };
  }, [e, t, n, r, s]), x.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function T(e, t) {
  return e.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return t != null && t.fallback ? t.fallback(n) : n;
    const r = {
      ...n.props
    };
    let s = r;
    Object.keys(n.slots).forEach((i) => {
      if (!n.slots[i] || !(n.slots[i] instanceof Element) && !n.slots[i].el)
        return;
      const l = i.split(".");
      l.forEach((m, p) => {
        s[m] || (s[m] = {}), p !== l.length - 1 && (s = r[m]);
      });
      const u = n.slots[i];
      let a, f, g = (t == null ? void 0 : t.clone) ?? !1;
      u instanceof Element ? a = u : (a = u.el, f = u.callback, g = u.clone ?? !1), s[l[l.length - 1]] = a ? f ? (...m) => (f(l[l.length - 1], m), /* @__PURE__ */ M.jsx(B, {
        slot: a,
        clone: g
      })) : /* @__PURE__ */ M.jsx(B, {
        slot: a,
        clone: g
      }) : s[l[l.length - 1]], s = r;
    });
    const o = (t == null ? void 0 : t.children) || "children";
    return n[o] && (r[o] = T(n[o], t)), r;
  });
}
function z(e, t) {
  return e ? /* @__PURE__ */ M.jsx(B, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function A({
  key: e,
  setSlotParams: t,
  slots: n
}, r) {
  return n[e] ? (...s) => (t(e, s), z(n[e], {
    clone: !0,
    ...r
  })) : void 0;
}
var Oe = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var o = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (o = s(o, r(l)));
      }
      return o;
    }
    function r(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var i = "";
      for (var l in o)
        t.call(o, l) && o[l] && (i = s(i, l));
      return i;
    }
    function s(o, i) {
      return i ? o ? o + " " + i : o + i : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(Oe);
var ft = Oe.exports;
const mt = /* @__PURE__ */ nt(ft), {
  getContext: pt,
  setContext: _t
} = window.__gradio__svelte__internal;
function ve(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(s = ["default"]) {
    const o = s.reduce((i, l) => (i[l] = h([]), i), {});
    return _t(t, {
      itemsMap: o,
      allowedSlots: s
    }), o;
  }
  function r() {
    const {
      itemsMap: s,
      allowedSlots: o
    } = pt(t);
    return function(i, l, u) {
      s && (i ? s[i].update((a) => {
        const f = [...a];
        return o.includes(i) ? f[l] = u : f[l] = void 0, f;
      }) : o.includes("default") && s.default.update((a) => {
        const f = [...a];
        return f[l] = u, f;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: gt,
  getSetItemFn: Kt
} = ve("menu"), {
  getItems: Lt,
  getSetItemFn: bt
} = ve("breadcrumb"), {
  SvelteComponent: ht,
  assign: ye,
  check_outros: yt,
  component_subscribe: C,
  compute_rest_props: Pe,
  create_slot: Pt,
  detach: wt,
  empty: we,
  exclude_internal_props: xt,
  flush: y,
  get_all_dirty_from_scope: It,
  get_slot_changes: Ct,
  group_outros: Et,
  init: Rt,
  insert_hydration: St,
  safe_not_equal: Ot,
  transition_in: F,
  transition_out: D,
  update_slot_base: vt
} = window.__gradio__svelte__internal;
function xe(e) {
  let t;
  const n = (
    /*#slots*/
    e[21].default
  ), r = Pt(
    n,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(s) {
      r && r.l(s);
    },
    m(s, o) {
      r && r.m(s, o), t = !0;
    },
    p(s, o) {
      r && r.p && (!t || o & /*$$scope*/
      1048576) && vt(
        r,
        n,
        s,
        /*$$scope*/
        s[20],
        t ? Ct(
          n,
          /*$$scope*/
          s[20],
          o,
          null
        ) : It(
          /*$$scope*/
          s[20]
        ),
        null
      );
    },
    i(s) {
      t || (F(r, s), t = !0);
    },
    o(s) {
      D(r, s), t = !1;
    },
    d(s) {
      r && r.d(s);
    }
  };
}
function jt(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && xe(e)
  );
  return {
    c() {
      r && r.c(), t = we();
    },
    l(s) {
      r && r.l(s), t = we();
    },
    m(s, o) {
      r && r.m(s, o), St(s, t, o), n = !0;
    },
    p(s, [o]) {
      /*$mergedProps*/
      s[0].visible ? r ? (r.p(s, o), o & /*$mergedProps*/
      1 && F(r, 1)) : (r = xe(s), r.c(), F(r, 1), r.m(t.parentNode, t)) : r && (Et(), D(r, 1, 1, () => {
        r = null;
      }), yt());
    },
    i(s) {
      n || (F(r), n = !0);
    },
    o(s) {
      D(r), n = !1;
    },
    d(s) {
      s && wt(t), r && r.d(s);
    }
  };
}
function kt(e, t, n) {
  const r = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let s = Pe(t, r), o, i, l, u, a, f, {
    $$slots: g = {},
    $$scope: m
  } = t, {
    gradio: p
  } = t, {
    props: c = {}
  } = t;
  const _ = h(c);
  C(e, _, (d) => n(19, f = d));
  let {
    _internal: b = {}
  } = t, {
    as_item: P
  } = t, {
    visible: R = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: O = []
  } = t, {
    elem_style: v = {}
  } = t;
  const W = Ee();
  C(e, W, (d) => n(16, l = d));
  const [G, je] = Ze({
    gradio: p,
    props: f,
    _internal: b,
    visible: R,
    elem_id: S,
    elem_classes: O,
    elem_style: v,
    as_item: P,
    restProps: s
  });
  C(e, G, (d) => n(0, i = d));
  const H = He();
  C(e, H, (d) => n(15, o = d));
  const ke = bt(), K = Ye(), {
    "menu.items": J,
    "dropdownProps.menu.items": Y
  } = gt(["menu.items", "dropdownProps.menu.items"]);
  return C(e, J, (d) => n(18, a = d)), C(e, Y, (d) => n(17, u = d)), e.$$set = (d) => {
    t = ye(ye({}, t), xt(d)), n(25, s = Pe(t, r)), "gradio" in d && n(7, p = d.gradio), "props" in d && n(8, c = d.props), "_internal" in d && n(9, b = d._internal), "as_item" in d && n(10, P = d.as_item), "visible" in d && n(11, R = d.visible), "elem_id" in d && n(12, S = d.elem_id), "elem_classes" in d && n(13, O = d.elem_classes), "elem_style" in d && n(14, v = d.elem_style), "$$scope" in d && n(20, m = d.$$scope);
  }, e.$$.update = () => {
    var d, Q, X, Z, V, $, ee, te, ne, re, oe, se, ie, le, ce, ue, de, ae, fe, me, pe, _e;
    if (e.$$.dirty & /*props*/
    256 && _.update((j) => ({
      ...j,
      ...c
    })), je({
      gradio: p,
      props: f,
      _internal: b,
      visible: R,
      elem_id: S,
      elem_classes: O,
      elem_style: v,
      as_item: P,
      restProps: s
    }), e.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, $slotKey*/
    491521) {
      const j = {
        ...i.restProps.menu || {},
        ...i.props.menu || {},
        items: (d = i.props.menu) != null && d.items || (Q = i.restProps.menu) != null && Q.items || a.length > 0 ? T(a, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: o,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((X = i.props.menu) == null ? void 0 : X.expandIcon) || ((Z = i.restProps.menu) == null ? void 0 : Z.expandIcon),
        overflowedIndicator: z(o["menu.overflowedIndicator"]) || ((V = i.props.menu) == null ? void 0 : V.overflowedIndicator) || (($ = i.restProps.menu) == null ? void 0 : $.overflowedIndicator)
      }, ge = {
        ...((ee = i.restProps.dropdownProps) == null ? void 0 : ee.menu) || {},
        ...((te = i.props.dropdownProps) == null ? void 0 : te.menu) || {},
        items: (re = (ne = i.props.dropdownProps) == null ? void 0 : ne.menu) != null && re.items || (se = (oe = i.restProps.dropdownProps) == null ? void 0 : oe.menu) != null && se.items || u.length > 0 ? T(u, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: o,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((le = (ie = i.props.dropdownProps) == null ? void 0 : ie.menu) == null ? void 0 : le.expandIcon) || ((ue = (ce = i.restProps.dropdownProps) == null ? void 0 : ce.menu) == null ? void 0 : ue.expandIcon),
        overflowedIndicator: z(o["dropdownProps.menu.overflowedIndicator"]) || ((ae = (de = i.props.dropdownProps) == null ? void 0 : de.menu) == null ? void 0 : ae.overflowedIndicator) || ((me = (fe = i.restProps.dropdownProps) == null ? void 0 : fe.menu) == null ? void 0 : me.overflowedIndicator)
      }, be = {
        ...i.restProps.dropdownProps || {},
        ...i.props.dropdownProps || {},
        dropdownRender: o["dropdownProps.dropdownRender"] ? A({
          setSlotParams: K,
          slots: o,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : tt(((pe = i.props.dropdownProps) == null ? void 0 : pe.dropdownRender) || ((_e = i.restProps.dropdownProps) == null ? void 0 : _e.dropdownRender)),
        menu: Object.values(ge).filter(Boolean).length > 0 ? ge : void 0
      };
      ke(l, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: mt(i.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...Ne(i),
          menu: Object.values(j).filter(Boolean).length > 0 ? j : void 0,
          dropdownProps: Object.values(be).filter(Boolean).length > 0 ? be : void 0
        },
        slots: {
          title: o.title
        }
      });
    }
  }, [i, _, W, G, H, J, Y, p, c, b, P, R, S, O, v, o, l, u, a, f, m, g];
}
class At extends ht {
  constructor(t) {
    super(), Rt(this, t, kt, jt, Ot, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  At as default
};
