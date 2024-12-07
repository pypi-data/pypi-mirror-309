import { b as ee, g as te, w as y } from "./Index-7xaYjh7M.js";
const g = window.ms_globals.React, U = window.ms_globals.React.forwardRef, k = window.ms_globals.React.useRef, H = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.internalContext.AutoCompleteContext, re = window.ms_globals.antd.AutoComplete;
function le(t, e) {
  return ee(t, e);
}
var B = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = g, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(t, e, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) ae.call(e, o) && !ue.hasOwnProperty(o) && (l[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: se,
    type: t,
    key: n,
    ref: s,
    props: l,
    _owner: ie.current
  };
}
R.Fragment = ce;
R.jsx = J;
R.jsxs = J;
B.exports = R;
var m = B.exports;
const {
  SvelteComponent: de,
  assign: N,
  binding_callbacks: V,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: _e,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: me,
  detach: b,
  element: Q,
  empty: M,
  exclude_internal_props: W,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: v,
  safe_not_equal: Ce,
  set_custom_element_data: X,
  space: Ee,
  transition_in: x,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: Re,
  setContext: Ie
} = window.__gradio__svelte__internal;
function q(t) {
  let e, r;
  const o = (
    /*#slots*/
    t[7].default
  ), l = me(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      v(n, e, s), l && l.m(e, null), t[9](e), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && ye(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? ge(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : he(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (x(l, n), r = !0);
    },
    o(n) {
      F(l, n), r = !1;
    },
    d(n) {
      n && b(e), l && l.d(n), t[9](null);
    }
  };
}
function Se(t) {
  let e, r, o, l, n = (
    /*$$slots*/
    t[4].default && q(t)
  );
  return {
    c() {
      e = Q("react-portal-target"), r = Ee(), n && n.c(), o = M(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(b), r = _e(s), n && n.l(s), o = M(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, e, c), t[8](e), v(s, r, c), n && n.m(s, c), v(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && x(n, 1)) : (n = q(s), n.c(), x(n, 1), n.m(o.parentNode, o)) : n && (we(), F(n, 1, 1, () => {
        n = null;
      }), fe());
    },
    i(s) {
      l || (x(n), l = !0);
    },
    o(s) {
      F(n), l = !1;
    },
    d(s) {
      s && (b(e), b(r), b(o)), t[8](null), n && n.d(s);
    }
  };
}
function z(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function Oe(t, e, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const c = pe(n);
  let {
    svelteInit: a
  } = e;
  const p = y(z(e)), d = y();
  D(t, d, (u) => r(0, o = u));
  const f = y();
  D(t, f, (u) => r(1, l = u));
  const i = [], _ = xe("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: w,
    subSlotIndex: I
  } = te() || {}, E = a({
    parent: _,
    props: p,
    target: d,
    slot: f,
    slotKey: h,
    slotIndex: w,
    subSlotIndex: I,
    onDestroy(u) {
      i.push(u);
    }
  });
  Ie("$$ms-gr-react-wrapper", E), ve(() => {
    p.set(z(e));
  }), Re(() => {
    i.forEach((u) => u());
  });
  function S(u) {
    V[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function $(u) {
    V[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  return t.$$set = (u) => {
    r(17, e = N(N({}, e), W(u))), "svelteInit" in u && r(5, a = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, e = W(e), [o, l, d, f, c, a, s, n, S, $];
}
class je extends de {
  constructor(e) {
    super(), be(this, e, Oe, Se, Ce, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, O = window.ms_globals.tree;
function ke(t) {
  function e(r) {
    const o = y(), l = new je({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? O;
          return c.nodes = [...c.nodes, s], G({
            createPortal: A,
            node: O
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), G({
              createPortal: A,
              node: O
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const o = t[r];
    return typeof o == "number" && !Pe.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function L(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(A(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: a
    }) => {
      r.addEventListener(c, s, a);
    });
  });
  const o = Array.from(t.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = L(n);
      e.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Fe(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const C = U(({
  slot: t,
  clone: e,
  className: r,
  style: o
}, l) => {
  const n = k(), [s, c] = H([]);
  return P(() => {
    var f;
    if (!n.current || !t)
      return;
    let a = t;
    function p() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Fe(l, i), r && i.classList.add(...r.split(" ")), o) {
        const _ = Ae(o);
        Object.keys(_).forEach((h) => {
          i.style[h] = _[h];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w;
        const {
          portals: _,
          clonedElement: h
        } = L(t);
        a = h, c(_), a.style.display = "contents", p(), (w = n.current) == null || w.appendChild(a);
      };
      i(), d = new window.MutationObserver(() => {
        var _, h;
        (_ = n.current) != null && _.contains(a) && ((h = n.current) == null || h.removeChild(a)), i();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", p(), (f = n.current) == null || f.appendChild(a);
    return () => {
      var i, _;
      a.style.display = "", (i = n.current) != null && i.contains(a) && ((_ = n.current) == null || _.removeChild(a)), d == null || d.disconnect();
    };
  }, [t, e, r, o, l]), g.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function j(t) {
  return T(() => Le(t), [t]);
}
function Te({
  value: t,
  onValueChange: e
}) {
  const [r, o] = H(t), l = k(e);
  l.current = e;
  const n = k(r);
  return n.current = r, P(() => {
    l.current(r);
  }, [r]), P(() => {
    le(t, n.current) || o(t);
  }, [t]), [r, o];
}
function Z(t, e) {
  return t.filter(Boolean).map((r) => {
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
      c.forEach((i, _) => {
        l[i] || (l[i] = {}), _ !== c.length - 1 && (l = o[i]);
      });
      const a = r.slots[s];
      let p, d, f = (e == null ? void 0 : e.clone) ?? !1;
      a instanceof Element ? p = a : (p = a.el, d = a.callback, f = a.clone ?? !1), l[c[c.length - 1]] = p ? d ? (...i) => (d(c[c.length - 1], i), /* @__PURE__ */ m.jsx(C, {
        slot: p,
        clone: f
      })) : /* @__PURE__ */ m.jsx(C, {
        slot: p,
        clone: f
      }) : l[c[c.length - 1]], l = o;
    });
    const n = (e == null ? void 0 : e.children) || "children";
    return r[n] && (o[n] = Z(r[n], e)), o;
  });
}
function Ne(t, e) {
  return t ? /* @__PURE__ */ m.jsx(C, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ve({
  key: t,
  setSlotParams: e,
  slots: r
}, o) {
  return r[t] ? (...l) => (e(t, l), Ne(r[t], {
    clone: !0,
    ...o
  })) : void 0;
}
const De = U(({
  children: t,
  ...e
}, r) => /* @__PURE__ */ m.jsx(ne.Provider, {
  value: T(() => ({
    ...e,
    elRef: r
  }), [e, r]),
  children: t
})), We = ke(({
  slots: t,
  children: e,
  onValueChange: r,
  filterOption: o,
  onChange: l,
  options: n,
  optionItems: s,
  getPopupContainer: c,
  dropdownRender: a,
  elRef: p,
  setSlotParams: d,
  ...f
}) => {
  const i = j(c), _ = j(o), h = j(a), [w, I] = Te({
    onValueChange: r,
    value: f.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [t.children ? null : /* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(re, {
      ...f,
      value: w,
      ref: p,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(C, {
          slot: t["allowClear.clearIcon"]
        })
      } : f.allowClear,
      options: T(() => n || Z(s, {
        children: "options",
        clone: !0
      }), [s, n]),
      onChange: (E, ...S) => {
        l == null || l(E, ...S), I(E);
      },
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ m.jsx(C, {
        slot: t.notFoundContent
      }) : f.notFoundContent,
      filterOption: _ || o,
      getPopupContainer: i,
      dropdownRender: t.dropdownRender ? Ve({
        slots: t,
        setSlotParams: d,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : h,
      children: t.children ? /* @__PURE__ */ m.jsxs(De, {
        children: [/* @__PURE__ */ m.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ m.jsx(C, {
          slot: t.children
        })]
      }) : null
    })]
  });
});
export {
  We as AutoComplete,
  We as default
};
