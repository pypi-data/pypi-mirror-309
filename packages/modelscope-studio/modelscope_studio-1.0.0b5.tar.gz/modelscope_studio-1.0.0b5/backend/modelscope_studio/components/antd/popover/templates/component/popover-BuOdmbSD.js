import { g as $, w as y } from "./Index-BVAwT52e.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, x = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Popover;
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
var te = m, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) re.call(n, l) && !le.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = W;
C.jsxs = W;
M.exports = C;
var w = M.exports;
const {
  SvelteComponent: ie,
  assign: O,
  binding_callbacks: P,
  check_outros: ce,
  children: z,
  claim_element: G,
  claim_space: ae,
  component_subscribe: k,
  compute_slots: ue,
  create_slot: de,
  detach: h,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: E,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: v,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function j(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = de(
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
      n = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(n);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      S(o, e), r = !1;
    },
    d(e) {
      e && h(n), o && o.d(e), t[9](null);
    }
  };
}
function Ce(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && j(t)
  );
  return {
    c() {
      n = U("react-portal-target"), r = ge(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      n = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(h), r = ae(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, n, c), t[8](n), E(s, r, c), e && e.m(s, c), E(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = j(s), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (_e(), S(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (v(e), o = !0);
    },
    o(s) {
      S(e), o = !1;
    },
    d(s) {
      s && (h(n), h(r), h(l)), t[8](null), e && e.d(s);
    }
  };
}
function F(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Re(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const g = y(F(n)), f = y();
  k(t, f, (a) => r(0, l = a));
  const _ = y();
  k(t, _, (a) => r(1, o = a));
  const u = [], d = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: K
  } = $() || {}, q = i({
    parent: d,
    props: g,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: K,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", q), be(() => {
    g.set(F(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function V(a) {
    P[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function B(a) {
    P[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, n = O(O({}, n), T(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, n = T(n), [l, o, f, _, c, i, s, e, V, B];
}
class xe extends ie {
  constructor(n) {
    super(), me(this, n, Re, Ce, he, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(t) {
  function n(r) {
    const l = y(), o = new xe({
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
      r(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Ie.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function I(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(x(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((o) => {
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
      } = I(e);
      n.push(...c), r.appendChild(s);
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
const A = J(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const d = Oe(l);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: d,
          clonedElement: p
        } = I(t);
        i = p, c(d), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), f.observe(t, {
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
  }, [t, n, r, l, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function D(t) {
  return Z(() => ke(t), [t]);
}
const Te = Se(({
  slots: t,
  afterOpenChange: n,
  getPopupContainer: r,
  children: l,
  ...o
}) => {
  const e = D(n), s = D(r);
  return /* @__PURE__ */ w.jsx(w.Fragment, {
    children: /* @__PURE__ */ w.jsx(ee, {
      ...o,
      afterOpenChange: e,
      getPopupContainer: s,
      title: t.title ? /* @__PURE__ */ w.jsx(A, {
        slot: t.title
      }) : o.title,
      content: t.content ? /* @__PURE__ */ w.jsx(A, {
        slot: t.content
      }) : o.content,
      children: l
    })
  });
});
export {
  Te as Popover,
  Te as default
};
