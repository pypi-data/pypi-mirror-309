import { g as $, w as E } from "./Index-nmNVfsX3.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Timeline;
var F = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(o, t, r) {
  var l, n = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !se.hasOwnProperty(l) && (n[l] = t[l]);
  if (o && o.defaultProps) for (l in t = o.defaultProps, t) n[l] === void 0 && (n[l] = t[l]);
  return {
    $$typeof: ne,
    type: o,
    key: e,
    ref: s,
    props: n,
    _owner: le.current
  };
}
x.Fragment = re;
x.jsx = M;
x.jsxs = M;
F.exports = x;
var h = F.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: j,
  check_outros: ce,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: T,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: ge,
  transition_in: v,
  transition_out: I,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(o) {
  let t, r;
  const l = (
    /*#slots*/
    o[7].default
  ), n = ue(
    l,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(t);
      n && n.l(s), s.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && be(
        n,
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
      r || (v(n, e), r = !0);
    },
    o(e) {
      I(n, e), r = !1;
    },
    d(e) {
      e && b(t), n && n.d(e), o[9](null);
    }
  };
}
function Ce(o) {
  let t, r, l, n, e = (
    /*$$slots*/
    o[4].default && D(o)
  );
  return {
    c() {
      t = G("react-portal-target"), r = ge(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), r = ae(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      y(s, t, i), o[8](t), y(s, r, i), e && e.m(s, i), y(s, l, i), n = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && v(e, 1)) : (e = D(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      n || (v(e), n = !0);
    },
    o(s) {
      I(e), n = !1;
    },
    d(s) {
      s && (b(t), b(r), b(l)), o[8](null), e && e.d(s);
    }
  };
}
function N(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function xe(o, t, r) {
  let l, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const p = E(N(t)), u = E();
  P(o, u, (d) => r(0, l = d));
  const _ = E();
  P(o, _, (d) => r(1, n = d));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = c({
    parent: f,
    props: p,
    target: u,
    slot: _,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", B), we(() => {
    p.set(N(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    j[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      n = d, _.set(n);
    });
  }
  return o.$$set = (d) => {
    r(17, t = k(k({}, t), L(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = L(t), [l, n, u, _, i, c, s, e, V, J];
}
class Re extends ie {
  constructor(t) {
    super(), me(this, t, xe, Ce, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(o) {
  function t(r) {
    const l = E(), n = new Re({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? R;
          return i.nodes = [...i.nodes, s], A({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), A({
              createPortal: S,
              node: R
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(o) {
  return o ? Object.keys(o).reduce((t, r) => {
    const l = o[r];
    return typeof l == "number" && !Ie.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function O(o) {
  const t = [], r = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(S(g.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: g.Children.toArray(o._reactElement.props.children).map((n) => {
        if (g.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(n.props.el);
          return g.cloneElement(n, {
            ...n.props,
            el: s,
            children: [...g.Children.toArray(n.props.children), ...e]
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
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(o.childNodes);
  for (let n = 0; n < l.length; n++) {
    const e = l[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = O(e);
      t.push(...i), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function ke(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const C = Y(({
  slot: o,
  clone: t,
  className: r,
  style: l
}, n) => {
  const e = K(), [s, i] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !o)
      return;
    let c = o;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(n, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Oe(l);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = O(o);
        c = m, i(f), c.style.display = "contents", p(), (w = e.current) == null || w.appendChild(c);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(c) && ((m = e.current) == null || m.removeChild(c)), a();
      }), u.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((f = e.current) == null || f.removeChild(c)), u == null || u.disconnect();
    };
  }, [o, t, r, l, n]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function H(o, t) {
  return o.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let n = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const i = s.split(".");
      i.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== i.length - 1 && (n = l[a]);
      });
      const c = r.slots[s];
      let p, u, _ = !1;
      c instanceof Element ? p = c : (p = c.el, u = c.callback, _ = c.clone ?? !1), n[i[i.length - 1]] = p ? u ? (...a) => (u(i[i.length - 1], a), /* @__PURE__ */ h.jsx(C, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ h.jsx(C, {
        slot: p,
        clone: _
      }) : n[i[i.length - 1]], n = l;
    });
    const e = "children";
    return r[e] && (l[e] = H(r[e])), l;
  });
}
const Pe = Se(({
  slots: o,
  items: t,
  slotItems: r,
  children: l,
  ...n
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ h.jsx(ee, {
    ...n,
    items: Z(() => t || H(r), [t, r]),
    pending: o.pending ? /* @__PURE__ */ h.jsx(C, {
      slot: o.pending
    }) : n.pending,
    pendingDot: o.pendingDot ? /* @__PURE__ */ h.jsx(C, {
      slot: o.pendingDot
    }) : n.pendingDot
  })]
}));
export {
  Pe as Timeline,
  Pe as default
};
