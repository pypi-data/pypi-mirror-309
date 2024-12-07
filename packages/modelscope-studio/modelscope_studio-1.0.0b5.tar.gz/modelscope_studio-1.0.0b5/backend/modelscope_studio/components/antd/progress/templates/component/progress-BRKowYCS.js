import { g as G, w as d } from "./Index-DRwWsSRz.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Progress;
var T = {
  exports: {}
}, g = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var V = z, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(o, t, r) {
  var l, n = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) Q.call(t, l) && !Z.hasOwnProperty(l) && (n[l] = t[l]);
  if (o && o.defaultProps) for (l in t = o.defaultProps, t) n[l] === void 0 && (n[l] = t[l]);
  return {
    $$typeof: Y,
    type: o,
    key: e,
    ref: s,
    props: n,
    _owner: X.current
  };
}
g.Fragment = H;
g.jsx = C;
g.jsxs = C;
T.exports = g;
var $ = T.exports;
const {
  SvelteComponent: ee,
  assign: I,
  binding_callbacks: k,
  check_outros: te,
  children: j,
  claim_element: D,
  claim_space: se,
  component_subscribe: R,
  compute_slots: oe,
  create_slot: ne,
  detach: c,
  element: F,
  empty: E,
  exclude_internal_props: P,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ie,
  init: ae,
  insert_hydration: m,
  safe_not_equal: ce,
  set_custom_element_data: L,
  space: ue,
  transition_in: p,
  transition_out: b,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(o) {
  let t, r;
  const l = (
    /*#slots*/
    o[7].default
  ), n = ne(
    l,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(t);
      n && n.l(s), s.forEach(c), this.h();
    },
    h() {
      L(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && _e(
        n,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? le(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : re(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (p(n, e), r = !0);
    },
    o(e) {
      b(n, e), r = !1;
    },
    d(e) {
      e && c(t), n && n.d(e), o[9](null);
    }
  };
}
function ge(o) {
  let t, r, l, n, e = (
    /*$$slots*/
    o[4].default && S(o)
  );
  return {
    c() {
      t = F("react-portal-target"), r = ue(), e && e.c(), l = E(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(c), r = se(s), e && e.l(s), l = E(), this.h();
    },
    h() {
      L(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      m(s, t, a), o[8](t), m(s, r, a), e && e.m(s, a), m(s, l, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && p(e, 1)) : (e = S(s), e.c(), p(e, 1), e.m(l.parentNode, l)) : e && (ie(), b(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(s) {
      n || (p(e), n = !0);
    },
    o(s) {
      b(e), n = !1;
    },
    d(s) {
      s && (c(t), c(r), c(l)), o[8](null), e && e.d(s);
    }
  };
}
function x(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function we(o, t, r) {
  let l, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = oe(e);
  let {
    svelteInit: u
  } = t;
  const h = d(x(t)), _ = d();
  R(o, _, (i) => r(0, l = i));
  const f = d();
  R(o, f, (i) => r(1, n = i));
  const v = [], A = de("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = G() || {}, M = u({
    parent: A,
    props: h,
    target: _,
    slot: f,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(i) {
      v.push(i);
    }
  });
  pe("$$ms-gr-react-wrapper", M), fe(() => {
    h.set(x(t));
  }), me(() => {
    v.forEach((i) => i());
  });
  function U(i) {
    k[i ? "unshift" : "push"](() => {
      l = i, _.set(l);
    });
  }
  function W(i) {
    k[i ? "unshift" : "push"](() => {
      n = i, f.set(n);
    });
  }
  return o.$$set = (i) => {
    r(17, t = I(I({}, t), P(i))), "svelteInit" in i && r(5, u = i.svelteInit), "$$scope" in i && r(6, s = i.$$scope);
  }, t = P(t), [l, n, _, f, a, u, s, e, U, W];
}
class be extends ee {
  constructor(t) {
    super(), ae(this, t, we, ge, ce, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, w = window.ms_globals.tree;
function he(o) {
  function t(r) {
    const l = d(), n = new be({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? w;
          return a.nodes = [...a.nodes, s], O({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((u) => u.svelteInstance !== l), O({
              createPortal: y,
              node: w
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function ve(o) {
  try {
    return typeof o == "string" ? new Function(`return (...args) => (${o})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ye(o) {
  return B(() => ve(o), [o]);
}
const ke = he(({
  format: o,
  ...t
}) => {
  const r = ye(o);
  return /* @__PURE__ */ $.jsx(J, {
    ...t,
    format: r
  });
});
export {
  ke as Progress,
  ke as default
};
