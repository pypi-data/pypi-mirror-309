import { g as ve, w as O } from "./Index-DElpaxHa.js";
const x = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, b = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var Q = {
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
var he = x, ye = Symbol.for("react.element"), be = Symbol.for("react.fragment"), ge = Object.prototype.hasOwnProperty, xe = he.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function X(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ge.call(n, l) && !Ee.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: ye,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: xe.current
  };
}
F.Fragment = be;
F.jsx = X;
F.jsxs = X;
Q.exports = F;
var _ = Q.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: Z,
  claim_element: $,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Ce,
  create_slot: je,
  detach: I,
  element: ee,
  empty: K,
  exclude_internal_props: V,
  get_all_dirty_from_scope: Oe,
  get_slot_changes: Pe,
  group_outros: ke,
  init: Fe,
  insert_hydration: P,
  safe_not_equal: Te,
  set_custom_element_data: te,
  space: De,
  transition_in: k,
  transition_out: M,
  update_slot_base: Ne
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ae,
  getContext: Le,
  onDestroy: Me,
  setContext: We
} = window.__gradio__svelte__internal;
function q(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = je(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = ee("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = $(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Z(n);
      r && r.l(s), s.forEach(I), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      P(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ne(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? Pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : Oe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (k(r, t), o = !0);
    },
    o(t) {
      M(r, t), o = !1;
    },
    d(t) {
      t && I(n), r && r.d(t), e[9](null);
    }
  };
}
function ze(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && q(e)
  );
  return {
    c() {
      n = ee("react-portal-target"), o = De(), t && t.c(), l = K(), this.h();
    },
    l(s) {
      n = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(n).forEach(I), o = Se(s), t && t.l(s), l = K(), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      P(s, n, c), e[8](n), P(s, o, c), t && t.m(s, c), P(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && k(t, 1)) : (t = q(s), t.c(), k(t, 1), t.m(l.parentNode, l)) : t && (ke(), M(t, 1, 1, () => {
        t = null;
      }), Re());
    },
    i(s) {
      r || (k(t), r = !0);
    },
    o(s) {
      M(t), r = !1;
    },
    d(s) {
      s && (I(n), I(o), I(l)), e[8](null), t && t.d(s);
    }
  };
}
function B(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Ge(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = Ce(t);
  let {
    svelteInit: i
  } = n;
  const v = O(B(n)), p = O();
  H(e, p, (a) => o(0, l = a));
  const w = O();
  H(e, w, (a) => o(1, r = a));
  const u = [], d = Le("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: h,
    subSlotIndex: T
  } = ve() || {}, j = i({
    parent: d,
    props: v,
    target: p,
    slot: w,
    slotKey: f,
    slotIndex: h,
    subSlotIndex: T,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", j), Ae(() => {
    v.set(B(n));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function D(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, p.set(l);
    });
  }
  function m(a) {
    U[a ? "unshift" : "push"](() => {
      r = a, w.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, n = G(G({}, n), V(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = V(n), [l, r, p, w, c, i, s, t, D, m];
}
class Ue extends Ie {
  constructor(n) {
    super(), Fe(this, n, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const J = window.ms_globals.rerender, N = window.ms_globals.tree;
function He(e) {
  function n(o) {
    const l = O(), r = new Ue({
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
          }, c = t.parent ?? N;
          return c.nodes = [...c.nodes, s], J({
            createPortal: L,
            node: N
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), J({
              createPortal: L,
              node: N
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
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Ke.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function W(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(L(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: x.Children.toArray(e._reactElement.props.children).map((r) => {
        if (x.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = W(r.props.el);
          return x.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...x.Children.toArray(r.props.children), ...t]
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
function qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const y = fe(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = pe(), [s, c] = _e([]);
  return me(() => {
    var w;
    if (!t.current || !e)
      return;
    let i = e;
    function v() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), qe(r, u), o && u.classList.add(...o.split(" ")), l) {
        const d = Ve(l);
        Object.keys(d).forEach((f) => {
          u.style[f] = d[f];
        });
      }
    }
    let p = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var h;
        const {
          portals: d,
          clonedElement: f
        } = W(e);
        i = f, c(d), i.style.display = "contents", v(), (h = t.current) == null || h.appendChild(i);
      };
      u(), p = new window.MutationObserver(() => {
        var d, f;
        (d = t.current) != null && d.contains(i) && ((f = t.current) == null || f.removeChild(i)), u();
      }), p.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", v(), (w = t.current) == null || w.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((d = t.current) == null || d.removeChild(i)), p == null || p.disconnect();
    };
  }, [e, n, o, l, r]), x.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Be(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function C(e) {
  return b(() => Be(e), [e]);
}
function Je(e, n) {
  return e ? /* @__PURE__ */ _.jsx(y, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Y({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Je(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function g(e) {
  return Array.isArray(e) ? e.map((n) => g(n)) : z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return Array.isArray(e) ? e.map((n) => n ? n.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Qe = He(({
  slots: e,
  disabledDate: n,
  disabledTime: o,
  value: l,
  defaultValue: r,
  defaultPickerValue: t,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: v,
  cellRender: p,
  panelRender: w,
  getPopupContainer: u,
  onValueChange: d,
  onPanelChange: f,
  onCalendarChange: h,
  children: T,
  setSlotParams: j,
  elRef: D,
  ...m
}) => {
  const a = C(n), ne = C(o), re = C(u), oe = C(p), le = C(w), se = b(() => l ? g(l) : void 0, [l]), ie = b(() => r ? g(r) : void 0, [r]), ce = b(() => t ? g(t) : void 0, [t]), ae = b(() => s ? g(s) : void 0, [s]), ue = b(() => i ? g(i) : void 0, [i]), de = b(() => v ? g(v) : void 0, [v]);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: T
    }), /* @__PURE__ */ _.jsx(we, {
      ...m,
      ref: D,
      value: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledTime: ne,
      disabledDate: a,
      getPopupContainer: re,
      cellRender: e.cellRender ? Y({
        slots: e,
        setSlotParams: j,
        key: "cellRender"
      }) : oe,
      panelRender: e.panelRender ? Y({
        slots: e,
        setSlotParams: j,
        key: "panelRender"
      }) : le,
      onPanelChange: (R, ...S) => {
        const E = A(R);
        f == null || f(E, ...S);
      },
      onChange: (R, ...S) => {
        const E = A(R);
        c == null || c(E, ...S), d(E);
      },
      onCalendarChange: (R, ...S) => {
        const E = A(R);
        h == null || h(E, ...S);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ _.jsx(y, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear
    })]
  });
});
export {
  Qe as TimePicker,
  Qe as default
};
