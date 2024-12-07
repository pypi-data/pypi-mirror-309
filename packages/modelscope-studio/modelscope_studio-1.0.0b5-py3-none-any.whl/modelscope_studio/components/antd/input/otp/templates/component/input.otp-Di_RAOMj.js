import { b as Y, g as H, w as d } from "./Index-EAbdYoMi.js";
const B = window.ms_globals.React, G = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, h = window.ms_globals.React.useRef, R = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Input;
function X(s, t) {
  return Y(s, t);
}
var C = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Z = B, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, se = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(s, t, n) {
  var l, o = {}, e = null, r = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (l in t) te.call(t, l) && !ne.hasOwnProperty(l) && (o[l] = t[l]);
  if (s && s.defaultProps) for (l in t = s.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: $,
    type: s,
    key: e,
    ref: r,
    props: o,
    _owner: se.current
  };
}
w.Fragment = ee;
w.jsx = D;
w.jsxs = D;
C.exports = w;
var oe = C.exports;
const {
  SvelteComponent: re,
  assign: E,
  binding_callbacks: k,
  check_outros: le,
  children: F,
  claim_element: L,
  claim_space: ue,
  component_subscribe: S,
  compute_slots: ae,
  create_slot: ce,
  detach: i,
  element: V,
  empty: O,
  exclude_internal_props: x,
  get_all_dirty_from_scope: ie,
  get_slot_changes: fe,
  group_outros: _e,
  init: de,
  insert_hydration: m,
  safe_not_equal: me,
  set_custom_element_data: q,
  space: pe,
  transition_in: p,
  transition_out: g,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ge,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function P(s) {
  let t, n;
  const l = (
    /*#slots*/
    s[7].default
  ), o = ce(
    l,
    s,
    /*$$scope*/
    s[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var r = F(t);
      o && o.l(r), r.forEach(i), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      m(e, t, r), o && o.m(t, null), s[9](t), n = !0;
    },
    p(e, r) {
      o && o.p && (!n || r & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        n ? fe(
          l,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (p(o, e), n = !0);
    },
    o(e) {
      g(o, e), n = !1;
    },
    d(e) {
      e && i(t), o && o.d(e), s[9](null);
    }
  };
}
function he(s) {
  let t, n, l, o, e = (
    /*$$slots*/
    s[4].default && P(s)
  );
  return {
    c() {
      t = V("react-portal-target"), n = pe(), e && e.c(), l = O(), this.h();
    },
    l(r) {
      t = L(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), F(t).forEach(i), n = ue(r), e && e.l(r), l = O(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(r, a) {
      m(r, t, a), s[8](t), m(r, n, a), e && e.m(r, a), m(r, l, a), o = !0;
    },
    p(r, [a]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, a), a & /*$$slots*/
      16 && p(e, 1)) : (e = P(r), e.c(), p(e, 1), e.m(l.parentNode, l)) : e && (_e(), g(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(r) {
      o || (p(e), o = !0);
    },
    o(r) {
      g(e), o = !1;
    },
    d(r) {
      r && (i(t), i(n), i(l)), s[8](null), e && e.d(r);
    }
  };
}
function T(s) {
  const {
    svelteInit: t,
    ...n
  } = s;
  return n;
}
function Re(s, t, n) {
  let l, o, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const a = ae(e);
  let {
    svelteInit: c
  } = t;
  const v = d(T(t)), f = d();
  S(s, f, (u) => n(0, l = u));
  const _ = d();
  S(s, _, (u) => n(1, o = u));
  const y = [], A = ge("$$ms-gr-react-wrapper"), {
    slotKey: M,
    slotIndex: N,
    subSlotIndex: K
  } = H() || {}, U = c({
    parent: A,
    props: v,
    target: f,
    slot: _,
    slotKey: M,
    slotIndex: N,
    subSlotIndex: K,
    onDestroy(u) {
      y.push(u);
    }
  });
  ye("$$ms-gr-react-wrapper", U), be(() => {
    v.set(T(t));
  }), ve(() => {
    y.forEach((u) => u());
  });
  function W(u) {
    k[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function z(u) {
    k[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return s.$$set = (u) => {
    n(17, t = E(E({}, t), x(u))), "svelteInit" in u && n(5, c = u.svelteInit), "$$scope" in u && n(6, r = u.$$scope);
  }, t = x(t), [l, o, f, _, a, c, r, e, W, z];
}
class Ie extends re {
  constructor(t) {
    super(), de(this, t, Re, he, me, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, b = window.ms_globals.tree;
function Ee(s) {
  function t(n) {
    const l = d(), o = new Ie({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: s,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? b;
          return a.nodes = [...a.nodes, r], j({
            createPortal: I,
            node: b
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== l), j({
              createPortal: I,
              node: b
            });
          }), r;
        },
        ...n.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
function ke(s) {
  try {
    return typeof s == "string" ? new Function(`return (...args) => (${s})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Se(s) {
  return G(() => ke(s), [s]);
}
function Oe({
  value: s,
  onValueChange: t
}) {
  const [n, l] = J(s), o = h(t);
  o.current = t;
  const e = h(n);
  return e.current = n, R(() => {
    o.current(n);
  }, [n]), R(() => {
    X(s, e.current) || l(s);
  }, [s]), [n, l];
}
const Pe = Ee(({
  formatter: s,
  onValueChange: t,
  onChange: n,
  elRef: l,
  ...o
}) => {
  const e = Se(s), [r, a] = Oe({
    onValueChange: t,
    value: o.value
  });
  return /* @__PURE__ */ oe.jsx(Q.OTP, {
    ...o,
    value: r,
    ref: l,
    formatter: e,
    onChange: (c) => {
      n == null || n(c), a(c);
    }
  });
});
export {
  Pe as InputOTP,
  Pe as default
};
