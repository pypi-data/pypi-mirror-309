import { g as $, w as E } from "./Index-DSD1W-yx.js";
const p = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Menu;
var F = {
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
var te = p, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, r) {
  var s, l = {}, t = null, o = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (s in e) le.call(e, s) && !se.hasOwnProperty(s) && (l[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: o,
    props: l,
    _owner: oe.current
  };
}
I.Fragment = re;
I.jsx = U;
I.jsxs = U;
F.exports = I;
var g = F.exports;
const {
  SvelteComponent: ce,
  assign: O,
  binding_callbacks: j,
  check_outros: ae,
  children: W,
  claim_element: z,
  claim_space: ie,
  component_subscribe: P,
  compute_slots: de,
  create_slot: ue,
  detach: w,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: D,
  space: ge,
  transition_in: y,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function N(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), l = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = G("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = z(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = W(e);
      l && l.l(o), o.forEach(w), this.h();
    },
    h() {
      D(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      v(t, e, o), l && l.m(e, null), n[9](e), r = !0;
    },
    p(t, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && we(
        l,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? _e(
          s,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (y(l, t), r = !0);
    },
    o(t) {
      S(l, t), r = !1;
    },
    d(t) {
      t && w(e), l && l.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, r, s, l, t = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      e = G("react-portal-target"), r = ge(), t && t.c(), s = L(), this.h();
    },
    l(o) {
      e = z(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(e).forEach(w), r = ie(o), t && t.l(o), s = L(), this.h();
    },
    h() {
      D(e, "class", "svelte-1rt0kpf");
    },
    m(o, a) {
      v(o, e, a), n[8](e), v(o, r, a), t && t.m(o, a), v(o, s, a), l = !0;
    },
    p(o, [a]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, a), a & /*$$slots*/
      16 && y(t, 1)) : (t = N(o), t.c(), y(t, 1), t.m(s.parentNode, s)) : t && (me(), S(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(o) {
      l || (y(t), l = !0);
    },
    o(o) {
      S(t), l = !1;
    },
    d(o) {
      o && (w(e), w(r), w(s)), n[8](null), t && t.d(o);
    }
  };
}
function A(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Ie(n, e, r) {
  let s, l, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const a = de(t);
  let {
    svelteInit: c
  } = e;
  const u = E(A(e)), f = E();
  P(n, f, (d) => r(0, s = d));
  const m = E();
  P(n, m, (d) => r(1, l = d));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: b,
    subSlotIndex: q
  } = $() || {}, B = c({
    parent: _,
    props: u,
    target: f,
    slot: m,
    slotKey: h,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(d) {
      i.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", B), be(() => {
    u.set(A(e));
  }), ve(() => {
    i.forEach((d) => d());
  });
  function V(d) {
    j[d ? "unshift" : "push"](() => {
      s = d, f.set(s);
    });
  }
  function J(d) {
    j[d ? "unshift" : "push"](() => {
      l = d, m.set(l);
    });
  }
  return n.$$set = (d) => {
    r(17, e = O(O({}, e), T(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, e = T(e), [s, l, f, m, a, c, o, t, V, J];
}
class Ce extends ce {
  constructor(e) {
    super(), he(this, e, Ie, xe, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, C = window.ms_globals.tree;
function Re(n) {
  function e(r) {
    const s = E(), l = new Ce({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? C;
          return a.nodes = [...a.nodes, o], M({
            createPortal: R,
            node: C
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== s), M({
              createPortal: R,
              node: C
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Se.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function k(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(R(p.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: p.Children.toArray(n._reactElement.props.children).map((l) => {
        if (p.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = k(l.props.el);
          return p.cloneElement(l, {
            ...l.props,
            el: o,
            children: [...p.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: o,
      type: a,
      useCapture: c
    }) => {
      r.addEventListener(a, o, c);
    });
  });
  const s = Array.from(n.childNodes);
  for (let l = 0; l < s.length; l++) {
    const t = s[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: a
      } = k(t);
      e.push(...a), r.appendChild(o);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const x = Y(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, l) => {
  const t = K(), [o, a] = Q([]);
  return X(() => {
    var m;
    if (!t.current || !n)
      return;
    let c = n;
    function u() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(l, i), r && i.classList.add(...r.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((h) => {
          i.style[h] = _[h];
        });
      }
    }
    let f = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var b;
        const {
          portals: _,
          clonedElement: h
        } = k(n);
        c = h, a(_), c.style.display = "contents", u(), (b = t.current) == null || b.appendChild(c);
      };
      i(), f = new window.MutationObserver(() => {
        var _, h;
        (_ = t.current) != null && _.contains(c) && ((h = t.current) == null || h.removeChild(c)), i();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", u(), (m = t.current) == null || m.appendChild(c);
    return () => {
      var i, _;
      c.style.display = "", (i = t.current) != null && i.contains(c) && ((_ = t.current) == null || _.removeChild(c)), f == null || f.disconnect();
    };
  }, [n, e, r, s, l]), p.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function je(n) {
  return Object.keys(n).reduce((e, r) => (n[r] !== void 0 && (e[r] = n[r]), e), {});
}
function H(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const s = {
      ...r.props
    };
    let l = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const a = o.split(".");
      a.forEach((i, _) => {
        l[i] || (l[i] = {}), _ !== a.length - 1 && (l = s[i]);
      });
      const c = r.slots[o];
      let u, f, m = (e == null ? void 0 : e.clone) ?? !1;
      c instanceof Element ? u = c : (u = c.el, f = c.callback, m = c.clone ?? !1), l[a[a.length - 1]] = u ? f ? (...i) => (f(a[a.length - 1], i), /* @__PURE__ */ g.jsx(x, {
        slot: u,
        clone: m
      })) : /* @__PURE__ */ g.jsx(x, {
        slot: u,
        clone: m
      }) : l[a[a.length - 1]], l = s;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (s[t] = H(r[t], e)), s;
  });
}
function Pe(n, e) {
  return n ? /* @__PURE__ */ g.jsx(x, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...l) => (e(n, l), Pe(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Re(({
  slots: n,
  items: e,
  slotItems: r,
  children: s,
  onOpenChange: l,
  onSelect: t,
  onDeselect: o,
  setSlotParams: a,
  ...c
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [s, /* @__PURE__ */ g.jsx(ee, {
    ...je(c),
    onOpenChange: (u) => {
      l == null || l(u);
    },
    onSelect: (u) => {
      t == null || t(u);
    },
    onDeselect: (u) => {
      o == null || o(u);
    },
    items: Z(() => e || H(r, {
      clone: !0
    }), [e, r]),
    expandIcon: n.expandIcon ? Le({
      key: "expandIcon",
      slots: n,
      setSlotParams: a
    }, {
      clone: !0
    }) : c.expandIcon,
    overflowedIndicator: n.overflowedIndicator ? /* @__PURE__ */ g.jsx(x, {
      slot: n.overflowedIndicator
    }) : c.overflowedIndicator
  })]
}));
export {
  Ne as Menu,
  Ne as default
};
