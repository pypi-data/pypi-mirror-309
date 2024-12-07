import { g as Oe, w as L } from "./Index-CDBbwO8S.js";
const C = window.ms_globals.React, Ce = window.ms_globals.React.forwardRef, be = window.ms_globals.React.useRef, Ee = window.ms_globals.React.useState, ye = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, B = window.ms_globals.ReactDOM.createPortal, R = window.ms_globals.antd.Table;
var Z = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ve = C, Re = Symbol.for("react.element"), Se = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(n, e, r) {
  var l, o = {}, t = null, i = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (l in e) ke.call(e, l) && !Ne.hasOwnProperty(l) && (o[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: Re,
    type: n,
    key: t,
    ref: i,
    props: o,
    _owner: xe.current
  };
}
F.Fragment = Se;
F.jsx = $;
F.jsxs = $;
Z.exports = F;
var m = Z.exports;
const {
  SvelteComponent: Te,
  assign: Q,
  binding_callbacks: W,
  check_outros: Le,
  children: ee,
  claim_element: te,
  claim_space: Ie,
  component_subscribe: z,
  compute_slots: je,
  create_slot: Pe,
  detach: O,
  element: ne,
  empty: X,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ae,
  group_outros: Me,
  init: Ue,
  insert_hydration: I,
  safe_not_equal: De,
  set_custom_element_data: re,
  space: Be,
  transition_in: j,
  transition_out: G,
  update_slot_base: Ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: He,
  onDestroy: Qe,
  setContext: We
} = window.__gradio__svelte__internal;
function V(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = Pe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = ne("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = te(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = ee(e);
      o && o.l(i), i.forEach(O), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      I(t, e, i), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, i) {
      o && o.p && (!r || i & /*$$scope*/
      64) && Ge(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Ae(
          l,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (j(o, t), r = !0);
    },
    o(t) {
      G(o, t), r = !1;
    },
    d(t) {
      t && O(e), o && o.d(t), n[9](null);
    }
  };
}
function ze(n) {
  let e, r, l, o, t = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      e = ne("react-portal-target"), r = Be(), t && t.c(), l = X(), this.h();
    },
    l(i) {
      e = te(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(O), r = Ie(i), t && t.l(i), l = X(), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      I(i, e, s), n[8](e), I(i, r, s), t && t.m(i, s), I(i, l, s), o = !0;
    },
    p(i, [s]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, s), s & /*$$slots*/
      16 && j(t, 1)) : (t = V(i), t.c(), j(t, 1), t.m(l.parentNode, l)) : t && (Me(), G(t, 1, 1, () => {
        t = null;
      }), Le());
    },
    i(i) {
      o || (j(t), o = !0);
    },
    o(i) {
      G(t), o = !1;
    },
    d(i) {
      i && (O(e), O(r), O(l)), n[8](null), t && t.d(i);
    }
  };
}
function K(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Xe(n, e, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: i
  } = e;
  const s = je(t);
  let {
    svelteInit: c
  } = e;
  const _ = L(K(e)), d = L();
  z(n, d, (u) => r(0, l = u));
  const p = L();
  z(n, p, (u) => r(1, o = u));
  const a = [], f = He("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: E,
    subSlotIndex: v
  } = Oe() || {}, A = c({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: g,
    slotIndex: E,
    subSlotIndex: v,
    onDestroy(u) {
      a.push(u);
    }
  });
  We("$$ms-gr-react-wrapper", A), Je(() => {
    _.set(K(e));
  }), Qe(() => {
    a.forEach((u) => u());
  });
  function M(u) {
    W[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function y(u) {
    W[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, e = Q(Q({}, e), q(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, i = u.$$scope);
  }, e = q(e), [l, o, d, p, s, c, i, t, M, y];
}
class qe extends Te {
  constructor(e) {
    super(), Ue(this, e, Xe, ze, De, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, D = window.ms_globals.tree;
function Ve(n) {
  function e(r) {
    const l = L(), o = new qe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, s = t.parent ?? D;
          return s.nodes = [...s.nodes, i], Y({
            createPortal: B,
            node: D
          }), t.onDestroy(() => {
            s.nodes = s.nodes.filter((c) => c.svelteInstance !== l), Y({
              createPortal: B,
              node: D
            });
          }), i;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ye(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !Ke.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function J(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(B(C.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: C.Children.toArray(n._reactElement.props.children).map((o) => {
        if (C.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = J(o.props.el);
          return C.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...C.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: i,
      type: s,
      useCapture: c
    }) => {
      r.addEventListener(s, i, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: i,
        portals: s
      } = J(t);
      e.push(...s), r.appendChild(i);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Ze(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const b = Ce(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, o) => {
  const t = be(), [i, s] = Ee([]);
  return ye(() => {
    var p;
    if (!t.current || !n)
      return;
    let c = n;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ze(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Ye(l);
        Object.keys(f).forEach((g) => {
          a.style[g] = f[g];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var E;
        const {
          portals: f,
          clonedElement: g
        } = J(n);
        c = g, s(f), c.style.display = "contents", _(), (E = t.current) == null || E.appendChild(c);
      };
      a(), d = new window.MutationObserver(() => {
        var f, g;
        (f = t.current) != null && f.contains(c) && ((g = t.current) == null || g.removeChild(c)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (p = t.current) == null || p.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((f = t.current) == null || f.removeChild(c)), d == null || d.disconnect();
    };
  }, [n, e, r, l, o]), C.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function $e(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function h(n) {
  return T(() => $e(n), [n]);
}
function et(n) {
  return Object.keys(n).reduce((e, r) => (n[r] !== void 0 && (e[r] = n[r]), e), {});
}
function P(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((i) => {
      if (!r.slots[i] || !(r.slots[i] instanceof Element) && !r.slots[i].el)
        return;
      const s = i.split(".");
      s.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== s.length - 1 && (o = l[a]);
      });
      const c = r.slots[i];
      let _, d, p = (e == null ? void 0 : e.clone) ?? !1;
      c instanceof Element ? _ = c : (_ = c.el, d = c.callback, p = c.clone ?? !1), o[s[s.length - 1]] = _ ? d ? (...a) => (d(s[s.length - 1], a), /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: p
      }) : o[s[s.length - 1]], o = l;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (l[t] = P(r[t], e)), l;
  });
}
function tt(n, e) {
  return n ? /* @__PURE__ */ m.jsx(b, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function x({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return r[n] ? (...o) => (e(n, o), tt(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
function N(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const rt = Ve(({
  children: n,
  slots: e,
  columnItems: r,
  columns: l,
  getPopupContainer: o,
  pagination: t,
  loading: i,
  rowKey: s,
  rowClassName: c,
  summary: _,
  rowSelection: d,
  rowSelectionItems: p,
  expandableItems: a,
  expandable: f,
  sticky: g,
  footer: E,
  showSorterTooltip: v,
  onRow: A,
  onHeaderRow: M,
  setSlotParams: y,
  ...u
}) => {
  const oe = h(o), le = e["loading.tip"] || e["loading.indicator"], U = N(i), ie = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], S = N(t), se = h(S.showTotal), ce = h(c), ae = h(s), ue = e["showSorterTooltip.title"] || typeof v == "object", k = N(v), de = h(k.afterOpenChange), fe = h(k.getPopupContainer), pe = typeof g == "object", H = N(g), _e = h(H.getContainer), ge = h(A), he = h(M), me = h(_), we = h(E);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ m.jsx(R, {
      ...u,
      columns: T(() => (l == null ? void 0 : l.map((w) => w === "EXPAND_COLUMN" ? R.EXPAND_COLUMN : w === "SELECTION_COLUMN" ? R.SELECTION_COLUMN : w)) || P(r, {
        fallback: (w) => w === "EXPAND_COLUMN" ? R.EXPAND_COLUMN : w === "SELECTION_COLUMN" ? R.SELECTION_COLUMN : w
      }), [r, l]),
      onRow: ge,
      onHeaderRow: he,
      summary: e.summary ? x({
        slots: e,
        setSlotParams: y,
        key: "summary"
      }) : me,
      rowSelection: T(() => d || P(p)[0], [d, p]),
      expandable: T(() => f || P(a)[0], [f, a]),
      rowClassName: ce,
      rowKey: ae || s,
      sticky: pe ? {
        ...H,
        getContainer: _e
      } : g,
      showSorterTooltip: ue ? {
        ...k,
        afterOpenChange: de,
        getPopupContainer: fe,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ m.jsx(b, {
          slot: e["showSorterTooltip.title"]
        }) : k.title
      } : v,
      pagination: ie ? et({
        ...S,
        showTotal: se,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ m.jsx(b, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : S.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? x({
          slots: e,
          setSlotParams: y,
          key: "pagination.itemRender"
        }) : S.itemRender
      }) : t,
      getPopupContainer: oe,
      loading: le ? {
        ...U,
        tip: e["loading.tip"] ? /* @__PURE__ */ m.jsx(b, {
          slot: e["loading.tip"]
        }) : U.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ m.jsx(b, {
          slot: e["loading.indicator"]
        }) : U.indicator
      } : i,
      footer: e.footer ? x({
        slots: e,
        setSlotParams: y,
        key: "footer"
      }) : we,
      title: e.title ? x({
        slots: e,
        setSlotParams: y,
        key: "title"
      }) : u.title
    })]
  });
});
export {
  rt as Table,
  rt as default
};
