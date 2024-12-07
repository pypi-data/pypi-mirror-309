import { g as le, w as k } from "./Index-DBzM-rvq.js";
const w = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.TreeSelect;
var B = {
  exports: {}
}, T = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = w, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, r) {
  var s, l = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) ae.call(t, s) && !de.hasOwnProperty(s) && (l[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: o,
    props: l,
    _owner: ue.current
  };
}
T.Fragment = ie;
T.jsx = V;
T.jsxs = V;
B.exports = T;
var g = B.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: D,
  check_outros: _e,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: M,
  compute_slots: pe,
  create_slot: me,
  detach: b,
  element: K,
  empty: U,
  exclude_internal_props: W,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: O,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: ve,
  transition_in: S,
  transition_out: P,
  update_slot_base: Re
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Ie,
  setContext: ke
} = window.__gradio__svelte__internal;
function z(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), l = me(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = J(t);
      l && l.l(o), o.forEach(b), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      O(n, t, o), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && Re(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? we(
          s,
          /*$$scope*/
          n[6],
          o,
          null
        ) : ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(l, n), r = !0);
    },
    o(n) {
      P(l, n), r = !1;
    },
    d(n) {
      n && b(t), l && l.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, r, s, l, n = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = ve(), n && n.c(), s = U(), this.h();
    },
    l(o) {
      t = Y(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(b), r = he(o), n && n.l(o), s = U(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      O(o, t, i), e[8](t), O(o, r, i), n && n.m(o, i), O(o, s, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, i), i & /*$$slots*/
      16 && S(n, 1)) : (n = z(o), n.c(), S(n, 1), n.m(s.parentNode, s)) : n && (be(), P(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(o) {
      l || (S(n), l = !0);
    },
    o(o) {
      P(n), l = !1;
    },
    d(o) {
      o && (b(t), b(r), b(s)), e[8](null), n && n.d(o);
    }
  };
}
function G(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Se(e, t, r) {
  let s, l, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const i = pe(n);
  let {
    svelteInit: c
  } = t;
  const h = k(G(t)), f = k();
  M(e, f, (u) => r(0, s = u));
  const _ = k();
  M(e, _, (u) => r(1, l = u));
  const a = [], d = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: m,
    subSlotIndex: R
  } = le() || {}, x = c({
    parent: d,
    props: h,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: m,
    subSlotIndex: R,
    onDestroy(u) {
      a.push(u);
    }
  });
  ke("$$ms-gr-react-wrapper", x), xe(() => {
    h.set(G(t));
  }), Ie(() => {
    a.forEach((u) => u());
  });
  function C(u) {
    D[u ? "unshift" : "push"](() => {
      s = u, f.set(s);
    });
  }
  function I(u) {
    D[u ? "unshift" : "push"](() => {
      l = u, _.set(l);
    });
  }
  return e.$$set = (u) => {
    r(17, t = A(A({}, t), W(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, o = u.$$scope);
  }, t = W(t), [s, l, f, _, i, c, o, n, C, I];
}
class Te extends fe {
  constructor(t) {
    super(), ye(this, t, Se, Oe, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, j = window.ms_globals.tree;
function je(e) {
  function t(r) {
    const s = k(), l = new Te({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? j;
          return i.nodes = [...i.nodes, o], H({
            createPortal: F,
            node: j
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), H({
              createPortal: F,
              node: j
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !Fe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((l) => {
        if (w.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: o
          } = L(l.props.el);
          return w.cloneElement(l, {
            ...l.props,
            el: o,
            children: [...w.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: o,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, o, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = L(n);
      t.push(...i), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = ee(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, l) => {
  const n = te(), [o, i] = ne([]);
  return re(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(l, a), r && a.classList.add(...r.split(" ")), s) {
        const d = Pe(s);
        Object.keys(d).forEach((p) => {
          a.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m;
        const {
          portals: d,
          clonedElement: p
        } = L(e);
        c = p, i(d), c.style.display = "contents", h(), (m = n.current) == null || m.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var d, p;
        (d = n.current) != null && d.contains(c) && ((p = n.current) == null || p.removeChild(c)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", h(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var a, d;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((d = n.current) == null || d.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, t, r, s, l]), w.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Ne(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return q(() => Ne(e), [e]);
}
function Ae(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function X(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const s = {
      ...r.props
    };
    let l = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const i = o.split(".");
      i.forEach((a, d) => {
        l[a] || (l[a] = {}), d !== i.length - 1 && (l = s[a]);
      });
      const c = r.slots[o];
      let h, f, _ = (t == null ? void 0 : t.clone) ?? !1;
      c instanceof Element ? h = c : (h = c.el, f = c.callback, _ = c.clone ?? !1), l[i[i.length - 1]] = h ? f ? (...a) => (f(i[i.length - 1], a), /* @__PURE__ */ g.jsx(y, {
        slot: h,
        clone: _
      })) : /* @__PURE__ */ g.jsx(y, {
        slot: h,
        clone: _
      }) : l[i[i.length - 1]], l = s;
    });
    const n = (t == null ? void 0 : t.children) || "children";
    return r[n] && (s[n] = X(r[n], t)), s;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function v({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return r[e] ? (...l) => (t(e, l), De(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ue = je(({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: r,
  dropdownRender: s,
  tagRender: l,
  treeTitleRender: n,
  treeData: o,
  onValueChange: i,
  onChange: c,
  children: h,
  slotItems: f,
  maxTagPlaceholder: _,
  elRef: a,
  setSlotParams: d,
  onLoadData: p,
  ...m
}) => {
  const R = E(t), x = E(r), C = E(l), I = E(s), u = E(n), Z = q(() => ({
    ...m,
    loadData: p,
    treeData: o || X(f, {
      clone: !0
    }),
    dropdownRender: e.dropdownRender ? v({
      slots: e,
      setSlotParams: d,
      key: "dropdownRender"
    }) : I,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ g.jsx(y, {
        slot: e["allowClear.clearIcon"]
      })
    } : m.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(y, {
      slot: e.suffixIcon
    }) : m.suffixIcon,
    switcherIcon: e.switcherIcon ? v({
      slots: e,
      setSlotParams: d,
      key: "switcherIcon"
    }) : m.switcherIcon,
    getPopupContainer: x,
    tagRender: e.tagRender ? v({
      slots: e,
      setSlotParams: d,
      key: "tagRender"
    }) : C,
    treeTitleRender: e.treeTitleRender ? v({
      slots: e,
      setSlotParams: d,
      key: "treeTitleRender"
    }) : u,
    filterTreeNode: R || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? v({
      slots: e,
      setSlotParams: d,
      key: "maxTagPlaceholder"
    }) : _,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(y, {
      slot: e.notFoundContent
    }) : m.notFoundContent
  }), [I, t, R, x, _, p, m, d, f, e, C, o, u]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: h
    }), /* @__PURE__ */ g.jsx(oe, {
      ...Ae(Z),
      ref: a,
      onChange: (N, ...$) => {
        c == null || c(N, ...$), i(N);
      }
    })]
  });
});
export {
  Ue as TreeSelect,
  Ue as default
};
