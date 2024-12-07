import { g as Q, w as y } from "./Index-Cr5Yul-x.js";
const m = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Badge;
var D = {
  exports: {}
}, C = {};
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
function F(n, t, o) {
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
C.Fragment = ee;
C.jsx = F;
C.jsxs = F;
D.exports = C;
var w = D.exports;
const {
  SvelteComponent: oe,
  assign: O,
  binding_callbacks: k,
  check_outros: se,
  children: W,
  claim_element: z,
  claim_space: le,
  component_subscribe: P,
  compute_slots: ie,
  create_slot: ae,
  detach: h,
  element: B,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ce,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: E,
  safe_not_equal: _e,
  set_custom_element_data: G,
  space: pe,
  transition_in: v,
  transition_out: S,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: be,
  setContext: we
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
      t = B("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), r && r.m(t, null), n[9](t), o = !0;
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
      o || (v(r, e), o = !0);
    },
    o(e) {
      S(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = B("react-portal-target"), o = pe(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(h), o = le(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      E(s, t, a), n[8](t), E(s, o, a), e && e.m(s, a), E(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && v(e, 1)) : (e = j(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (ue(), S(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      r || (v(e), r = !0);
    },
    o(s) {
      S(e), r = !1;
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
function Ee(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = y(N(t)), f = y();
  P(n, f, (c) => o(0, l = c));
  const p = y();
  P(n, p, (c) => o(1, r = c));
  const d = [], u = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: U
  } = Q() || {}, H = i({
    parent: u,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: U,
    onDestroy(c) {
      d.push(c);
    }
  });
  we("$$ms-gr-react-wrapper", H), he(() => {
    g.set(N(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function K(c) {
    k[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function M(c) {
    k[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = O(O({}, t), T(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = T(t), [l, r, f, p, a, i, s, e, K, M];
}
class ve extends oe {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const l = y(), r = new ve({
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
          }, a = e.parent ?? x;
          return a.nodes = [...a.nodes, s], A({
            createPortal: R,
            node: x
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: x
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
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !xe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
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
      } = I(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Se(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = q(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = V(), [s, a] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Se(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Re(l);
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
        } = I(n);
        i = _, a(u), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
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
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), ke = Ce(({
  slots: n,
  children: t,
  ...o
}) => /* @__PURE__ */ w.jsx(w.Fragment, {
  children: /* @__PURE__ */ w.jsx(X.Ribbon, {
    ...o,
    text: n.text ? /* @__PURE__ */ w.jsx(Ie, {
      slot: n.text
    }) : o.text,
    children: t
  })
}));
export {
  ke as BadgeRibbon,
  ke as default
};
