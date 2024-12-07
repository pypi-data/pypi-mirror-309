import { g as $, w as y } from "./Index-C94et7sc.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Slider;
var G = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(r, t, n) {
  var l, o = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !le.hasOwnProperty(l) && (o[l] = t[l]);
  if (r && r.defaultProps) for (l in t = r.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = W;
S.jsxs = W;
G.exports = S;
var g = G.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: j,
  check_outros: ce,
  children: z,
  claim_element: U,
  claim_space: ae,
  component_subscribe: L,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: H,
  empty: T,
  exclude_internal_props: F,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: E,
  safe_not_equal: he,
  set_custom_element_data: K,
  space: ge,
  transition_in: C,
  transition_out: I,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: Ce
} = window.__gradio__svelte__internal;
function v(r) {
  let t, n;
  const l = (
    /*#slots*/
    r[7].default
  ), o = de(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), o && o.m(t, null), r[9](t), n = !0;
    },
    p(e, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        n ? pe(
          l,
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
      n || (C(o, e), n = !0);
    },
    o(e) {
      I(o, e), n = !1;
    },
    d(e) {
      e && w(t), o && o.d(e), r[9](null);
    }
  };
}
function Se(r) {
  let t, n, l, o, e = (
    /*$$slots*/
    r[4].default && v(r)
  );
  return {
    c() {
      t = H("react-portal-target"), n = ge(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = U(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(w), n = ae(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, t, c), r[8](t), E(s, n, c), e && e.m(s, c), E(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = v(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (_e(), I(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      I(e), o = !1;
    },
    d(s) {
      s && (w(t), w(n), w(l)), r[8](null), e && e.d(s);
    }
  };
}
function N(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function xe(r, t, n) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const m = y(N(t)), f = y();
  L(r, f, (u) => n(0, l = u));
  const _ = y();
  L(r, _, (u) => n(1, o = u));
  const a = [], d = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: q
  } = $() || {}, V = i({
    parent: d,
    props: m,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", V), be(() => {
    m.set(N(t));
  }), Ee(() => {
    a.forEach((u) => u());
  });
  function B(u) {
    j[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function J(u) {
    j[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return r.$$set = (u) => {
    n(17, t = k(k({}, t), F(u))), "svelteInit" in u && n(5, i = u.svelteInit), "$$scope" in u && n(6, s = u.$$scope);
  }, t = F(t), [l, o, f, _, c, i, s, e, B, J];
}
class Re extends ie {
  constructor(t) {
    super(), me(this, t, xe, Se, he, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ie(r) {
  function t(n) {
    const l = y(), o = new Re({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], A({
            createPortal: R,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: x
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
      n(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(r) {
  return r ? Object.keys(r).reduce((t, n) => {
    const l = r[n];
    return typeof l == "number" && !Oe.includes(n) ? t[n] = l + "px" : t[n] = l, t;
  }, {}) : {};
}
function O(r) {
  const t = [], n = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(R(h.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: h.Children.toArray(r._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      n.addEventListener(c, s, i);
    });
  });
  const l = Array.from(r.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = O(e);
      t.push(...c), n.appendChild(s);
    } else e.nodeType === 3 && n.appendChild(e.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function ke(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const P = Y(({
  slot: r,
  clone: t,
  className: n,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return Z(() => {
    var _;
    if (!e.current || !r)
      return;
    let i = r;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(o, a), n && a.classList.add(...n.split(" ")), l) {
        const d = Pe(l);
        Object.keys(d).forEach((p) => {
          a.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: d,
          clonedElement: p
        } = O(r);
        i = p, c(d), i.style.display = "contents", m(), (b = e.current) == null || b.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), a();
      }), f.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var a, d;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [r, t, n, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(r) {
  try {
    return typeof r == "string" ? new Function(`return (...args) => (${r})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(r) {
  return M(() => je(r), [r]);
}
function Le(r, t) {
  return r ? /* @__PURE__ */ g.jsx(P, {
    slot: r,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: r,
  setSlotParams: t,
  slots: n
}, l) {
  return n[r] ? (...o) => (t(r, o), Le(n[r], {
    clone: !0,
    ...l
  })) : void 0;
}
const Fe = (r) => r.reduce((t, n) => {
  const l = n == null ? void 0 : n.props.number;
  return l !== void 0 && (t[l] = (n == null ? void 0 : n.slots.label) instanceof Element ? {
    ...n.props,
    label: /* @__PURE__ */ g.jsx(P, {
      slot: n == null ? void 0 : n.slots.label
    })
  } : (n == null ? void 0 : n.slots.children) instanceof Element ? /* @__PURE__ */ g.jsx(P, {
    slot: n == null ? void 0 : n.slots.children
  }) : {
    ...n == null ? void 0 : n.props
  }), t;
}, {}), Ne = Ie(({
  marks: r,
  markItems: t,
  children: n,
  onValueChange: l,
  onChange: o,
  elRef: e,
  tooltip: s,
  step: c,
  slots: i,
  setSlotParams: m,
  ...f
}) => {
  const _ = (p) => {
    o == null || o(p), l(p);
  }, a = D(s == null ? void 0 : s.getPopupContainer), d = D(s == null ? void 0 : s.formatter);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ g.jsx(ee, {
      ...f,
      tooltip: {
        ...s,
        getPopupContainer: a,
        formatter: i["tooltip.formatter"] ? Te({
          key: "tooltip.formatter",
          setSlotParams: m,
          slots: i
        }) : d
      },
      marks: M(() => r || Fe(t), [t, r]),
      step: c === void 0 ? null : c,
      ref: e,
      onChange: _
    })]
  });
});
export {
  Ne as Slider,
  Ne as default
};
