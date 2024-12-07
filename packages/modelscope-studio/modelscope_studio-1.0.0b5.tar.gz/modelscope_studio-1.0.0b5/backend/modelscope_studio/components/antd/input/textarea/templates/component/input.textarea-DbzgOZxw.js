import { b as $, g as ee, w as E } from "./Index-PvPdjcs0.js";
const g = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, R = window.ms_globals.React.useRef, M = window.ms_globals.React.useState, S = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function re(e, r) {
  return $(e, r);
}
var W = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = g, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(e, r, n) {
  var s, o = {}, t = null, l = null;
  n !== void 0 && (t = "" + n), r.key !== void 0 && (t = "" + r.key), r.ref !== void 0 && (l = r.ref);
  for (s in r) le.call(r, s) && !ae.hasOwnProperty(s) && (o[s] = r[s]);
  if (e && e.defaultProps) for (s in r = e.defaultProps, r) o[s] === void 0 && (o[s] = r[s]);
  return {
    $$typeof: oe,
    type: e,
    key: t,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
C.Fragment = se;
C.jsx = q;
C.jsxs = q;
W.exports = C;
var w = W.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: F,
  check_outros: ue,
  children: z,
  claim_element: G,
  claim_space: de,
  component_subscribe: T,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: H,
  empty: L,
  exclude_internal_props: A,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: v,
  safe_not_equal: we,
  set_custom_element_data: K,
  space: be,
  transition_in: x,
  transition_out: P,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(e) {
  let r, n;
  const s = (
    /*#slots*/
    e[7].default
  ), o = _e(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      r = H("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      r = G(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = z(r);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      K(r, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      v(t, r, l), o && o.m(r, null), e[9](r), n = !0;
    },
    p(t, l) {
      o && o.p && (!n || l & /*$$scope*/
      64) && ye(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        n ? pe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (x(o, t), n = !0);
    },
    o(t) {
      P(o, t), n = !1;
    },
    d(t) {
      t && b(r), o && o.d(t), e[9](null);
    }
  };
}
function Ie(e) {
  let r, n, s, o, t = (
    /*$$slots*/
    e[4].default && N(e)
  );
  return {
    c() {
      r = H("react-portal-target"), n = be(), t && t.c(), s = L(), this.h();
    },
    l(l) {
      r = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(r).forEach(b), n = de(l), t && t.l(l), s = L(), this.h();
    },
    h() {
      K(r, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      v(l, r, a), e[8](r), v(l, n, a), t && t.m(l, a), v(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, a), a & /*$$slots*/
      16 && x(t, 1)) : (t = N(l), t.c(), x(t, 1), t.m(s.parentNode, s)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(l) {
      o || (x(t), o = !0);
    },
    o(l) {
      P(t), o = !1;
    },
    d(l) {
      l && (b(r), b(n), b(s)), e[8](null), t && t.d(l);
    }
  };
}
function V(e) {
  const {
    svelteInit: r,
    ...n
  } = e;
  return n;
}
function Re(e, r, n) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = r;
  const a = fe(t);
  let {
    svelteInit: i
  } = r;
  const p = E(V(r)), f = E();
  T(e, f, (u) => n(0, s = u));
  const m = E();
  T(e, m, (u) => n(1, o = u));
  const c = [], d = ve("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: h,
    subSlotIndex: J
  } = ee() || {}, Y = i({
    parent: d,
    props: p,
    target: f,
    slot: m,
    slotKey: _,
    slotIndex: h,
    subSlotIndex: J,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", Y), Ee(() => {
    p.set(V(r));
  }), xe(() => {
    c.forEach((u) => u());
  });
  function Q(u) {
    F[u ? "unshift" : "push"](() => {
      s = u, f.set(s);
    });
  }
  function X(u) {
    F[u ? "unshift" : "push"](() => {
      o = u, m.set(o);
    });
  }
  return e.$$set = (u) => {
    n(17, r = j(j({}, r), A(u))), "svelteInit" in u && n(5, i = u.svelteInit), "$$scope" in u && n(6, l = u.$$scope);
  }, r = A(r), [s, o, f, m, a, i, l, t, Q, X];
}
class Se extends ce {
  constructor(r) {
    super(), ge(this, r, Re, Ie, we, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Oe(e) {
  function r(n) {
    const s = E(), o = new Se({
      ...n,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? I;
          return a.nodes = [...a.nodes, l], D({
            createPortal: O,
            node: I
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: O,
              node: I
            });
          }), l;
        },
        ...n.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((r, n) => {
    const s = e[n];
    return typeof s == "number" && !Pe.includes(n) ? r[n] = s + "px" : r[n] = s, r;
  }, {}) : {};
}
function k(e) {
  const r = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return r.push(O(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = k(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: r
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = k(t);
      r.push(...a), n.appendChild(l);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: r
  };
}
function je(e, r) {
  e && (typeof e == "function" ? e(r) : e.current = r);
}
const B = Z(({
  slot: e,
  clone: r,
  className: n,
  style: s
}, o) => {
  const t = R(), [l, a] = M([]);
  return S(() => {
    var m;
    if (!t.current || !e)
      return;
    let i = e;
    function p() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), je(o, c), n && c.classList.add(...n.split(" ")), s) {
        const d = ke(s);
        Object.keys(d).forEach((_) => {
          c.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var h;
        const {
          portals: d,
          clonedElement: _
        } = k(e);
        i = _, a(d), i.style.display = "contents", p(), (h = t.current) == null || h.appendChild(i);
      };
      c(), f = new window.MutationObserver(() => {
        var d, _;
        (d = t.current) != null && d.contains(i) && ((_ = t.current) == null || _.removeChild(i)), c();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var c, d;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((d = t.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, r, n, s, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Fe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function y(e) {
  return U(() => Fe(e), [e]);
}
function Te({
  value: e,
  onValueChange: r
}) {
  const [n, s] = M(e), o = R(r);
  o.current = r;
  const t = R(n);
  return t.current = n, S(() => {
    o.current(n);
  }, [n]), S(() => {
    re(e, t.current) || s(e);
  }, [e]), [n, s];
}
function Le(e) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (r[n] = e[n]), r), {});
}
function Ae(e, r) {
  return e ? /* @__PURE__ */ w.jsx(B, {
    slot: e,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function Ne({
  key: e,
  setSlotParams: r,
  slots: n
}, s) {
  return n[e] ? (...o) => (r(e, o), Ae(n[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const De = Oe(({
  slots: e,
  children: r,
  count: n,
  showCount: s,
  onValueChange: o,
  onChange: t,
  elRef: l,
  setSlotParams: a,
  ...i
}) => {
  const p = y(n == null ? void 0 : n.strategy), f = y(n == null ? void 0 : n.exceedFormatter), m = y(n == null ? void 0 : n.show), c = y(typeof s == "object" ? s.formatter : void 0), [d, _] = Te({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ w.jsx(te.TextArea, {
      ...i,
      ref: l,
      value: d,
      onChange: (h) => {
        t == null || t(h), _(h.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Ne({
          slots: e,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && c ? {
        ...s,
        formatter: c
      } : s,
      count: U(() => Le({
        ...n,
        exceedFormatter: f,
        strategy: p,
        show: m || (n == null ? void 0 : n.show)
      }), [n, f, p, m]),
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ w.jsx(B, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear
    })]
  });
});
export {
  De as InputTextarea,
  De as default
};
