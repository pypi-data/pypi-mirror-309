import { g as X, w as E } from "./Index-CyzaNeHG.js";
const h = window.ms_globals.React, V = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, S = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.FloatButton;
var D = {
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
var $ = h, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !re.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: oe.current
  };
}
x.Fragment = te;
x.jsx = W;
x.jsxs = W;
D.exports = x;
var p = D.exports;
const {
  SvelteComponent: le,
  assign: k,
  binding_callbacks: P,
  check_outros: se,
  children: z,
  claim_element: B,
  claim_space: ie,
  component_subscribe: j,
  compute_slots: ce,
  create_slot: ae,
  detach: g,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: U,
  space: me,
  transition_in: C,
  transition_out: I,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: we,
  setContext: ye
} = window.__gradio__svelte__internal;
function N(n) {
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
      t = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), r && r.m(t, null), n[9](t), o = !0;
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
      o || (C(r, e), o = !0);
    },
    o(e) {
      I(r, e), o = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = G("react-portal-target"), o = me(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(g), o = ie(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, t, c), n[8](t), v(s, o, c), e && e.m(s, c), v(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = N(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (fe(), I(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      r || (C(e), r = !0);
    },
    o(s) {
      I(e), r = !1;
    },
    d(s) {
      s && (g(t), g(o), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function A(n) {
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
  const b = E(A(t)), f = E();
  j(n, f, (a) => o(0, l = a));
  const m = E();
  j(n, m, (a) => o(1, r = a));
  const d = [], u = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H
  } = X() || {}, K = i({
    parent: u,
    props: b,
    target: f,
    slot: m,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(a) {
      d.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", K), ge(() => {
    b.set(A(t));
  }), we(() => {
    d.forEach((a) => a());
  });
  function M(a) {
    P[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function q(a) {
    P[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = k(k({}, t), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = T(t), [l, r, f, m, c, i, s, e, M, q];
}
class Ce extends le {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, R = window.ms_globals.tree;
function xe(n) {
  function t(o) {
    const l = E(), r = new Ce({
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
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, s], F({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), F({
              createPortal: S,
              node: R
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
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Re.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function O(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
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
      } = O(e);
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
const y = V(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function b() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Se(l);
        Object.keys(u).forEach((_) => {
          d.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var w;
        const {
          portals: u,
          clonedElement: _
        } = O(n);
        i = _, c(u), i.style.display = "contents", b(), (w = e.current) == null || w.appendChild(i);
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
      i.style.display = "contents", b(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, o, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), ke = xe(({
  slots: n,
  children: t,
  ...o
}) => {
  var l;
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(Z, {
      ...o,
      icon: n.icon ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: n.icon
      }) : o.icon,
      description: n.description ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: n.description
      }) : o.description,
      tooltip: n.tooltip ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: n.tooltip
      }) : o.tooltip,
      badge: {
        ...o.badge,
        count: n["badge.count"] ? /* @__PURE__ */ p.jsx(y, {
          slot: n["badge.count"]
        }) : (l = o.badge) == null ? void 0 : l.count
      }
    })]
  });
});
export {
  ke as FloatButton,
  ke as default
};
