import { g as $, w as E } from "./Index-BtzzENi6.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Descriptions;
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(o, t, r) {
  var s, n = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) oe.call(t, s) && !le.hasOwnProperty(s) && (n[s] = t[s]);
  if (o && o.defaultProps) for (s in t = o.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: ne,
    type: o,
    key: e,
    ref: l,
    props: n,
    _owner: se.current
  };
}
C.Fragment = re;
C.jsx = M;
C.jsxs = M;
F.exports = C;
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
  empty: L,
  exclude_internal_props: T,
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
function N(o) {
  let t, r;
  const s = (
    /*#slots*/
    o[7].default
  ), n = ue(
    s,
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
      var l = W(t);
      n && n.l(l), l.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, l) {
      n && n.p && (!r || l & /*$$scope*/
      64) && be(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
          s,
          /*$$scope*/
          e[6],
          l,
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
function xe(o) {
  let t, r, s, n, e = (
    /*$$slots*/
    o[4].default && N(o)
  );
  return {
    c() {
      t = G("react-portal-target"), r = ge(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), r = ae(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      y(l, t, i), o[8](t), y(l, r, i), e && e.m(l, i), y(l, s, i), n = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      n || (v(e), n = !0);
    },
    o(l) {
      I(e), n = !1;
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
function Ce(o, t, r) {
  let s, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const p = E(A(t)), u = E();
  P(o, u, (d) => r(0, s = d));
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
    p.set(A(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    j[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      n = d, _.set(n);
    });
  }
  return o.$$set = (d) => {
    r(17, t = k(k({}, t), T(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, t = T(t), [s, n, u, _, i, c, l, e, V, J];
}
class Re extends ie {
  constructor(t) {
    super(), me(this, t, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, R = window.ms_globals.tree;
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
          }, i = e.parent ?? R;
          return i.nodes = [...i.nodes, l], D({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), D({
              createPortal: S,
              node: R
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(o) {
  return o ? Object.keys(o).reduce((t, r) => {
    const s = o[r];
    return typeof s == "number" && !Ie.includes(r) ? t[r] = s + "px" : t[r] = s, t;
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
            clonedElement: l
          } = O(n.props.el);
          return g.cloneElement(n, {
            ...n.props,
            el: l,
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
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(o.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = O(e);
      t.push(...i), r.appendChild(l);
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
const x = Y(({
  slot: o,
  clone: t,
  className: r,
  style: s
}, n) => {
  const e = K(), [l, i] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !o)
      return;
    let c = o;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(n, a), r && a.classList.add(...r.split(" ")), s) {
        const f = Oe(s);
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
  }, [o, t, r, s, n]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function H(o, t) {
  return o.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let n = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== i.length - 1 && (n = s[a]);
      });
      const c = r.slots[l];
      let p, u, _ = !1;
      c instanceof Element ? p = c : (p = c.el, u = c.callback, _ = c.clone ?? !1), n[i[i.length - 1]] = p ? u ? (...a) => (u(i[i.length - 1], a), /* @__PURE__ */ h.jsx(x, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ h.jsx(x, {
        slot: p,
        clone: _
      }) : n[i[i.length - 1]], n = s;
    });
    const e = "children";
    return r[e] && (s[e] = H(r[e])), s;
  });
}
const Pe = Se(({
  slots: o,
  items: t,
  slotItems: r,
  children: s,
  ...n
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: s
  }), /* @__PURE__ */ h.jsx(ee, {
    ...n,
    extra: o.extra ? /* @__PURE__ */ h.jsx(x, {
      slot: o.extra
    }) : n.extra,
    title: o.title ? /* @__PURE__ */ h.jsx(x, {
      slot: o.title
    }) : n.title,
    items: Z(() => t || H(r), [t, r])
  })]
}));
export {
  Pe as Descriptions,
  Pe as default
};
