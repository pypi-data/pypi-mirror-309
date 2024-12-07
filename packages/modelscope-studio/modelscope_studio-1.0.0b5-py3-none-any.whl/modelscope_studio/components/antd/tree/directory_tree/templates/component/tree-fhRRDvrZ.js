import { g as re, w as C } from "./Index-AhEc-1c4.js";
const p = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, B = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, F = window.ms_globals.antd.Tree;
var V = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = p, le = Symbol.for("react.element"), se = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(e, t, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ce.call(t, l) && !ae.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: le,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: ie.current
  };
}
L.Fragment = se;
L.jsx = J;
L.jsxs = J;
V.exports = L;
var g = V.exports;
const {
  SvelteComponent: ue,
  assign: A,
  binding_callbacks: M,
  check_outros: de,
  children: Y,
  claim_element: K,
  claim_space: fe,
  component_subscribe: U,
  compute_slots: _e,
  create_slot: he,
  detach: b,
  element: Q,
  empty: W,
  exclude_internal_props: z,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: we,
  init: pe,
  insert_hydration: x,
  safe_not_equal: be,
  set_custom_element_data: X,
  space: ye,
  transition_in: O,
  transition_out: N,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: Ie,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function G(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = he(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(t);
      o && o.l(s), s.forEach(b), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      x(n, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ve(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? ge(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (O(o, n), r = !0);
    },
    o(n) {
      N(o, n), r = !1;
    },
    d(n) {
      n && b(t), o && o.d(n), e[9](null);
    }
  };
}
function xe(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = Q("react-portal-target"), r = ye(), n && n.c(), l = W(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(t).forEach(b), r = fe(s), n && n.l(s), l = W(), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, t, c), e[8](t), x(s, r, c), n && n.m(s, c), x(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && O(n, 1)) : (n = G(s), n.c(), O(n, 1), n.m(l.parentNode, l)) : n && (we(), N(n, 1, 1, () => {
        n = null;
      }), de());
    },
    i(s) {
      o || (O(n), o = !0);
    },
    o(s) {
      N(n), o = !1;
    },
    d(s) {
      s && (b(t), b(r), b(l)), e[8](null), n && n.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Oe(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = _e(n);
  let {
    svelteInit: i
  } = t;
  const h = C(H(t)), f = C();
  U(e, f, (u) => r(0, l = u));
  const _ = C();
  U(e, _, (u) => r(1, o = u));
  const a = [], d = Ie("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: y
  } = re() || {}, j = i({
    parent: d,
    props: h,
    target: f,
    slot: _,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", j), Ee(() => {
    h.set(H(t));
  }), Re(() => {
    a.forEach((u) => u());
  });
  function k(u) {
    M[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function S(u) {
    M[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, t = A(A({}, t), z(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = z(t), [l, o, f, _, c, i, s, n, k, S];
}
class Le extends ue {
  constructor(t) {
    super(), pe(this, t, Oe, xe, be, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, T = window.ms_globals.tree;
function je(e) {
  function t(r) {
    const l = C(), o = new Le({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, c = n.parent ?? T;
          return c.nodes = [...c.nodes, s], q({
            createPortal: P,
            node: T
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), q({
              createPortal: P,
              node: T
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
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !ke.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: p.Children.toArray(e._reactElement.props.children).map((o) => {
        if (p.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(o.props.el);
          return p.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...p.Children.toArray(o.props.children), ...n]
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = D(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Te(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const E = $(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = ee(), [s, c] = te([]);
  return ne(() => {
    var _;
    if (!n.current || !e)
      return;
    let i = e;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Te(o, a), r && a.classList.add(...r.split(" ")), l) {
        const d = Se(l);
        Object.keys(d).forEach((m) => {
          a.style[m] = d[m];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var w;
        const {
          portals: d,
          clonedElement: m
        } = D(e);
        i = m, c(d), i.style.display = "contents", h(), (w = n.current) == null || w.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var d, m;
        (d = n.current) != null && d.contains(i) && ((m = n.current) == null || m.removeChild(i)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (_ = n.current) == null || _.appendChild(i);
    return () => {
      var a, d;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((d = n.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, t, r, l, o]), p.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Pe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(e) {
  return B(() => Pe(e), [e]);
}
function Ne(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function Z(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return t != null && t.fallback ? t.fallback(r) : r;
    const l = {
      ...r.props
    };
    let o = l;
    Object.keys(r.slots).forEach((s) => {
      if (!r.slots[s] || !(r.slots[s] instanceof Element) && !r.slots[s].el)
        return;
      const c = s.split(".");
      c.forEach((a, d) => {
        o[a] || (o[a] = {}), d !== c.length - 1 && (o = l[a]);
      });
      const i = r.slots[s];
      let h, f, _ = (t == null ? void 0 : t.clone) ?? !1;
      i instanceof Element ? h = i : (h = i.el, f = i.callback, _ = i.clone ?? !1), o[c[c.length - 1]] = h ? f ? (...a) => (f(c[c.length - 1], a), /* @__PURE__ */ g.jsx(E, {
        slot: h,
        clone: _
      })) : /* @__PURE__ */ g.jsx(E, {
        slot: h,
        clone: _
      }) : o[c[c.length - 1]], o = l;
    });
    const n = (t == null ? void 0 : t.children) || "children";
    return r[n] && (l[n] = Z(r[n], t)), l;
  });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(E, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function R({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), De(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = je(({
  slots: e,
  filterTreeNode: t,
  treeData: r,
  draggable: l,
  allowDrop: o,
  onCheck: n,
  onSelect: s,
  onExpand: c,
  children: i,
  directory: h,
  slotItems: f,
  setSlotParams: _,
  onLoadData: a,
  ...d
}) => {
  const m = I(t), w = I(l), y = I(typeof l == "object" ? l.nodeDraggable : void 0), j = I(o), k = h ? F.DirectoryTree : F, S = B(() => ({
    ...d,
    treeData: r || Z(f, {
      clone: !0
    }),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: R({
        slots: e,
        setSlotParams: _,
        key: "showLine.showLeafIcon"
      })
    } : d.showLine,
    icon: e.icon ? R({
      slots: e,
      setSlotParams: _,
      key: "icon"
    }) : d.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ g.jsx(E, {
      slot: e.switcherLoadingIcon
    }) : d.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? R({
      slots: e,
      setSlotParams: _,
      key: "switcherIcon"
    }) : d.switcherIcon,
    titleRender: e.titleRender ? R({
      slots: e,
      setSlotParams: _,
      key: "titleRender"
    }) : d.titleRender,
    draggable: e["draggable.icon"] || y ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ g.jsx(E, {
        slot: e["draggable.icon"]
      }) : typeof l == "object" ? l.icon : void 0,
      nodeDraggable: y
    } : w || l,
    loadData: a
  }), [d, r, f, e, _, y, l, w, a]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ g.jsx(k, {
      ...Ne(S),
      filterTreeNode: m,
      allowDrop: j,
      onSelect: (u, ...v) => {
        s == null || s(u, ...v);
      },
      onExpand: (u, ...v) => {
        c == null || c(u, ...v);
      },
      onCheck: (u, ...v) => {
        n == null || n(u, ...v);
      }
    })]
  });
});
export {
  Ae as Tree,
  Ae as default
};
