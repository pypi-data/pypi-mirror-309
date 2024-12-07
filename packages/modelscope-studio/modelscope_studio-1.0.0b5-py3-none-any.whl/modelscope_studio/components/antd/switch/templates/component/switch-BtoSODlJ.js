import { g as Z, w as y } from "./Index-DVADlw_m.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, k = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Switch;
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
function W(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
C.Fragment = te;
C.jsx = W;
C.jsxs = W;
F.exports = C;
var h = F.exports;
const {
  SvelteComponent: se,
  assign: I,
  binding_callbacks: O,
  check_outros: le,
  children: z,
  claim_element: G,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: ce,
  create_slot: de,
  detach: w,
  element: U,
  empty: L,
  exclude_internal_props: j,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: pe,
  set_custom_element_data: H,
  space: me,
  transition_in: v,
  transition_out: x,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ge,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function T(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = de(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = z(t);
      r && r.l(l), l.forEach(w), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && he(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ae(
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
      x(r, e), o = !1;
    },
    d(e) {
      e && w(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && T(n)
  );
  return {
    c() {
      t = U("react-portal-target"), o = me(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(w), o = ie(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, t, c), n[8](t), E(l, o, c), e && e.m(l, c), E(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = T(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (fe(), x(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      x(e), r = !1;
    },
    d(l) {
      l && (w(t), w(o), w(s)), n[8](null), e && e.d(l);
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
function ve(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = y(N(t)), f = y();
  P(n, f, (d) => o(0, s = d));
  const p = y();
  P(n, p, (d) => o(1, r = d));
  const a = [], u = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: K
  } = Z() || {}, M = i({
    parent: u,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: K,
    onDestroy(d) {
      a.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", M), we(() => {
    g.set(N(t));
  }), be(() => {
    a.forEach((d) => d());
  });
  function q(d) {
    O[d ? "unshift" : "push"](() => {
      s = d, f.set(s);
    });
  }
  function B(d) {
    O[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, t = I(I({}, t), j(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = j(t), [s, r, f, p, c, i, l, e, q, B];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const s = y(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, l], A({
            createPortal: k,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), A({
              createPortal: k,
              node: S
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ke.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function R(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = R(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = R(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Re(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = J(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Y(), [l, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Re(r, a), o && a.classList.add(...o.split(" ")), s) {
        const u = xe(s);
        Object.keys(u).forEach((_) => {
          a.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: u,
          clonedElement: _
        } = R(n);
        i = _, c(u), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var u, _;
        (u = e.current) != null && u.contains(i) && ((_ = e.current) == null || _.removeChild(i)), a();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, u;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), Oe = Se(({
  slots: n,
  children: t,
  onValueChange: o,
  onChange: s,
  ...r
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ h.jsx(V, {
    ...r,
    onChange: (e, ...l) => {
      o == null || o(e), s == null || s(e, ...l);
    },
    checkedChildren: n.checkedChildren ? /* @__PURE__ */ h.jsx(D, {
      slot: n.checkedChildren
    }) : r.checkedChildren,
    unCheckedChildren: n.unCheckedChildren ? /* @__PURE__ */ h.jsx(D, {
      slot: n.unCheckedChildren
    }) : r.unCheckedChildren
  })]
}));
export {
  Oe as Switch,
  Oe as default
};
