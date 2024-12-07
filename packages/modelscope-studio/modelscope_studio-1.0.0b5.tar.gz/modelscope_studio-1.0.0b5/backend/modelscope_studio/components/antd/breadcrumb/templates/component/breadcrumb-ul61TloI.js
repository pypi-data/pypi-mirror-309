import { g as $, w as E } from "./Index-C9cJH5Fp.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Breadcrumb;
var B = {
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
var te = g, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(r, e, n) {
  var o, l = {}, t = null, s = null;
  n !== void 0 && (t = "" + n), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) le.call(e, o) && !se.hasOwnProperty(o) && (l[o] = e[o]);
  if (r && r.defaultProps) for (o in e = r.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: re,
    type: r,
    key: t,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
C.Fragment = ne;
C.jsx = F;
C.jsxs = F;
B.exports = C;
var h = B.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ae,
  children: M,
  claim_element: W,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: de,
  detach: b,
  element: z,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: pe,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: G,
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
function N(r) {
  let e, n;
  const o = (
    /*#slots*/
    r[7].default
  ), l = de(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      e = z("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = W(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = M(e);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      G(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      y(t, e, s), l && l.m(e, null), r[9](e), n = !0;
    },
    p(t, s) {
      l && l.p && (!n || s & /*$$scope*/
      64) && be(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        n ? _e(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (v(l, t), n = !0);
    },
    o(t) {
      I(l, t), n = !1;
    },
    d(t) {
      t && b(e), l && l.d(t), r[9](null);
    }
  };
}
function Re(r) {
  let e, n, o, l, t = (
    /*$$slots*/
    r[4].default && N(r)
  );
  return {
    c() {
      e = z("react-portal-target"), n = ge(), t && t.c(), o = L(), this.h();
    },
    l(s) {
      e = W(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(e).forEach(b), n = ie(s), t && t.l(s), o = L(), this.h();
    },
    h() {
      G(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, e, c), r[8](e), y(s, n, c), t && t.m(s, c), y(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = N(s), t.c(), v(t, 1), t.m(o.parentNode, o)) : t && (me(), I(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      l || (v(t), l = !0);
    },
    o(s) {
      I(t), l = !1;
    },
    d(s) {
      s && (b(e), b(n), b(o)), r[8](null), t && t.d(s);
    }
  };
}
function A(r) {
  const {
    svelteInit: e,
    ...n
  } = r;
  return n;
}
function Ce(r, e, n) {
  let o, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = ue(t);
  let {
    svelteInit: a
  } = e;
  const _ = E(A(e)), d = E();
  P(r, d, (u) => n(0, o = u));
  const m = E();
  P(r, m, (u) => n(1, l = u));
  const i = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H
  } = $() || {}, q = a({
    parent: f,
    props: _,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(u) {
      i.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", q), we(() => {
    _.set(A(e));
  }), ye(() => {
    i.forEach((u) => u());
  });
  function V(u) {
    j[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function J(u) {
    j[u ? "unshift" : "push"](() => {
      l = u, m.set(l);
    });
  }
  return r.$$set = (u) => {
    n(17, e = k(k({}, e), T(u))), "svelteInit" in u && n(5, a = u.svelteInit), "$$scope" in u && n(6, s = u.$$scope);
  }, e = T(e), [o, l, d, m, c, a, s, t, V, J];
}
class xe extends ce {
  constructor(e) {
    super(), pe(this, e, Ce, Re, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, x = window.ms_globals.tree;
function Se(r) {
  function e(n) {
    const o = E(), l = new xe({
      ...n,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? x;
          return c.nodes = [...c.nodes, s], D({
            createPortal: S,
            node: x
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), D({
              createPortal: S,
              node: x
            });
          }), s;
        },
        ...n.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(e);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(r) {
  return r ? Object.keys(r).reduce((e, n) => {
    const o = r[n];
    return typeof o == "number" && !Ie.includes(n) ? e[n] = o + "px" : e[n] = o, e;
  }, {}) : {};
}
function O(r) {
  const e = [], n = r.cloneNode(!1);
  if (r._reactElement)
    return e.push(S(g.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: g.Children.toArray(r._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = O(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: e
    };
  Object.keys(r.getEventListeners()).forEach((l) => {
    r.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      n.addEventListener(c, s, a);
    });
  });
  const o = Array.from(r.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = O(t);
      e.push(...c), n.appendChild(s);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function ke(r, e) {
  r && (typeof r == "function" ? r(e) : r.current = e);
}
const R = Y(({
  slot: r,
  clone: e,
  className: n,
  style: o
}, l) => {
  const t = K(), [s, c] = Q([]);
  return X(() => {
    var m;
    if (!t.current || !r)
      return;
    let a = r;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(l, i), n && i.classList.add(...n.split(" ")), o) {
        const f = Oe(o);
        Object.keys(f).forEach((p) => {
          i.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: p
        } = O(r);
        a = p, c(f), a.style.display = "contents", _(), (w = t.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var f, p;
        (f = t.current) != null && f.contains(a) && ((p = t.current) == null || p.removeChild(a)), i();
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (m = t.current) == null || m.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = t.current) != null && i.contains(a) && ((f = t.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [r, e, n, o, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function U(r, e) {
  return r.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return e != null && e.fallback ? e.fallback(n) : n;
    const o = {
      ...n.props
    };
    let l = o;
    Object.keys(n.slots).forEach((s) => {
      if (!n.slots[s] || !(n.slots[s] instanceof Element) && !n.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((i, f) => {
        l[i] || (l[i] = {}), f !== c.length - 1 && (l = o[i]);
      });
      const a = n.slots[s];
      let _, d, m = (e == null ? void 0 : e.clone) ?? !1;
      a instanceof Element ? _ = a : (_ = a.el, d = a.callback, m = a.clone ?? !1), l[c[c.length - 1]] = _ ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ h.jsx(R, {
        slot: _,
        clone: m
      })) : /* @__PURE__ */ h.jsx(R, {
        slot: _,
        clone: m
      }) : l[c[c.length - 1]], l = o;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return n[t] && (o[t] = U(n[t], e)), o;
  });
}
function je(r, e) {
  return r ? /* @__PURE__ */ h.jsx(R, {
    slot: r,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Pe({
  key: r,
  setSlotParams: e,
  slots: n
}, o) {
  return n[r] ? (...l) => (e(r, l), je(n[r], {
    clone: !0,
    ...o
  })) : void 0;
}
const Te = Se(({
  slots: r,
  items: e,
  slotItems: n,
  setSlotParams: o,
  children: l,
  ...t
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ h.jsx(ee, {
    ...t,
    itemRender: r.itemRender ? Pe({
      setSlotParams: o,
      slots: r,
      key: "itemRender"
    }, {
      clone: !0
    }) : t.itemRender,
    items: Z(() => e || U(n, {
      clone: !0
    }), [e, n]),
    separator: r.separator ? /* @__PURE__ */ h.jsx(R, {
      slot: r.separator,
      clone: !0
    }) : t.separator
  })]
}));
export {
  Te as Breadcrumb,
  Te as default
};
