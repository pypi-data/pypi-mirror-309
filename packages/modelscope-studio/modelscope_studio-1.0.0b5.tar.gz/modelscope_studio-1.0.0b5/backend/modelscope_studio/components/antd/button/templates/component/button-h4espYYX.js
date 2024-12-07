import { g as Q, w as b } from "./Index-CQjJkuGd.js";
const m = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Button;
var D = {
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) te.call(t, l) && !oe.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ne.current
  };
}
v.Fragment = ee;
v.jsx = W;
v.jsxs = W;
D.exports = v;
var I = D.exports;
const {
  SvelteComponent: re,
  assign: O,
  binding_callbacks: k,
  check_outros: se,
  children: z,
  claim_element: B,
  claim_space: le,
  component_subscribe: P,
  compute_slots: ie,
  create_slot: ce,
  detach: h,
  element: F,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ae,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: y,
  safe_not_equal: _e,
  set_custom_element_data: G,
  space: pe,
  transition_in: E,
  transition_out: S,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ce(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && me(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? de(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (E(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = F("react-portal-target"), r = pe(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(h), r = le(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), n[8](t), y(s, r, c), e && e.m(s, c), y(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && E(e, 1)) : (e = N(s), e.c(), E(e, 1), e.m(l.parentNode, l)) : e && (ue(), S(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      o || (E(e), o = !0);
    },
    o(s) {
      S(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function j(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ee(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = b(j(t)), f = b();
  P(n, f, (a) => r(0, l = a));
  const p = b();
  P(n, p, (a) => r(1, o = a));
  const d = [], u = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: U
  } = Q() || {}, H = i({
    parent: u,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: U,
    onDestroy(a) {
      d.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", H), he(() => {
    g.set(j(t));
  }), we(() => {
    d.forEach((a) => a());
  });
  function K(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function M(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = O(O({}, t), T(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = T(t), [l, o, f, p, c, i, s, e, K, M];
}
class ve extends re {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const l = b(), o = new ve({
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
          }, c = e.parent ?? C;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: C
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Re.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function x(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = x(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...m.Children.toArray(o.props.children), ...e]
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = x(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = q(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = V(), [s, c] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(o, d), r && d.classList.add(...r.split(" ")), l) {
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
        } = x(n);
        i = _, c(u), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
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
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, l, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), ke = Ce(({
  slots: n,
  ...t
}) => /* @__PURE__ */ I.jsx(X, {
  ...t,
  icon: n.icon ? /* @__PURE__ */ I.jsx(Ie, {
    slot: n.icon
  }) : t.icon
}));
export {
  ke as Button,
  ke as default
};
