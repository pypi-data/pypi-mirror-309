import { g as ne, w as x, d as re, a as y } from "./Index-BMLAsQmM.js";
const g = window.ms_globals.React, I = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, O = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.ColorPicker;
var V = {
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
var se = g, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ie.call(n, l) && !ue.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: le,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
R.Fragment = ce;
R.jsx = q;
R.jsxs = q;
V.exports = R;
var b = V.exports;
const {
  SvelteComponent: de,
  assign: L,
  binding_callbacks: A,
  check_outros: fe,
  children: J,
  claim_element: Y,
  claim_space: pe,
  component_subscribe: F,
  compute_slots: _e,
  create_slot: he,
  detach: w,
  element: K,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: v,
  safe_not_equal: ye,
  set_custom_element_data: Q,
  space: Ee,
  transition_in: S,
  transition_out: P,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Se,
  onDestroy: Ie,
  setContext: Re
} = window.__gradio__svelte__internal;
function H(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = he(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = Y(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && xe(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function Ce(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && H(t)
  );
  return {
    c() {
      n = K("react-portal-target"), r = Ee(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      n = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(n).forEach(w), r = pe(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, n, c), t[8](n), v(s, r, c), e && e.m(s, c), v(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && S(e, 1)) : (e = H(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (be(), P(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (S(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function M(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function ke(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = _e(e);
  let {
    svelteInit: i
  } = n;
  const p = x(M(n)), u = x();
  F(t, u, (d) => r(0, l = d));
  const _ = x();
  F(t, _, (d) => r(1, o = d));
  const a = [], f = Se("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: C
  } = ne() || {}, E = i({
    parent: f,
    props: p,
    target: u,
    slot: _,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: C,
    onDestroy(d) {
      a.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", E), ve(() => {
    p.set(M(n));
  }), Ie(() => {
    a.forEach((d) => d());
  });
  function Z(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function $(d) {
    A[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return t.$$set = (d) => {
    r(17, n = L(L({}, n), D(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = D(n), [l, o, u, _, c, i, s, e, Z, $];
}
class Oe extends de {
  constructor(n) {
    super(), we(this, n, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, k = window.ms_globals.tree;
function Pe(t) {
  function n(r) {
    const l = x(), o = new Oe({
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
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, s], W({
            createPortal: O,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: O,
              node: k
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
function je(t) {
  const [n, r] = U(() => y(t));
  return B(() => {
    let l = !0;
    return t.subscribe((e) => {
      l && (l = !1, e === n) || r(e);
    });
  }, [t]), n;
}
function Te(t) {
  const n = I(() => re(t, (r) => r), [t]);
  return je(n);
}
function Le(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function z(t) {
  return I(() => Le(t), [t]);
}
function Ae(t, n) {
  const r = I(() => g.Children.toArray(t).filter((e) => e.props.node && (!e.props.nodeSlotKey || n)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = y(e.props.node.slotIndex) || 0, i = y(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Te(r);
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Fe.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function j(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(O(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
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
      } = j(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function De(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const T = ee(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = te(), [s, c] = U([]);
  return B(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), De(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Ne(l);
        Object.keys(f).forEach((h) => {
          a.style[h] = f[h];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var m;
        const {
          portals: f,
          clonedElement: h
        } = j(t);
        i = h, c(f), i.style.display = "contents", p(), (m = e.current) == null || m.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, h;
        (f = e.current) != null && f.contains(i) && ((h = e.current) == null || h.removeChild(i)), a();
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, n, r, l, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function X(t, n) {
  return t.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== c.length - 1 && (o = l[a]);
      });
      const i = r.slots[s];
      let p, u, _ = !1;
      i instanceof Element ? p = i : (p = i.el, u = i.callback, _ = i.clone ?? !1), o[c[c.length - 1]] = p ? u ? (...a) => (u(c[c.length - 1], a), /* @__PURE__ */ b.jsx(T, {
        slot: p,
        clone: _
      })) : /* @__PURE__ */ b.jsx(T, {
        slot: p,
        clone: _
      }) : o[c[c.length - 1]], o = l;
    });
    const e = "children";
    return r[e] && (l[e] = X(r[e])), l;
  });
}
function He(t, n) {
  return t ? /* @__PURE__ */ b.jsx(T, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function G({
  key: t,
  setSlotParams: n,
  slots: r
}, l) {
  return r[t] ? (...o) => (n(t, o), He(r[t], {
    clone: !0,
    ...l
  })) : void 0;
}
const We = Pe(({
  onValueChange: t,
  onChange: n,
  panelRender: r,
  showText: l,
  value: o,
  presets: e,
  presetItems: s,
  children: c,
  value_format: i,
  setSlotParams: p,
  slots: u,
  ..._
}) => {
  const a = z(r), f = z(l), h = Ae(c);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [h.length === 0 && /* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ b.jsx(oe, {
      ..._,
      value: o,
      presets: I(() => e || X(s), [e, s]),
      showText: u.showText ? G({
        slots: u,
        setSlotParams: p,
        key: "showText"
      }) : f || l,
      panelRender: u.panelRender ? G({
        slots: u,
        setSlotParams: p,
        key: "panelRender"
      }) : a,
      onChange: (m, ...C) => {
        const E = {
          rgb: m.toRgbString(),
          hex: m.toHexString(),
          hsb: m.toHsbString()
        };
        n == null || n(E[i], ...C), t(E[i]);
      },
      children: h.length === 0 ? null : c
    })]
  });
});
export {
  We as ColorPicker,
  We as default
};
