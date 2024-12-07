import { g as X, w as y } from "./Index-JVikoZn8.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Avatar;
var F = {
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !oe.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: re.current
  };
}
C.Fragment = te;
C.jsx = W;
C.jsxs = W;
F.exports = C;
var w = F.exports;
const {
  SvelteComponent: se,
  assign: O,
  binding_callbacks: k,
  check_outros: le,
  children: z,
  claim_element: G,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: ce,
  create_slot: ae,
  detach: h,
  element: U,
  empty: L,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: pe,
  set_custom_element_data: H,
  space: me,
  transition_in: v,
  transition_out: S,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function T(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ae(
    l,
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
      var s = z(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && he(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && T(n)
  );
  return {
    c() {
      t = U("react-portal-target"), r = me(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(h), r = ie(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, t, c), n[8](t), E(s, r, c), e && e.m(s, c), E(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = T(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (fe(), S(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (v(e), o = !0);
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
function ve(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = y(j(t)), f = y();
  P(n, f, (a) => r(0, l = a));
  const p = y();
  P(n, p, (a) => r(1, o = a));
  const d = [], u = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: K
  } = X() || {}, M = i({
    parent: u,
    props: g,
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
    g.set(j(t));
  }), be(() => {
    d.forEach((a) => a());
  });
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function V(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = O(O({}, t), A(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = A(t), [l, o, f, p, c, i, s, e, q, V];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = y(), o = new Ce({
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
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], N({
            createPortal: R,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), N({
              createPortal: R,
              node: x
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
function I(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = I(o.props.el);
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
      } = I(e);
      t.push(...c), r.appendChild(s);
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
const D = B(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(o, d), r && d.classList.add(...r.split(" ")), l) {
        const u = Se(l);
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
        i = _, c(u), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
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
}), ke = xe(({
  slots: n,
  children: t,
  ...r
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [n.icon ? t : null, /* @__PURE__ */ w.jsx(Z, {
    ...r,
    icon: n.icon ? /* @__PURE__ */ w.jsx(D, {
      slot: n.icon
    }) : r.icon,
    src: n.src ? /* @__PURE__ */ w.jsx(D, {
      slot: n.src
    }) : r.src,
    children: n.icon ? null : t
  })]
}));
export {
  ke as Avatar,
  ke as default
};
