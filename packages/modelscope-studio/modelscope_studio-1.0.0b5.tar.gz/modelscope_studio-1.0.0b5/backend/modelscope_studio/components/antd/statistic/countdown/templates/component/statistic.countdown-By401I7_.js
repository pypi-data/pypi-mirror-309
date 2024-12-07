import { g as X, w as y } from "./Index-3EHOKVb7.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Statistic;
var F = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $ = h, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
x.Fragment = te;
x.jsx = W;
x.jsxs = W;
F.exports = x;
var m = F.exports;
const {
  SvelteComponent: se,
  assign: k,
  binding_callbacks: P,
  check_outros: le,
  children: z,
  claim_element: G,
  claim_space: ie,
  component_subscribe: j,
  compute_slots: ce,
  create_slot: ae,
  detach: g,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: pe,
  set_custom_element_data: H,
  space: me,
  transition_in: v,
  transition_out: I,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = z(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && he(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (v(o, e), r = !0);
    },
    o(e) {
      I(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = U("react-portal-target"), r = me(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(g), r = ie(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, t, c), n[8](t), E(l, r, c), e && e.m(l, c), E(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (fe(), I(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      o || (v(e), o = !0);
    },
    o(l) {
      I(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ve(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const w = y(A(t)), f = y();
  j(n, f, (a) => r(0, s = a));
  const p = y();
  j(n, p, (a) => r(1, o = a));
  const d = [], u = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: K
  } = X() || {}, M = i({
    parent: u,
    props: w,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: K,
    onDestroy(a) {
      d.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", M), ge(() => {
    w.set(A(t));
  }), be(() => {
    d.forEach((a) => a());
  });
  function q(a) {
    P[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function V(a) {
    P[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = k(k({}, t), T(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = T(t), [s, o, f, p, c, i, l, e, q, V];
}
class xe extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, C = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const s = y(), o = new xe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? C;
          return c.nodes = [...c.nodes, l], D({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: R,
              node: C
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Se.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function O(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      t.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const S = B(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(o, d), r && d.classList.add(...r.split(" ")), s) {
        const u = Re(s);
        Object.keys(u).forEach((_) => {
          d.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b;
        const {
          portals: u,
          clonedElement: _
        } = O(n);
        i = _, c(u), i.style.display = "contents", w(), (b = e.current) == null || b.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, _;
        (u = e.current) != null && u.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, s, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), ke = Ce(({
  children: n,
  value: t,
  slots: r,
  ...s
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: n
  }), /* @__PURE__ */ m.jsx(Z.Countdown, {
    ...s,
    value: typeof t == "number" ? t * 1e3 : t,
    title: r.title ? /* @__PURE__ */ m.jsx(S, {
      slot: r.title
    }) : s.title,
    prefix: r.prefix ? /* @__PURE__ */ m.jsx(S, {
      slot: r.prefix
    }) : s.prefix,
    suffix: r.suffix ? /* @__PURE__ */ m.jsx(S, {
      slot: r.suffix
    }) : s.suffix
  })]
}));
export {
  ke as StatisticCountdown,
  ke as default
};
