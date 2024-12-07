import { g as te, w as E } from "./Index-ncrmHqDv.js";
const w = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, W = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Dropdown;
var z = {
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
var re = w, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) se.call(e, l) && !ie.hasOwnProperty(l) && (o[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: s,
    props: o,
    _owner: ce.current
  };
}
C.Fragment = le;
C.jsx = G;
C.jsxs = G;
z.exports = C;
var h = z.exports;
const {
  SvelteComponent: ae,
  assign: O,
  binding_callbacks: j,
  check_outros: de,
  children: U,
  claim_element: H,
  claim_space: ue,
  component_subscribe: P,
  compute_slots: fe,
  create_slot: _e,
  detach: g,
  element: q,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: we,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: be,
  transition_in: v,
  transition_out: S,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = _e(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = q("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = H(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(e);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      y(t, e, s), o && o.m(e, null), n[9](e), r = !0;
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
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (v(o, t), r = !0);
    },
    o(t) {
      S(o, t), r = !1;
    },
    d(t) {
      t && g(e), o && o.d(t), n[9](null);
    }
  };
}
function Ie(n) {
  let e, r, l, o, t = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      e = q("react-portal-target"), r = be(), t && t.c(), l = L(), this.h();
    },
    l(s) {
      e = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(e).forEach(g), r = ue(s), t && t.l(s), l = L(), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, e, c), n[8](e), y(s, r, c), t && t.m(s, c), y(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = N(s), t.c(), v(t, 1), t.m(l.parentNode, l)) : t && (he(), S(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(s) {
      o || (v(t), o = !0);
    },
    o(s) {
      S(t), o = !1;
    },
    d(s) {
      s && (g(e), g(r), g(l)), n[8](null), t && t.d(s);
    }
  };
}
function F(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Re(n, e, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = fe(t);
  let {
    svelteInit: i
  } = e;
  const m = E(F(e)), u = E();
  P(n, u, (d) => r(0, l = d));
  const _ = E();
  P(n, _, (d) => r(1, o = d));
  const a = [], f = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: J
  } = te() || {}, Y = i({
    parent: f,
    props: m,
    target: u,
    slot: _,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: J,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", Y), ye(() => {
    m.set(F(e));
  }), xe(() => {
    a.forEach((d) => d());
  });
  function K(d) {
    j[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Q(d) {
    j[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, e = O(O({}, e), T(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, e = T(e), [l, o, u, _, c, i, s, t, K, Q];
}
class Se extends ae {
  constructor(e) {
    super(), we(this, e, Re, Ie, ge, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function ke(n) {
  function e(r) {
    const l = E(), o = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
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
      r(e);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !Oe.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function k(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(R(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = k(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
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
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(t);
      e.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Pe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const x = X(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, o) => {
  const t = Z(), [s, c] = $([]);
  return ee(() => {
    var _;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = je(l);
        Object.keys(f).forEach((p) => {
          a.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: p
        } = k(n);
        i = p, c(f), i.style.display = "contents", m(), (b = t.current) == null || b.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, p;
        (f = t.current) != null && f.contains(i) && ((p = t.current) == null || p.removeChild(i)), a();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((f = t.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, r, l, o]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(n) {
  return W(() => Le(n), [n]);
}
function V(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== c.length - 1 && (o = l[a]);
      });
      const i = r.slots[s];
      let m, u, _ = (e == null ? void 0 : e.clone) ?? !1;
      i instanceof Element ? m = i : (m = i.el, u = i.callback, _ = i.clone ?? !1), o[c[c.length - 1]] = m ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ h.jsx(x, {
        slot: m,
        clone: _
      })) : /* @__PURE__ */ h.jsx(x, {
        slot: m,
        clone: _
      }) : o[c[c.length - 1]], o = l;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (l[t] = V(r[t], e)), l;
  });
}
function Te(n, e) {
  return n ? /* @__PURE__ */ h.jsx(x, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function M({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return r[n] ? (...o) => (e(n, o), Te(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Fe = ke(({
  getPopupContainer: n,
  innerStyle: e,
  children: r,
  slots: l,
  menuItems: o,
  dropdownRender: t,
  setSlotParams: s,
  ...c
}) => {
  var u, _, a;
  const i = D(n), m = D(t);
  return /* @__PURE__ */ h.jsx(h.Fragment, {
    children: /* @__PURE__ */ h.jsx(ne, {
      ...c,
      menu: {
        ...c.menu,
        items: W(() => {
          var f;
          return ((f = c.menu) == null ? void 0 : f.items) || V(o, {
            clone: !0
          });
        }, [o, (u = c.menu) == null ? void 0 : u.items]),
        expandIcon: l["menu.expandIcon"] ? M({
          slots: l,
          setSlotParams: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (_ = c.menu) == null ? void 0 : _.expandIcon,
        overflowedIndicator: l["menu.overflowedIndicator"] ? /* @__PURE__ */ h.jsx(x, {
          slot: l["menu.overflowedIndicator"]
        }) : (a = c.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: i,
      dropdownRender: l.dropdownRender ? M({
        slots: l,
        setSlotParams: s,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : m,
      children: /* @__PURE__ */ h.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...e
        },
        children: r
      })
    })
  });
});
export {
  Fe as Dropdown,
  Fe as default
};
