import { b as $, g as ee, w as E } from "./Index-K3Abg_tV.js";
const g = window.ms_globals.React, X = window.ms_globals.React.forwardRef, R = window.ms_globals.React.useRef, M = window.ms_globals.React.useState, S = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Cascader;
function ne(r, t) {
  return $(r, t);
}
var W = {
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
var re = g, le = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(r, t, n) {
  var o, l = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) se.call(t, o) && !ae.hasOwnProperty(o) && (l[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: le,
    type: r,
    key: e,
    ref: s,
    props: l,
    _owner: ce.current
  };
}
x.Fragment = oe;
x.jsx = q;
x.jsxs = q;
W.exports = x;
var h = W.exports;
const {
  SvelteComponent: ie,
  assign: P,
  binding_callbacks: L,
  check_outros: ue,
  children: z,
  claim_element: G,
  claim_space: de,
  component_subscribe: T,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: U,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: he,
  init: ge,
  insert_hydration: y,
  safe_not_equal: be,
  set_custom_element_data: H,
  space: we,
  transition_in: v,
  transition_out: O,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: ve,
  onDestroy: Ce,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(r) {
  let t, n;
  const o = (
    /*#slots*/
    r[7].default
  ), l = _e(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = U("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), l && l.m(t, null), r[9](t), n = !0;
    },
    p(e, s) {
      l && l.p && (!n || s & /*$$scope*/
      64) && Ee(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? me(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (v(l, e), n = !0);
    },
    o(e) {
      O(l, e), n = !1;
    },
    d(e) {
      e && b(t), l && l.d(e), r[9](null);
    }
  };
}
function Ie(r) {
  let t, n, o, l, e = (
    /*$$slots*/
    r[4].default && F(r)
  );
  return {
    c() {
      t = U("react-portal-target"), n = we(), e && e.c(), o = N(), this.h();
    },
    l(s) {
      t = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(b), n = de(s), e && e.l(s), o = N(), this.h();
    },
    h() {
      H(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), r[8](t), y(s, n, c), e && e.m(s, c), y(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = F(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (he(), O(e, 1, 1, () => {
        e = null;
      }), ue());
    },
    i(s) {
      l || (v(e), l = !0);
    },
    o(s) {
      O(e), l = !1;
    },
    d(s) {
      s && (b(t), b(n), b(o)), r[8](null), e && e.d(s);
    }
  };
}
function D(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function Re(r, t, n) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = fe(e);
  let {
    svelteInit: a
  } = t;
  const _ = E(D(t)), d = E();
  T(r, d, (u) => n(0, o = u));
  const p = E();
  T(r, p, (u) => n(1, l = u));
  const i = [], f = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: J
  } = ee() || {}, Y = a({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: J,
    onDestroy(u) {
      i.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", Y), ye(() => {
    _.set(D(t));
  }), Ce(() => {
    i.forEach((u) => u());
  });
  function K(u) {
    L[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function Q(u) {
    L[u ? "unshift" : "push"](() => {
      l = u, p.set(l);
    });
  }
  return r.$$set = (u) => {
    n(17, t = P(P({}, t), A(u))), "svelteInit" in u && n(5, a = u.svelteInit), "$$scope" in u && n(6, s = u.$$scope);
  }, t = A(t), [o, l, d, p, c, a, s, e, K, Q];
}
class Se extends ie {
  constructor(t) {
    super(), ge(this, t, Re, Ie, be, {
      svelteInit: 5
    });
  }
}
const V = window.ms_globals.rerender, I = window.ms_globals.tree;
function ke(r) {
  function t(n) {
    const o = E(), l = new Se({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], V({
            createPortal: k,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), V({
              createPortal: k,
              node: I
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
      n(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(r) {
  return r ? Object.keys(r).reduce((t, n) => {
    const o = r[n];
    return typeof o == "number" && !Oe.includes(n) ? t[n] = o + "px" : t[n] = o, t;
  }, {}) : {};
}
function j(r) {
  const t = [], n = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(k(g.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: g.Children.toArray(r._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
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
    const e = o[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      t.push(...c), n.appendChild(s);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Pe(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const C = X(({
  slot: r,
  clone: t,
  className: n,
  style: o
}, l) => {
  const e = R(), [s, c] = M([]);
  return S(() => {
    var p;
    if (!e.current || !r)
      return;
    let a = r;
    function _() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Pe(l, i), n && i.classList.add(...n.split(" ")), o) {
        const f = je(o);
        Object.keys(f).forEach((m) => {
          i.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = j(r);
        a = m, c(f), a.style.display = "contents", _(), (w = e.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(a) && ((m = e.current) == null || m.removeChild(a)), i();
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", _(), (p = e.current) == null || p.appendChild(a);
    return () => {
      var i, f;
      a.style.display = "", (i = e.current) != null && i.contains(a) && ((f = e.current) == null || f.removeChild(a)), d == null || d.disconnect();
    };
  }, [r, t, n, o, l]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le({
  value: r,
  onValueChange: t
}) {
  const [n, o] = M(r), l = R(t);
  l.current = t;
  const e = R(n);
  return e.current = n, S(() => {
    l.current(n);
  }, [n]), S(() => {
    ne(r, e.current) || o(r);
  }, [r]), [n, o];
}
function B(r, t) {
  return r.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return t != null && t.fallback ? t.fallback(n) : n;
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
      let _, d, p = (t == null ? void 0 : t.clone) ?? !1;
      a instanceof Element ? _ = a : (_ = a.el, d = a.callback, p = a.clone ?? !1), l[c[c.length - 1]] = _ ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ h.jsx(C, {
        slot: _,
        clone: p
      }) : l[c[c.length - 1]], l = o;
    });
    const e = (t == null ? void 0 : t.children) || "children";
    return n[e] && (o[e] = B(n[e], t)), o;
  });
}
const Ne = ke(({
  slots: r,
  children: t,
  onValueChange: n,
  onChange: o,
  onLoadData: l,
  optionItems: e,
  options: s,
  ...c
}) => {
  const [a, _] = Le({
    onValueChange: n,
    value: c.value
  });
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(te.Panel, {
      ...c,
      value: a,
      options: Z(() => s || B(e, {
        clone: !0
      }), [s, e]),
      loadData: l,
      onChange: (d, ...p) => {
        o == null || o(d, ...p), _(d);
      },
      expandIcon: r.expandIcon ? /* @__PURE__ */ h.jsx(C, {
        slot: r.expandIcon
      }) : c.expandIcon,
      notFoundContent: r.notFoundContent ? /* @__PURE__ */ h.jsx(C, {
        slot: r.notFoundContent
      }) : c.notFoundContent
    })]
  });
});
export {
  Ne as CascaderPanel,
  Ne as default
};
