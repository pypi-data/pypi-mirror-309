import { g as le, w as I } from "./Index-f3_y8qCp.js";
const y = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, ce = window.ms_globals.antd.Select;
var B = {
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
var se = y, ie = Symbol.for("react.element"), ae = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, r) {
  var l, o = {}, n = null, c = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (c = t.ref);
  for (l in t) de.call(t, l) && !fe.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ie,
    type: e,
    key: n,
    ref: c,
    props: o,
    _owner: ue.current
  };
}
C.Fragment = ae;
C.jsx = V;
C.jsxs = V;
B.exports = C;
var g = B.exports;
const {
  SvelteComponent: _e,
  assign: A,
  binding_callbacks: D,
  check_outros: me,
  children: J,
  claim_element: Y,
  claim_space: pe,
  component_subscribe: M,
  compute_slots: he,
  create_slot: ge,
  detach: E,
  element: K,
  empty: W,
  exclude_internal_props: z,
  get_all_dirty_from_scope: we,
  get_slot_changes: be,
  group_outros: ye,
  init: Ee,
  insert_hydration: R,
  safe_not_equal: ve,
  set_custom_element_data: Q,
  space: Ie,
  transition_in: x,
  transition_out: T,
  update_slot_base: Re
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Se,
  setContext: ke
} = window.__gradio__svelte__internal;
function G(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = ge(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var c = J(t);
      o && o.l(c), c.forEach(E), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      R(n, t, c), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, c) {
      o && o.p && (!r || c & /*$$scope*/
      64) && Re(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? be(
          l,
          /*$$scope*/
          n[6],
          c,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (x(o, n), r = !0);
    },
    o(n) {
      T(o, n), r = !1;
    },
    d(n) {
      n && E(t), o && o.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = Ie(), n && n.c(), l = W(), this.h();
    },
    l(c) {
      t = Y(c, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(E), r = pe(c), n && n.l(c), l = W(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(c, s) {
      R(c, t, s), e[8](t), R(c, r, s), n && n.m(c, s), R(c, l, s), o = !0;
    },
    p(c, [s]) {
      /*$$slots*/
      c[4].default ? n ? (n.p(c, s), s & /*$$slots*/
      16 && x(n, 1)) : (n = G(c), n.c(), x(n, 1), n.m(l.parentNode, l)) : n && (ye(), T(n, 1, 1, () => {
        n = null;
      }), me());
    },
    i(c) {
      o || (x(n), o = !0);
    },
    o(c) {
      T(n), o = !1;
    },
    d(c) {
      c && (E(t), E(r), E(l)), e[8](null), n && n.d(c);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function je(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: c
  } = t;
  const s = he(n);
  let {
    svelteInit: i
  } = t;
  const m = I(U(t)), u = I();
  M(e, u, (d) => r(0, l = d));
  const p = I();
  M(e, p, (d) => r(1, o = d));
  const a = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: h,
    subSlotIndex: S
  } = le() || {}, k = i({
    parent: f,
    props: m,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: h,
    subSlotIndex: S,
    onDestroy(d) {
      a.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", k), xe(() => {
    m.set(U(t));
  }), Se(() => {
    a.forEach((d) => d());
  });
  function O(d) {
    D[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function j(d) {
    D[d ? "unshift" : "push"](() => {
      o = d, p.set(o);
    });
  }
  return e.$$set = (d) => {
    r(17, t = A(A({}, t), z(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, c = d.$$scope);
  }, t = z(t), [l, o, u, p, s, i, c, n, O, j];
}
class Fe extends _e {
  constructor(t) {
    super(), Ee(this, t, je, Oe, ve, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, F = window.ms_globals.tree;
function Pe(e) {
  function t(r) {
    const l = I(), o = new Fe({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, s = n.parent ?? F;
          return s.nodes = [...s.nodes, c], H({
            createPortal: P,
            node: F
          }), n.onDestroy(() => {
            s.nodes = s.nodes.filter((i) => i.svelteInstance !== l), H({
              createPortal: P,
              node: F
            });
          }), c;
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
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !Te.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((o) => {
        if (y.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: c
          } = L(o.props.el);
          return y.cloneElement(o, {
            ...o.props,
            el: c,
            children: [...y.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: c,
      type: s,
      useCapture: i
    }) => {
      r.addEventListener(s, c, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: c,
        portals: s
      } = L(n);
      t.push(...s), r.appendChild(c);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ne(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const w = te(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = ne(), [c, s] = re([]);
  return oe(() => {
    var p;
    if (!n.current || !e)
      return;
    let i = e;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ne(o, a), r && a.classList.add(...r.split(" ")), l) {
        const f = Le(l);
        Object.keys(f).forEach((_) => {
          a.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var h;
        const {
          portals: f,
          clonedElement: _
        } = L(e);
        i = _, s(f), i.style.display = "contents", m(), (h = n.current) == null || h.appendChild(i);
      };
      a(), u = new window.MutationObserver(() => {
        var f, _;
        (f = n.current) != null && f.contains(i) && ((_ = n.current) == null || _.removeChild(i)), a();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (p = n.current) == null || p.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((f = n.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, r, l, o]), y.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...c);
});
function Ae(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function b(e) {
  return q(() => Ae(e), [e]);
}
function X(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((c) => {
      if (!r.slots[c] || !(r.slots[c] instanceof Element) && !r.slots[c].el)
        return;
      const s = c.split(".");
      s.forEach((a, f) => {
        o[a] || (o[a] = {}), f !== s.length - 1 && (o = l[a]);
      });
      const i = r.slots[c];
      let m, u, p = (t == null ? void 0 : t.clone) ?? !1;
      i instanceof Element ? m = i : (m = i.el, u = i.callback, p = i.clone ?? !1), o[s[s.length - 1]] = m ? u ? (...a) => (u(s[s.length - 1], a), /* @__PURE__ */ g.jsx(w, {
        slot: m,
        clone: p
      })) : /* @__PURE__ */ g.jsx(w, {
        slot: m,
        clone: p
      }) : o[s[s.length - 1]], o = l;
    });
    const n = (t == null ? void 0 : t.children) || "children";
    return r[n] && (l[n] = X(r[n], t)), l;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(w, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function v({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), De(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const We = Pe(({
  slots: e,
  children: t,
  onValueChange: r,
  filterOption: l,
  onChange: o,
  options: n,
  optionItems: c,
  getPopupContainer: s,
  dropdownRender: i,
  optionRender: m,
  tagRender: u,
  labelRender: p,
  filterSort: a,
  elRef: f,
  setSlotParams: _,
  ...h
}) => {
  const S = b(s), k = b(l), O = b(i), j = b(a), d = b(m), Z = b(u), $ = b(p);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(ce, {
      ...h,
      ref: f,
      options: q(() => n || X(c, {
        children: "options",
        clone: !0
      }), [c, n]),
      onChange: (N, ...ee) => {
        o == null || o(N, ...ee), r(N);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ g.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : h.allowClear,
      removeIcon: e.removeIcon ? /* @__PURE__ */ g.jsx(w, {
        slot: e.removeIcon
      }) : h.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(w, {
        slot: e.suffixIcon
      }) : h.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(w, {
        slot: e.notFoundContent
      }) : h.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ g.jsx(w, {
        slot: e.menuItemSelectedIcon
      }) : h.menuItemSelectedIcon,
      filterOption: k || l,
      maxTagPlaceholder: e.maxTagPlaceholder ? v({
        slots: e,
        setSlotParams: _,
        key: "maxTagPlaceholder"
      }) : h.maxTagPlaceholder,
      getPopupContainer: S,
      dropdownRender: e.dropdownRender ? v({
        slots: e,
        setSlotParams: _,
        key: "dropdownRender"
      }) : O,
      optionRender: e.optionRender ? v({
        slots: e,
        setSlotParams: _,
        key: "optionRender"
      }) : d,
      tagRender: e.tagRender ? v({
        slots: e,
        setSlotParams: _,
        key: "tagRender"
      }) : Z,
      labelRender: e.labelRender ? v({
        slots: e,
        setSlotParams: _,
        key: "labelRender"
      }) : $,
      filterSort: j
    })]
  });
});
export {
  We as Select,
  We as default
};
