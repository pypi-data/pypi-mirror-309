import { g as ee, w as E } from "./Index-Bg1-Gj4E.js";
const g = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tour;
var W = {
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
var ne = g, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(t, n, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) se.call(n, s) && !ce.hasOwnProperty(s) && (o[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: re,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: le.current
  };
}
x.Fragment = oe;
x.jsx = z;
x.jsxs = z;
W.exports = x;
var h = W.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: P,
  check_outros: ae,
  children: G,
  claim_element: U,
  claim_space: ue,
  component_subscribe: j,
  compute_slots: de,
  create_slot: fe,
  detach: w,
  element: H,
  empty: T,
  exclude_internal_props: L,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: we,
  transition_in: v,
  transition_out: C,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Re
} = window.__gradio__svelte__internal;
function F(t) {
  let n, r;
  const s = (
    /*#slots*/
    t[7].default
  ), o = fe(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(n);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, n, l), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && be(
        o,
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      C(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, r, s, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = H("react-portal-target"), r = we(), e && e.c(), s = T(), this.h();
    },
    l(l) {
      n = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(n).forEach(w), r = ue(l), e && e.l(l), s = T(), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, n, c), t[8](n), y(l, r, c), e && e.m(l, c), y(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = F(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (me(), C(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      o || (v(e), o = !0);
    },
    o(l) {
      C(e), o = !1;
    },
    d(l) {
      l && (w(n), w(r), w(s)), t[8](null), e && e.d(l);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Ie(t, n, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = de(e);
  let {
    svelteInit: i
  } = n;
  const p = E(N(n)), d = E();
  j(t, d, (u) => r(0, s = u));
  const _ = E();
  j(t, _, (u) => r(1, o = u));
  const a = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: V
  } = ee() || {}, J = i({
    parent: f,
    props: p,
    target: d,
    slot: _,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: V,
    onDestroy(u) {
      a.push(u);
    }
  });
  Re("$$ms-gr-react-wrapper", J), Ee(() => {
    p.set(N(n));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function Y(u) {
    P[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function K(u) {
    P[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return t.$$set = (u) => {
    r(17, n = k(k({}, n), L(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, n = L(n), [s, o, d, _, c, i, l, e, Y, K];
}
class Se extends ie {
  constructor(n) {
    super(), he(this, n, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(t) {
  function n(r) {
    const s = E(), o = new Se({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], A({
            createPortal: S,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), A({
              createPortal: S,
              node: I
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
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const s = t[r];
    return typeof s == "number" && !Oe.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function O(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(S(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      n.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Pe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const R = Q(({
  slot: t,
  clone: n,
  className: r,
  style: s
}, o) => {
  const e = X(), [l, c] = Z([]);
  return $(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((m) => {
          a.style[m] = f[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: f,
          clonedElement: m
        } = O(t);
        i = m, c(f), i.style.display = "contents", p(), (b = e.current) == null || b.appendChild(i);
      };
      a(), d = new window.MutationObserver(() => {
        var f, m;
        (f = e.current) != null && f.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, r, s, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(t) {
  return M(() => je(t), [t]);
}
function B(t, n) {
  return t.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let o = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== c.length - 1 && (o = s[a]);
      });
      const i = r.slots[l];
      let p, d, _ = !1;
      i instanceof Element ? p = i : (p = i.el, d = i.callback, _ = i.clone ?? !1), o[c[c.length - 1]] = p ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ h.jsx(R, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ h.jsx(R, {
        slot: p,
        clone: _
      }) : o[c[c.length - 1]], o = s;
    });
    const e = "children";
    return r[e] && (s[e] = B(r[e])), s;
  });
}
function Te(t, n) {
  return t ? /* @__PURE__ */ h.jsx(R, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Le({
  key: t,
  setSlotParams: n,
  slots: r
}, s) {
  return r[t] ? (...o) => (n(t, o), Te(r[t], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Ce(({
  slots: t,
  steps: n,
  slotItems: r,
  children: s,
  onChange: o,
  onClose: e,
  getPopupContainer: l,
  setSlotParams: c,
  indicatorsRender: i,
  ...p
}) => {
  const d = D(l), _ = D(i);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ h.jsx(te, {
      ...p,
      steps: M(() => n || B(r), [n, r]),
      onChange: (a) => {
        o == null || o(a);
      },
      closeIcon: t.closeIcon ? /* @__PURE__ */ h.jsx(R, {
        slot: t.closeIcon
      }) : p.closeIcon,
      indicatorsRender: t.indicatorsRender ? Le({
        slots: t,
        setSlotParams: c,
        key: "indicatorsRender"
      }) : _,
      getPopupContainer: d,
      onClose: (a, ...f) => {
        e == null || e(a, ...f);
      }
    })]
  });
});
export {
  Ne as Tour,
  Ne as default
};
