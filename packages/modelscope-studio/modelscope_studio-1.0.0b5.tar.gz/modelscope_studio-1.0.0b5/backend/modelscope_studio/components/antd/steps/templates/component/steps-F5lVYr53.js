import { g as $, w as E } from "./Index-CWFL82Qw.js";
const h = window.ms_globals.React, F = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Steps;
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(t, n, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !le.hasOwnProperty(s) && (o[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: se.current
  };
}
C.Fragment = re;
C.jsx = W;
C.jsxs = W;
M.exports = C;
var g = M.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: j,
  check_outros: ie,
  children: z,
  claim_element: G,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: U,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: v,
  transition_out: R,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function N(t) {
  let n, r;
  const s = (
    /*#slots*/
    t[7].default
  ), o = de(
    s,
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
      var l = z(n);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      y(e, n, l), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
          s,
          /*$$scope*/
          e[6],
          l,
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
      R(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function Ce(t) {
  let n, r, s, o, e = (
    /*$$slots*/
    t[4].default && N(t)
  );
  return {
    c() {
      n = U("react-portal-target"), r = ge(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      n = G(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(w), r = ae(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, n, c), t[8](n), y(l, r, c), e && e.m(l, c), y(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = N(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (_e(), R(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      o || (v(e), o = !0);
    },
    o(l) {
      R(e), o = !1;
    },
    d(l) {
      l && (w(n), w(r), w(s)), t[8](null), e && e.d(l);
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
function Se(t, n, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const p = E(A(n)), d = E();
  P(t, d, (u) => r(0, s = u));
  const _ = E();
  P(t, _, (u) => r(1, o = u));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B
  } = $() || {}, V = i({
    parent: f,
    props: p,
    target: d,
    slot: _,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: B,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", V), be(() => {
    p.set(A(n));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function J(u) {
    j[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function Y(u) {
    j[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return t.$$set = (u) => {
    r(17, n = k(k({}, n), T(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, n = T(n), [s, o, d, _, c, i, l, e, J, Y];
}
class xe extends ce {
  constructor(n) {
    super(), me(this, n, Se, Ce, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(t) {
  function n(r) {
    const s = E(), o = new xe({
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
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, l], D({
            createPortal: x,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: x,
              node: S
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
function Ie(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Oe(t) {
  return F(() => Ie(t), [t]);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const s = t[r];
    return typeof s == "number" && !ke.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function I(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(x(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = I(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...e]
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
      } = I(e);
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
const O = K(({
  slot: t,
  clone: n,
  className: r,
  style: s
}, o) => {
  const e = Q(), [l, c] = X([]);
  return Z(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const f = je(s);
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
        } = I(t);
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
  }, [t, n, r, s, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function q(t, n) {
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
      i instanceof Element ? p = i : (p = i.el, d = i.callback, _ = i.clone ?? !1), o[c[c.length - 1]] = p ? d ? (...a) => (d(c[c.length - 1], a), /* @__PURE__ */ g.jsx(O, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ g.jsx(O, {
        slot: p,
        clone: _
      }) : o[c[c.length - 1]], o = s;
    });
    const e = "children";
    return r[e] && (s[e] = q(r[e])), s;
  });
}
function Le(t, n) {
  return t ? /* @__PURE__ */ g.jsx(O, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Te({
  key: t,
  setSlotParams: n,
  slots: r
}, s) {
  return r[t] ? (...o) => (n(t, o), Le(r[t], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ae = Re(({
  slots: t,
  items: n,
  slotItems: r,
  setSlotParams: s,
  children: o,
  progressDot: e,
  ...l
}) => {
  const c = Oe(e);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ g.jsx(ee, {
      ...l,
      items: F(() => n || q(r), [n, r]),
      progressDot: t.progressDot ? Te({
        slots: t,
        setSlotParams: s,
        key: "progressDot"
      }, {
        clone: !0
      }) : c || e
    })]
  });
});
export {
  Ae as Steps,
  Ae as default
};
