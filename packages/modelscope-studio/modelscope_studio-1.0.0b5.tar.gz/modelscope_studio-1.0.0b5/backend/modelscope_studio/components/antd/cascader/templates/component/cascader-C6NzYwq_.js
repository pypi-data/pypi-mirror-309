import { b as fe, g as _e, w as v } from "./Index-CAIQVcVx.js";
const E = window.ms_globals.React, de = window.ms_globals.React.forwardRef, T = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, L = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.antd.Cascader;
function pe(e, t) {
  return fe(e, t);
}
var K = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = E, ge = Symbol.for("react.element"), we = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ye = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, t, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) be.call(t, l) && !Ee.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ge,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: ye.current
  };
}
k.Fragment = we;
k.jsx = Q;
k.jsxs = Q;
K.exports = k;
var m = K.exports;
const {
  SvelteComponent: xe,
  assign: M,
  binding_callbacks: W,
  check_outros: Ce,
  children: X,
  claim_element: Z,
  claim_space: Re,
  component_subscribe: q,
  compute_slots: ve,
  create_slot: Ie,
  detach: C,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Se,
  get_slot_changes: ke,
  group_outros: je,
  init: Oe,
  insert_hydration: I,
  safe_not_equal: Fe,
  set_custom_element_data: ee,
  space: Pe,
  transition_in: S,
  transition_out: A,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Le,
  getContext: Ne,
  onDestroy: Ae,
  setContext: De
} = window.__gradio__svelte__internal;
function U(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = Ie(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Z(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(t);
      o && o.l(s), s.forEach(C), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      I(n, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Te(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? ke(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : Se(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(o, n), r = !0);
    },
    o(n) {
      A(o, n), r = !1;
    },
    d(n) {
      n && C(t), o && o.d(n), e[9](null);
    }
  };
}
function Ve(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && U(e)
  );
  return {
    c() {
      t = $("react-portal-target"), r = Pe(), n && n.c(), l = z(), this.h();
    },
    l(s) {
      t = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(t).forEach(C), r = Re(s), n && n.l(s), l = z(), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, t, a), e[8](t), I(s, r, a), n && n.m(s, a), I(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, a), a & /*$$slots*/
      16 && S(n, 1)) : (n = U(s), n.c(), S(n, 1), n.m(l.parentNode, l)) : n && (je(), A(n, 1, 1, () => {
        n = null;
      }), Ce());
    },
    i(s) {
      o || (S(n), o = !0);
    },
    o(s) {
      A(n), o = !1;
    },
    d(s) {
      s && (C(t), C(r), C(l)), e[8](null), n && n.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Me(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const a = ve(n);
  let {
    svelteInit: c
  } = t;
  const p = v(H(t)), f = v();
  q(e, f, (u) => r(0, l = u));
  const _ = v();
  q(e, _, (u) => r(1, o = u));
  const i = [], d = Ne("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: x,
    subSlotIndex: g
  } = _e() || {}, j = c({
    parent: d,
    props: p,
    target: f,
    slot: _,
    slotKey: h,
    slotIndex: x,
    subSlotIndex: g,
    onDestroy(u) {
      i.push(u);
    }
  });
  De("$$ms-gr-react-wrapper", j), Le(() => {
    p.set(H(t));
  }), Ae(() => {
    i.forEach((u) => u());
  });
  function O(u) {
    W[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function F(u) {
    W[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, t = M(M({}, t), G(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = G(t), [l, o, f, _, a, c, s, n, O, F];
}
class We extends xe {
  constructor(t) {
    super(), Oe(this, t, Me, Ve, Fe, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, P = window.ms_globals.tree;
function qe(e) {
  function t(r) {
    const l = v(), o = new We({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? P;
          return a.nodes = [...a.nodes, s], B({
            createPortal: N,
            node: P
          }), n.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== l), B({
              createPortal: N,
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
      r(t);
    });
  });
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !ze.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(N(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...E.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, s, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(n);
      t.push(...a), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ue(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const b = de(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = T(), [s, a] = J([]);
  return L(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function p() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ue(o, i), r && i.classList.add(...r.split(" ")), l) {
        const d = Ge(l);
        Object.keys(d).forEach((h) => {
          i.style[h] = d[h];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var x;
        const {
          portals: d,
          clonedElement: h
        } = D(e);
        c = h, a(d), c.style.display = "contents", p(), (x = n.current) == null || x.appendChild(c);
      };
      i(), f = new window.MutationObserver(() => {
        var d, h;
        (d = n.current) != null && d.contains(c) && ((h = n.current) == null || h.removeChild(c)), i();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var i, d;
      c.style.display = "", (i = n.current) != null && i.contains(c) && ((d = n.current) == null || d.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, t, r, l, o]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function He(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(e) {
  return Y(() => He(e), [e]);
}
function Be({
  value: e,
  onValueChange: t
}) {
  const [r, l] = J(e), o = T(t);
  o.current = t;
  const n = T(r);
  return n.current = r, L(() => {
    o.current(r);
  }, [r]), L(() => {
    pe(e, n.current) || l(e);
  }, [e]), [r, l];
}
function te(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const a = s.split(".");
      a.forEach((i, d) => {
        o[i] || (o[i] = {}), d !== a.length - 1 && (o = l[i]);
      });
      const c = r.slots[s];
      let p, f, _ = (t == null ? void 0 : t.clone) ?? !1;
      c instanceof Element ? p = c : (p = c.el, f = c.callback, _ = c.clone ?? !1), o[a[a.length - 1]] = p ? f ? (...i) => (f(a[a.length - 1], i), /* @__PURE__ */ m.jsx(b, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ m.jsx(b, {
        slot: p,
        clone: _
      }) : o[a[a.length - 1]], o = l;
    });
    const n = (t == null ? void 0 : t.children) || "children";
    return r[n] && (l[n] = te(r[n], t)), l;
  });
}
function Je(e, t) {
  return e ? /* @__PURE__ */ m.jsx(b, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function R({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), Je(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function Ye(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Qe = qe(({
  slots: e,
  children: t,
  onValueChange: r,
  onChange: l,
  displayRender: o,
  elRef: n,
  getPopupContainer: s,
  tagRender: a,
  maxTagPlaceholder: c,
  dropdownRender: p,
  optionRender: f,
  showSearch: _,
  optionItems: i,
  options: d,
  setSlotParams: h,
  onLoadData: x,
  ...g
}) => {
  const j = w(s), O = w(o), F = w(a), u = w(f), ne = w(p), re = w(c), oe = typeof _ == "object" || e["showSearch.render"], y = Ye(_), le = w(y.filter), se = w(y.render), ce = w(y.sort), [ae, ie] = Be({
    onValueChange: r,
    value: g.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ m.jsx(he, {
      ...g,
      ref: n,
      value: ae,
      options: Y(() => d || te(i, {
        clone: !0
      }), [d, i]),
      showSearch: oe ? {
        ...y,
        filter: le || y.filter,
        render: e["showSearch.render"] ? R({
          slots: e,
          setSlotParams: h,
          key: "showSearch.render"
        }) : se || y.render,
        sort: ce || y.sort
      } : _,
      loadData: x,
      optionRender: u,
      getPopupContainer: j,
      dropdownRender: e.dropdownRender ? R({
        slots: e,
        setSlotParams: h,
        key: "dropdownRender"
      }) : ne,
      displayRender: e.displayRender ? R({
        slots: e,
        setSlotParams: h,
        key: "displayRender"
      }) : O,
      tagRender: e.tagRender ? R({
        slots: e,
        setSlotParams: h,
        key: "tagRender"
      }) : F,
      onChange: (V, ...ue) => {
        l == null || l(V, ...ue), ie(V);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.suffixIcon
      }) : g.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.expandIcon
      }) : g.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.removeIcon
      }) : g.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(b, {
        slot: e.notFoundContent
      }) : g.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? R({
        slots: e,
        setSlotParams: h,
        key: "maxTagPlaceholder"
      }) : re || c,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : g.allowClear
    })]
  });
});
export {
  Qe as Cascader,
  Qe as default
};
