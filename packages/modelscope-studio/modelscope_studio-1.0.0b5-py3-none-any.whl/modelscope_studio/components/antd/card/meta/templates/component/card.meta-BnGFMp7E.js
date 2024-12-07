import { g as X, w as y } from "./Index-vdTkwSyb.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, S = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Card;
var M = {
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
function W(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !oe.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: re.current
  };
}
C.Fragment = te;
C.jsx = W;
C.jsxs = W;
M.exports = C;
var b = M.exports;
const {
  SvelteComponent: se,
  assign: k,
  binding_callbacks: P,
  check_outros: le,
  children: z,
  claim_element: F,
  claim_space: ie,
  component_subscribe: L,
  compute_slots: ae,
  create_slot: ce,
  detach: h,
  element: G,
  empty: T,
  exclude_internal_props: j,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: pe,
  set_custom_element_data: U,
  space: me,
  transition_in: v,
  transition_out: I,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ce(
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
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && he(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
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
      o || (v(r, e), o = !0);
    },
    o(e) {
      I(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = G("react-portal-target"), o = me(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = F(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(h), o = ie(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      E(s, t, a), n[8](t), E(s, o, a), e && e.m(s, a), E(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && v(e, 1)) : (e = N(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (fe(), I(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      r || (v(e), r = !0);
    },
    o(s) {
      I(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function A(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = y(A(t)), f = y();
  L(n, f, (c) => o(0, l = c));
  const p = y();
  L(n, p, (c) => o(1, r = c));
  const d = [], u = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H
  } = X() || {}, K = i({
    parent: u,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", K), ge(() => {
    g.set(A(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function q(c) {
    P[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function V(c) {
    P[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = k(k({}, t), j(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = j(t), [l, r, f, p, a, i, s, e, q, V];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(n) {
  function t(o) {
    const l = y(), r = new Ce({
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
          return a.nodes = [...a.nodes, s], D({
            createPortal: S,
            node: x
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: S,
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Re.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function O(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(r.props.el);
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
      } = O(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const R = B(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = J(), [s, a] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(r, d), o && d.classList.add(...o.split(" ")), l) {
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
        } = O(n);
        i = _, a(u), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
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
}), ke = xe(({
  slots: n,
  ...t
}) => /* @__PURE__ */ b.jsx(Z.Meta, {
  ...t,
  title: n.title ? /* @__PURE__ */ b.jsx(R, {
    slot: n.title
  }) : t.title,
  description: n.description ? /* @__PURE__ */ b.jsx(R, {
    slot: n.description
  }) : t.description,
  avatar: n.avatar ? /* @__PURE__ */ b.jsx(R, {
    slot: n.avatar
  }) : t.avatar
}));
export {
  ke as CardMeta,
  ke as default
};
