import { g as ne, w as E, d as re, a as v } from "./Index-CWwwIG_Y.js";
const g = window.ms_globals.React, R = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Dropdown;
var V = {
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
var le = g, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ue = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) ue.call(e, s) && !ie.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: se,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: ae.current
  };
}
C.Fragment = ce;
C.jsx = q;
C.jsxs = q;
V.exports = C;
var b = V.exports;
const {
  SvelteComponent: de,
  assign: A,
  binding_callbacks: F,
  check_outros: fe,
  children: J,
  claim_element: Y,
  claim_space: pe,
  component_subscribe: N,
  compute_slots: _e,
  create_slot: me,
  detach: w,
  element: K,
  empty: D,
  exclude_internal_props: B,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: I,
  safe_not_equal: ve,
  set_custom_element_data: Q,
  space: ye,
  transition_in: x,
  transition_out: T,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: xe,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = me(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = Y(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(e);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      I(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && Ee(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? ge(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (x(o, t), r = !0);
    },
    o(t) {
      T(o, t), r = !1;
    },
    d(t) {
      t && w(e), o && o.d(t), n[9](null);
    }
  };
}
function Se(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      e = K("react-portal-target"), r = ye(), t && t.c(), s = D(), this.h();
    },
    l(l) {
      e = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(e).forEach(w), r = pe(l), t && t.l(l), s = D(), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      I(l, e, c), n[8](e), I(l, r, c), t && t.m(l, c), I(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = M(l), t.c(), x(t, 1), t.m(s.parentNode, s)) : t && (we(), T(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(l) {
      o || (x(t), o = !0);
    },
    o(l) {
      T(t), o = !1;
    },
    d(l) {
      l && (w(e), w(r), w(s)), n[8](null), t && t.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ke(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = _e(t);
  let {
    svelteInit: u
  } = e;
  const _ = E(W(e)), f = E();
  N(n, f, (i) => r(0, s = i));
  const p = E();
  N(n, p, (i) => r(1, o = i));
  const a = [], d = xe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: h,
    subSlotIndex: S
  } = ne() || {}, k = u({
    parent: d,
    props: _,
    target: f,
    slot: p,
    slotKey: m,
    slotIndex: h,
    subSlotIndex: S,
    onDestroy(i) {
      a.push(i);
    }
  });
  Ce("$$ms-gr-react-wrapper", k), Ie(() => {
    _.set(W(e));
  }), Re(() => {
    a.forEach((i) => i());
  });
  function Z(i) {
    F[i ? "unshift" : "push"](() => {
      s = i, f.set(s);
    });
  }
  function $(i) {
    F[i ? "unshift" : "push"](() => {
      o = i, p.set(o);
    });
  }
  return n.$$set = (i) => {
    r(17, e = A(A({}, e), B(i))), "svelteInit" in i && r(5, u = i.svelteInit), "$$scope" in i && r(6, l = i.$$scope);
  }, e = B(e), [s, o, f, p, c, u, l, t, Z, $];
}
class Oe extends de {
  constructor(e) {
    super(), be(this, e, ke, Se, ve, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function je(n) {
  function e(r) {
    const s = E(), o = new Oe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? O;
          return c.nodes = [...c.nodes, l], z({
            createPortal: P,
            node: O
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== s), z({
              createPortal: P,
              node: O
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
      r(e);
    });
  });
}
function Pe(n) {
  const [e, r] = U(() => v(n));
  return H(() => {
    let s = !0;
    return n.subscribe((t) => {
      s && (s = !1, t === e) || r(t);
    });
  }, [n]), e;
}
function Te(n) {
  const e = R(() => re(n, (r) => r), [n]);
  return Pe(e);
}
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Le.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function L(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(P(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...t]
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
      listener: l,
      type: c,
      useCapture: u
    }) => {
      r.addEventListener(c, l, u);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(t);
      e.push(...c), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const y = ee(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = te(), [l, c] = U([]);
  return H(() => {
    var p;
    if (!t.current || !n)
      return;
    let u = n;
    function _() {
      let a = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (a = u.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const d = Ae(s);
        Object.keys(d).forEach((m) => {
          a.style[m] = d[m];
        });
      }
    }
    let f = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var h;
        const {
          portals: d,
          clonedElement: m
        } = L(n);
        u = m, c(d), u.style.display = "contents", _(), (h = t.current) == null || h.appendChild(u);
      };
      a(), f = new window.MutationObserver(() => {
        var d, m;
        (d = t.current) != null && d.contains(u) && ((m = t.current) == null || m.removeChild(u)), a();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", _(), (p = t.current) == null || p.appendChild(u);
    return () => {
      var a, d;
      u.style.display = "", (a = t.current) != null && a.contains(u) && ((d = t.current) == null || d.removeChild(u)), f == null || f.disconnect();
    };
  }, [n, e, r, s, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ne(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function j(n) {
  return R(() => Ne(n), [n]);
}
function De(n, e) {
  const r = R(() => g.Children.toArray(n).filter((t) => t.props.node && e === t.props.nodeSlotKey).sort((t, l) => {
    if (t.props.node.slotIndex && l.props.node.slotIndex) {
      const c = v(t.props.node.slotIndex) || 0, u = v(l.props.node.slotIndex) || 0;
      return c - u === 0 && t.props.node.subSlotIndex && l.props.node.subSlotIndex ? (v(t.props.node.subSlotIndex) || 0) - (v(l.props.node.subSlotIndex) || 0) : c - u;
    }
    return 0;
  }).map((t) => t.props.node.target), [n, e]);
  return Te(r);
}
function X(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const s = {
      ...r.props
    };
    let o = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((a, d) => {
        o[a] || (o[a] = {}), d !== c.length - 1 && (o = s[a]);
      });
      const u = r.slots[l];
      let _, f, p = (e == null ? void 0 : e.clone) ?? !1;
      u instanceof Element ? _ = u : (_ = u.el, f = u.callback, p = u.clone ?? !1), o[c[c.length - 1]] = _ ? f ? (...a) => (f(c[c.length - 1], a), /* @__PURE__ */ b.jsx(y, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ b.jsx(y, {
        slot: _,
        clone: p
      }) : o[c[c.length - 1]], o = s;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (s[t] = X(r[t], e)), s;
  });
}
function Be(n, e) {
  return n ? /* @__PURE__ */ b.jsx(y, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function G({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...o) => (e(n, o), Be(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const We = je(({
  getPopupContainer: n,
  slots: e,
  menuItems: r,
  children: s,
  dropdownRender: o,
  buttonsRender: t,
  setSlotParams: l,
  ...c
}) => {
  var a, d, m;
  const u = j(n), _ = j(o), f = j(t), p = De(s, "buttonsRender");
  return /* @__PURE__ */ b.jsx(oe.Button, {
    ...c,
    buttonsRender: p.length ? (...h) => (l("buttonsRender", h), p.map((S, k) => /* @__PURE__ */ b.jsx(y, {
      slot: S
    }, k))) : f,
    menu: {
      ...c.menu,
      items: R(() => {
        var h;
        return ((h = c.menu) == null ? void 0 : h.items) || X(r, {
          clone: !0
        });
      }, [r, (a = c.menu) == null ? void 0 : a.items]),
      expandIcon: e["menu.expandIcon"] ? G({
        slots: e,
        setSlotParams: l,
        key: "menu.expandIcon"
      }, {
        clone: !0
      }) : (d = c.menu) == null ? void 0 : d.expandIcon,
      overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ b.jsx(y, {
        slot: e["menu.overflowedIndicator"]
      }) : (m = c.menu) == null ? void 0 : m.overflowedIndicator
    },
    getPopupContainer: u,
    dropdownRender: e.dropdownRender ? G({
      slots: e,
      setSlotParams: l,
      key: "dropdownRender"
    }) : _,
    children: s
  });
});
export {
  We as DropdownButton,
  We as default
};
