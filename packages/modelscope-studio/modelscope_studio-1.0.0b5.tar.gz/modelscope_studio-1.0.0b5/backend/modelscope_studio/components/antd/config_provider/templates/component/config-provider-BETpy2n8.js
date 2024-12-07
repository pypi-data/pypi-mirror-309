import { g as Lt, w as A } from "./Index-NWHcLgoD.js";
const j = window.ms_globals.React, Nt = window.ms_globals.React.forwardRef, Tt = window.ms_globals.React.useRef, jt = window.ms_globals.React.useState, bt = window.ms_globals.React.useEffect, Mt = window.ms_globals.React.useMemo, J = window.ms_globals.ReactDOM.createPortal, Kt = window.ms_globals.antdCssinjs.StyleProvider, Ut = window.ms_globals.antd.ConfigProvider, it = window.ms_globals.antd.theme, Bt = window.ms_globals.dayjs;
var kt = {
  exports: {}
}, M = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Gt = j, Wt = Symbol.for("react.element"), Ht = Symbol.for("react.fragment"), Zt = Object.prototype.hasOwnProperty, qt = Gt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Yt = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Et(e, t, n) {
  var r, a = {}, o = null, i = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (r in t) Zt.call(t, r) && !Yt.hasOwnProperty(r) && (a[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) a[r] === void 0 && (a[r] = t[r]);
  return {
    $$typeof: Wt,
    type: e,
    key: o,
    ref: i,
    props: a,
    _owner: qt.current
  };
}
M.Fragment = Ht;
M.jsx = Et;
M.jsxs = Et;
kt.exports = M;
var z = kt.exports;
const {
  SvelteComponent: Jt,
  assign: st,
  binding_callbacks: lt,
  check_outros: Qt,
  children: vt,
  claim_element: St,
  claim_space: Xt,
  component_subscribe: ct,
  compute_slots: Vt,
  create_slot: $t,
  detach: v,
  element: Ct,
  empty: ut,
  exclude_internal_props: dt,
  get_all_dirty_from_scope: te,
  get_slot_changes: ee,
  group_outros: ne,
  init: re,
  insert_hydration: F,
  safe_not_equal: ae,
  set_custom_element_data: zt,
  space: oe,
  transition_in: x,
  transition_out: Q,
  update_slot_base: ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: se,
  getContext: le,
  onDestroy: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ft(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), a = $t(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Ct("svelte-slot"), a && a.c(), this.h();
    },
    l(o) {
      t = St(o, "SVELTE-SLOT", {
        class: !0
      });
      var i = vt(t);
      a && a.l(i), i.forEach(v), this.h();
    },
    h() {
      zt(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      F(o, t, i), a && a.m(t, null), e[9](t), n = !0;
    },
    p(o, i) {
      a && a.p && (!n || i & /*$$scope*/
      64) && ie(
        a,
        r,
        o,
        /*$$scope*/
        o[6],
        n ? ee(
          r,
          /*$$scope*/
          o[6],
          i,
          null
        ) : te(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      n || (x(a, o), n = !0);
    },
    o(o) {
      Q(a, o), n = !1;
    },
    d(o) {
      o && v(t), a && a.d(o), e[9](null);
    }
  };
}
function de(e) {
  let t, n, r, a, o = (
    /*$$slots*/
    e[4].default && ft(e)
  );
  return {
    c() {
      t = Ct("react-portal-target"), n = oe(), o && o.c(), r = ut(), this.h();
    },
    l(i) {
      t = St(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), vt(t).forEach(v), n = Xt(i), o && o.l(i), r = ut(), this.h();
    },
    h() {
      zt(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      F(i, t, s), e[8](t), F(i, n, s), o && o.m(i, s), F(i, r, s), a = !0;
    },
    p(i, [s]) {
      /*$$slots*/
      i[4].default ? o ? (o.p(i, s), s & /*$$slots*/
      16 && x(o, 1)) : (o = ft(i), o.c(), x(o, 1), o.m(r.parentNode, r)) : o && (ne(), Q(o, 1, 1, () => {
        o = null;
      }), Qt());
    },
    i(i) {
      a || (x(o), a = !0);
    },
    o(i) {
      Q(o), a = !1;
    },
    d(i) {
      i && (v(t), v(n), v(r)), e[8](null), o && o.d(i);
    }
  };
}
function mt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function fe(e, t, n) {
  let r, a, {
    $$slots: o = {},
    $$scope: i
  } = t;
  const s = Vt(o);
  let {
    svelteInit: l
  } = t;
  const w = A(mt(t)), d = A();
  ct(e, d, (c) => n(0, r = c));
  const y = A();
  ct(e, y, (c) => n(1, a = c));
  const u = [], f = le("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: E,
    subSlotIndex: G
  } = Lt() || {}, W = l({
    parent: f,
    props: w,
    target: d,
    slot: y,
    slotKey: m,
    slotIndex: E,
    subSlotIndex: G,
    onDestroy(c) {
      u.push(c);
    }
  });
  ue("$$ms-gr-react-wrapper", W), se(() => {
    w.set(mt(t));
  }), ce(() => {
    u.forEach((c) => c());
  });
  function I(c) {
    lt[c ? "unshift" : "push"](() => {
      r = c, d.set(r);
    });
  }
  function P(c) {
    lt[c ? "unshift" : "push"](() => {
      a = c, y.set(a);
    });
  }
  return e.$$set = (c) => {
    n(17, t = st(st({}, t), dt(c))), "svelteInit" in c && n(5, l = c.svelteInit), "$$scope" in c && n(6, i = c.$$scope);
  }, t = dt(t), [r, a, d, y, s, l, i, o, I, P];
}
class me extends Jt {
  constructor(t) {
    super(), re(this, t, fe, de, ae, {
      svelteInit: 5
    });
  }
}
const ht = window.ms_globals.rerender, H = window.ms_globals.tree;
function he(e) {
  function t(n) {
    const r = A(), a = new me({
      ...n,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            slotKey: o.slotKey,
            nodes: []
          }, s = o.parent ?? H;
          return s.nodes = [...s.nodes, i], ht({
            createPortal: J,
            node: H
          }), o.onDestroy(() => {
            s.nodes = s.nodes.filter((l) => l.svelteInstance !== r), ht({
              createPortal: J,
              node: H
            });
          }), i;
        },
        ...n.props
      }
    });
    return r.set(a), a;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ye(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return typeof r == "number" && !pe.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function X(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(J(j.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: j.Children.toArray(e._reactElement.props.children).map((a) => {
        if (j.isValidElement(a) && a.props.__slot__) {
          const {
            portals: o,
            clonedElement: i
          } = X(a.props.el);
          return j.cloneElement(a, {
            ...a.props,
            el: i,
            children: [...j.Children.toArray(a.props.children), ...o]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((a) => {
    e.getEventListeners(a).forEach(({
      listener: i,
      type: s,
      useCapture: l
    }) => {
      n.addEventListener(s, i, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let a = 0; a < r.length; a++) {
    const o = r[a];
    if (o.nodeType === 1) {
      const {
        clonedElement: i,
        portals: s
      } = X(o);
      t.push(...s), n.appendChild(i);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function _e(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Rt = Nt(({
  slot: e,
  clone: t,
  className: n,
  style: r
}, a) => {
  const o = Tt(), [i, s] = jt([]);
  return bt(() => {
    var y;
    if (!o.current || !e)
      return;
    let l = e;
    function w() {
      let u = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (u = l.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), _e(a, u), n && u.classList.add(...n.split(" ")), r) {
        const f = ye(r);
        Object.keys(f).forEach((m) => {
          u.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var E;
        const {
          portals: f,
          clonedElement: m
        } = X(e);
        l = m, s(f), l.style.display = "contents", w(), (E = o.current) == null || E.appendChild(l);
      };
      u(), d = new window.MutationObserver(() => {
        var f, m;
        (f = o.current) != null && f.contains(l) && ((m = o.current) == null || m.removeChild(l)), u();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", w(), (y = o.current) == null || y.appendChild(l);
    return () => {
      var u, f;
      l.style.display = "", (u = o.current) != null && u.contains(l) && ((f = o.current) == null || f.removeChild(l)), d == null || d.disconnect();
    };
  }, [e, t, n, r, a]), j.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function we(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Z(e) {
  return Mt(() => we(e), [e]);
}
function Pe(e, t) {
  return e ? /* @__PURE__ */ z.jsx(Rt, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ge({
  key: e,
  setSlotParams: t,
  slots: n
}, r) {
  return n[e] ? (...a) => (t(e, a), Pe(n[e], {
    clone: !0,
    ...r
  })) : void 0;
}
var Ot = Symbol.for("immer-nothing"), pt = Symbol.for("immer-draftable"), h = Symbol.for("immer-state");
function _(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var S = Object.getPrototypeOf;
function C(e) {
  return !!e && !!e[h];
}
function b(e) {
  var t;
  return e ? It(e) || Array.isArray(e) || !!e[pt] || !!((t = e.constructor) != null && t[pt]) || K(e) || U(e) : !1;
}
var je = Object.prototype.constructor.toString();
function It(e) {
  if (!e || typeof e != "object") return !1;
  const t = S(e);
  if (t === null)
    return !0;
  const n = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return n === Object ? !0 : typeof n == "function" && Function.toString.call(n) === je;
}
function D(e, t) {
  L(e) === 0 ? Reflect.ownKeys(e).forEach((n) => {
    t(n, e[n], e);
  }) : e.forEach((n, r) => t(r, n, e));
}
function L(e) {
  const t = e[h];
  return t ? t.type_ : Array.isArray(e) ? 1 : K(e) ? 2 : U(e) ? 3 : 0;
}
function V(e, t) {
  return L(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function At(e, t, n) {
  const r = L(e);
  r === 2 ? e.set(t, n) : r === 3 ? e.add(n) : e[t] = n;
}
function be(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function K(e) {
  return e instanceof Map;
}
function U(e) {
  return e instanceof Set;
}
function g(e) {
  return e.copy_ || e.base_;
}
function $(e, t) {
  if (K(e))
    return new Map(e);
  if (U(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const n = It(e);
  if (t === !0 || t === "class_only" && !n) {
    const r = Object.getOwnPropertyDescriptors(e);
    delete r[h];
    let a = Reflect.ownKeys(r);
    for (let o = 0; o < a.length; o++) {
      const i = a[o], s = r[i];
      s.writable === !1 && (s.writable = !0, s.configurable = !0), (s.get || s.set) && (r[i] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: s.enumerable,
        value: e[i]
      });
    }
    return Object.create(S(e), r);
  } else {
    const r = S(e);
    if (r !== null && n)
      return {
        ...e
      };
    const a = Object.create(r);
    return Object.assign(a, e);
  }
}
function at(e, t = !1) {
  return B(e) || C(e) || !b(e) || (L(e) > 1 && (e.set = e.add = e.clear = e.delete = ke), Object.freeze(e), t && Object.entries(e).forEach(([n, r]) => at(r, !0))), e;
}
function ke() {
  _(2);
}
function B(e) {
  return Object.isFrozen(e);
}
var Ee = {};
function k(e) {
  const t = Ee[e];
  return t || _(0, e), t;
}
var R;
function Ft() {
  return R;
}
function ve(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function yt(e, t) {
  t && (k("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function tt(e) {
  et(e), e.drafts_.forEach(Se), e.drafts_ = null;
}
function et(e) {
  e === R && (R = e.parent_);
}
function _t(e) {
  return R = ve(R, e);
}
function Se(e) {
  const t = e[h];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function wt(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const n = t.drafts_[0];
  return e !== void 0 && e !== n ? (n[h].modified_ && (tt(t), _(4)), b(e) && (e = N(t, e), t.parent_ || T(t, e)), t.patches_ && k("Patches").generateReplacementPatches_(n[h].base_, e, t.patches_, t.inversePatches_)) : e = N(t, n, []), tt(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== Ot ? e : void 0;
}
function N(e, t, n) {
  if (B(t)) return t;
  const r = t[h];
  if (!r)
    return D(t, (a, o) => Pt(e, r, t, a, o, n)), t;
  if (r.scope_ !== e) return t;
  if (!r.modified_)
    return T(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    r.finalized_ = !0, r.scope_.unfinalizedDrafts_--;
    const a = r.copy_;
    let o = a, i = !1;
    r.type_ === 3 && (o = new Set(a), a.clear(), i = !0), D(o, (s, l) => Pt(e, r, a, s, l, n, i)), T(e, a, !1), n && e.patches_ && k("Patches").generatePatches_(r, n, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function Pt(e, t, n, r, a, o, i) {
  if (C(a)) {
    const s = o && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !V(t.assigned_, r) ? o.concat(r) : void 0, l = N(e, a, s);
    if (At(n, r, l), C(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else i && n.add(a);
  if (b(a) && !B(a)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    N(e, a), (!t || !t.scope_.parent_) && typeof r != "symbol" && Object.prototype.propertyIsEnumerable.call(n, r) && T(e, a);
  }
}
function T(e, t, n = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && at(t, n);
}
function Ce(e, t) {
  const n = Array.isArray(e), r = {
    type_: n ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : Ft(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let a = r, o = ot;
  n && (a = [r], o = O);
  const {
    revoke: i,
    proxy: s
  } = Proxy.revocable(a, o);
  return r.draft_ = s, r.revoke_ = i, s;
}
var ot = {
  get(e, t) {
    if (t === h) return e;
    const n = g(e);
    if (!V(n, t))
      return ze(e, n, t);
    const r = n[t];
    return e.finalized_ || !b(r) ? r : r === q(e.base_, t) ? (Y(e), e.copy_[t] = rt(r, e)) : r;
  },
  has(e, t) {
    return t in g(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(g(e));
  },
  set(e, t, n) {
    const r = xt(g(e), t);
    if (r != null && r.set)
      return r.set.call(e.draft_, n), !0;
    if (!e.modified_) {
      const a = q(g(e), t), o = a == null ? void 0 : a[h];
      if (o && o.base_ === n)
        return e.copy_[t] = n, e.assigned_[t] = !1, !0;
      if (be(n, a) && (n !== void 0 || V(e.base_, t))) return !0;
      Y(e), nt(e);
    }
    return e.copy_[t] === n && // special case: handle new props with value 'undefined'
    (n !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(n) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = n, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return q(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, Y(e), nt(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const n = g(e), r = Reflect.getOwnPropertyDescriptor(n, t);
    return r && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: r.enumerable,
      value: n[t]
    };
  },
  defineProperty() {
    _(11);
  },
  getPrototypeOf(e) {
    return S(e.base_);
  },
  setPrototypeOf() {
    _(12);
  }
}, O = {};
D(ot, (e, t) => {
  O[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
O.deleteProperty = function(e, t) {
  return O.set.call(this, e, t, void 0);
};
O.set = function(e, t, n) {
  return ot.set.call(this, e[0], t, n, e[0]);
};
function q(e, t) {
  const n = e[h];
  return (n ? g(n) : e)[t];
}
function ze(e, t, n) {
  var a;
  const r = xt(t, n);
  return r ? "value" in r ? r.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (a = r.get) == null ? void 0 : a.call(e.draft_)
  ) : void 0;
}
function xt(e, t) {
  if (!(t in e)) return;
  let n = S(e);
  for (; n; ) {
    const r = Object.getOwnPropertyDescriptor(n, t);
    if (r) return r;
    n = S(n);
  }
}
function nt(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && nt(e.parent_));
}
function Y(e) {
  e.copy_ || (e.copy_ = $(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var Re = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, n, r) => {
      if (typeof t == "function" && typeof n != "function") {
        const o = n;
        n = t;
        const i = this;
        return function(l = o, ...w) {
          return i.produce(l, (d) => n.call(this, d, ...w));
        };
      }
      typeof n != "function" && _(6), r !== void 0 && typeof r != "function" && _(7);
      let a;
      if (b(t)) {
        const o = _t(this), i = rt(t, void 0);
        let s = !0;
        try {
          a = n(i), s = !1;
        } finally {
          s ? tt(o) : et(o);
        }
        return yt(o, r), wt(a, o);
      } else if (!t || typeof t != "object") {
        if (a = n(t), a === void 0 && (a = t), a === Ot && (a = void 0), this.autoFreeze_ && at(a, !0), r) {
          const o = [], i = [];
          k("Patches").generateReplacementPatches_(t, a, o, i), r(o, i);
        }
        return a;
      } else _(1, t);
    }, this.produceWithPatches = (t, n) => {
      if (typeof t == "function")
        return (i, ...s) => this.produceWithPatches(i, (l) => t(l, ...s));
      let r, a;
      return [this.produce(t, n, (i, s) => {
        r = i, a = s;
      }), r, a];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    b(e) || _(8), C(e) && (e = Oe(e));
    const t = _t(this), n = rt(e, void 0);
    return n[h].isManual_ = !0, et(t), n;
  }
  finishDraft(e, t) {
    const n = e && e[h];
    (!n || !n.isManual_) && _(9);
    const {
      scope_: r
    } = n;
    return yt(r, t), wt(void 0, r);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let n;
    for (n = t.length - 1; n >= 0; n--) {
      const a = t[n];
      if (a.path.length === 0 && a.op === "replace") {
        e = a.value;
        break;
      }
    }
    n > -1 && (t = t.slice(n + 1));
    const r = k("Patches").applyPatches_;
    return C(e) ? r(e, t) : this.produce(e, (a) => r(a, t));
  }
};
function rt(e, t) {
  const n = K(e) ? k("MapSet").proxyMap_(e, t) : U(e) ? k("MapSet").proxySet_(e, t) : Ce(e, t);
  return (t ? t.scope_ : Ft()).drafts_.push(n), n;
}
function Oe(e) {
  return C(e) || _(10, e), Dt(e);
}
function Dt(e) {
  if (!b(e) || B(e)) return e;
  const t = e[h];
  let n;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, n = $(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    n = $(e, !0);
  return D(n, (r, a) => {
    At(n, r, Dt(a));
  }), t && (t.finalized_ = !1), n;
}
var p = new Re(), Ie = p.produce;
p.produceWithPatches.bind(p);
p.setAutoFreeze.bind(p);
p.setUseStrictShallowCopy.bind(p);
p.applyPatches.bind(p);
p.createDraft.bind(p);
p.finishDraft.bind(p);
const gt = {
  ar_EG: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ar_EG-DXu1XGvZ.js").then((t) => t.a), import("./ar-Ck6Th0ll.js").then((t) => t.a)]);
    return {
      antd: e,
      dayjs: "ar"
    };
  },
  az_AZ: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./az_AZ-BtIHEkbN.js").then((t) => t.a), import("./az-Bkj6DwS6.js").then((t) => t.a)]);
    return {
      antd: e,
      dayjs: "az"
    };
  },
  bg_BG: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./bg_BG-C57dl2m3.js").then((t) => t.b), import("./bg-2py63dEK.js").then((t) => t.b)]);
    return {
      antd: e,
      dayjs: "bg"
    };
  },
  bn_BD: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./bn_BD-o3YZ_Vna.js").then((t) => t.b), import("./bn-DcO3k2jT.js").then((t) => t.b)]);
    return {
      antd: e,
      dayjs: "bn"
    };
  },
  by_BY: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./by_BY-BymgKgbZ.js").then((t) => t.b),
      import("./be-DVvuMryA.js").then((t) => t.b)
      // Belarusian (Belarus)
    ]);
    return {
      antd: e,
      dayjs: "be"
    };
  },
  ca_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ca_ES-CmvM9GxM.js").then((t) => t.c), import("./ca-CJmdi-gC.js").then((t) => t.c)]);
    return {
      antd: e,
      dayjs: "ca"
    };
  },
  cs_CZ: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./cs_CZ-BvXmCFHL.js").then((t) => t.c), import("./cs-CyK38te6.js").then((t) => t.c)]);
    return {
      antd: e,
      dayjs: "cs"
    };
  },
  da_DK: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./da_DK-rMBWOO3G.js").then((t) => t.d), import("./da-jpM4Qzz5.js").then((t) => t.d)]);
    return {
      antd: e,
      dayjs: "da"
    };
  },
  de_DE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./de_DE-DT4V2lOA.js").then((t) => t.d), import("./de-JUuPZ0aj.js").then((t) => t.d)]);
    return {
      antd: e,
      dayjs: "de"
    };
  },
  el_GR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./el_GR-CdMBbwwb.js").then((t) => t.e), import("./el-hzz2wBrD.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "el"
    };
  },
  en_GB: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./en_GB-DVrARRcg.js").then((t) => t.e), import("./en-gb-ri8dQsKI.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "en-gb"
    };
  },
  en_US: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./en_US-egb-j-MZ.js").then((t) => t.e), import("./en-DoPRzsOK.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "en"
    };
  },
  es_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./es_ES-D2nrnCDT.js").then((t) => t.e), import("./es-Ir1sq4fE.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "es"
    };
  },
  et_EE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./et_EE-DGlg3Ak3.js").then((t) => t.e), import("./et-DfBeScDM.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "et"
    };
  },
  eu_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./eu_ES-iIwrI-Pe.js").then((t) => t.e),
      import("./eu-pTcChqo2.js").then((t) => t.e)
      // Basque
    ]);
    return {
      antd: e,
      dayjs: "eu"
    };
  },
  fa_IR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fa_IR-D23eSDEG.js").then((t) => t.f), import("./fa-Spy1R7A8.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fa"
    };
  },
  fi_FI: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fi_FI-BS4TiMRM.js").then((t) => t.f), import("./fi-pP9P9l-P.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fi"
    };
  },
  fr_BE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_BE-D1_Y2M3J.js").then((t) => t.f), import("./fr-i7iZvaT7.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr"
    };
  },
  fr_CA: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_CA-D-fTl9Uj.js").then((t) => t.f), import("./fr-ca-B-aA6SLq.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr-ca"
    };
  },
  fr_FR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_FR-BMzRQQ3b.js").then((t) => t.f), import("./fr-i7iZvaT7.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr"
    };
  },
  ga_IE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ga_IE-D0kBnOlc.js").then((t) => t.g),
      import("./ga-CiqmVY9W.js").then((t) => t.g)
      // Irish
    ]);
    return {
      antd: e,
      dayjs: "ga"
    };
  },
  gl_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./gl_ES-D0hrO0ks.js").then((t) => t.g),
      import("./gl-CCtlCy_4.js").then((t) => t.g)
      // Galician
    ]);
    return {
      antd: e,
      dayjs: "gl"
    };
  },
  he_IL: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./he_IL-Be8t_Cau.js").then((t) => t.h), import("./he-DXtAjAaI.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "he"
    };
  },
  hi_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hi_IN-DyGXuIPj.js").then((t) => t.h), import("./hi-BdO5RuhG.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hi"
    };
  },
  hr_HR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hr_HR-DhsJoiC1.js").then((t) => t.h), import("./hr-eg9cB2m9.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hr"
    };
  },
  hu_HU: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hu_HU-B2Hb13dz.js").then((t) => t.h), import("./hu-ZxMOhCp9.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hu"
    };
  },
  hy_AM: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./hy_AM-CGgKlzJj.js").then((t) => t.h),
      import("./am-CV6UGDqa.js").then((t) => t.a)
      // Armenian
    ]);
    return {
      antd: e,
      dayjs: "am"
    };
  },
  id_ID: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./id_ID-DeKNuHbn.js").then((t) => t.i), import("./id-NrGfwF78.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "id"
    };
  },
  is_IS: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./is_IS-BVlj6g5Y.js").then((t) => t.i), import("./is-BNrApygP.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "is"
    };
  },
  it_IT: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./it_IT-B4bVNybT.js").then((t) => t.i), import("./it-CY_RfJMm.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "it"
    };
  },
  ja_JP: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ja_JP-FNs4_zZv.js").then((t) => t.j), import("./ja-rAEfi78a.js").then((t) => t.j)]);
    return {
      antd: e,
      dayjs: "ja"
    };
  },
  ka_GE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ka_GE-Bk1x9N0N.js").then((t) => t.k),
      import("./ka-BIsfuEWl.js").then((t) => t.k)
      // Georgian
    ]);
    return {
      antd: e,
      dayjs: "ka"
    };
  },
  kk_KZ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./kk_KZ-_YzfOHks.js").then((t) => t.k),
      import("./kk-C5F6k8yv.js").then((t) => t.k)
      // Kazakh
    ]);
    return {
      antd: e,
      dayjs: "kk"
    };
  },
  km_KH: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./km_KH-DUIksZhj.js").then((t) => t.k),
      import("./km-DzQpM0wN.js").then((t) => t.k)
      // Khmer
    ]);
    return {
      antd: e,
      dayjs: "km"
    };
  },
  kmr_IQ: async () => {
    const [e] = await Promise.all([
      import("./kmr_IQ-CxTsey8L.js").then((t) => t.k)
      // Not available in Day.js, so no need to load a locale file.
    ]);
    return {
      antd: e.default,
      dayjs: ""
    };
  },
  kn_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./kn_IN-vqiUotwC.js").then((t) => t.k),
      import("./kn-a2CctB2d.js").then((t) => t.k)
      // Kannada
    ]);
    return {
      antd: e,
      dayjs: "kn"
    };
  },
  ko_KR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ko_KR-BTVzuL_0.js").then((t) => t.k), import("./ko-CluNwiQc.js").then((t) => t.k)]);
    return {
      antd: e,
      dayjs: "ko"
    };
  },
  ku_IQ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ku_IQ-Q4S8_UzZ.js").then((t) => t.k),
      import("./ku-C38LKggM.js").then((t) => t.k)
      // Kurdish (Central)
    ]);
    return {
      antd: e,
      dayjs: "ku"
    };
  },
  lt_LT: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./lt_LT-Crmi0Dk6.js").then((t) => t.l), import("./lt-BS4cFAJ6.js").then((t) => t.l)]);
    return {
      antd: e,
      dayjs: "lt"
    };
  },
  lv_LV: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./lv_LV-DVVrYZe6.js").then((t) => t.l), import("./lv-nhSWPvDD.js").then((t) => t.l)]);
    return {
      antd: e,
      dayjs: "lv"
    };
  },
  mk_MK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./mk_MK-Bw58BLY7.js").then((t) => t.m),
      import("./mk-CJaF-C0c.js").then((t) => t.m)
      // Macedonian
    ]);
    return {
      antd: e,
      dayjs: "mk"
    };
  },
  ml_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ml_IN-C24sOdFb.js").then((t) => t.m),
      import("./ml-DfBv3qhW.js").then((t) => t.m)
      // Malayalam
    ]);
    return {
      antd: e,
      dayjs: "ml"
    };
  },
  mn_MN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./mn_MN-DrPYm927.js").then((t) => t.m),
      import("./mn-DxvqzIqh.js").then((t) => t.m)
      // Mongolian
    ]);
    return {
      antd: e,
      dayjs: "mn"
    };
  },
  ms_MY: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ms_MY-DMSuimU8.js").then((t) => t.m), import("./ms-CBBoGRan.js").then((t) => t.m)]);
    return {
      antd: e,
      dayjs: "ms"
    };
  },
  my_MM: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./my_MM-BdHsh9EB.js").then((t) => t.m),
      import("./my-pKPkW2NC.js").then((t) => t.m)
      // Burmese
    ]);
    return {
      antd: e,
      dayjs: "my"
    };
  },
  nb_NO: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nb_NO-Cw1cFLnD.js").then((t) => t.n),
      import("./nb-mgEziIBT.js").then((t) => t.n)
      // Norwegian Bokmål
    ]);
    return {
      antd: e,
      dayjs: "nb"
    };
  },
  ne_NP: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ne_NP-BlR_MxJM.js").then((t) => t.n),
      import("./ne-DCBXPTSr.js").then((t) => t.n)
      // Nepali
    ]);
    return {
      antd: e,
      dayjs: "ne"
    };
  },
  nl_BE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nl_BE-CPe57EOD.js").then((t) => t.n),
      import("./nl-be-BF47khjh.js").then((t) => t.n)
      // Dutch (Belgium)
    ]);
    return {
      antd: e,
      dayjs: "nl-be"
    };
  },
  nl_NL: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nl_NL-BVf2dwtP.js").then((t) => t.n),
      import("./nl-CBngIIii.js").then((t) => t.n)
      // Dutch (Netherlands)
    ]);
    return {
      antd: e,
      dayjs: "nl"
    };
  },
  pl_PL: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./pl_PL-C0kfEy5R.js").then((t) => t.p), import("./pl-BoIYteYg.js").then((t) => t.p)]);
    return {
      antd: e,
      dayjs: "pl"
    };
  },
  pt_BR: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./pt_BR-_p3WGyDT.js").then((t) => t.p),
      import("./pt-br-DSnM3Gc7.js").then((t) => t.p)
      // Portuguese (Brazil)
    ]);
    return {
      antd: e,
      dayjs: "pt-br"
    };
  },
  pt_PT: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./pt_PT-B9ocJu4A.js").then((t) => t.p),
      import("./pt-dtCKTrQu.js").then((t) => t.p)
      // Portuguese (Portugal)
    ]);
    return {
      antd: e,
      dayjs: "pt"
    };
  },
  ro_RO: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ro_RO-C4iMXsqc.js").then((t) => t.r), import("./ro-BeOxhsUp.js").then((t) => t.r)]);
    return {
      antd: e,
      dayjs: "ro"
    };
  },
  ru_RU: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ru_RU-BczoH71V.js").then((t) => t.r), import("./ru-DgPmdrPT.js").then((t) => t.r)]);
    return {
      antd: e,
      dayjs: "ru"
    };
  },
  si_LK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./si_LK-B8at1O3X.js").then((t) => t.s),
      import("./si-BDfiJECy.js").then((t) => t.s)
      // Sinhala
    ]);
    return {
      antd: e,
      dayjs: "si"
    };
  },
  sk_SK: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sk_SK-098uxbVS.js").then((t) => t.s), import("./sk-BrmGzdVk.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sk"
    };
  },
  sl_SI: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sl_SI-B1tNObDC.js").then((t) => t.s), import("./sl-Dy1025Bu.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sl"
    };
  },
  sr_RS: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./sr_RS-CcUzhwGZ.js").then((t) => t.s),
      import("./sr-DfuU0V7U.js").then((t) => t.s)
      // Serbian
    ]);
    return {
      antd: e,
      dayjs: "sr"
    };
  },
  sv_SE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sv_SE-C7YRa_lc.js").then((t) => t.s), import("./sv-CbJaOH2j.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sv"
    };
  },
  ta_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ta_IN-Bp00Qfz8.js").then((t) => t.t),
      import("./ta-CXeayFHm.js").then((t) => t.t)
      // Tamil
    ]);
    return {
      antd: e,
      dayjs: "ta"
    };
  },
  th_TH: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./th_TH-C8fF9CyU.js").then((t) => t.t), import("./th-ClRa7mf_.js").then((t) => t.t)]);
    return {
      antd: e,
      dayjs: "th"
    };
  },
  tk_TK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./tk_TK-gY71Nf7B.js").then((t) => t.t),
      import("./tk-DS8yv5iK.js").then((t) => t.t)
      // Turkmen
    ]);
    return {
      antd: e,
      dayjs: "tk"
    };
  },
  tr_TR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./tr_TR-CbvszlPM.js").then((t) => t.t), import("./tr-BOWb6omD.js").then((t) => t.t)]);
    return {
      antd: e,
      dayjs: "tr"
    };
  },
  uk_UA: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./uk_UA-7WLRAnnY.js").then((t) => t.u),
      import("./uk-6TnifFr8.js").then((t) => t.u)
      // Ukrainian
    ]);
    return {
      antd: e,
      dayjs: "uk"
    };
  },
  ur_PK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ur_PK-D08-DhkX.js").then((t) => t.u),
      import("./ur-BfzoT-bq.js").then((t) => t.u)
      // Urdu
    ]);
    return {
      antd: e,
      dayjs: "ur"
    };
  },
  uz_UZ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./uz_UZ-CMwnzz88.js").then((t) => t.u),
      import("./uz-CNjnbpur.js").then((t) => t.u)
      // Uzbek
    ]);
    return {
      antd: e,
      dayjs: "uz"
    };
  },
  vi_VN: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./vi_VN-aAc8wk0T.js").then((t) => t.v), import("./vi-x72YrX0I.js").then((t) => t.v)]);
    return {
      antd: e,
      dayjs: "vi"
    };
  },
  zh_CN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_CN-CEhgo0Cb.js").then((t) => t.z),
      import("./zh-cn-6Uj8Tdpu.js").then((t) => t.z)
      // Chinese (Simplified)
    ]);
    return {
      antd: e,
      dayjs: "zh-cn"
    };
  },
  zh_HK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_HK-vUuhE9Nz.js").then((t) => t.z),
      import("./zh-hk-C1APFz5J.js").then((t) => t.z)
      // Chinese (Hong Kong)
    ]);
    return {
      antd: e,
      dayjs: "zh-hk"
    };
  },
  zh_TW: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_TW-j_zWwazB.js").then((t) => t.z),
      import("./zh-tw-BLm3v1Sv.js").then((t) => t.z)
      // Chinese (Taiwan)
    ]);
    return {
      antd: e,
      dayjs: "zh-tw"
    };
  }
}, Ae = (e, t) => Ie(e, (n) => {
  Object.keys(t).forEach((r) => {
    const a = r.split(".");
    let o = n;
    for (let i = 0; i < a.length - 1; i++) {
      const s = a[i];
      o[s] || (o[s] = {}), o = o[s];
    }
    o[a[a.length - 1]] = /* @__PURE__ */ z.jsx(Rt, {
      slot: t[r],
      clone: !0
    });
  });
}), xe = he(({
  slots: e,
  themeMode: t,
  id: n,
  className: r,
  style: a,
  locale: o,
  getTargetContainer: i,
  getPopupContainer: s,
  renderEmpty: l,
  setSlotParams: w,
  children: d,
  ...y
}) => {
  var I;
  const [u, f] = jt(), m = {
    dark: t === "dark",
    ...((I = y.theme) == null ? void 0 : I.algorithm) || {}
  }, E = Z(s), G = Z(i), W = Z(l);
  return bt(() => {
    o && gt[o] && gt[o]().then(({
      antd: P,
      dayjs: c
    }) => {
      f(P), Bt.locale(c);
    });
  }, [o]), /* @__PURE__ */ z.jsx("div", {
    id: n,
    className: r,
    style: a,
    children: /* @__PURE__ */ z.jsx(Kt, {
      hashPriority: "high",
      container: document.body,
      children: /* @__PURE__ */ z.jsx(Ut, {
        prefixCls: "ms-gr-ant",
        ...Ae(y, e),
        locale: u,
        getPopupContainer: E,
        getTargetContainer: G,
        renderEmpty: e.renderEmpty ? ge({
          slots: e,
          setSlotParams: w,
          key: "renderEmpty"
        }) : W,
        theme: {
          cssVar: !0,
          ...y.theme,
          algorithm: Object.keys(m).map((P) => {
            switch (P) {
              case "dark":
                return m[P] ? it.darkAlgorithm : null;
              case "compact":
                return m[P] ? it.compactAlgorithm : null;
              default:
                return null;
            }
          }).filter(Boolean)
        },
        children: d
      })
    })
  });
});
export {
  xe as ConfigProvider,
  xe as default
};
