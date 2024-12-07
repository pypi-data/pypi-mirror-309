import { g as $, w as E } from "./Index-CS5UZsxL.js";
const h = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Popconfirm;
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
var te = h, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) re.call(n, l) && !le.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var m = D.exports;
const {
  SvelteComponent: ie,
  assign: I,
  binding_callbacks: O,
  check_outros: ce,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: T,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: G,
  empty: j,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: v,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: ge,
  transition_in: x,
  transition_out: R,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function B(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = de(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (x(o, e), r = !0);
    },
    o(e) {
      R(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && B(t)
  );
  return {
    c() {
      n = G("react-portal-target"), r = ge(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      n = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(n).forEach(w), r = ae(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, n, c), t[8](n), v(s, r, c), e && e.m(s, c), v(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = B(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (_e(), R(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      R(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Ce(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const b = E(N(n)), f = E();
  T(t, f, (a) => r(0, l = a));
  const _ = E();
  T(t, _, (a) => r(1, o = a));
  const u = [], d = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H
  } = $() || {}, K = i({
    parent: d,
    props: b,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: H,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", K), be(() => {
    b.set(N(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function q(a) {
    O[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function V(a) {
    O[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, n = I(I({}, n), L(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, n = L(n), [l, o, f, _, c, i, s, e, q, V];
}
class Pe extends ie {
  constructor(n) {
    super(), me(this, n, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, P = window.ms_globals.tree;
function ke(t) {
  function n(r) {
    const l = E(), o = new Pe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? P;
          return c.nodes = [...c.nodes, s], A({
            createPortal: k,
            node: P
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: k,
              node: P
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Re.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function S(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(k(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = S(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = S(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Ie(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const g = J(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function b() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ie(o, u), r && u.classList.add(...r.split(" ")), l) {
        const d = Se(l);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y;
        const {
          portals: d,
          clonedElement: p
        } = S(t);
        i = p, c(d), i.style.display = "contents", b(), (y = e.current) == null || y.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", b(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Oe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function F(t) {
  return Z(() => Oe(t), [t]);
}
const je = ke(({
  slots: t,
  afterOpenChange: n,
  getPopupContainer: r,
  children: l,
  ...o
}) => {
  var c, i;
  const e = F(n), s = F(r);
  return /* @__PURE__ */ m.jsx(ee, {
    ...o,
    afterOpenChange: e,
    getPopupContainer: s,
    okText: t.okText ? /* @__PURE__ */ m.jsx(g, {
      slot: t.okText
    }) : o.okText,
    okButtonProps: {
      ...o.okButtonProps || {},
      icon: t["okButtonProps.icon"] ? /* @__PURE__ */ m.jsx(g, {
        slot: t["okButtonProps.icon"]
      }) : (c = o.okButtonProps) == null ? void 0 : c.icon
    },
    cancelText: t.cancelText ? /* @__PURE__ */ m.jsx(g, {
      slot: t.cancelText
    }) : o.cancelText,
    cancelButtonProps: {
      ...o.cancelButtonProps || {},
      icon: t["cancelButtonProps.icon"] ? /* @__PURE__ */ m.jsx(g, {
        slot: t["cancelButtonProps.icon"]
      }) : (i = o.cancelButtonProps) == null ? void 0 : i.icon
    },
    title: t.title ? /* @__PURE__ */ m.jsx(g, {
      slot: t.title
    }) : o.title,
    description: t.description ? /* @__PURE__ */ m.jsx(g, {
      slot: t.description
    }) : o.description,
    children: l
  });
});
export {
  je as Popconfirm,
  je as default
};
