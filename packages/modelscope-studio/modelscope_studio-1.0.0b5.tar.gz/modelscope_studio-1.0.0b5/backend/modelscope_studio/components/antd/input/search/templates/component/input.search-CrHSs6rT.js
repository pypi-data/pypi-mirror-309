import { b as $, g as ee, w as v } from "./Index-D-QLICkA.js";
const b = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, R = window.ms_globals.React.useRef, M = window.ms_globals.React.useState, O = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function re(e, r) {
  return $(e, r);
}
var W = {
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
var ne = b, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ie = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(e, r, n) {
  var l, o = {}, t = null, s = null;
  n !== void 0 && (t = "" + n), r.key !== void 0 && (t = "" + r.key), r.ref !== void 0 && (s = r.ref);
  for (l in r) se.call(r, l) && !ae.hasOwnProperty(l) && (o[l] = r[l]);
  if (e && e.defaultProps) for (l in r = e.defaultProps, r) o[l] === void 0 && (o[l] = r[l]);
  return {
    $$typeof: oe,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: ie.current
  };
}
I.Fragment = le;
I.jsx = q;
I.jsxs = q;
W.exports = I;
var m = W.exports;
const {
  SvelteComponent: ce,
  assign: F,
  binding_callbacks: A,
  check_outros: de,
  children: z,
  claim_element: G,
  claim_space: ue,
  component_subscribe: L,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: H,
  empty: T,
  exclude_internal_props: N,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: x,
  safe_not_equal: we,
  set_custom_element_data: K,
  space: be,
  transition_in: C,
  transition_out: P,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function B(e) {
  let r, n;
  const l = (
    /*#slots*/
    e[7].default
  ), o = _e(
    l,
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
      var s = z(r);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      K(r, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      x(t, r, s), o && o.m(r, null), e[9](r), n = !0;
    },
    p(t, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && ye(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        n ? pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : me(
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
      P(o, t), n = !1;
    },
    d(t) {
      t && y(r), o && o.d(t), e[9](null);
    }
  };
}
function Ie(e) {
  let r, n, l, o, t = (
    /*$$slots*/
    e[4].default && B(e)
  );
  return {
    c() {
      r = H("react-portal-target"), n = be(), t && t.c(), l = T(), this.h();
    },
    l(s) {
      r = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(r).forEach(y), n = ue(s), t && t.l(s), l = T(), this.h();
    },
    h() {
      K(r, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      x(s, r, a), e[8](r), x(s, n, a), t && t.m(s, a), x(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && C(t, 1)) : (t = B(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      P(t), o = !1;
    },
    d(s) {
      s && (y(r), y(n), y(l)), e[8](null), t && t.d(s);
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
function Se(e, r, n) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = r;
  const a = fe(t);
  let {
    svelteInit: i
  } = r;
  const h = v(V(r)), f = v();
  L(e, f, (d) => n(0, l = d));
  const p = v();
  L(e, p, (d) => n(1, o = d));
  const c = [], u = ve("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: J
  } = ee() || {}, Y = i({
    parent: u,
    props: h,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: J,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", Y), Ee(() => {
    h.set(V(r));
  }), xe(() => {
    c.forEach((d) => d());
  });
  function Q(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function X(d) {
    A[d ? "unshift" : "push"](() => {
      o = d, p.set(o);
    });
  }
  return e.$$set = (d) => {
    n(17, r = F(F({}, r), N(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, r = N(r), [l, o, f, p, a, i, s, t, Q, X];
}
class Re extends ce {
  constructor(r) {
    super(), ge(this, r, Se, Ie, we, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Oe(e) {
  function r(n) {
    const l = v(), o = new Re({
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
          }, a = t.parent ?? S;
          return a.nodes = [...a.nodes, s], D({
            createPortal: j,
            node: S
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: j,
              node: S
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
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(e) {
  return e ? Object.keys(e).reduce((r, n) => {
    const l = e[n];
    return typeof l == "number" && !je.includes(n) ? r[n] = l + "px" : r[n] = l, r;
  }, {}) : {};
}
function k(e) {
  const r = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return r.push(j(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: b.Children.toArray(e._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = k(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...b.Children.toArray(o.props.children), ...t]
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
      } = k(t);
      r.push(...a), n.appendChild(s);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: r
  };
}
function ke(e, r) {
  e && (typeof e == "function" ? e(r) : e.current = r);
}
const w = Z(({
  slot: e,
  clone: r,
  className: n,
  style: l
}, o) => {
  const t = R(), [s, a] = M([]);
  return O(() => {
    var p;
    if (!t.current || !e)
      return;
    let i = e;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(o, c), n && c.classList.add(...n.split(" ")), l) {
        const u = Pe(l);
        Object.keys(u).forEach((_) => {
          c.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var g;
        const {
          portals: u,
          clonedElement: _
        } = k(e);
        i = _, a(u), i.style.display = "contents", h(), (g = t.current) == null || g.appendChild(i);
      };
      c(), f = new window.MutationObserver(() => {
        var u, _;
        (u = t.current) != null && u.contains(i) && ((_ = t.current) == null || _.removeChild(i)), c();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var c, u;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((u = t.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, r, n, l, o]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Fe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return U(() => Fe(e), [e]);
}
function Ae({
  value: e,
  onValueChange: r
}) {
  const [n, l] = M(e), o = R(r);
  o.current = r;
  const t = R(n);
  return t.current = n, O(() => {
    o.current(n);
  }, [n]), O(() => {
    re(e, t.current) || l(e);
  }, [e]), [n, l];
}
function Le(e) {
  return Object.keys(e).reduce((r, n) => (e[n] !== void 0 && (r[n] = e[n]), r), {});
}
function Te(e, r) {
  return e ? /* @__PURE__ */ m.jsx(w, {
    slot: e,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function Ne({
  key: e,
  setSlotParams: r,
  slots: n
}, l) {
  return n[e] ? (...o) => (r(e, o), Te(n[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ve = Oe(({
  slots: e,
  children: r,
  count: n,
  showCount: l,
  onValueChange: o,
  onChange: t,
  elRef: s,
  setSlotParams: a,
  ...i
}) => {
  const h = E(n == null ? void 0 : n.strategy), f = E(n == null ? void 0 : n.exceedFormatter), p = E(n == null ? void 0 : n.show), c = E(typeof l == "object" ? l.formatter : void 0), [u, _] = Ae({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ m.jsx(te.Search, {
      ...i,
      value: u,
      ref: s,
      onChange: (g) => {
        t == null || t(g), _(g.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Ne({
          slots: e,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof l == "object" && c ? {
        ...l,
        formatter: c
      } : l,
      count: U(() => Le({
        ...n,
        exceedFormatter: f,
        strategy: h,
        show: p || (n == null ? void 0 : n.show)
      }), [n, f, h, p]),
      enterButton: e.enterButton ? /* @__PURE__ */ m.jsx(w, {
        slot: e.enterButton
      }) : i.enterButton,
      addonAfter: e.addonAfter ? /* @__PURE__ */ m.jsx(w, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ m.jsx(w, {
        slot: e.addonBefore
      }) : i.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ m.jsx(w, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ m.jsx(w, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Ve as InputSearch,
  Ve as default
};
