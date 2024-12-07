import { g as $, w as E } from "./Index-CIcel_0i.js";
const h = window.ms_globals.React, D = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Collapse;
var M = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, e, r) {
  var o, l = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) le.call(e, o) && !se.hasOwnProperty(o) && (l[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
x.Fragment = re;
x.jsx = W;
x.jsxs = W;
M.exports = x;
var b = M.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: P,
  check_outros: ae,
  children: z,
  claim_element: G,
  claim_space: ie,
  component_subscribe: j,
  compute_slots: ue,
  create_slot: de,
  detach: g,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: v,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(n) {
  let e, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = de(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = U("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = G(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(e);
      l && l.l(s), s.forEach(g), this.h();
    },
    h() {
      H(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      y(t, e, s), l && l.m(e, null), n[9](e), r = !0;
    },
    p(t, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && be(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? _e(
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
      r || (v(l, t), r = !0);
    },
    o(t) {
      R(l, t), r = !1;
    },
    d(t) {
      t && g(e), l && l.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, r, o, l, t = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      e = U("react-portal-target"), r = ge(), t && t.c(), o = L(), this.h();
    },
    l(s) {
      e = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(e).forEach(g), r = ie(s), t && t.l(s), o = L(), this.h();
    },
    h() {
      H(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, e, c), n[8](e), y(s, r, c), t && t.m(s, c), y(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = N(s), t.c(), v(t, 1), t.m(o.parentNode, o)) : t && (pe(), R(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      l || (v(t), l = !0);
    },
    o(s) {
      R(t), l = !1;
    },
    d(s) {
      s && (g(e), g(r), g(o)), n[8](null), t && t.d(s);
    }
  };
}
function A(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Ce(n, e, r) {
  let o, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = ue(t);
  let {
    svelteInit: a
  } = e;
  const _ = E(A(e)), d = E();
  j(n, d, (u) => r(0, o = u));
  const p = E();
  j(n, p, (u) => r(1, l = u));
  const i = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: B
  } = $() || {}, V = a({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: B,
    onDestroy(u) {
      i.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", V), we(() => {
    _.set(A(e));
  }), ye(() => {
    i.forEach((u) => u());
  });
  function J(u) {
    P[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function Y(u) {
    P[u ? "unshift" : "push"](() => {
      l = u, p.set(l);
    });
  }
  return n.$$set = (u) => {
    r(17, e = k(k({}, e), T(u))), "svelteInit" in u && r(5, a = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, e = T(e), [o, l, d, p, c, a, s, t, J, Y];
}
class Ie extends ce {
  constructor(e) {
    super(), me(this, e, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, C = window.ms_globals.tree;
function Re(n) {
  function e(r) {
    const o = E(), l = new Ie({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? C;
          return c.nodes = [...c.nodes, s], F({
            createPortal: I,
            node: C
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), F({
              createPortal: I,
              node: C
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
function Se(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Oe(n) {
  return D(() => Se(n), [n]);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const o = n[r];
    return typeof o == "number" && !ke.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function S(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(I(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((l) => {
        if (h.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = S(l.props.el);
          return h.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...h.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      r.addEventListener(c, s, a);
    });
  });
  const o = Array.from(n.childNodes);
  for (let l = 0; l < o.length; l++) {
    const t = o[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = S(t);
      e.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const O = K(({
  slot: n,
  clone: e,
  className: r,
  style: o
}, l) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var p;
    if (!t.current || !n)
      return;
    let a = n;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), je(l, i), r && i.classList.add(...r.split(" ")), o) {
        const f = Pe(o);
        Object.keys(f).forEach((m) => {
          i.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = S(n);
        a = m, c(f), a.style.display = "contents", _(), (w = t.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var f, m;
        (f = t.current) != null && f.contains(a) && ((m = t.current) == null || m.removeChild(a)), i();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (p = t.current) == null || p.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = t.current) != null && i.contains(a) && ((f = t.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [n, e, r, o, l]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function q(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const o = {
      ...r.props
    };
    let l = o;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((i, f) => {
        l[i] || (l[i] = {}), f !== c.length - 1 && (l = o[i]);
      });
      const a = r.slots[s];
      let _, d, p = (e == null ? void 0 : e.clone) ?? !1;
      a instanceof Element ? _ = a : (_ = a.el, d = a.callback, p = a.clone ?? !1), l[c[c.length - 1]] = _ ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ b.jsx(O, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ b.jsx(O, {
        slot: _,
        clone: p
      }) : l[c[c.length - 1]], l = o;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (o[t] = q(r[t], e)), o;
  });
}
function Le(n, e) {
  return n ? /* @__PURE__ */ b.jsx(O, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: e,
  slots: r
}, o) {
  return r[n] ? (...l) => (e(n, l), Le(r[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ae = Re(({
  slots: n,
  items: e,
  slotItems: r,
  children: o,
  onChange: l,
  setSlotParams: t,
  expandIcon: s,
  ...c
}) => {
  const a = Oe(s);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [o, /* @__PURE__ */ b.jsx(ee, {
      ...c,
      onChange: (_) => {
        l == null || l(_);
      },
      expandIcon: n.expandIcon ? Te({
        slots: n,
        setSlotParams: t,
        key: "expandIcon"
      }) : a,
      items: D(() => e || q(r, {
        clone: !0
      }), [e, r])
    })]
  });
});
export {
  Ae as Collapse,
  Ae as default
};
