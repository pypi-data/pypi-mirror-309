import { g as X, b as Y } from "./Index-BxwFAwFh.js";
function Z(e) {
  return e === void 0;
}
function E() {
}
function v(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function V(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return E;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function P(e) {
  let t;
  return V(e, (n) => t = n)(), t;
}
const C = [];
function b(e, t = E) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function o(l) {
    if (v(e, l) && (e = l, n)) {
      const d = !C.length;
      for (const a of s)
        a[1](), C.push(a, e);
      if (d) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function r(l) {
    o(l(e));
  }
  function i(l, d = E) {
    const a = [l, d];
    return s.add(a), s.size === 1 && (n = t(o, r) || E), l(e), () => {
      s.delete(a), s.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: i
  };
}
const {
  getContext: $,
  setContext: qe
} = window.__gradio__svelte__internal, ee = "$$ms-gr-loading-status-key";
function te() {
  const e = window.ms_globals.loadingKey++, t = $(ee);
  return (n) => {
    if (!t)
      return;
    const {
      loadingStatusMap: s,
      options: o
    } = t, {
      generating: r,
      error: i
    } = P(o);
    (n == null ? void 0 : n.status) === "pending" || i && (n == null ? void 0 : n.status) === "error" || (r && (n == null ? void 0 : n.status)) === "generating" ? s.update(({
      map: l
    }) => (l.set(e, n), {
      map: l
    })) : s.update(({
      map: l
    }) => (l.delete(e), {
      map: l
    }));
  };
}
const {
  getContext: N,
  setContext: I
} = window.__gradio__svelte__internal, ne = "$$ms-gr-slots-key";
function se() {
  const e = b({});
  return I(ne, e);
}
const re = "$$ms-gr-render-slot-context-key";
function oe() {
  const e = I(re, b({}));
  return (t, n) => {
    e.update((s) => typeof n == "function" ? {
      ...s,
      [t]: n(s[t])
    } : {
      ...s,
      [t]: n
    });
  };
}
const ie = "$$ms-gr-context-key";
function F(e) {
  return Z(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const B = "$$ms-gr-sub-index-context-key";
function le() {
  return N(B) || null;
}
function T(e) {
  return I(B, e);
}
function ue(e, t, n) {
  var x, h;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = H(), o = fe({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), r = le();
  typeof r == "number" && T(void 0);
  const i = te();
  typeof e._internal.subIndex == "number" && T(e._internal.subIndex), s && s.subscribe((u) => {
    o.slotKey.set(u);
  }), ce();
  const l = N(ie), d = ((x = P(l)) == null ? void 0 : x.as_item) || e.as_item, a = F(l ? d ? ((h = P(l)) == null ? void 0 : h[d]) || {} : P(l) || {} : {}), _ = (u, f) => u ? X({
    ...u,
    ...f || {}
  }, t) : void 0, m = b({
    ...e,
    _internal: {
      ...e._internal,
      index: r ?? e._internal.index
    },
    ...a,
    restProps: _(e.restProps, a),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((u) => {
    const {
      as_item: f
    } = P(m);
    f && (u = u == null ? void 0 : u[f]), u = F(u), m.update((p) => ({
      ...p,
      ...u || {},
      restProps: _(p.restProps, u)
    }));
  }), [m, (u) => {
    var p, y;
    const f = F(u.as_item ? ((p = P(l)) == null ? void 0 : p[u.as_item]) || {} : P(l) || {});
    return i((y = u.restProps) == null ? void 0 : y.loading_status), m.set({
      ...u,
      _internal: {
        ...u._internal,
        index: r ?? u._internal.index
      },
      ...f,
      restProps: _(u.restProps, f),
      originalRestProps: u.restProps
    });
  }]) : [m, (u) => {
    var f;
    i((f = u.restProps) == null ? void 0 : f.loading_status), m.set({
      ...u,
      _internal: {
        ...u._internal,
        index: r ?? u._internal.index
      },
      restProps: _(u.restProps),
      originalRestProps: u.restProps
    });
  }];
}
const G = "$$ms-gr-slot-key";
function ce() {
  I(G, b(void 0));
}
function H() {
  return N(G);
}
const ae = "$$ms-gr-component-slot-context-key";
function fe({
  slot: e,
  index: t,
  subIndex: n
}) {
  return I(ae, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(n)
  });
}
function S(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function de(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var J = {
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
      for (var r = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (r = o(r, s(l)));
      }
      return r;
    }
    function s(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return n.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var i = "";
      for (var l in r)
        t.call(r, l) && r[l] && (i = o(i, l));
      return i;
    }
    function o(r, i) {
      return i ? r ? r + " " + i : r + i : r;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(J);
var _e = J.exports;
const me = /* @__PURE__ */ de(_e), {
  getContext: pe,
  setContext: be
} = window.__gradio__svelte__internal;
function ge(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(o = ["default"]) {
    const r = o.reduce((i, l) => (i[l] = b([]), i), {});
    return be(t, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = pe(t);
    return function(i, l, d) {
      o && (i ? o[i].update((a) => {
        const _ = [...a];
        return r.includes(i) ? _[l] = d : _[l] = void 0, _;
      }) : r.includes("default") && o.default.update((a) => {
        const _ = [...a];
        return _[l] = d, _;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: s
  };
}
const {
  getItems: Ae,
  getSetItemFn: xe
} = ge("table-expandable"), {
  SvelteComponent: ye,
  assign: z,
  check_outros: Pe,
  component_subscribe: w,
  compute_rest_props: L,
  create_slot: he,
  detach: Ce,
  empty: D,
  exclude_internal_props: Ie,
  flush: g,
  get_all_dirty_from_scope: Re,
  get_slot_changes: Ke,
  group_outros: Se,
  init: we,
  insert_hydration: Ee,
  safe_not_equal: ke,
  transition_in: k,
  transition_out: j,
  update_slot_base: Fe
} = window.__gradio__svelte__internal;
function U(e) {
  let t;
  const n = (
    /*#slots*/
    e[17].default
  ), s = he(
    n,
    e,
    /*$$scope*/
    e[16],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(o) {
      s && s.l(o);
    },
    m(o, r) {
      s && s.m(o, r), t = !0;
    },
    p(o, r) {
      s && s.p && (!t || r & /*$$scope*/
      65536) && Fe(
        s,
        n,
        o,
        /*$$scope*/
        o[16],
        t ? Ke(
          n,
          /*$$scope*/
          o[16],
          r,
          null
        ) : Re(
          /*$$scope*/
          o[16]
        ),
        null
      );
    },
    i(o) {
      t || (k(s, o), t = !0);
    },
    o(o) {
      j(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function je(e) {
  let t, n, s = (
    /*$mergedProps*/
    e[0].visible && U(e)
  );
  return {
    c() {
      s && s.c(), t = D();
    },
    l(o) {
      s && s.l(o), t = D();
    },
    m(o, r) {
      s && s.m(o, r), Ee(o, t, r), n = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, r), r & /*$mergedProps*/
      1 && k(s, 1)) : (s = U(o), s.c(), k(s, 1), s.m(t.parentNode, t)) : s && (Se(), j(s, 1, 1, () => {
        s = null;
      }), Pe());
    },
    i(o) {
      n || (k(s), n = !0);
    },
    o(o) {
      j(s), n = !1;
    },
    d(o) {
      o && Ce(t), s && s.d(o);
    }
  };
}
function Ne(e, t, n) {
  const s = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = L(t, s), r, i, l, d, {
    $$slots: a = {},
    $$scope: _
  } = t, {
    gradio: m
  } = t, {
    props: x = {}
  } = t;
  const h = b(x);
  w(e, h, (c) => n(15, d = c));
  let {
    _internal: u = {}
  } = t, {
    as_item: f
  } = t, {
    visible: p = !0
  } = t, {
    elem_id: y = ""
  } = t, {
    elem_classes: R = []
  } = t, {
    elem_style: K = {}
  } = t;
  const O = H();
  w(e, O, (c) => n(14, l = c));
  const [q, Q] = ue({
    gradio: m,
    props: d,
    _internal: u,
    visible: p,
    elem_id: y,
    elem_classes: R,
    elem_style: K,
    as_item: f,
    restProps: o
  });
  w(e, q, (c) => n(0, i = c));
  const A = se();
  w(e, A, (c) => n(13, r = c));
  const M = oe(), W = xe();
  return e.$$set = (c) => {
    t = z(z({}, t), Ie(c)), n(21, o = L(t, s)), "gradio" in c && n(5, m = c.gradio), "props" in c && n(6, x = c.props), "_internal" in c && n(7, u = c._internal), "as_item" in c && n(8, f = c.as_item), "visible" in c && n(9, p = c.visible), "elem_id" in c && n(10, y = c.elem_id), "elem_classes" in c && n(11, R = c.elem_classes), "elem_style" in c && n(12, K = c.elem_style), "$$scope" in c && n(16, _ = c.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    64 && h.update((c) => ({
      ...c,
      ...x
    })), Q({
      gradio: m,
      props: d,
      _internal: u,
      visible: p,
      elem_id: y,
      elem_classes: R,
      elem_style: K,
      as_item: f,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slotKey, $slots*/
    24577) {
      const c = Y(i);
      W(l, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: me(i.elem_classes, "ms-gr-antd-table-expandable"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...c,
          expandedRowClassName: S(i.props.expandedRowClassName || i.restProps.expandedRowClassName),
          expandedRowRender: S(i.props.expandedRowRender || i.restProps.expandedRowRender),
          rowExpandable: S(i.props.rowExpandable || i.restProps.rowExpandable),
          expandIcon: S(i.props.expandIcon || i.restProps.expandIcon),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...r,
          expandIcon: {
            el: r.expandIcon,
            callback: M,
            clone: !0
          },
          expandedRowRender: {
            el: r.expandedRowRender,
            callback: M,
            clone: !0
          }
        }
      });
    }
  }, [i, h, O, q, A, m, x, u, f, p, y, R, K, r, l, d, _, a];
}
class Me extends ye {
  constructor(t) {
    super(), we(this, t, Ne, je, ke, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      visible: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), g();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(t) {
    this.$$set({
      props: t
    }), g();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), g();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), g();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), g();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), g();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), g();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), g();
  }
}
export {
  Me as default
};
