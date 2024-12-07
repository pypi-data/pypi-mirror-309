import { g as Z, w as E } from "./Index-DEHxK9xu.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, F = window.ms_globals.React.useEffect, R = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.notification;
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
var $ = g, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ne.call(n, l) && !re.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ee,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: oe.current
  };
}
I.Fragment = te;
I.jsx = z;
I.jsxs = z;
W.exports = I;
var h = W.exports;
const {
  SvelteComponent: se,
  assign: O,
  binding_callbacks: P,
  check_outros: le,
  children: G,
  claim_element: H,
  claim_space: ie,
  component_subscribe: j,
  compute_slots: ce,
  create_slot: ae,
  detach: w,
  element: U,
  empty: L,
  exclude_internal_props: N,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: K,
  space: me,
  transition_in: x,
  transition_out: S,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: ye,
  setContext: be
} = window.__gradio__svelte__internal;
function T(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = ae(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = U("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = G(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && he(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (x(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function Ee(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && T(t)
  );
  return {
    c() {
      n = U("react-portal-target"), r = me(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      n = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(n).forEach(w), r = ie(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, n, c), t[8](n), v(s, r, c), e && e.m(s, c), v(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = T(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (fe(), S(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      S(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function A(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function ve(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ce(e);
  let {
    svelteInit: i
  } = n;
  const u = E(A(n)), f = E();
  j(t, f, (d) => r(0, l = d));
  const p = E();
  j(t, p, (d) => r(1, o = d));
  const a = [], _ = we("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: M
  } = Z() || {}, q = i({
    parent: _,
    props: u,
    target: f,
    slot: p,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: M,
    onDestroy(d) {
      a.push(d);
    }
  });
  be("$$ms-gr-react-wrapper", q), ge(() => {
    u.set(A(n));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function B(d) {
    P[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  function J(d) {
    P[d ? "unshift" : "push"](() => {
      o = d, p.set(o);
    });
  }
  return t.$$set = (d) => {
    r(17, n = O(O({}, n), N(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = N(n), [l, o, f, p, c, i, s, e, B, J];
}
class xe extends se {
  constructor(n) {
    super(), _e(this, n, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, C = window.ms_globals.tree;
function Ie(t) {
  function n(r) {
    const l = E(), o = new xe({
      ...r,
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
          }, c = e.parent ?? C;
          return c.nodes = [...c.nodes, s], D({
            createPortal: R,
            node: C
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: R,
              node: C
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Ce.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function k(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(R(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Se(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const y = Y(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return F(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function u() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Se(o, a), r && a.classList.add(...r.split(" ")), l) {
        const _ = Re(l);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var b;
        const {
          portals: _,
          clonedElement: m
        } = k(t);
        i = m, c(_), i.style.display = "contents", u(), (b = e.current) == null || b.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var _, m;
        (_ = e.current) != null && _.contains(i) && ((m = e.current) == null || m.removeChild(i)), a();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", u(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, r, l, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Oe = Ie(({
  slots: t,
  bottom: n,
  rtl: r,
  stack: l,
  top: o,
  children: e,
  visible: s,
  onClose: c,
  onVisible: i,
  ...u
}) => {
  const [f, p] = V.useNotification({
    bottom: n,
    rtl: r,
    stack: l,
    top: o
  });
  return F(() => (s ? f.open({
    ...u,
    btn: t.btn ? /* @__PURE__ */ h.jsx(y, {
      slot: t.btn
    }) : u.btn,
    closeIcon: t.closeIcon ? /* @__PURE__ */ h.jsx(y, {
      slot: t.closeIcon
    }) : u.closeIcon,
    description: t.description ? /* @__PURE__ */ h.jsx(y, {
      slot: t.description
    }) : u.description,
    message: t.message ? /* @__PURE__ */ h.jsx(y, {
      slot: t.message
    }) : u.message,
    icon: t.icon ? /* @__PURE__ */ h.jsx(y, {
      slot: t.icon
    }) : u.icon,
    onClose(...a) {
      i == null || i(!1), c == null || c(...a);
    }
  }) : f.destroy(u.key), () => {
    f.destroy(u.key);
  }), [s]), /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [e, p]
  });
});
export {
  Oe as Notification,
  Oe as default
};
