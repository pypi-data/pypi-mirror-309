import { g as we, w as O } from "./Index-Dxa4uPO8.js";
const E = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, x = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var X = {
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
var ve = E, ye = Symbol.for("react.element"), be = Symbol.for("react.fragment"), ge = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, n, o) {
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
F.jsx = Z;
F.jsxs = Z;
X.exports = F;
var _ = X.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: V,
  claim_element: $,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Ce,
  create_slot: je,
  detach: R,
  element: ee,
  empty: K,
  exclude_internal_props: q,
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
function B(e) {
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
      var s = V(n);
      r && r.l(s), s.forEach(R), this.h();
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
      t && R(n), r && r.d(t), e[9](null);
    }
  };
}
function ze(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && B(e)
  );
  return {
    c() {
      n = ee("react-portal-target"), o = De(), t && t.c(), l = K(), this.h();
    },
    l(s) {
      n = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), V(n).forEach(R), o = Se(s), t && t.l(s), l = K(), this.h();
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
      16 && k(t, 1)) : (t = B(s), t.c(), k(t, 1), t.m(l.parentNode, l)) : t && (ke(), M(t, 1, 1, () => {
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
      s && (R(n), R(o), R(l)), e[8](null), t && t.d(s);
    }
  };
}
function J(e) {
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
  const h = O(J(n)), m = O();
  H(e, m, (a) => o(0, l = a));
  const v = O();
  H(e, v, (a) => o(1, r = a));
  const u = [], d = Le("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: b,
    subSlotIndex: T
  } = we() || {}, j = i({
    parent: d,
    props: h,
    target: m,
    slot: v,
    slotKey: f,
    slotIndex: b,
    subSlotIndex: T,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", j), Ae(() => {
    h.set(J(n));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function D(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, m.set(l);
    });
  }
  function w(a) {
    U[a ? "unshift" : "push"](() => {
      r = a, v.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, n = G(G({}, n), q(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = q(n), [l, r, m, v, c, i, s, t, D, w];
}
class Ue extends Ie {
  constructor(n) {
    super(), Fe(this, n, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, N = window.ms_globals.tree;
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
          return c.nodes = [...c.nodes, s], Y({
            createPortal: L,
            node: N
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), Y({
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
function qe(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Ke.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function W(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(L(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = W(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...E.Children.toArray(r.props.children), ...t]
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
function Be(e, n) {
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
    var v;
    if (!t.current || !e)
      return;
    let i = e;
    function h() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Be(r, u), o && u.classList.add(...o.split(" ")), l) {
        const d = qe(l);
        Object.keys(d).forEach((f) => {
          u.style[f] = d[f];
        });
      }
    }
    let m = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: d,
          clonedElement: f
        } = W(e);
        i = f, c(d), i.style.display = "contents", h(), (b = t.current) == null || b.appendChild(i);
      };
      u(), m = new window.MutationObserver(() => {
        var d, f;
        (d = t.current) != null && d.contains(i) && ((f = t.current) == null || f.removeChild(i)), u();
      }), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (v = t.current) == null || v.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((d = t.current) == null || d.removeChild(i)), m == null || m.disconnect();
    };
  }, [e, n, o, l, r]), E.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Je(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function C(e) {
  return x(() => Je(e), [e]);
}
function Ye(e, n) {
  return e ? /* @__PURE__ */ _.jsx(y, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Q({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Ye(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function g(e) {
  return z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const Xe = He(({
  slots: e,
  disabledDate: n,
  disabledTime: o,
  value: l,
  defaultValue: r,
  defaultPickerValue: t,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: h,
  cellRender: m,
  panelRender: v,
  getPopupContainer: u,
  onValueChange: d,
  onPanelChange: f,
  onCalendarChange: b,
  children: T,
  setSlotParams: j,
  elRef: D,
  ...w
}) => {
  const a = C(n), ne = C(u), re = C(m), oe = C(v), se = C(o), le = x(() => l == null ? void 0 : l.map((p) => g(p)), [l]), ie = x(() => r == null ? void 0 : r.map((p) => g(p)), [r]), ce = x(() => Array.isArray(t) ? t.map((p) => g(p)) : t ? g(t) : void 0, [t]), ae = x(() => Array.isArray(s) ? s.map((p) => g(p)) : s ? g(s) : void 0, [s]), ue = x(() => i ? g(i) : void 0, [i]), de = x(() => h ? g(h) : void 0, [h]);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: T
    }), /* @__PURE__ */ _.jsx(he.RangePicker, {
      ...w,
      ref: D,
      value: le,
      disabledTime: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledDate: a,
      getPopupContainer: ne,
      cellRender: e.cellRender ? Q({
        slots: e,
        setSlotParams: j,
        key: "cellRender"
      }) : re,
      panelRender: e.panelRender ? Q({
        slots: e,
        setSlotParams: j,
        key: "panelRender"
      }) : oe,
      onPanelChange: (p, ...S) => {
        const I = A(p);
        f == null || f(I, ...S);
      },
      onChange: (p, ...S) => {
        const I = A(p);
        c == null || c(I, ...S), d(I);
      },
      onCalendarChange: (p, ...S) => {
        const I = A(p);
        b == null || b(I, ...S);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ _.jsx(y, {
        slot: e.renderExtraFooter
      }) : null : w.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.prevIcon
      }) : w.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.nextIcon
      }) : w.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.suffixIcon
      }) : w.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.superNextIcon
      }) : w.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.superPrevIcon
      }) : w.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : w.allowClear,
      separator: e.separator ? /* @__PURE__ */ _.jsx(y, {
        slot: e.separator
      }) : w.separator
    })]
  });
});
export {
  Xe as TimeRangePicker,
  Xe as default
};
