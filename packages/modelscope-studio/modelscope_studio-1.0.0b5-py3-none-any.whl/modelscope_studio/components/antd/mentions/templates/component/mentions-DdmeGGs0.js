import { b as ee, g as te, w as y } from "./Index-B8Aa9pk7.js";
const h = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Mentions;
function re(n, t) {
  return ee(n, t);
}
var U = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = h, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var o, l = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) ce.call(t, o) && !ae.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: s,
    props: l,
    _owner: ie.current
  };
}
R.Fragment = se;
R.jsx = H;
R.jsxs = H;
U.exports = R;
var g = U.exports;
const {
  SvelteComponent: ue,
  assign: T,
  binding_callbacks: N,
  check_outros: de,
  children: B,
  claim_element: J,
  claim_space: fe,
  component_subscribe: A,
  compute_slots: _e,
  create_slot: pe,
  detach: w,
  element: Y,
  empty: M,
  exclude_internal_props: V,
  get_all_dirty_from_scope: me,
  get_slot_changes: he,
  group_outros: ge,
  init: be,
  insert_hydration: v,
  safe_not_equal: we,
  set_custom_element_data: K,
  space: Ee,
  transition_in: C,
  transition_out: j,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Re,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = pe(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = Y("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      t = J(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = B(t);
      l && l.l(s), s.forEach(w), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && ye(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? he(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(l, e), r = !0);
    },
    o(e) {
      j(l, e), r = !1;
    },
    d(e) {
      e && w(t), l && l.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, r, o, l, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = Y("react-portal-target"), r = Ee(), e && e.c(), o = M(), this.h();
    },
    l(s) {
      t = J(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), B(t).forEach(w), r = fe(s), e && e.l(s), o = M(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, t, c), n[8](t), v(s, r, c), e && e.m(s, c), v(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = D(s), e.c(), C(e, 1), e.m(o.parentNode, o)) : e && (ge(), j(e, 1, 1, () => {
        e = null;
      }), de());
    },
    i(s) {
      l || (C(e), l = !0);
    },
    o(s) {
      j(e), l = !1;
    },
    d(s) {
      s && (w(t), w(r), w(o)), n[8](null), e && e.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ie(n, t, r) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = _e(e);
  let {
    svelteInit: i
  } = t;
  const _ = y(W(t)), d = y();
  A(n, d, (u) => r(0, o = u));
  const p = y();
  A(n, p, (u) => r(1, l = u));
  const a = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: E
  } = te() || {}, x = i({
    parent: f,
    props: _,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: E,
    onDestroy(u) {
      a.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", x), ve(() => {
    _.set(W(t));
  }), Re(() => {
    a.forEach((u) => u());
  });
  function X(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function Z(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, p.set(l);
    });
  }
  return n.$$set = (u) => {
    r(17, t = T(T({}, t), V(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = V(t), [o, l, d, p, c, i, s, e, X, Z];
}
class Oe extends ue {
  constructor(t) {
    super(), be(this, t, Ie, Se, we, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, S = window.ms_globals.tree;
function ke(n) {
  function t(r) {
    const o = y(), l = new Oe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], q({
            createPortal: P,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), q({
              createPortal: P,
              node: S
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const o = n[r];
    return typeof o == "number" && !Pe.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function F(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((l) => {
        if (h.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = F(l.props.el);
          return h.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...h.Children.toArray(l.props.children), ...e]
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let l = 0; l < o.length; l++) {
    const e = o[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = F(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Fe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const L = $(({
  slot: n,
  clone: t,
  className: r,
  style: o
}, l) => {
  const e = O(), [s, c] = z([]);
  return k(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function _() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(l, a), r && a.classList.add(...r.split(" ")), o) {
        const f = je(o);
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
        } = F(n);
        i = m, c(f), i.style.display = "contents", _(), (b = e.current) == null || b.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
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
  }, [n, t, r, o, l]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(n) {
  return G(() => Le(n), [n]);
}
function Te({
  value: n,
  onValueChange: t
}) {
  const [r, o] = z(n), l = O(t);
  l.current = t;
  const e = O(r);
  return e.current = r, k(() => {
    l.current(r);
  }, [r]), k(() => {
    re(n, e.current) || o(n);
  }, [n]), [r, o];
}
function Q(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const o = {
      ...r.props
    };
    let l = o;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        l[a] || (l[a] = {}), f !== c.length - 1 && (l = o[a]);
      });
      const i = r.slots[s];
      let _, d, p = (t == null ? void 0 : t.clone) ?? !1;
      i instanceof Element ? _ = i : (_ = i.el, d = i.callback, p = i.clone ?? !1), l[c[c.length - 1]] = _ ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ g.jsx(L, {
        slot: _,
        clone: p
      })) : /* @__PURE__ */ g.jsx(L, {
        slot: _,
        clone: p
      }) : l[c[c.length - 1]], l = o;
    });
    const e = (t == null ? void 0 : t.children) || "children";
    return r[e] && (o[e] = Q(r[e], t)), o;
  });
}
const Ae = ke(({
  slots: n,
  children: t,
  onValueChange: r,
  filterOption: o,
  onChange: l,
  options: e,
  validateSearch: s,
  optionItems: c,
  getPopupContainer: i,
  elRef: _,
  ...d
}) => {
  const p = I(i), a = I(o), f = I(s), [m, b] = Te({
    onValueChange: r,
    value: d.value
  });
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(ne, {
      ...d,
      ref: _,
      value: m,
      options: G(() => e || Q(c, {
        clone: !0
      }), [c, e]),
      onChange: (E, ...x) => {
        l == null || l(E, ...x), b(E);
      },
      validateSearch: f,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ g.jsx(L, {
        slot: n.notFoundContent
      }) : d.notFoundContent,
      filterOption: a || o,
      getPopupContainer: p
    })]
  });
});
export {
  Ae as Mentions,
  Ae as default
};
