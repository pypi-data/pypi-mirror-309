import { g as Q, w as b } from "./Index-9Wo-6nMb.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, S = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Layout;
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) te.call(t, l) && !re.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: ne.current
  };
}
v.Fragment = ee;
v.jsx = W;
v.jsxs = W;
D.exports = v;
var I = D.exports;
const {
  SvelteComponent: oe,
  assign: O,
  binding_callbacks: k,
  check_outros: se,
  children: z,
  claim_element: F,
  claim_space: le,
  component_subscribe: L,
  compute_slots: ie,
  create_slot: ae,
  detach: g,
  element: G,
  empty: P,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ce,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: y,
  safe_not_equal: _e,
  set_custom_element_data: U,
  space: pe,
  transition_in: E,
  transition_out: R,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: he,
  onDestroy: we,
  setContext: be
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
      t = F(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && me(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ce(
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
      R(r, e), o = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = G("react-portal-target"), o = pe(), e && e.c(), l = P(), this.h();
    },
    l(s) {
      t = F(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(g), o = le(s), e && e.l(s), l = P(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      y(s, t, a), n[8](t), y(s, o, a), e && e.m(s, a), y(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && E(e, 1)) : (e = N(s), e.c(), E(e, 1), e.m(l.parentNode, l)) : e && (ue(), R(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      r || (E(e), r = !0);
    },
    o(s) {
      R(e), r = !1;
    },
    d(s) {
      s && (g(t), g(o), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function j(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ee(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ie(e);
  let {
    svelteInit: i
  } = t;
  const h = b(j(t)), f = b();
  L(n, f, (c) => o(0, l = c));
  const p = b();
  L(n, p, (c) => o(1, r = c));
  const d = [], u = he("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H
  } = Q() || {}, K = i({
    parent: u,
    props: h,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(c) {
      d.push(c);
    }
  });
  be("$$ms-gr-react-wrapper", K), ge(() => {
    h.set(j(t));
  }), we(() => {
    d.forEach((c) => c());
  });
  function M(c) {
    k[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function q(c) {
    k[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = O(O({}, t), T(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = T(t), [l, r, f, p, a, i, s, e, M, q];
}
class ve extends oe {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const l = b(), r = new ve({
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
          }, a = e.parent ?? C;
          return a.nodes = [...a.nodes, s], A({
            createPortal: S,
            node: C
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: S,
              node: C
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
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Se.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function x(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = x(r.props.el);
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
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = x(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = V(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = B(), [s, a] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function h() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Re(l);
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
        i = _, a(u), i.style.display = "contents", h(), (w = e.current) == null || w.appendChild(i);
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
      i.style.display = "contents", h(), (p = e.current) == null || p.appendChild(i);
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
}), ke = Ce(({
  slots: n,
  ...t
}) => /* @__PURE__ */ I.jsx(X.Sider, {
  ...t,
  trigger: n.trigger ? /* @__PURE__ */ I.jsx(Ie, {
    slot: n.trigger,
    clone: !0
  }) : t.trigger === void 0 ? null : t.trigger === "default" ? void 0 : t.trigger
}));
export {
  ke as LayoutSider,
  ke as default
};
