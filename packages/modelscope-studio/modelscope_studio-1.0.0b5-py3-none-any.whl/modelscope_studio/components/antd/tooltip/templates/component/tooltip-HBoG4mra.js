import { g as Z, w as y } from "./Index-9rGoiA0J.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, x = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Tooltip;
var D = {
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
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: re.current
  };
}
C.Fragment = ne;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var b = D.exports;
const {
  SvelteComponent: le,
  assign: O,
  binding_callbacks: k,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ce,
  component_subscribe: P,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: G,
  empty: T,
  exclude_internal_props: L,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: v,
  transition_out: S,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function j(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = G("react-portal-target"), r = he(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(h), r = ce(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, t, c), n[8](t), E(s, r, c), e && e.m(s, c), E(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = j(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      o || (v(e), o = !0);
    },
    o(s) {
      S(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = y(F(t)), f = y();
  P(n, f, (a) => r(0, l = a));
  const _ = y();
  P(n, _, (a) => r(1, o = a));
  const u = [], d = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H
  } = Z() || {}, K = i({
    parent: d,
    props: g,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", K), we(() => {
    g.set(F(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function V(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = O(O({}, t), L(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = L(t), [l, o, f, _, c, i, s, e, q, V];
}
class Re extends le {
  constructor(t) {
    super(), _e(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, R = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = y(), o = new Re({
      ...r,
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
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, s], N({
            createPortal: x,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), N({
              createPortal: x,
              node: R
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
      r(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Se.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function I(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(x(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = I(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...m.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = I(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const ke = B(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const d = Ie(l);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w;
        const {
          portals: d,
          clonedElement: p
        } = I(n);
        i = p, c(d), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, l, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function A(n) {
  return X(() => Pe(n), [n]);
}
const Le = xe(({
  slots: n,
  afterOpenChange: t,
  getPopupContainer: r,
  children: l,
  ...o
}) => {
  const e = A(t), s = A(r);
  return /* @__PURE__ */ b.jsx(b.Fragment, {
    children: /* @__PURE__ */ b.jsx($, {
      ...o,
      afterOpenChange: e,
      getPopupContainer: s,
      title: n.title ? /* @__PURE__ */ b.jsx(ke, {
        slot: n.title
      }) : o.title,
      children: l
    })
  });
});
export {
  Le as Tooltip,
  Le as default
};
