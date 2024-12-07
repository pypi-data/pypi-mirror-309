import { b as $, g as ee, w as E } from "./Index-Dv3IC9Z-.js";
const g = window.ms_globals.React, X = window.ms_globals.React.forwardRef, C = window.ms_globals.React.useRef, B = window.ms_globals.React.useState, S = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.InputNumber;
function ne(e, n) {
  return $(e, n);
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
var oe = g, re = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(e, n, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) le.call(n, s) && !ce.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
I.Fragment = se;
I.jsx = q;
I.jsxs = q;
W.exports = I;
var _ = W.exports;
const {
  SvelteComponent: ae,
  assign: P,
  binding_callbacks: A,
  check_outros: ue,
  children: z,
  claim_element: G,
  claim_space: de,
  component_subscribe: L,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: U,
  empty: N,
  exclude_internal_props: T,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: he,
  init: ge,
  insert_hydration: v,
  safe_not_equal: we,
  set_custom_element_data: H,
  space: be,
  transition_in: x,
  transition_out: j,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ie
} = window.__gradio__svelte__internal;
function F(e) {
  let n, r;
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
      n = U("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = G(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = z(n);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      v(t, n, l), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ye(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? me(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (x(o, t), r = !0);
    },
    o(t) {
      j(o, t), r = !1;
    },
    d(t) {
      t && b(n), o && o.d(t), e[9](null);
    }
  };
}
function Re(e) {
  let n, r, s, o, t = (
    /*$$slots*/
    e[4].default && F(e)
  );
  return {
    c() {
      n = U("react-portal-target"), r = be(), t && t.c(), s = N(), this.h();
    },
    l(l) {
      n = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(b), r = de(l), t && t.l(l), s = N(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      v(l, n, i), e[8](n), v(l, r, i), t && t.m(l, i), v(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && x(t, 1)) : (t = F(l), t.c(), x(t, 1), t.m(s.parentNode, s)) : t && (he(), j(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(l) {
      o || (x(t), o = !0);
    },
    o(l) {
      j(t), o = !1;
    },
    d(l) {
      l && (b(n), b(r), b(s)), e[8](null), t && t.d(l);
    }
  };
}
function V(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ce(e, n, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const i = fe(t);
  let {
    svelteInit: c
  } = n;
  const h = E(V(n)), d = E();
  L(e, d, (u) => r(0, s = u));
  const p = E();
  L(e, p, (u) => r(1, o = u));
  const a = [], f = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: y,
    subSlotIndex: K
  } = ee() || {}, J = c({
    parent: f,
    props: h,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ie("$$ms-gr-react-wrapper", J), Ee(() => {
    h.set(V(n));
  }), xe(() => {
    a.forEach((u) => u());
  });
  function Y(u) {
    A[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function Q(u) {
    A[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = P(P({}, n), T(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, n = T(n), [s, o, d, p, i, c, l, t, Y, Q];
}
class Se extends ae {
  constructor(n) {
    super(), ge(this, n, Ce, Re, we, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, R = window.ms_globals.tree;
function Oe(e) {
  function n(r) {
    const s = E(), o = new Se({
      ...r,
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
          }, i = t.parent ?? R;
          return i.nodes = [...i.nodes, l], D({
            createPortal: O,
            node: R
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), D({
              createPortal: O,
              node: R
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const s = e[r];
    return typeof s == "number" && !je.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function k(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(O(g.cloneElement(e._reactElement, {
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
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = k(t);
      n.push(...i), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Pe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const w = X(({
  slot: e,
  clone: n,
  className: r,
  style: s
}, o) => {
  const t = C(), [l, i] = B([]);
  return S(() => {
    var p;
    if (!t.current || !e)
      return;
    let c = e;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: f,
          clonedElement: m
        } = k(e);
        c = m, i(f), c.style.display = "contents", h(), (y = t.current) == null || y.appendChild(c);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = t.current) != null && f.contains(c) && ((m = t.current) == null || m.removeChild(c)), a();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", h(), (p = t.current) == null || p.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((f = t.current) == null || f.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, n, r, s, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function M(e) {
  return Z(() => Ae(e), [e]);
}
function Le({
  value: e,
  onValueChange: n
}) {
  const [r, s] = B(e), o = C(n);
  o.current = n;
  const t = C(r);
  return t.current = r, S(() => {
    o.current(r);
  }, [r]), S(() => {
    ne(e, t.current) || s(e);
  }, [e]), [r, s];
}
const Te = Oe(({
  slots: e,
  children: n,
  onValueChange: r,
  onChange: s,
  formatter: o,
  parser: t,
  elRef: l,
  ...i
}) => {
  const c = M(o), h = M(t), [d, p] = Le({
    onValueChange: r,
    value: i.value
  });
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(te, {
      ...i,
      ref: l,
      value: d,
      onChange: (a) => {
        s == null || s(a), p(a);
      },
      parser: h,
      formatter: c,
      controls: e["controls.upIcon"] || e["controls.downIcon"] ? {
        upIcon: e["controls.upIcon"] ? /* @__PURE__ */ _.jsx(w, {
          slot: e["controls.upIcon"]
        }) : typeof i.controls == "object" ? i.controls.upIcon : void 0,
        downIcon: e["controls.downIcon"] ? /* @__PURE__ */ _.jsx(w, {
          slot: e["controls.downIcon"]
        }) : typeof i.controls == "object" ? i.controls.downIcon : void 0
      } : i.controls,
      addonAfter: e.addonAfter ? /* @__PURE__ */ _.jsx(w, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ _.jsx(w, {
        slot: e.addonBefore
      }) : i.addonBefore,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(w, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ _.jsx(w, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Te as InputNumber,
  Te as default
};
