import { g as X, w as b } from "./Index-DGfR5xQg.js";
const m = window.ms_globals.React, q = window.ms_globals.React.useMemo, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, C = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.QRCode;
var A = {
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
v.Fragment = te;
v.jsx = F;
v.jsxs = F;
A.exports = v;
var D = A.exports;
const {
  SvelteComponent: se,
  assign: I,
  binding_callbacks: O,
  check_outros: le,
  children: M,
  claim_element: W,
  claim_space: ie,
  component_subscribe: k,
  compute_slots: ce,
  create_slot: ae,
  detach: h,
  element: z,
  empty: P,
  exclude_internal_props: L,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert_hydration: y,
  safe_not_equal: pe,
  set_custom_element_data: G,
  space: me,
  transition_in: E,
  transition_out: S,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function T(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = z("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = M(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && he(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (E(r, e), o = !0);
    },
    o(e) {
      S(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && T(n)
  );
  return {
    c() {
      t = z("react-portal-target"), o = me(), e && e.c(), s = P(), this.h();
    },
    l(l) {
      t = W(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(t).forEach(h), o = ie(l), e && e.l(l), s = P(), this.h();
    },
    h() {
      G(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, t, c), n[8](t), y(l, o, c), e && e.m(l, c), y(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && E(e, 1)) : (e = T(l), e.c(), E(e, 1), e.m(s.parentNode, s)) : e && (fe(), S(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      r || (E(e), r = !0);
    },
    o(l) {
      S(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function N(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = b(N(t)), f = b();
  k(n, f, (a) => o(0, s = a));
  const p = b();
  k(n, p, (a) => o(1, r = a));
  const u = [], d = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: U
  } = X() || {}, H = i({
    parent: d,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: U,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", H), ge(() => {
    g.set(N(t));
  }), be(() => {
    u.forEach((a) => a());
  });
  function K(a) {
    O[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function Q(a) {
    O[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = I(I({}, t), L(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = L(t), [s, r, f, p, c, i, l, e, K, Q];
}
class Re extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, R = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const s = b(), r = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, l], j({
            createPortal: C,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), j({
              createPortal: C,
              node: R
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
      o(t);
    });
  });
}
function Se(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function xe(n) {
  return q(() => Se(n), [n]);
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Ie.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function x(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(C(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = x(r.props.el);
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
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = x(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Pe = V(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = B(), [l, c] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(r, u), o && u.classList.add(...o.split(" ")), s) {
        const d = Oe(s);
        Object.keys(d).forEach((_) => {
          u.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w;
        const {
          portals: d,
          clonedElement: _
        } = x(n);
        i = _, c(d), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, _;
        (d = e.current) != null && d.contains(i) && ((_ = e.current) == null || _.removeChild(i)), u();
      }), f.observe(n, {
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
  }, [n, t, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n, t) {
  return n ? /* @__PURE__ */ D.jsx(Pe, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: t,
  slots: o
}, s) {
  return o[n] ? (...r) => (t(n, r), Le(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const je = Ce(({
  setSlotParams: n,
  slots: t,
  statusRender: o,
  ...s
}) => {
  const r = xe(o);
  return /* @__PURE__ */ D.jsx(Z, {
    ...s,
    statusRender: t.statusRender ? Te({
      slots: t,
      setSlotParams: n,
      key: "statusRender"
    }) : r
  });
});
export {
  je as QRCode,
  je as default
};
