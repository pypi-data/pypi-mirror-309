import { g as ee, w as v } from "./Index-D3f_jg9f.js";
const g = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tabs;
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
var ne = g, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) le.call(n, l) && !ae.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var h = D.exports;
const {
  SvelteComponent: ie,
  assign: P,
  binding_callbacks: k,
  check_outros: ce,
  children: U,
  claim_element: W,
  claim_space: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: E,
  element: G,
  empty: B,
  exclude_internal_props: L,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: be,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: H,
  space: ge,
  transition_in: y,
  transition_out: O,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ve,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = W(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(n);
      o && o.l(s), s.forEach(E), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      x(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (y(o, t), r = !0);
    },
    o(t) {
      O(o, t), r = !1;
    },
    d(t) {
      t && E(n), o && o.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && F(e)
  );
  return {
    c() {
      n = G("react-portal-target"), r = ge(), t && t.c(), l = B(), this.h();
    },
    l(s) {
      n = W(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(E), r = ue(s), t && t.l(s), l = B(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      x(s, n, a), e[8](n), x(s, r, a), t && t.m(s, a), x(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && y(t, 1)) : (t = F(s), t.c(), y(t, 1), t.m(l.parentNode, l)) : t && (he(), O(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(s) {
      o || (y(t), o = !0);
    },
    o(s) {
      O(t), o = !1;
    },
    d(s) {
      s && (E(n), E(r), E(l)), e[8](null), t && t.d(s);
    }
  };
}
function N(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ie(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const a = de(t);
  let {
    svelteInit: i
  } = n;
  const f = v(N(n)), d = v();
  T(e, d, (u) => r(0, l = u));
  const p = v();
  T(e, p, (u) => r(1, o = u));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: w,
    subSlotIndex: V
  } = ee() || {}, J = i({
    parent: _,
    props: f,
    target: d,
    slot: p,
    slotKey: b,
    slotIndex: w,
    subSlotIndex: V,
    onDestroy(u) {
      c.push(u);
    }
  });
  ye("$$ms-gr-react-wrapper", J), we(() => {
    f.set(N(n));
  }), xe(() => {
    c.forEach((u) => u());
  });
  function Y(u) {
    k[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function K(u) {
    k[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = P(P({}, n), L(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = L(n), [l, o, d, p, a, i, s, t, Y, K];
}
class Se extends ie {
  constructor(n) {
    super(), be(this, n, Ie, Ce, me, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(e) {
  function n(r) {
    const l = v(), o = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? I;
          return a.nodes = [...a.nodes, s], A({
            createPortal: R,
            node: I
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: I
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
      r(n);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Oe.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function j(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(R(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...g.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = j(t);
      n.push(...a), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Pe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const m = Q(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = X(), [s, a] = Z([]);
  return $(() => {
    var p;
    if (!t.current || !e)
      return;
    let i = e;
    function f() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Pe(o, c), r && c.classList.add(...r.split(" ")), l) {
        const _ = je(l);
        Object.keys(_).forEach((b) => {
          c.style[b] = _[b];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var w;
        const {
          portals: _,
          clonedElement: b
        } = j(e);
        i = b, a(_), i.style.display = "contents", f(), (w = t.current) == null || w.appendChild(i);
      };
      c(), d = new window.MutationObserver(() => {
        var _, b;
        (_ = t.current) != null && _.contains(i) && ((b = t.current) == null || b.removeChild(i)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", f(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((_ = t.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, r, l, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function S(e) {
  return z(() => ke(e), [e]);
}
function Te(e) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
function q(e, n) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const a = s.split(".");
      a.forEach((c, _) => {
        o[c] || (o[c] = {}), _ !== a.length - 1 && (o = l[c]);
      });
      const i = r.slots[s];
      let f, d, p = !1;
      i instanceof Element ? f = i : (f = i.el, d = i.callback, p = i.clone ?? !1), o[a[a.length - 1]] = f ? d ? (...c) => (d(a[a.length - 1], c), /* @__PURE__ */ h.jsx(m, {
        slot: f,
        clone: p
      })) : /* @__PURE__ */ h.jsx(m, {
        slot: f,
        clone: p
      }) : o[a[a.length - 1]], o = l;
    });
    const t = "children";
    return r[t] && (l[t] = q(r[t])), l;
  });
}
function Be(e, n) {
  return e ? /* @__PURE__ */ h.jsx(m, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Le({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return r[e] ? (...o) => (n(e, o), Be(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ne = Re(({
  slots: e,
  indicator: n,
  items: r,
  onChange: l,
  slotItems: o,
  more: t,
  children: s,
  renderTabBar: a,
  setSlotParams: i,
  ...f
}) => {
  const d = S(n == null ? void 0 : n.size), p = S(t == null ? void 0 : t.getPopupContainer), c = S(a);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ h.jsx(te, {
      ...f,
      indicator: d ? {
        ...n,
        size: d
      } : n,
      renderTabBar: e.renderTabBar ? Le({
        slots: e,
        setSlotParams: i,
        key: "renderTabBar"
      }) : c,
      items: z(() => r || q(o), [r, o]),
      more: Te({
        ...t || {},
        getPopupContainer: p || (t == null ? void 0 : t.getPopupContainer),
        icon: e["more.icon"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["more.icon"]
        }) : t == null ? void 0 : t.icon
      }),
      tabBarExtraContent: e.tabBarExtraContent ? /* @__PURE__ */ h.jsx(m, {
        slot: e.tabBarExtraContent
      }) : e["tabBarExtraContent.left"] || e["tabBarExtraContent.right"] ? {
        left: e["tabBarExtraContent.left"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["tabBarExtraContent.left"]
        }) : void 0,
        right: e["tabBarExtraContent.right"] ? /* @__PURE__ */ h.jsx(m, {
          slot: e["tabBarExtraContent.right"]
        }) : void 0
      } : f.tabBarExtraContent,
      addIcon: e.addIcon ? /* @__PURE__ */ h.jsx(m, {
        slot: e.addIcon
      }) : f.addIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ h.jsx(m, {
        slot: e.removeIcon
      }) : f.removeIcon,
      onChange: (_) => {
        l == null || l(_);
      }
    })]
  });
});
export {
  Ne as Tabs,
  Ne as default
};
