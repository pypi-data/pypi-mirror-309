import { g as V, w as b } from "./Index-CRffszdU.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, M = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.message;
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(t, n, s) {
  var l, r = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (l in n) re.call(n, l) && !se.hasOwnProperty(l) && (r[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: o,
    props: r,
    _owner: oe.current
  };
}
C.Fragment = ne;
C.jsx = W;
C.jsxs = W;
D.exports = C;
var w = D.exports;
const {
  SvelteComponent: le,
  assign: k,
  binding_callbacks: O,
  check_outros: ie,
  children: z,
  claim_element: G,
  claim_space: ce,
  component_subscribe: P,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: H,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: v,
  transition_out: S,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ye,
  onDestroy: be,
  setContext: Ee
} = window.__gradio__svelte__internal;
function j(t) {
  let n, s;
  const l = (
    /*#slots*/
    t[7].default
  ), r = ue(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = G(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = z(n);
      r && r.l(o), o.forEach(g), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      E(e, n, o), r && r.m(n, null), t[9](n), s = !0;
    },
    p(e, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && ge(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          l,
          /*$$scope*/
          e[6],
          o,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (v(r, e), s = !0);
    },
    o(e) {
      S(r, e), s = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, s, l, r, e = (
    /*$$slots*/
    t[4].default && j(t)
  );
  return {
    c() {
      n = H("react-portal-target"), s = he(), e && e.c(), l = L(), this.h();
    },
    l(o) {
      n = G(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(g), s = ce(o), e && e.l(o), l = L(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      E(o, n, c), t[8](n), E(o, s, c), e && e.m(o, c), E(o, l, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = j(o), e.c(), v(e, 1), e.m(l.parentNode, l)) : e && (_e(), S(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(o) {
      r || (v(e), r = !0);
    },
    o(o) {
      S(e), r = !1;
    },
    d(o) {
      o && (g(n), g(s), g(l)), t[8](null), e && e.d(o);
    }
  };
}
function A(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function Ce(t, n, s) {
  let l, r, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const p = b(A(n)), d = b();
  P(t, d, (a) => s(0, l = a));
  const m = b();
  P(t, m, (a) => s(1, r = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: y,
    subSlotIndex: K
  } = V() || {}, q = i({
    parent: f,
    props: p,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", q), we(() => {
    p.set(A(n));
  }), be(() => {
    u.forEach((a) => a());
  });
  function B(a) {
    O[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function J(a) {
    O[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return t.$$set = (a) => {
    s(17, n = k(k({}, n), T(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, n = T(n), [l, r, d, m, c, i, o, e, B, J];
}
class xe extends le {
  constructor(n) {
    super(), pe(this, n, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, x = window.ms_globals.tree;
function Re(t) {
  function n(s) {
    const l = b(), r = new xe({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, o], N({
            createPortal: R,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), N({
              createPortal: R,
              node: x
            });
          }), o;
        },
        ...s.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const l = t[s];
    return typeof l == "number" && !Se.includes(s) ? n[s] = l + "px" : n[s] = l, n;
  }, {}) : {};
}
function I(t) {
  const n = [], s = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(R(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = I(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, o, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = I(e);
      n.push(...c), s.appendChild(o);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: n
  };
}
function ke(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const F = Y(({
  slot: t,
  clone: n,
  className: s,
  style: l
}, r) => {
  const e = Q(), [o, c] = X([]);
  return M(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(r, u), s && u.classList.add(...s.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y;
        const {
          portals: f,
          clonedElement: _
        } = I(t);
        i = _, c(f), i.style.display = "contents", p(), (y = e.current) == null || y.appendChild(i);
      };
      u(), d = new window.MutationObserver(() => {
        var f, _;
        (f = e.current) != null && f.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, s, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Oe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Pe(t) {
  return Z(() => Oe(t), [t]);
}
const Te = Re(({
  slots: t,
  children: n,
  visible: s,
  onVisible: l,
  onClose: r,
  getContainer: e,
  ...o
}) => {
  const c = Pe(e), [i, p] = $.useMessage({
    ...o,
    getContainer: c
  });
  return M(() => (s ? i.open({
    ...o,
    icon: t.icon ? /* @__PURE__ */ w.jsx(F, {
      slot: t.icon
    }) : o.icon,
    content: t.content ? /* @__PURE__ */ w.jsx(F, {
      slot: t.content
    }) : o.content,
    onClose(...d) {
      l == null || l(!1), r == null || r(...d);
    }
  }) : i.destroy(o.key), () => {
    i.destroy(o.key);
  }), [s]), /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), p]
  });
});
export {
  Te as Message,
  Te as default
};
