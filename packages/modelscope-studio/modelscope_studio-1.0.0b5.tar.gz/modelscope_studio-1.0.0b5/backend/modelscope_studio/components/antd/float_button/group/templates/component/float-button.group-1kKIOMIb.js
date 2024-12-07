import { g as Z, w as E, c as $ } from "./Index-DQ5J-fBH.js";
const h = window.ms_globals.React, V = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.theme, te = window.ms_globals.antd.FloatButton;
var G = {
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
var ne = h, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(o, t, r) {
  var s, n = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (n[s] = t[s]);
  if (o && o.defaultProps) for (s in t = o.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: oe,
    type: o,
    key: e,
    ref: l,
    props: n,
    _owner: le.current
  };
}
x.Fragment = re;
x.jsx = D;
x.jsxs = D;
G.exports = x;
var _ = G.exports;
const {
  SvelteComponent: ce,
  assign: O,
  binding_callbacks: j,
  check_outros: ae,
  children: M,
  claim_element: W,
  claim_space: de,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: fe,
  detach: b,
  element: z,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: v,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: be,
  transition_in: C,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(o) {
  let t, r;
  const s = (
    /*#slots*/
    o[7].default
  ), n = fe(
    s,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = M(t);
      n && n.l(l), l.forEach(b), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, l) {
      n && n.p && (!r || l & /*$$scope*/
      64) && we(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(n, e), r = !0);
    },
    o(e) {
      S(n, e), r = !1;
    },
    d(e) {
      e && b(t), n && n.d(e), o[9](null);
    }
  };
}
function xe(o) {
  let t, r, s, n, e = (
    /*$$slots*/
    o[4].default && N(o)
  );
  return {
    c() {
      t = z("react-portal-target"), r = be(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = W(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(t).forEach(b), r = de(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, t, c), o[8](t), v(l, r, c), e && e.m(l, c), v(l, s, c), n = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = N(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (me(), S(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      n || (C(e), n = !0);
    },
    o(l) {
      S(e), n = !1;
    },
    d(l) {
      l && (b(t), b(r), b(s)), o[8](null), e && e.d(l);
    }
  };
}
function A(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function Ie(o, t, r) {
  let s, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const m = E(A(t)), f = E();
  P(o, f, (a) => r(0, s = a));
  const g = E();
  P(o, g, (a) => r(1, n = a));
  const d = [], u = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: K
  } = Z() || {}, U = i({
    parent: u,
    props: m,
    target: f,
    slot: g,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(a) {
      d.push(a);
    }
  });
  Ce("$$ms-gr-react-wrapper", U), ye(() => {
    m.set(A(t));
  }), ve(() => {
    d.forEach((a) => a());
  });
  function H(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function q(a) {
    j[a ? "unshift" : "push"](() => {
      n = a, g.set(n);
    });
  }
  return o.$$set = (a) => {
    r(17, t = O(O({}, t), T(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = T(t), [s, n, f, g, c, i, l, e, H, q];
}
class Re extends ce {
  constructor(t) {
    super(), he(this, t, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(o) {
  function t(r) {
    const s = E(), n = new Re({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], F({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: R,
              node: I
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(o) {
  return o ? Object.keys(o).reduce((t, r) => {
    const s = o[r];
    return typeof s == "number" && !ke.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function k(o) {
  const t = [], r = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(R(h.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: h.Children.toArray(o._reactElement.props.children).map((n) => {
        if (h.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = k(n.props.el);
          return h.cloneElement(n, {
            ...n.props,
            el: l,
            children: [...h.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(o.getEventListeners()).forEach((n) => {
    o.getEventListeners(n).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(o.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = k(e);
      t.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function je(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const w = V(({
  slot: o,
  clone: t,
  className: r,
  style: s
}, n) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var g;
    if (!e.current || !o)
      return;
    let i = o;
    function m() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), je(n, d), r && d.classList.add(...r.split(" ")), s) {
        const u = Oe(s);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y;
        const {
          portals: u,
          clonedElement: p
        } = k(o);
        i = p, c(u), i.style.display = "contents", m(), (y = e.current) == null || y.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(i) && ((p = e.current) == null || p.removeChild(i)), d();
      }), f.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (g = e.current) == null || g.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [o, t, r, s, n]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(o) {
  return X(() => {
    const t = h.Children.toArray(o), r = [], s = [];
    return t.forEach((n) => {
      n.props.node && n.props.nodeSlotKey ? r.push(n) : s.push(n);
    }), [r, s];
  }, [o]);
}
const Te = Se(({
  children: o,
  slots: t,
  style: r,
  shape: s = "circle",
  className: n,
  ...e
}) => {
  var m;
  const {
    token: l
  } = ee.useToken(), [c, i] = Pe(o);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ _.jsx(te.Group, {
      ...e,
      shape: s,
      className: $(n, `ms-gr-antd-float-button-group-${s}`),
      style: {
        ...r,
        "--ms-gr-antd-border-radius-lg": l.borderRadiusLG + "px"
      },
      closeIcon: t.closeIcon ? /* @__PURE__ */ _.jsx(w, {
        clone: !0,
        slot: t.closeIcon
      }) : e.closeIcon,
      icon: t.icon ? /* @__PURE__ */ _.jsx(w, {
        clone: !0,
        slot: t.icon
      }) : e.icon,
      description: t.description ? /* @__PURE__ */ _.jsx(w, {
        clone: !0,
        slot: t.description
      }) : e.description,
      tooltip: t.tooltip ? /* @__PURE__ */ _.jsx(w, {
        clone: !0,
        slot: t.tooltip
      }) : e.tooltip,
      badge: {
        ...e.badge,
        count: t["badge.count"] ? /* @__PURE__ */ _.jsx(w, {
          slot: t["badge.count"]
        }) : (m = e.badge) == null ? void 0 : m.count
      },
      children: i
    })]
  });
});
export {
  Te as FloatButtonGroup,
  Te as default
};
