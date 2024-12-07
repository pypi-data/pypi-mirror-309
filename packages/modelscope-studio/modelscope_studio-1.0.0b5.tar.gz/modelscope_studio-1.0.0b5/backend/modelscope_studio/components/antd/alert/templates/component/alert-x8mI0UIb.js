import { g as Z, w as E } from "./Index-CysfZvJK.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Alert;
var D = {
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
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !se.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
x.Fragment = ne;
x.jsx = M;
x.jsxs = M;
D.exports = x;
var h = D.exports;
const {
  SvelteComponent: le,
  assign: k,
  binding_callbacks: P,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: G,
  empty: L,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: C,
  transition_out: S,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: we,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function T(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = ue(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(n);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? fe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (C(r, e), o = !0);
    },
    o(e) {
      S(r, e), o = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && T(t)
  );
  return {
    c() {
      n = G("react-portal-target"), o = he(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      n = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(n).forEach(g), o = ce(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, n, c), t[8](n), v(l, o, c), e && e.m(l, c), v(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = T(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (_e(), S(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (C(e), r = !0);
    },
    o(l) {
      S(e), r = !1;
    },
    d(l) {
      l && (g(n), g(o), g(s)), t[8](null), e && e.d(l);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Ce(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const b = E(N(n)), f = E();
  j(t, f, (a) => o(0, s = a));
  const p = E();
  j(t, p, (a) => o(1, r = a));
  const u = [], d = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: y,
    subSlotIndex: H
  } = Z() || {}, K = i({
    parent: d,
    props: b,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: y,
    subSlotIndex: H,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", K), be(() => {
    b.set(N(n));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function q(a) {
    P[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function V(a) {
    P[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = k(k({}, n), A(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, n = A(n), [s, r, f, p, c, i, l, e, q, V];
}
class xe extends le {
  constructor(n) {
    super(), pe(this, n, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ie(t) {
  function n(o) {
    const s = E(), r = new xe({
      ...o,
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
          return c.nodes = [...c.nodes, l], F({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: R,
              node: I
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !Re.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function O(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(R(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      n.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Oe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const w = B(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function b() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const d = Se(s);
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
        } = O(t);
        i = _, c(d), i.style.display = "contents", b(), (y = e.current) == null || y.appendChild(i);
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
      i.style.display = "contents", b(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ke(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Pe(t) {
  return X(() => ke(t), [t]);
}
const Le = Ie(({
  slots: t,
  afterClose: n,
  ...o
}) => {
  const s = Pe(n);
  return /* @__PURE__ */ h.jsx($, {
    ...o,
    afterClose: s,
    action: t.action ? /* @__PURE__ */ h.jsx(w, {
      slot: t.action
    }) : o.action,
    closable: t["closable.closeIcon"] ? {
      ...typeof o.closable == "object" ? o.closable : {},
      closeIcon: /* @__PURE__ */ h.jsx(w, {
        slot: t["closable.closeIcon"]
      })
    } : o.closable,
    description: t.description ? /* @__PURE__ */ h.jsx(w, {
      slot: t.description
    }) : o.description,
    icon: t.icon ? /* @__PURE__ */ h.jsx(w, {
      slot: t.icon
    }) : o.icon,
    message: t.message ? /* @__PURE__ */ h.jsx(w, {
      slot: t.message
    }) : o.message
  });
});
export {
  Le as Alert,
  Le as default
};
