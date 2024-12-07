import { g as G, w as d } from "./Index-Bycfx9Y2.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Affix;
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
function C(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) Q.call(t, l) && !Z.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: Y,
    type: n,
    key: e,
    ref: s,
    props: o,
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
  children: A,
  claim_element: j,
  claim_space: se,
  component_subscribe: x,
  compute_slots: ne,
  create_slot: oe,
  detach: c,
  element: D,
  empty: R,
  exclude_internal_props: E,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ie,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ce,
  set_custom_element_data: F,
  space: ue,
  transition_in: m,
  transition_out: b,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: pe,
  setContext: me
} = window.__gradio__svelte__internal;
function S(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = oe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = j(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = A(t);
      o && o.l(s), s.forEach(c), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && _e(
        o,
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
      r || (m(o, e), r = !0);
    },
    o(e) {
      b(o, e), r = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), n[9](null);
    }
  };
}
function ge(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = D("react-portal-target"), r = ue(), e && e.c(), l = R(), this.h();
    },
    l(s) {
      t = j(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), A(t).forEach(c), r = se(s), e && e.l(s), l = R(), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      p(s, t, a), n[8](t), p(s, r, a), e && e.m(s, a), p(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && m(e, 1)) : (e = S(s), e.c(), m(e, 1), e.m(l.parentNode, l)) : e && (ie(), b(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      b(e), o = !1;
    },
    d(s) {
      s && (c(t), c(r), c(l)), n[8](null), e && e.d(s);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function we(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ne(e);
  let {
    svelteInit: u
  } = t;
  const h = d(O(t)), _ = d();
  x(n, _, (i) => r(0, l = i));
  const f = d();
  x(n, f, (i) => r(1, o = i));
  const v = [], L = de("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = G() || {}, M = u({
    parent: L,
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
  me("$$ms-gr-react-wrapper", M), fe(() => {
    h.set(O(t));
  }), pe(() => {
    v.forEach((i) => i());
  });
  function U(i) {
    k[i ? "unshift" : "push"](() => {
      l = i, _.set(l);
    });
  }
  function W(i) {
    k[i ? "unshift" : "push"](() => {
      o = i, f.set(o);
    });
  }
  return n.$$set = (i) => {
    r(17, t = I(I({}, t), E(i))), "svelteInit" in i && r(5, u = i.svelteInit), "$$scope" in i && r(6, s = i.$$scope);
  }, t = E(t), [l, o, _, f, a, u, s, e, U, W];
}
class be extends ee {
  constructor(t) {
    super(), ae(this, t, we, ge, ce, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function he(n) {
  function t(r) {
    const l = d(), o = new be({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? w;
          return a.nodes = [...a.nodes, s], P({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((u) => u.svelteInstance !== l), P({
              createPortal: y,
              node: w
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function ve(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function ye(n) {
  return B(() => ve(n), [n]);
}
const ke = he(({
  target: n,
  ...t
}) => {
  const r = ye(n);
  return /* @__PURE__ */ $.jsx(J, {
    ...t,
    target: r
  });
});
export {
  ke as Affix,
  ke as default
};
