import { g as Z, w as E } from "./Index-DK69o12Q.js";
const h = window.ms_globals.React, V = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.FloatButton;
var B = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(t, n, s) {
  var r, o = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (r in n) oe.call(n, r) && !se.hasOwnProperty(r) && (o[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) o[r] === void 0 && (o[r] = n[r]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
x.Fragment = ne;
x.jsx = D;
x.jsxs = D;
B.exports = x;
var p = B.exports;
const {
  SvelteComponent: le,
  assign: O,
  binding_callbacks: P,
  check_outros: ie,
  children: M,
  claim_element: W,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: z,
  empty: T,
  exclude_internal_props: L,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: G,
  space: he,
  transition_in: C,
  transition_out: I,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function F(t) {
  let n, s;
  const r = (
    /*#slots*/
    t[7].default
  ), o = ue(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = z("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = M(n);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      G(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, n, l), o && o.m(n, null), t[9](n), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ge(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          r,
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
      s || (C(o, e), s = !0);
    },
    o(e) {
      I(o, e), s = !1;
    },
    d(e) {
      e && g(n), o && o.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, s, r, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = z("react-portal-target"), s = he(), e && e.c(), r = T(), this.h();
    },
    l(l) {
      n = W(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(n).forEach(g), s = ce(l), e && e.l(l), r = T(), this.h();
    },
    h() {
      G(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, n, c), t[8](n), v(l, s, c), e && e.m(l, c), v(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = F(l), e.c(), C(e, 1), e.m(r.parentNode, r)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      o || (C(e), o = !0);
    },
    o(l) {
      I(e), o = !1;
    },
    d(l) {
      l && (g(n), g(s), g(r)), t[8](null), e && e.d(l);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function Ce(t, n, s) {
  let r, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const w = E(N(n)), f = E();
  j(t, f, (a) => s(0, r = a));
  const m = E();
  j(t, m, (a) => s(1, o = a));
  const u = [], d = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: U
  } = Z() || {}, H = i({
    parent: d,
    props: w,
    target: f,
    slot: m,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: U,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", H), we(() => {
    w.set(N(n));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function K(a) {
    P[a ? "unshift" : "push"](() => {
      r = a, f.set(r);
    });
  }
  function q(a) {
    P[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return t.$$set = (a) => {
    s(17, n = O(O({}, n), L(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, l = a.$$scope);
  }, n = L(n), [r, o, f, m, c, i, l, e, K, q];
}
class xe extends le {
  constructor(n) {
    super(), pe(this, n, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, R = window.ms_globals.tree;
function Re(t) {
  function n(s) {
    const r = E(), o = new xe({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, l], A({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), A({
              createPortal: S,
              node: R
            });
          }), l;
        },
        ...s.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !Se.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function k(t) {
  const n = [], s = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(S(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = k(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const r = Array.from(t.childNodes);
  for (let o = 0; o < r.length; o++) {
    const e = r[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = k(e);
      n.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: n
  };
}
function ke(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const y = V(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, o) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), s && u.classList.add(...s.split(" ")), r) {
        const d = Ie(r);
        Object.keys(d).forEach((_) => {
          u.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: d,
          clonedElement: _
        } = k(t);
        i = _, c(d), i.style.display = "contents", w(), (b = e.current) == null || b.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, _;
        (d = e.current) != null && d.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, s, r, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Pe(t) {
  return X(() => Oe(t), [t]);
}
const Te = Re(({
  slots: t,
  children: n,
  target: s,
  ...r
}) => {
  var e;
  const o = Pe(s);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx($.BackTop, {
      ...r,
      target: o,
      icon: t.icon ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: t.icon
      }) : r.icon,
      description: t.description ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: t.description
      }) : r.description,
      tooltip: t.tooltip ? /* @__PURE__ */ p.jsx(y, {
        clone: !0,
        slot: t.tooltip
      }) : r.tooltip,
      badge: {
        ...r.badge,
        count: t["badge.count"] ? /* @__PURE__ */ p.jsx(y, {
          slot: t["badge.count"]
        }) : (e = r.badge) == null ? void 0 : e.count
      }
    })]
  });
});
export {
  Te as FloatButtonBackTop,
  Te as default
};
