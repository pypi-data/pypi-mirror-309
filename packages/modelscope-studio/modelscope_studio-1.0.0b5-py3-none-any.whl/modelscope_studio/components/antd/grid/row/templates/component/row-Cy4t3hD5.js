import { g as X, w as b } from "./Index-BnmO_TR7.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, Q = window.ms_globals.React.createElement, R = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Row, $ = window.ms_globals.antd.Col;
var D = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) re.call(t, l) && !se.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: oe.current
  };
}
v.Fragment = ne;
v.jsx = W;
v.jsxs = W;
D.exports = v;
var I = D.exports;
const {
  SvelteComponent: le,
  assign: O,
  binding_callbacks: k,
  check_outros: ie,
  children: z,
  claim_element: F,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: ce,
  create_slot: de,
  detach: h,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ue,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: y,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: Ee,
  setContext: ye
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = de(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = F(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? fe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (y(r, e), o = !0);
    },
    o(e) {
      S(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = G("react-portal-target"), o = he(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = F(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(t).forEach(h), o = ae(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      E(s, t, a), n[8](t), E(s, o, a), e && e.m(s, a), E(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && y(e, 1)) : (e = N(s), e.c(), y(e, 1), e.m(l.parentNode, l)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      r || (y(e), r = !0);
    },
    o(s) {
      S(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function j(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ce(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ce(e);
  let {
    svelteInit: i
  } = t;
  const w = b(j(t)), f = b();
  P(n, f, (c) => o(0, l = c));
  const _ = b();
  P(n, _, (c) => o(1, r = c));
  const d = [], u = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: H
  } = X() || {}, K = i({
    parent: u,
    props: w,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: H,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", K), ge(() => {
    w.set(j(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function M(c) {
    k[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function q(c) {
    k[c ? "unshift" : "push"](() => {
      r = c, _.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = O(O({}, t), T(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = T(t), [l, r, f, _, a, i, s, e, M, q];
}
class Re extends le {
  constructor(t) {
    super(), _e(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const l = b(), r = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? C;
          return a.nodes = [...a.nodes, s], A({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: R,
              node: C
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !xe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function x(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = x(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = x(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const ke = V(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = B(), [s, a] = J([]);
  return Y(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Oe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Ie(l);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var g;
        const {
          portals: u,
          clonedElement: p
        } = x(n);
        i = p, a(u), i.style.display = "contents", w(), (g = e.current) == null || g.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(i) && ((p = e.current) == null || p.removeChild(i)), d();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Le = Se(({
  cols: n,
  children: t,
  ...o
}) => /* @__PURE__ */ I.jsxs(Z, {
  ...o,
  children: [t, n == null ? void 0 : n.map((l, r) => {
    if (!l)
      return;
    const {
      el: e,
      props: s
    } = l;
    return /* @__PURE__ */ Q($, {
      ...s,
      key: r
    }, e && /* @__PURE__ */ I.jsx(ke, {
      slot: e
    }));
  })]
}));
export {
  Le as Row,
  Le as default
};
