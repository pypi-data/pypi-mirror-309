import { g as $, w as E } from "./Index-jNH2fBvi.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.internalContext.FormItemContext, te = window.ms_globals.antd.Radio;
var D = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = h, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(o, t, r) {
  var s, n = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) le.call(t, s) && !ie.hasOwnProperty(s) && (n[s] = t[s]);
  if (o && o.defaultProps) for (s in t = o.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: re,
    type: o,
    key: e,
    ref: l,
    props: n,
    _owner: se.current
  };
}
x.Fragment = oe;
x.jsx = G;
x.jsxs = G;
D.exports = x;
var g = D.exports;
const {
  SvelteComponent: ce,
  assign: O,
  binding_callbacks: k,
  check_outros: ae,
  children: M,
  claim_element: W,
  claim_space: ue,
  component_subscribe: P,
  compute_slots: de,
  create_slot: fe,
  detach: w,
  element: z,
  empty: j,
  exclude_internal_props: L,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: U,
  space: we,
  transition_in: v,
  transition_out: I,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function T(o) {
  let t, r;
  const s = (
    /*#slots*/
    o[7].default
  ), n = fe(
    s,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = M(t);
      n && n.l(l), l.forEach(w), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), n && n.m(t, null), o[9](t), r = !0;
    },
    p(e, l) {
      n && n.p && (!r || l & /*$$scope*/
      64) && be(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (v(n, e), r = !0);
    },
    o(e) {
      I(n, e), r = !1;
    },
    d(e) {
      e && w(t), n && n.d(e), o[9](null);
    }
  };
}
function Ce(o) {
  let t, r, s, n, e = (
    /*$$slots*/
    o[4].default && T(o)
  );
  return {
    c() {
      t = z("react-portal-target"), r = we(), e && e.c(), s = j(), this.h();
    },
    l(l) {
      t = W(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(t).forEach(w), r = ue(l), e && e.l(l), s = j(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      y(l, t, i), o[8](t), y(l, r, i), e && e.m(l, i), y(l, s, i), n = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && v(e, 1)) : (e = T(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (me(), I(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      n || (v(e), n = !0);
    },
    o(l) {
      I(e), n = !1;
    },
    d(l) {
      l && (w(t), w(r), w(s)), o[8](null), e && e.d(l);
    }
  };
}
function N(o) {
  const {
    svelteInit: t,
    ...r
  } = o;
  return r;
}
function Re(o, t, r) {
  let s, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const p = E(N(t)), d = E();
  P(o, d, (u) => r(0, s = u));
  const _ = E();
  P(o, _, (u) => r(1, n = u));
  const a = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: q
  } = $() || {}, B = c({
    parent: f,
    props: p,
    target: d,
    slot: _,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(u) {
      a.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", B), Ee(() => {
    p.set(N(t));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function V(u) {
    k[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function J(u) {
    k[u ? "unshift" : "push"](() => {
      n = u, _.set(n);
    });
  }
  return o.$$set = (u) => {
    r(17, t = O(O({}, t), L(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, t = L(t), [s, n, d, _, i, c, l, e, V, J];
}
class Ie extends ce {
  constructor(t) {
    super(), he(this, t, Re, Ce, ge, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function Se(o) {
  function t(r) {
    const s = E(), n = new Ie({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? C;
          return i.nodes = [...i.nodes, l], A({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), A({
              createPortal: R,
              node: C
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(o) {
  return o ? Object.keys(o).reduce((t, r) => {
    const s = o[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function S(o) {
  const t = [], r = o.cloneNode(!1);
  if (o._reactElement)
    return t.push(R(h.cloneElement(o._reactElement, {
      ...o._reactElement.props,
      children: h.Children.toArray(o._reactElement.props.children).map((n) => {
        if (h.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = S(n.props.el);
          return h.cloneElement(n, {
            ...n.props,
            el: l,
            children: [...h.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(o.getEventListeners()).forEach((n) => {
    o.getEventListeners(n).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(o.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = S(e);
      t.push(...i), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Pe(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const F = Y(({
  slot: o,
  clone: t,
  className: r,
  style: s
}, n) => {
  const e = K(), [l, i] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !o)
      return;
    let c = o;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(n, a), r && a.classList.add(...r.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: m
        } = S(o);
        c = m, i(f), c.style.display = "contents", p(), (b = e.current) == null || b.appendChild(c);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(c) && ((m = e.current) == null || m.removeChild(c)), a();
      }), d.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((f = e.current) == null || f.removeChild(c)), d == null || d.disconnect();
    };
  }, [o, t, r, s, n]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function H(o, t) {
  return o.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let n = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((a, f) => {
        n[a] || (n[a] = {}), f !== i.length - 1 && (n = s[a]);
      });
      const c = r.slots[l];
      let p, d, _ = !1;
      c instanceof Element ? p = c : (p = c.el, d = c.callback, _ = c.clone ?? !1), n[i[i.length - 1]] = p ? d ? (...a) => (d(i[i.length - 1], a), /* @__PURE__ */ g.jsx(F, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ g.jsx(F, {
        slot: p,
        clone: _
      }) : n[i[i.length - 1]], n = s;
    });
    const e = "children";
    return r[e] && (s[e] = H(r[e])), s;
  });
}
const Le = Se(({
  onValueChange: o,
  onChange: t,
  elRef: r,
  optionItems: s,
  options: n,
  children: e,
  ...l
}) => /* @__PURE__ */ g.jsx(g.Fragment, {
  children: /* @__PURE__ */ g.jsx(te.Group, {
    ...l,
    ref: r,
    options: Z(() => n || H(s), [s, n]),
    onChange: (i) => {
      t == null || t(i), o(i.target.value);
    },
    children: /* @__PURE__ */ g.jsx(ee.Provider, {
      value: null,
      children: e
    })
  })
}));
export {
  Le as RadioGroup,
  Le as default
};
