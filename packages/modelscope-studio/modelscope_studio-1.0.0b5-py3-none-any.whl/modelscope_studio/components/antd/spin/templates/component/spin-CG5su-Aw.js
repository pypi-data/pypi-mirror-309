import { g as X, w as b } from "./Index-DXcMikxc.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Spin;
var W = {
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !oe.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: re.current
  };
}
v.Fragment = te;
v.jsx = z;
v.jsxs = z;
W.exports = v;
var C = W.exports;
const {
  SvelteComponent: se,
  assign: O,
  binding_callbacks: k,
  check_outros: le,
  children: F,
  claim_element: G,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: ce,
  create_slot: ae,
  detach: h,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: pe,
  insert_hydration: y,
  safe_not_equal: _e,
  set_custom_element_data: H,
  space: me,
  transition_in: E,
  transition_out: x,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function j(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ae(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = F(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && he(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (E(r, e), o = !0);
    },
    o(e) {
      x(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = U("react-portal-target"), o = me(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), F(t).forEach(h), o = ie(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), n[8](t), y(s, o, c), e && e.m(s, c), y(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && E(e, 1)) : (e = j(s), e.c(), E(e, 1), e.m(l.parentNode, l)) : e && (fe(), x(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      r || (E(e), r = !0);
    },
    o(s) {
      x(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function N(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = b(N(t)), f = b();
  P(n, f, (a) => o(0, l = a));
  const _ = b();
  P(n, _, (a) => o(1, r = a));
  const d = [], u = we("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: K
  } = X() || {}, M = i({
    parent: u,
    props: g,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: K,
    onDestroy(a) {
      d.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", M), ge(() => {
    g.set(N(t));
  }), be(() => {
    d.forEach((a) => a());
  });
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function V(a) {
    k[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = O(O({}, t), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = T(t), [l, r, f, _, c, i, s, e, q, V];
}
class Ce extends se {
  constructor(t) {
    super(), pe(this, t, ve, Ee, _e, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const l = b(), r = new Ce({
      ...o,
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: S
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Re.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function I(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = I(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = I(e);
      t.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = B(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = xe(l);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var w;
        const {
          portals: u,
          clonedElement: p
        } = I(n);
        i = p, c(u), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(i) && ((p = e.current) == null || p.removeChild(i)), d();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), ke = Se(({
  slots: n,
  ...t
}) => /* @__PURE__ */ C.jsx(Z, {
  ...t,
  tip: n.tip ? /* @__PURE__ */ C.jsx(D, {
    slot: n.tip
  }) : t.tip,
  indicator: n.indicator ? /* @__PURE__ */ C.jsx(D, {
    slot: n.indicator
  }) : t.indicator
}));
export {
  ke as Spin,
  ke as default
};
