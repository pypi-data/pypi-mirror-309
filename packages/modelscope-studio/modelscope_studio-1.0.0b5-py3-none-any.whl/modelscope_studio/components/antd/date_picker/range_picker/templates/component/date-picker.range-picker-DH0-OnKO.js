import { g as ge, w as D } from "./Index-Bf_72jnQ.js";
const E = window.ms_globals.React, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, ve = window.ms_globals.React.useState, be = window.ms_globals.React.useEffect, y = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.DatePicker, U = window.ms_globals.dayjs;
var Z = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ye = E, xe = Symbol.for("react.element"), Ee = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, Re = ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) Ie.call(n, l) && !je.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: xe,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: Re.current
  };
}
A.Fragment = Ee;
A.jsx = V;
A.jsxs = V;
Z.exports = A;
var h = Z.exports;
const {
  SvelteComponent: Se,
  assign: H,
  binding_callbacks: q,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: Ce,
  component_subscribe: B,
  compute_slots: ke,
  create_slot: Pe,
  detach: j,
  element: te,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: De,
  get_slot_changes: Fe,
  group_outros: Ne,
  init: Ae,
  insert_hydration: F,
  safe_not_equal: Le,
  set_custom_element_data: ne,
  space: Te,
  transition_in: N,
  transition_out: z,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function K(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = Pe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(n);
      o && o.l(s), s.forEach(j), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      F(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Me(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Fe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : De(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (N(o, t), r = !0);
    },
    o(t) {
      z(o, t), r = !1;
    },
    d(t) {
      t && j(n), o && o.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      n = te("react-portal-target"), r = Te(), t && t.c(), l = J(), this.h();
    },
    l(s) {
      n = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(j), r = Ce(s), t && t.l(s), l = J(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      F(s, n, i), e[8](n), F(s, r, i), t && t.m(s, i), F(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && N(t, 1)) : (t = K(s), t.c(), N(t, 1), t.m(l.parentNode, l)) : t && (Ne(), z(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(s) {
      o || (N(t), o = !0);
    },
    o(s) {
      z(t), o = !1;
    },
    d(s) {
      s && (j(n), j(r), j(l)), e[8](null), t && t.d(s);
    }
  };
}
function Q(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function qe(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = ke(t);
  let {
    svelteInit: c
  } = n;
  const _ = D(Q(n)), f = D();
  B(e, f, (u) => r(0, l = u));
  const m = D();
  B(e, m, (u) => r(1, o = u));
  const a = [], p = ze("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: I,
    subSlotIndex: S
  } = ge() || {}, O = c({
    parent: p,
    props: _,
    target: f,
    slot: m,
    slotKey: v,
    slotIndex: I,
    subSlotIndex: S,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ue("$$ms-gr-react-wrapper", O), We(() => {
    _.set(Q(n));
  }), Ge(() => {
    a.forEach((u) => u());
  });
  function L(u) {
    q[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function C(u) {
    q[u ? "unshift" : "push"](() => {
      o = u, m.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = H(H({}, n), Y(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = Y(n), [l, o, f, m, i, c, s, t, L, C];
}
class Be extends Se {
  constructor(n) {
    super(), Ae(this, n, qe, He, Le, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, T = window.ms_globals.tree;
function Je(e) {
  function n(r) {
    const l = D(), o = new Be({
      ...r,
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
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, s], X({
            createPortal: W,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), X({
              createPortal: W,
              node: T
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
      r(n);
    });
  });
}
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Ye.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function G(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(W(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = G(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...E.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = G(t);
      n.push(...i), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = me(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = he(), [s, i] = ve([]);
  return be(() => {
    var m;
    if (!t.current || !e)
      return;
    let c = e;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const p = Ke(l);
        Object.keys(p).forEach((v) => {
          a.style[v] = p[v];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var I;
        const {
          portals: p,
          clonedElement: v
        } = G(e);
        c = v, i(p), c.style.display = "contents", _(), (I = t.current) == null || I.appendChild(c);
      };
      a(), f = new window.MutationObserver(() => {
        var p, v;
        (p = t.current) != null && p.contains(c) && ((v = t.current) == null || v.removeChild(c)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (m = t.current) == null || m.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((p = t.current) == null || p.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, n, r, l, o]), E.createElement("react-child", {
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
function k(e) {
  return y(() => Xe(e), [e]);
}
function re(e, n) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const i = s.split(".");
      i.forEach((a, p) => {
        o[a] || (o[a] = {}), p !== i.length - 1 && (o = l[a]);
      });
      const c = r.slots[s];
      let _, f, m = !1;
      c instanceof Element ? _ = c : (_ = c.el, f = c.callback, m = c.clone ?? !1), o[i[i.length - 1]] = _ ? f ? (...a) => (f(i[i.length - 1], a), /* @__PURE__ */ h.jsx(b, {
        slot: _,
        clone: m
      })) : /* @__PURE__ */ h.jsx(b, {
        slot: _,
        clone: m
      }) : o[i[i.length - 1]], o = l;
    });
    const t = "children";
    return r[t] && (l[t] = re(r[t])), l;
  });
}
function Ze(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return r[e] ? (...o) => (n(e, o), Ze(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function w(e) {
  return U(typeof e == "number" ? e * 1e3 : e);
}
function P(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const $e = Je(({
  slots: e,
  disabledDate: n,
  value: r,
  defaultValue: l,
  defaultPickerValue: o,
  pickerValue: t,
  presets: s,
  presetItems: i,
  showTime: c,
  onChange: _,
  minDate: f,
  maxDate: m,
  cellRender: a,
  panelRender: p,
  getPopupContainer: v,
  onValueChange: I,
  onPanelChange: S,
  onCalendarChange: O,
  children: L,
  setSlotParams: C,
  elRef: u,
  ...g
}) => {
  const oe = k(n), le = k(v), se = k(a), ce = k(p), ie = y(() => {
    var d;
    return typeof c == "object" ? {
      ...c,
      defaultValue: (d = c.defaultValue) == null ? void 0 : d.map((x) => w(x))
    } : c;
  }, [c]), ae = y(() => r == null ? void 0 : r.map((d) => w(d)), [r]), ue = y(() => l == null ? void 0 : l.map((d) => w(d)), [l]), de = y(() => Array.isArray(o) ? o.map((d) => w(d)) : o ? w(o) : void 0, [o]), fe = y(() => Array.isArray(t) ? t.map((d) => w(d)) : t ? w(t) : void 0, [t]), pe = y(() => f ? w(f) : void 0, [f]), _e = y(() => m ? w(m) : void 0, [m]);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: L
    }), /* @__PURE__ */ h.jsx(we.RangePicker, {
      ...g,
      ref: u,
      value: ae,
      defaultValue: ue,
      defaultPickerValue: de,
      pickerValue: fe,
      minDate: pe,
      maxDate: _e,
      showTime: ie,
      disabledDate: oe,
      getPopupContainer: le,
      cellRender: e.cellRender ? M({
        slots: e,
        setSlotParams: C,
        key: "cellRender"
      }) : se,
      panelRender: e.panelRender ? M({
        slots: e,
        setSlotParams: C,
        key: "panelRender"
      }) : ce,
      presets: y(() => (s || re(i)).map((d) => ({
        ...d,
        value: P(d.value)
      })), [s, i]),
      onPanelChange: (d, ...x) => {
        const R = P(d);
        S == null || S(R, ...x);
      },
      onChange: (d, ...x) => {
        const R = P(d);
        _ == null || _(R, ...x), I(R);
      },
      onCalendarChange: (d, ...x) => {
        const R = P(d);
        O == null || O(R, ...x);
      },
      renderExtraFooter: e.renderExtraFooter ? M({
        slots: e,
        setSlotParams: C,
        key: "renderExtraFooter"
      }) : g.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.prevIcon
      }) : g.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.nextIcon
      }) : g.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.suffixIcon
      }) : g.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.superNextIcon
      }) : g.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.superPrevIcon
      }) : g.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : g.allowClear,
      separator: e.separator ? /* @__PURE__ */ h.jsx(b, {
        slot: e.separator,
        clone: !0
      }) : g.separator
    })]
  });
});
export {
  $e as DateRangePicker,
  $e as default
};
