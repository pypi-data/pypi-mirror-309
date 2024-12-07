import { g as $, w as E } from "./Index-Hq9GblMU.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Segmented;
var F = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(l, t, n) {
  var o, r = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) le.call(t, o) && !oe.hasOwnProperty(o) && (r[o] = t[o]);
  if (l && l.defaultProps) for (o in t = l.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: ne,
    type: l,
    key: e,
    ref: s,
    props: r,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = M;
S.jsxs = M;
F.exports = S;
var g = F.exports;
const {
  SvelteComponent: ce,
  assign: I,
  binding_callbacks: O,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: j,
  compute_slots: de,
  create_slot: ue,
  detach: b,
  element: G,
  empty: P,
  exclude_internal_props: L,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: U,
  space: ge,
  transition_in: v,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function T(l) {
  let t, n;
  const o = (
    /*#slots*/
    l[7].default
  ), r = ue(
    o,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(t);
      r && r.l(s), s.forEach(b), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), r && r.m(t, null), l[9](t), n = !0;
    },
    p(e, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && be(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? _e(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (v(r, e), n = !0);
    },
    o(e) {
      R(r, e), n = !1;
    },
    d(e) {
      e && b(t), r && r.d(e), l[9](null);
    }
  };
}
function Se(l) {
  let t, n, o, r, e = (
    /*$$slots*/
    l[4].default && T(l)
  );
  return {
    c() {
      t = G("react-portal-target"), n = ge(), e && e.c(), o = P(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(b), n = ae(s), e && e.l(s), o = P(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, t, c), l[8](t), y(s, n, c), e && e.m(s, c), y(s, o, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = T(s), e.c(), v(e, 1), e.m(o.parentNode, o)) : e && (pe(), R(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      r || (v(e), r = !0);
    },
    o(s) {
      R(e), r = !1;
    },
    d(s) {
      s && (b(t), b(n), b(o)), l[8](null), e && e.d(s);
    }
  };
}
function N(l) {
  const {
    svelteInit: t,
    ...n
  } = l;
  return n;
}
function xe(l, t, n) {
  let o, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(N(t)), u = E();
  j(l, u, (d) => n(0, o = d));
  const p = E();
  j(l, p, (d) => n(1, r = d));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q
  } = $() || {}, B = i({
    parent: f,
    props: _,
    target: u,
    slot: p,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: q,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", B), we(() => {
    _.set(N(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function V(d) {
    O[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function J(d) {
    O[d ? "unshift" : "push"](() => {
      r = d, p.set(r);
    });
  }
  return l.$$set = (d) => {
    n(17, t = I(I({}, t), L(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, t = L(t), [o, r, u, p, c, i, s, e, V, J];
}
class Ce extends ce {
  constructor(t) {
    super(), me(this, t, xe, Se, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, x = window.ms_globals.tree;
function Re(l) {
  function t(n) {
    const o = E(), r = new Ce({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], A({
            createPortal: C,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), A({
              createPortal: C,
              node: x
            });
          }), s;
        },
        ...n.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(l) {
  return l ? Object.keys(l).reduce((t, n) => {
    const o = l[n];
    return typeof o == "number" && !ke.includes(n) ? t[n] = o + "px" : t[n] = o, t;
  }, {}) : {};
}
function k(l) {
  const t = [], n = l.cloneNode(!1);
  if (l._reactElement)
    return t.push(C(h.cloneElement(l._reactElement, {
      ...l._reactElement.props,
      children: h.Children.toArray(l._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(l.getEventListeners()).forEach((r) => {
    l.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      n.addEventListener(c, s, i);
    });
  });
  const o = Array.from(l.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      t.push(...c), n.appendChild(s);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Oe(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const D = Y(({
  slot: l,
  clone: t,
  className: n,
  style: o
}, r) => {
  const e = K(), [s, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !l)
      return;
    let i = l;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(r, a), n && a.classList.add(...n.split(" ")), o) {
        const f = Ie(o);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: f,
          clonedElement: m
        } = k(l);
        i = m, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), u.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [l, t, n, o, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function H(l, t) {
  return l.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return t != null && t.fallback ? t.fallback(n) : n;
    const o = {
      ...n.props
    };
    let r = o;
    Object.keys(n.slots).forEach((s) => {
      if (!n.slots[s] || !(n.slots[s] instanceof Element) && !n.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        r[a] || (r[a] = {}), f !== c.length - 1 && (r = o[a]);
      });
      const i = n.slots[s];
      let _, u, p = (t == null ? void 0 : t.clone) ?? !1;
      i instanceof Element ? _ = i : (_ = i.el, u = i.callback, p = i.clone ?? !1), r[c[c.length - 1]] = _ ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ g.jsx(D, {
        slot: _,
        clone: p
      }) : r[c[c.length - 1]], r = o;
    });
    const e = (t == null ? void 0 : t.children) || "children";
    return n[e] && (o[e] = H(n[e], t)), o;
  });
}
const Pe = Re(({
  slotItems: l,
  options: t,
  onChange: n,
  onValueChange: o,
  children: r,
  ...e
}) => /* @__PURE__ */ g.jsxs(g.Fragment, {
  children: [/* @__PURE__ */ g.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ g.jsx(ee, {
    ...e,
    onChange: (s) => {
      n == null || n(s), o(s);
    },
    options: Z(() => t || H(l, {
      clone: !0
    }), [t, l])
  })]
}));
export {
  Pe as Segmented,
  Pe as default
};
