import { g as we, w as O } from "./Index-Ci1kjl9s.js";
const y = window.ms_globals.React, he = window.ms_globals.React.forwardRef, ve = window.ms_globals.React.useRef, be = window.ms_globals.React.useState, ge = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, ye = window.ms_globals.antd.DatePicker, z = window.ms_globals.dayjs;
var X = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xe = y, Ee = Symbol.for("react.element"), Ie = Symbol.for("react.fragment"), Re = Object.prototype.hasOwnProperty, Ce = xe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) Re.call(n, l) && !je.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: Ee,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: Ce.current
  };
}
D.Fragment = Ie;
D.jsx = Z;
D.jsxs = Z;
X.exports = D;
var m = X.exports;
const {
  SvelteComponent: ke,
  assign: G,
  binding_callbacks: U,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: De,
  detach: I,
  element: te,
  empty: q,
  exclude_internal_props: B,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ne,
  group_outros: Ae,
  init: Le,
  insert_hydration: S,
  safe_not_equal: Te,
  set_custom_element_data: ne,
  space: Me,
  transition_in: P,
  transition_out: V,
  update_slot_base: Ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function J(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = De(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(n);
      r && r.l(s), s.forEach(I), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      S(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ve(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? Ne(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : Fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (P(r, t), o = !0);
    },
    o(t) {
      V(r, t), o = !1;
    },
    d(t) {
      t && I(n), r && r.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && J(e)
  );
  return {
    c() {
      n = te("react-portal-target"), o = Me(), t && t.c(), l = q(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(I), o = Se(s), t && t.l(s), l = q(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      S(s, n, c), e[8](n), S(s, o, c), t && t.m(s, c), S(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && P(t, 1)) : (t = J(s), t.c(), P(t, 1), t.m(l.parentNode, l)) : t && (Ae(), V(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(s) {
      r || (P(t), r = !0);
    },
    o(s) {
      V(t), r = !1;
    },
    d(s) {
      s && (I(n), I(o), I(l)), e[8](null), t && t.d(s);
    }
  };
}
function Y(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function qe(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = Pe(t);
  let {
    svelteInit: i
  } = n;
  const _ = O(Y(n)), d = O();
  H(e, d, (u) => o(0, l = u));
  const p = O();
  H(e, p, (u) => o(1, r = u));
  const a = [], f = ze("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: x,
    subSlotIndex: F
  } = we() || {}, R = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: h,
    slotIndex: x,
    subSlotIndex: F,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ue("$$ms-gr-react-wrapper", R), We(() => {
    _.set(Y(n));
  }), Ge(() => {
    a.forEach((u) => u());
  });
  function N(u) {
    U[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function C(u) {
    U[u ? "unshift" : "push"](() => {
      r = u, p.set(r);
    });
  }
  return e.$$set = (u) => {
    o(17, n = G(G({}, n), B(u))), "svelteInit" in u && o(5, i = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = B(n), [l, r, d, p, c, i, s, t, N, C];
}
class Be extends ke {
  constructor(n) {
    super(), Le(this, n, qe, He, Te, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Je(e) {
  function n(o) {
    const l = O(), r = new Be({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? L;
          return c.nodes = [...c.nodes, s], K({
            createPortal: M,
            node: L
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), K({
              createPortal: M,
              node: L
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Ye.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function W(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(M(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((r) => {
        if (y.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = W(r.props.el);
          return y.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...y.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = W(t);
      n.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = he(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = ve(), [s, c] = be([]);
  return ge(() => {
    var p;
    if (!t.current || !e)
      return;
    let i = e;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(r, a), o && a.classList.add(...o.split(" ")), l) {
        const f = Ke(l);
        Object.keys(f).forEach((h) => {
          a.style[h] = f[h];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var x;
        const {
          portals: f,
          clonedElement: h
        } = W(e);
        i = h, c(f), i.style.display = "contents", _(), (x = t.current) == null || x.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, h;
        (f = t.current) != null && f.contains(i) && ((h = t.current) == null || h.removeChild(i)), a();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, o, l, r]), y.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Xe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function j(e) {
  return v(() => Xe(e), [e]);
}
function re(e, n) {
  return e.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const l = {
      ...o.props
    };
    let r = l;
    Object.keys(o.slots).forEach((s) => {
      if (!o.slots[s] || !(o.slots[s] instanceof Element) && !o.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== c.length - 1 && (r = l[a]);
      });
      const i = o.slots[s];
      let _, d, p = !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone ?? !1), r[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: p
      }) : r[c[c.length - 1]], r = l;
    });
    const t = "children";
    return o[t] && (l[t] = re(o[t])), l;
  });
}
function Ze(e, n) {
  return e ? /* @__PURE__ */ m.jsx(g, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function T({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Ze(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function b(e) {
  return Array.isArray(e) ? e.map((n) => b(n)) : z(typeof e == "number" ? e * 1e3 : e);
}
function Q(e) {
  return Array.isArray(e) ? e.map((n) => n ? n.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const et = Je(({
  slots: e,
  disabledDate: n,
  disabledTime: o,
  value: l,
  defaultValue: r,
  defaultPickerValue: t,
  pickerValue: s,
  showTime: c,
  presets: i,
  presetItems: _,
  onChange: d,
  minDate: p,
  maxDate: a,
  cellRender: f,
  panelRender: h,
  getPopupContainer: x,
  onValueChange: F,
  onPanelChange: R,
  children: N,
  setSlotParams: C,
  elRef: u,
  ...w
}) => {
  const oe = j(n), le = j(o), se = j(x), ce = j(f), ie = j(h), ae = v(() => typeof c == "object" ? {
    ...c,
    defaultValue: c.defaultValue ? b(c.defaultValue) : void 0
  } : c, [c]), ue = v(() => l ? b(l) : void 0, [l]), de = v(() => r ? b(r) : void 0, [r]), fe = v(() => t ? b(t) : void 0, [t]), pe = v(() => s ? b(s) : void 0, [s]), _e = v(() => p ? b(p) : void 0, [p]), me = v(() => a ? b(a) : void 0, [a]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: N
    }), /* @__PURE__ */ m.jsx(ye, {
      ...w,
      ref: u,
      value: ue,
      defaultValue: de,
      defaultPickerValue: fe,
      pickerValue: pe,
      minDate: _e,
      maxDate: me,
      showTime: ae,
      disabledDate: oe,
      disabledTime: le,
      getPopupContainer: se,
      cellRender: e.cellRender ? T({
        slots: e,
        setSlotParams: C,
        key: "cellRender"
      }) : ce,
      panelRender: e.panelRender ? T({
        slots: e,
        setSlotParams: C,
        key: "panelRender"
      }) : ie,
      presets: v(() => (i || re(_)).map((E) => ({
        ...E,
        value: b(E.value)
      })), [i, _]),
      onPanelChange: (E, ...A) => {
        const k = Q(E);
        R == null || R(k, ...A);
      },
      onChange: (E, ...A) => {
        const k = Q(E);
        d == null || d(k, ...A), F(k);
      },
      renderExtraFooter: e.renderExtraFooter ? T({
        slots: e,
        setSlotParams: C,
        key: "renderExtraFooter"
      }) : w.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.prevIcon
      }) : w.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.nextIcon
      }) : w.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.suffixIcon
      }) : w.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.superNextIcon
      }) : w.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ m.jsx(g, {
        slot: e.superPrevIcon
      }) : w.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(g, {
          slot: e["allowClear.clearIcon"]
        })
      } : w.allowClear
    })]
  });
});
export {
  et as DatePicker,
  et as default
};
