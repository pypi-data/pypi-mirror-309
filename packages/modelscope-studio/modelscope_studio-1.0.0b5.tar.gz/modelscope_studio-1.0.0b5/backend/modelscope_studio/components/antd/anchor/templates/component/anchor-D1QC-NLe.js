import { g as ee, w as E } from "./Index-CqNTUCYj.js";
const m = window.ms_globals.React, M = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Anchor;
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
var ne = m, re = Symbol.for("react.element"), le = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, r) {
  var s, l = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) oe.call(t, s) && !ce.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: se.current
  };
}
C.Fragment = le;
C.jsx = z;
C.jsxs = z;
W.exports = C;
var b = W.exports;
const {
  SvelteComponent: ie,
  assign: I,
  binding_callbacks: O,
  check_outros: ae,
  children: G,
  claim_element: U,
  claim_space: ue,
  component_subscribe: P,
  compute_slots: de,
  create_slot: fe,
  detach: g,
  element: H,
  empty: j,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: me,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: be,
  transition_in: v,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function L(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), l = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = G(t);
      l && l.l(o), o.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      y(e, t, o), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && we(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
          s,
          /*$$scope*/
          e[6],
          o,
          null
        ) : _e(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (v(l, e), r = !0);
    },
    o(e) {
      S(l, e), r = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function Re(n) {
  let t, r, s, l, e = (
    /*$$slots*/
    n[4].default && L(n)
  );
  return {
    c() {
      t = H("react-portal-target"), r = be(), e && e.c(), s = j(), this.h();
    },
    l(o) {
      t = U(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(g), r = ue(o), e && e.l(o), s = j(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      y(o, t, c), n[8](t), y(o, r, c), e && e.m(o, c), y(o, s, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = L(o), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (he(), S(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(o) {
      l || (v(e), l = !0);
    },
    o(o) {
      S(e), l = !1;
    },
    d(o) {
      o && (g(t), g(r), g(s)), n[8](null), e && e.d(o);
    }
  };
}
function T(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function xe(n, t, r) {
  let s, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const _ = E(T(t)), d = E();
  P(n, d, (u) => r(0, s = u));
  const p = E();
  P(n, p, (u) => r(1, l = u));
  const a = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: w,
    subSlotIndex: V
  } = ee() || {}, J = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: h,
    slotIndex: w,
    subSlotIndex: V,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", J), Ee(() => {
    _.set(T(t));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function Y(u) {
    O[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function K(u) {
    O[u ? "unshift" : "push"](() => {
      l = u, p.set(l);
    });
  }
  return n.$$set = (u) => {
    r(17, t = I(I({}, t), A(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, o = u.$$scope);
  }, t = A(t), [s, l, d, p, c, i, o, e, Y, K];
}
class Se extends ie {
  constructor(t) {
    super(), me(this, t, xe, Re, ge, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, R = window.ms_globals.tree;
function ke(n) {
  function t(r) {
    const s = E(), l = new Se({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, o], F({
            createPortal: x,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: x,
              node: R
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
      r(t);
    });
  });
}
function Ie(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function N(n) {
  return M(() => Ie(n), [n]);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function k(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(x(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((l) => {
        if (m.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = k(l.props.el);
          return m.cloneElement(l, {
            ...l.props,
            el: o,
            children: [...m.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, o, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let l = 0; l < s.length; l++) {
    const e = s[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = k(e);
      t.push(...c), r.appendChild(o);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = Q(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, l) => {
  const e = X(), [o, c] = Z([]);
  return $(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(l, a), r && a.classList.add(...r.split(" ")), s) {
        const f = Pe(s);
        Object.keys(f).forEach((h) => {
          a.style[h] = f[h];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: f,
          clonedElement: h
        } = k(n);
        i = h, c(f), i.style.display = "contents", _(), (w = e.current) == null || w.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, h;
        (f = e.current) != null && f.contains(i) && ((h = e.current) == null || h.removeChild(i)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, s, l]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function B(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const s = {
      ...r.props
    };
    let l = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((a, f) => {
        l[a] || (l[a] = {}), f !== c.length - 1 && (l = s[a]);
      });
      const i = r.slots[o];
      let _, d, p = (t == null ? void 0 : t.clone) ?? !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone ?? !1), l[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ b.jsx(D, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ b.jsx(D, {
        slot: _,
        clone: p
      }) : l[c[c.length - 1]], l = s;
    });
    const e = (t == null ? void 0 : t.children) || "children";
    return r[e] && (s[e] = B(r[e], t)), s;
  });
}
const Le = ke(({
  getContainer: n,
  getCurrentAnchor: t,
  children: r,
  items: s,
  slotItems: l,
  ...e
}) => {
  const o = N(n), c = N(t);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [r, /* @__PURE__ */ b.jsx(te, {
      ...e,
      items: M(() => s || B(l, {
        clone: !0
      }), [s, l]),
      getContainer: o,
      getCurrentAnchor: c
    })]
  });
});
export {
  Le as Anchor,
  Le as default
};
