import { b as ee, g as te, w as x } from "./Index-DPj9OQD0.js";
const w = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, j = window.ms_globals.React.useRef, q = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, re = window.ms_globals.antd.Input;
function ne(e, r) {
  return ee(e, r);
}
var G = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = w, le = Symbol.for("react.element"), se = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, r, n) {
  var l, o = {}, t = null, s = null;
  n !== void 0 && (t = "" + n), r.key !== void 0 && (t = "" + r.key), r.ref !== void 0 && (s = r.ref);
  for (l in r) ie.call(r, l) && !ce.hasOwnProperty(l) && (o[l] = r[l]);
  if (e && e.defaultProps) for (l in r = e.defaultProps, r) o[l] === void 0 && (o[l] = r[l]);
  return {
    $$typeof: le,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
I.Fragment = se;
I.jsx = H;
I.jsxs = H;
G.exports = I;
var h = G.exports;
const {
  SvelteComponent: de,
  assign: L,
  binding_callbacks: T,
  check_outros: ue,
  children: K,
  claim_element: J,
  claim_space: fe,
  component_subscribe: N,
  compute_slots: _e,
  create_slot: me,
  detach: y,
  element: Y,
  empty: V,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  group_outros: we,
  init: ge,
  insert_hydration: R,
  safe_not_equal: be,
  set_custom_element_data: Q,
  space: ye,
  transition_in: C,
  transition_out: F,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(e) {
  let r, n;
  const l = (
    /*#slots*/
    e[7].default
  ), o = me(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      r = Y("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      r = J(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(r);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      Q(r, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      R(t, r, s), o && o.m(r, null), e[9](r), n = !0;
    },
    p(t, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        n ? he(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (C(o, t), n = !0);
    },
    o(t) {
      F(o, t), n = !1;
    },
    d(t) {
      t && y(r), o && o.d(t), e[9](null);
    }
  };
}
function Ie(e) {
  let r, n, l, o, t = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      r = Y("react-portal-target"), n = ye(), t && t.c(), l = V(), this.h();
    },
    l(s) {
      r = J(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(r).forEach(y), n = fe(s), t && t.l(s), l = V(), this.h();
    },
    h() {
      Q(r, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      R(s, r, a), e[8](r), R(s, n, a), t && t.m(s, a), R(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && C(t, 1)) : (t = M(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (we(), F(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      F(t), o = !1;
    },
    d(s) {
      s && (y(r), y(n), y(l)), e[8](null), t && t.d(s);
    }
  };
}
function B(e) {
  const {
    svelteInit: r,
    ...n
  } = e;
  return n;
}
function Se(e, r, n) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = r;
  const a = _e(t);
  let {
    svelteInit: i
  } = r;
  const f = x(B(r)), _ = x();
  N(e, _, (d) => n(0, l = d));
  const p = x();
  N(e, p, (d) => n(1, o = d));
  const c = [], u = xe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: S
  } = te() || {}, v = i({
    parent: u,
    props: f,
    target: _,
    slot: p,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: S,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", v), ve(() => {
    f.set(B(r));
  }), Re(() => {
    c.forEach((d) => d());
  });
  function X(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  function Z(d) {
    T[d ? "unshift" : "push"](() => {
      o = d, p.set(o);
    });
  }
  return e.$$set = (d) => {
    n(17, r = L(L({}, r), D(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, r = D(r), [l, o, _, p, a, i, s, t, X, Z];
}
class Oe extends de {
  constructor(r) {
    super(), ge(this, r, Se, Ie, be, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, O = window.ms_globals.tree;
function je(e) {
  function r(n) {
    const l = x(), o = new Oe({
      ...n,
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
          }, a = t.parent ?? O;
          return a.nodes = [...a.nodes, s], U({
            createPortal: k,
            node: O
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...n.props
      }
    });
    return l.set(o), o;
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
    const l = e[n];
    return typeof l == "number" && !Pe.includes(n) ? r[n] = l + "px" : r[n] = l, r;
  }, {}) : {};
}
function A(e) {
  const r = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return r.push(k(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = A(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...t]
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = A(t);
      r.push(...a), n.appendChild(s);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: r
  };
}
function Fe(e, r) {
  e && (typeof e == "function" ? e(r) : e.current = r);
}
const b = $(({
  slot: e,
  clone: r,
  className: n,
  style: l
}, o) => {
  const t = j(), [s, a] = q([]);
  return P(() => {
    var p;
    if (!t.current || !e)
      return;
    let i = e;
    function f() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(o, c), n && c.classList.add(...n.split(" ")), l) {
        const u = ke(l);
        Object.keys(u).forEach((m) => {
          c.style[m] = u[m];
        });
      }
    }
    let _ = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var g;
        const {
          portals: u,
          clonedElement: m
        } = A(e);
        i = m, a(u), i.style.display = "contents", f(), (g = t.current) == null || g.appendChild(i);
      };
      c(), _ = new window.MutationObserver(() => {
        var u, m;
        (u = t.current) != null && u.contains(i) && ((m = t.current) == null || m.removeChild(i)), c();
      }), _.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", f(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var c, u;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((u = t.current) == null || u.removeChild(i)), _ == null || _.disconnect();
    };
  }, [e, r, n, l, o]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return z(() => Ae(e), [e]);
}
function Le({
  value: e,
  onValueChange: r
}) {
  const [n, l] = q(e), o = j(r);
  o.current = r;
  const t = j(n);
  return t.current = n, P(() => {
    o.current(n);
  }, [n]), P(() => {
    ne(e, t.current) || l(e);
  }, [e]), [n, l];
}
function Te(e) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (r[n] = e[n]), r), {});
}
function Ne(e, r) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function W({
  key: e,
  setSlotParams: r,
  slots: n
}, l) {
  return n[e] ? (...o) => (r(e, o), Ne(n[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const De = je(({
  slots: e,
  children: r,
  count: n,
  showCount: l,
  onValueChange: o,
  onChange: t,
  iconRender: s,
  elRef: a,
  setSlotParams: i,
  ...f
}) => {
  const _ = E(n == null ? void 0 : n.strategy), p = E(n == null ? void 0 : n.exceedFormatter), c = E(n == null ? void 0 : n.show), u = E(typeof l == "object" ? l.formatter : void 0), m = E(s), [g, S] = Le({
    onValueChange: o,
    value: f.value
  });
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ h.jsx(re.Password, {
      ...f,
      value: g,
      ref: a,
      onChange: (v) => {
        t == null || t(v), S(v.target.value);
      },
      iconRender: e.iconRender ? W({
        slots: e,
        setSlotParams: i,
        key: "iconRender"
      }) : m,
      showCount: e["showCount.formatter"] ? {
        formatter: W({
          slots: e,
          setSlotParams: i,
          key: "showCount.formatter"
        })
      } : typeof l == "object" && u ? {
        ...l,
        formatter: u
      } : l,
      count: z(() => Te({
        ...n,
        exceedFormatter: p,
        strategy: _,
        show: c || (n == null ? void 0 : n.show)
      }), [n, p, _, c]),
      addonAfter: e.addonAfter ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addonAfter
      }) : f.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addonBefore
      }) : f.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : f.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ h.jsx(b, {
        slot: e.prefix
      }) : f.prefix,
      suffix: e.suffix ? /* @__PURE__ */ h.jsx(b, {
        slot: e.suffix
      }) : f.suffix
    })]
  });
});
export {
  De as InputPassword,
  De as default
};
