import { g as oe, w as v } from "./Index-CICwyCeX.js";
const E = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, re = window.ms_globals.internalContext.FormItemContext, le = window.ms_globals.antd.Form;
var q = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = E, ie = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(e, n, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) ae.call(n, s) && !de.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: ie,
    type: e,
    key: t,
    ref: l,
    props: o,
    _owner: ue.current
  };
}
R.Fragment = ce;
R.jsx = B;
R.jsxs = B;
q.exports = R;
var m = q.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: N,
  check_outros: pe,
  children: J,
  claim_element: Y,
  claim_space: _e,
  component_subscribe: z,
  compute_slots: me,
  create_slot: he,
  detach: C,
  element: K,
  empty: D,
  exclude_internal_props: V,
  get_all_dirty_from_scope: ge,
  get_slot_changes: be,
  group_outros: we,
  init: Ee,
  insert_hydration: I,
  safe_not_equal: ye,
  set_custom_element_data: Q,
  space: Ce,
  transition_in: O,
  transition_out: P,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ie,
  onDestroy: Oe,
  setContext: Re
} = window.__gradio__svelte__internal;
function W(e) {
  let n, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = he(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = K("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = Y(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(n);
      o && o.l(l), l.forEach(C), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      I(t, n, l), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && xe(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? be(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : ge(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (O(o, t), r = !0);
    },
    o(t) {
      P(o, t), r = !1;
    },
    d(t) {
      t && C(n), o && o.d(t), e[9](null);
    }
  };
}
function je(e) {
  let n, r, s, o, t = (
    /*$$slots*/
    e[4].default && W(e)
  );
  return {
    c() {
      n = K("react-portal-target"), r = Ce(), t && t.c(), s = D(), this.h();
    },
    l(l) {
      n = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(n).forEach(C), r = _e(l), t && t.l(l), s = D(), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      I(l, n, i), e[8](n), I(l, r, i), t && t.m(l, i), I(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && O(t, 1)) : (t = W(l), t.c(), O(t, 1), t.m(s.parentNode, s)) : t && (we(), P(t, 1, 1, () => {
        t = null;
      }), pe());
    },
    i(l) {
      o || (O(t), o = !0);
    },
    o(l) {
      P(t), o = !1;
    },
    d(l) {
      l && (C(n), C(r), C(s)), e[8](null), t && t.d(l);
    }
  };
}
function G(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Fe(e, n, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const i = me(t);
  let {
    svelteInit: c
  } = n;
  const p = v(G(n)), d = v();
  z(e, d, (u) => r(0, s = u));
  const _ = v();
  z(e, _, (u) => r(1, o = u));
  const a = [], f = Ie("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: y,
    subSlotIndex: j
  } = oe() || {}, F = c({
    parent: f,
    props: p,
    target: d,
    slot: _,
    slotKey: h,
    slotIndex: y,
    subSlotIndex: j,
    onDestroy(u) {
      a.push(u);
    }
  });
  Re("$$ms-gr-react-wrapper", F), ve(() => {
    p.set(G(n));
  }), Oe(() => {
    a.forEach((u) => u());
  });
  function x(u) {
    N[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function b(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = A(A({}, n), V(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, n = V(n), [s, o, d, _, i, c, l, t, x, b];
}
class Se extends fe {
  constructor(n) {
    super(), Ee(this, n, Fe, je, ye, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, S = window.ms_globals.tree;
function ke(e) {
  function n(r) {
    const s = v(), o = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? S;
          return i.nodes = [...i.nodes, l], M({
            createPortal: k,
            node: S
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), M({
              createPortal: k,
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const s = e[r];
    return typeof s == "number" && !Pe.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function L(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...E.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(t);
      n.push(...i), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Te(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = $(({
  slot: e,
  clone: n,
  className: r,
  style: s
}, o) => {
  const t = ee(), [l, i] = te([]);
  return ne(() => {
    var _;
    if (!t.current || !e)
      return;
    let c = e;
    function p() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Te(o, a), r && a.classList.add(...r.split(" ")), s) {
        const f = Le(s);
        Object.keys(f).forEach((h) => {
          a.style[h] = f[h];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: f,
          clonedElement: h
        } = L(e);
        c = h, i(f), c.style.display = "contents", p(), (y = t.current) == null || y.appendChild(c);
      };
      a(), d = new window.MutationObserver(() => {
        var f, h;
        (f = t.current) != null && f.contains(c) && ((h = t.current) == null || h.removeChild(c)), a();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", p(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((f = t.current) == null || f.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, n, r, s, o]), E.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(e) {
  return T(() => Ae(e), [e]);
}
function X(e, n) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let o = s;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== i.length - 1 && (o = s[a]);
      });
      const c = r.slots[l];
      let p, d, _ = !1;
      c instanceof Element ? p = c : (p = c.el, d = c.callback, _ = c.clone ?? !1), o[i[i.length - 1]] = p ? d ? (...a) => (d(i[i.length - 1], a), /* @__PURE__ */ m.jsx(g, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ m.jsx(g, {
        slot: p,
        clone: _
      }) : o[i[i.length - 1]], o = s;
    });
    const t = "children";
    return r[t] && (s[t] = X(r[t])), s;
  });
}
function H(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const U = ({
  children: e,
  ...n
}) => /* @__PURE__ */ m.jsx(re.Provider, {
  value: T(() => n, [n]),
  children: e
}), ze = ke(({
  slots: e,
  getValueFromEvent: n,
  getValueProps: r,
  normalize: s,
  shouldUpdate: o,
  tooltip: t,
  ruleItems: l,
  rules: i,
  children: c,
  hasFeedback: p,
  ...d
}) => {
  const _ = e["tooltip.icon"] || e["tooltip.title"] || typeof t == "object", a = typeof p == "object", f = H(p), h = w(f.icons), y = w(n), j = w(r), F = w(s), x = w(o), b = H(t), u = w(b.afterOpenChange), Z = w(b.getPopupContainer);
  return /* @__PURE__ */ m.jsx(le.Item, {
    ...d,
    hasFeedback: a ? {
      ...f,
      icons: h || f.icons
    } : p,
    getValueFromEvent: y,
    getValueProps: j,
    normalize: F,
    shouldUpdate: x || o,
    rules: T(() => i || X(l), [l, i]),
    tooltip: e.tooltip ? /* @__PURE__ */ m.jsx(g, {
      slot: e.tooltip
    }) : _ ? {
      ...b,
      afterOpenChange: u,
      getPopupContainer: Z,
      icon: e["tooltip.icon"] ? /* @__PURE__ */ m.jsx(g, {
        slot: e["tooltip.icon"]
      }) : b.icon,
      title: e["tooltip.title"] ? /* @__PURE__ */ m.jsx(g, {
        slot: e["tooltip.title"]
      }) : b.title
    } : t,
    extra: e.extra ? /* @__PURE__ */ m.jsx(g, {
      slot: e.extra
    }) : d.extra,
    help: e.help ? /* @__PURE__ */ m.jsx(g, {
      slot: e.help
    }) : d.help,
    label: e.label ? /* @__PURE__ */ m.jsx(g, {
      slot: e.label
    }) : d.label,
    children: x || o ? () => /* @__PURE__ */ m.jsx(U, {
      children: c
    }) : /* @__PURE__ */ m.jsx(U, {
      children: c
    })
  });
});
export {
  ze as FormItem,
  ze as default
};
