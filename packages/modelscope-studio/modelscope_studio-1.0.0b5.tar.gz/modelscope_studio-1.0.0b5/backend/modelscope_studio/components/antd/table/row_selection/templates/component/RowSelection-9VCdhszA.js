import { g as oe, b as ie } from "./Index-Cz3VjGk9.js";
const P = window.ms_globals.React, le = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, ae = window.ms_globals.React.useEffect, fe = window.ms_globals.ReactDOM.createPortal;
function de(e) {
  return e === void 0;
}
function k() {
}
function me(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function _e(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return k;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function C(e) {
  let t;
  return _e(e, (n) => t = n)(), t;
}
const E = [];
function h(e, t = k) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function o(l) {
    if (me(e, l) && (e = l, n)) {
      const u = !E.length;
      for (const f of r)
        f[1](), E.push(f, e);
      if (u) {
        for (let f = 0; f < E.length; f += 2)
          E[f][0](E[f + 1]);
        E.length = 0;
      }
    }
  }
  function s(l) {
    o(l(e));
  }
  function i(l, u = k) {
    const f = [l, u];
    return r.add(f), r.size === 1 && (n = t(o, s) || k), l(e), () => {
      r.delete(f), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: i
  };
}
const {
  getContext: pe,
  setContext: ot
} = window.__gradio__svelte__internal, ge = "$$ms-gr-loading-status-key";
function be() {
  const e = window.ms_globals.loadingKey++, t = pe(ge);
  return (n) => {
    if (!t)
      return;
    const {
      loadingStatusMap: r,
      options: o
    } = t, {
      generating: s,
      error: i
    } = C(o);
    (n == null ? void 0 : n.status) === "pending" || i && (n == null ? void 0 : n.status) === "error" || (s && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
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
  getContext: T,
  setContext: S
} = window.__gradio__svelte__internal, he = "$$ms-gr-slots-key";
function ye() {
  const e = h({});
  return S(he, e);
}
const xe = "$$ms-gr-render-slot-context-key";
function Ce() {
  const e = S(xe, h({}));
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
const Pe = "$$ms-gr-context-key";
function F(e) {
  return de(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Q = "$$ms-gr-sub-index-context-key";
function Ee() {
  return T(Q) || null;
}
function U(e) {
  return S(Q, e);
}
function we(e, t, n) {
  var d, _;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Z(), o = Re({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = Ee();
  typeof s == "number" && U(void 0);
  const i = be();
  typeof e._internal.subIndex == "number" && U(e._internal.subIndex), r && r.subscribe((c) => {
    o.slotKey.set(c);
  }), Se();
  const l = T(Pe), u = ((d = C(l)) == null ? void 0 : d.as_item) || e.as_item, f = F(l ? u ? ((_ = C(l)) == null ? void 0 : _[u]) || {} : C(l) || {} : {}), m = (c, p) => c ? oe({
    ...c,
    ...p || {}
  }, t) : void 0, g = h({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    ...f,
    restProps: m(e.restProps, f),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: p
    } = C(g);
    p && (c = c == null ? void 0 : c[p]), c = F(c), g.update((b) => ({
      ...b,
      ...c || {},
      restProps: m(b.restProps, c)
    }));
  }), [g, (c) => {
    var b, x;
    const p = F(c.as_item ? ((b = C(l)) == null ? void 0 : b[c.as_item]) || {} : C(l) || {});
    return i((x = c.restProps) == null ? void 0 : x.loading_status), g.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      ...p,
      restProps: m(c.restProps, p),
      originalRestProps: c.restProps
    });
  }]) : [g, (c) => {
    var p;
    i((p = c.restProps) == null ? void 0 : p.loading_status), g.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      restProps: m(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const X = "$$ms-gr-slot-key";
function Se() {
  S(X, h(void 0));
}
function Z() {
  return T(X);
}
const Ie = "$$ms-gr-component-slot-context-key";
function Re({
  slot: e,
  index: t,
  subIndex: n
}) {
  return S(Ie, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(n)
  });
}
function N(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Oe(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ke = P, je = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), Fe = Object.prototype.hasOwnProperty, Ne = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ke = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(e, t, n) {
  var r, o = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (r in t) Fe.call(t, r) && !Ke.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: je,
    type: e,
    key: s,
    ref: i,
    props: o,
    _owner: Ne.current
  };
}
v.Fragment = ve;
v.jsx = $;
v.jsxs = $;
V.exports = v;
var W = V.exports;
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return typeof r == "number" && !Le.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function K(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(fe(P.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: P.Children.toArray(e._reactElement.props.children).map((o) => {
        if (P.isValidElement(o) && o.props.__slot__) {
          const {
            portals: s,
            clonedElement: i
          } = K(o.props.el);
          return P.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...P.Children.toArray(o.props.children), ...s]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: i,
      type: l,
      useCapture: u
    }) => {
      n.addEventListener(l, i, u);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const s = r[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = K(s);
      t.push(...l), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Ae(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const G = le(({
  slot: e,
  clone: t,
  className: n,
  style: r
}, o) => {
  const s = ce(), [i, l] = ue([]);
  return ae(() => {
    var g;
    if (!s.current || !e)
      return;
    let u = e;
    function f() {
      let d = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (d = u.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ae(o, d), n && d.classList.add(...n.split(" ")), r) {
        const _ = Te(r);
        Object.keys(_).forEach((c) => {
          d.style[c] = _[c];
        });
      }
    }
    let m = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var p;
        const {
          portals: _,
          clonedElement: c
        } = K(e);
        u = c, l(_), u.style.display = "contents", f(), (p = s.current) == null || p.appendChild(u);
      };
      d(), m = new window.MutationObserver(() => {
        var _, c;
        (_ = s.current) != null && _.contains(u) && ((c = s.current) == null || c.removeChild(u)), d();
      }), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", f(), (g = s.current) == null || g.appendChild(u);
    return () => {
      var d, _;
      u.style.display = "", (d = s.current) != null && d.contains(u) && ((_ = s.current) == null || _.removeChild(u)), m == null || m.disconnect();
    };
  }, [e, t, n, r, o]), P.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...i);
});
function ee(e, t) {
  return e.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const r = {
      ...n.props
    };
    let o = r;
    Object.keys(n.slots).forEach((i) => {
      if (!n.slots[i] || !(n.slots[i] instanceof Element) && !n.slots[i].el)
        return;
      const l = i.split(".");
      l.forEach((d, _) => {
        o[d] || (o[d] = {}), _ !== l.length - 1 && (o = r[d]);
      });
      const u = n.slots[i];
      let f, m, g = !1;
      u instanceof Element ? f = u : (f = u.el, m = u.callback, g = u.clone ?? !1), o[l[l.length - 1]] = f ? m ? (...d) => (m(l[l.length - 1], d), /* @__PURE__ */ W.jsx(G, {
        slot: f,
        clone: g
      })) : /* @__PURE__ */ W.jsx(G, {
        slot: f,
        clone: g
      }) : o[l[l.length - 1]], o = r;
    });
    const s = "children";
    return n[s] && (r[s] = ee(n[s])), r;
  });
}
var te = {
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
      for (var s = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (s = o(s, r(l)));
      }
      return s;
    }
    function r(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return n.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var i = "";
      for (var l in s)
        t.call(s, l) && s[l] && (i = o(i, l));
      return i;
    }
    function o(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(te);
var Me = te.exports;
const qe = /* @__PURE__ */ Oe(Me), {
  getContext: ze,
  setContext: De
} = window.__gradio__svelte__internal;
function ne(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(o = ["default"]) {
    const s = o.reduce((i, l) => (i[l] = h([]), i), {});
    return De(t, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function r() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = ze(t);
    return function(i, l, u) {
      o && (i ? o[i].update((f) => {
        const m = [...f];
        return s.includes(i) ? m[l] = u : m[l] = void 0, m;
      }) : s.includes("default") && o.default.update((f) => {
        const m = [...f];
        return m[l] = u, m;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: Ue,
  getSetItemFn: it
} = ne("table-row-selection-selection"), {
  getItems: lt,
  getSetItemFn: We
} = ne("table-row-selection"), {
  SvelteComponent: Ge,
  assign: H,
  check_outros: He,
  component_subscribe: w,
  compute_rest_props: B,
  create_slot: Be,
  detach: Je,
  empty: J,
  exclude_internal_props: Ye,
  flush: y,
  get_all_dirty_from_scope: Qe,
  get_slot_changes: Xe,
  group_outros: Ze,
  init: Ve,
  insert_hydration: $e,
  safe_not_equal: et,
  transition_in: j,
  transition_out: L,
  update_slot_base: tt
} = window.__gradio__svelte__internal;
function Y(e) {
  let t;
  const n = (
    /*#slots*/
    e[19].default
  ), r = Be(
    n,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(o) {
      r && r.l(o);
    },
    m(o, s) {
      r && r.m(o, s), t = !0;
    },
    p(o, s) {
      r && r.p && (!t || s & /*$$scope*/
      262144) && tt(
        r,
        n,
        o,
        /*$$scope*/
        o[18],
        t ? Xe(
          n,
          /*$$scope*/
          o[18],
          s,
          null
        ) : Qe(
          /*$$scope*/
          o[18]
        ),
        null
      );
    },
    i(o) {
      t || (j(r, o), t = !0);
    },
    o(o) {
      L(r, o), t = !1;
    },
    d(o) {
      r && r.d(o);
    }
  };
}
function nt(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && Y(e)
  );
  return {
    c() {
      r && r.c(), t = J();
    },
    l(o) {
      r && r.l(o), t = J();
    },
    m(o, s) {
      r && r.m(o, s), $e(o, t, s), n = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? r ? (r.p(o, s), s & /*$mergedProps*/
      1 && j(r, 1)) : (r = Y(o), r.c(), j(r, 1), r.m(t.parentNode, t)) : r && (Ze(), L(r, 1, 1, () => {
        r = null;
      }), He());
    },
    i(o) {
      n || (j(r), n = !0);
    },
    o(o) {
      L(r), n = !1;
    },
    d(o) {
      o && Je(t), r && r.d(o);
    }
  };
}
function rt(e, t, n) {
  const r = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = B(t, r), s, i, l, u, f, {
    $$slots: m = {},
    $$scope: g
  } = t, {
    gradio: d
  } = t, {
    props: _ = {}
  } = t;
  const c = h(_);
  w(e, c, (a) => n(17, f = a));
  let {
    _internal: p = {}
  } = t, {
    as_item: b
  } = t, {
    visible: x = !0
  } = t, {
    elem_id: I = ""
  } = t, {
    elem_classes: R = []
  } = t, {
    elem_style: O = {}
  } = t;
  const A = Z();
  w(e, A, (a) => n(16, u = a));
  const [M, re] = we({
    gradio: d,
    props: f,
    _internal: p,
    visible: x,
    elem_id: I,
    elem_classes: R,
    elem_style: O,
    as_item: b,
    restProps: o
  });
  w(e, M, (a) => n(0, i = a));
  const q = Ce(), z = ye();
  w(e, z, (a) => n(14, s = a));
  const {
    selections: D
  } = Ue(["selections"]);
  w(e, D, (a) => n(15, l = a));
  const se = We();
  return e.$$set = (a) => {
    t = H(H({}, t), Ye(a)), n(23, o = B(t, r)), "gradio" in a && n(6, d = a.gradio), "props" in a && n(7, _ = a.props), "_internal" in a && n(8, p = a._internal), "as_item" in a && n(9, b = a.as_item), "visible" in a && n(10, x = a.visible), "elem_id" in a && n(11, I = a.elem_id), "elem_classes" in a && n(12, R = a.elem_classes), "elem_style" in a && n(13, O = a.elem_style), "$$scope" in a && n(18, g = a.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    128 && c.update((a) => ({
      ...a,
      ..._
    })), re({
      gradio: d,
      props: f,
      _internal: p,
      visible: x,
      elem_id: I,
      elem_classes: R,
      elem_style: O,
      as_item: b,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    114689) {
      const a = ie(i);
      se(u, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: qe(i.elem_classes, "ms-gr-antd-table-row-selection"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...a,
          selections: i.props.selections || i.restProps.selections || ee(l),
          onCell: N(i.props.onCell || i.restProps.onCell),
          getCheckboxProps: N(i.props.getCheckboxProps || i.restProps.getCheckboxProps),
          renderCell: N(i.props.renderCell || i.restProps.renderCell),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...s,
          columnTitle: {
            el: s.columnTitle,
            callback: q,
            clone: !0
          },
          renderCell: {
            el: s.renderCell,
            callback: q,
            clone: !0
          }
        }
      });
    }
  }, [i, c, A, M, z, D, d, _, p, b, x, I, R, O, s, l, u, f, g, m];
}
class ct extends Ge {
  constructor(t) {
    super(), Ve(this, t, rt, nt, et, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), y();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), y();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), y();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), y();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), y();
  }
}
export {
  ct as default
};
