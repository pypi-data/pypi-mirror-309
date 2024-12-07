import { g as $, w as E } from "./Index-CxixO46B.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Drawer;
var M = {
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
var te = m, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(t, n, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) oe.call(n, l) && !se.hasOwnProperty(l) && (r[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = W;
C.jsxs = W;
M.exports = C;
var h = M.exports;
const {
  SvelteComponent: ie,
  assign: P,
  binding_callbacks: j,
  check_outros: ce,
  children: z,
  claim_element: G,
  claim_space: ae,
  component_subscribe: L,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: U,
  empty: T,
  exclude_internal_props: F,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: v,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: we,
  transition_in: x,
  transition_out: O,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(t) {
  let n, o;
  const l = (
    /*#slots*/
    t[7].default
  ), r = de(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = U("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(n);
      r && r.l(s), s.forEach(w), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, n, s), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && ge(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
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
      o || (x(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && w(n), r && r.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, o, l, r, e = (
    /*$$slots*/
    t[4].default && N(t)
  );
  return {
    c() {
      n = U("react-portal-target"), o = we(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      n = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(w), o = ae(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, n, c), t[8](n), v(s, o, c), e && e.m(s, c), v(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = N(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (pe(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (x(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (w(n), w(o), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function A(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Ce(t, n, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const g = E(A(n)), f = E();
  L(t, f, (a) => o(0, l = a));
  const p = E();
  L(t, p, (a) => o(1, r = a));
  const u = [], d = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: y,
    subSlotIndex: K
  } = $() || {}, q = i({
    parent: d,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", q), be(() => {
    g.set(A(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function V(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function B(a) {
    j[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = P(P({}, n), F(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = F(n), [l, r, f, p, c, i, s, e, V, B];
}
class Re extends ie {
  constructor(n) {
    super(), me(this, n, Ce, xe, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, R = window.ms_globals.tree;
function Ie(t) {
  function n(o) {
    const l = E(), r = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, s], D({
            createPortal: S,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: S,
              node: R
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
      o(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const l = t[o];
    return typeof l == "number" && !Se.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function k(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(S(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
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
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      n.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function ke(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const b = J(({
  slot: t,
  clone: n,
  className: o,
  style: l
}, r) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(r, u), o && u.classList.add(...o.split(" ")), l) {
        const d = Oe(l);
        Object.keys(d).forEach((_) => {
          u.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y;
        const {
          portals: d,
          clonedElement: _
        } = k(t);
        i = _, c(d), i.style.display = "contents", g(), (y = e.current) == null || y.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, _;
        (d = e.current) != null && d.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(t) {
  return Z(() => Pe(t), [t]);
}
function je(t, n) {
  return t ? /* @__PURE__ */ h.jsx(b, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Le({
  key: t,
  setSlotParams: n,
  slots: o
}, l) {
  return o[t] ? (...r) => (n(t, r), je(o[t], {
    clone: !0,
    ...l
  })) : void 0;
}
const Fe = Ie(({
  slots: t,
  afterOpenChange: n,
  getContainer: o,
  drawerRender: l,
  setSlotParams: r,
  ...e
}) => {
  const s = I(n), c = I(o), i = I(l);
  return /* @__PURE__ */ h.jsx(ee, {
    ...e,
    afterOpenChange: s,
    closeIcon: t.closeIcon ? /* @__PURE__ */ h.jsx(b, {
      slot: t.closeIcon
    }) : e.closeIcon,
    extra: t.extra ? /* @__PURE__ */ h.jsx(b, {
      slot: t.extra
    }) : e.extra,
    footer: t.footer ? /* @__PURE__ */ h.jsx(b, {
      slot: t.footer
    }) : e.footer,
    title: t.title ? /* @__PURE__ */ h.jsx(b, {
      slot: t.title
    }) : e.title,
    drawerRender: t.drawerRender ? Le({
      slots: t,
      setSlotParams: r,
      key: "drawerRender"
    }) : i,
    getContainer: typeof o == "string" ? c : o
  });
});
export {
  Fe as Drawer,
  Fe as default
};
