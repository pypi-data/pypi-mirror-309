import { g as ee, w as v } from "./Index-DvDenV5g.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Modal;
var D = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = b, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) le.call(n, l) && !ce.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: oe,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: se.current
  };
}
I.Fragment = re;
I.jsx = W;
I.jsxs = W;
D.exports = I;
var p = D.exports;
const {
  SvelteComponent: ie,
  assign: O,
  binding_callbacks: T,
  check_outros: ae,
  children: z,
  claim_element: G,
  claim_space: ue,
  component_subscribe: j,
  compute_slots: de,
  create_slot: fe,
  detach: w,
  element: U,
  empty: L,
  exclude_internal_props: B,
  get_all_dirty_from_scope: _e,
  get_slot_changes: me,
  group_outros: pe,
  init: he,
  insert_hydration: x,
  safe_not_equal: ge,
  set_custom_element_data: H,
  space: be,
  transition_in: C,
  transition_out: P,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = U("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = G(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      x(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? me(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(o, t), r = !0);
    },
    o(t) {
      P(o, t), r = !1;
    },
    d(t) {
      t && w(n), o && o.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && F(e)
  );
  return {
    c() {
      n = U("react-portal-target"), r = be(), t && t.c(), l = L(), this.h();
    },
    l(s) {
      n = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(w), r = ue(s), t && t.l(s), l = L(), this.h();
    },
    h() {
      H(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, n, c), e[8](n), x(s, r, c), t && t.m(s, c), x(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = F(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (pe(), P(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      P(t), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), e[8](null), t && t.d(s);
    }
  };
}
function N(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ie(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = de(t);
  let {
    svelteInit: i
  } = n;
  const g = v(N(n)), f = v();
  j(e, f, (u) => r(0, l = u));
  const _ = v();
  j(e, _, (u) => r(1, o = u));
  const a = [], d = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: y,
    subSlotIndex: K
  } = ee() || {}, q = i({
    parent: d,
    props: g,
    target: f,
    slot: _,
    slotKey: m,
    slotIndex: y,
    subSlotIndex: K,
    onDestroy(u) {
      a.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", q), ye(() => {
    g.set(N(n));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function V(u) {
    T[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = O(O({}, n), B(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = B(n), [l, o, f, _, c, i, s, t, V, J];
}
class Re extends ie {
  constructor(n) {
    super(), he(this, n, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, R = window.ms_globals.tree;
function ke(e) {
  function n(r) {
    const l = v(), o = new Re({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? R;
          return c.nodes = [...c.nodes, s], A({
            createPortal: k,
            node: R
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), A({
              createPortal: k,
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Pe.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function S(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: b.Children.toArray(e._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = S(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...b.Children.toArray(o.props.children), ...t]
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = S(t);
      n.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Oe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const h = Y(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var _;
    if (!t.current || !e)
      return;
    let i = e;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const d = Se(l);
        Object.keys(d).forEach((m) => {
          a.style[m] = d[m];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y;
        const {
          portals: d,
          clonedElement: m
        } = S(e);
        i = m, c(d), i.style.display = "contents", g(), (y = t.current) == null || y.appendChild(i);
      };
      a(), f = new window.MutationObserver(() => {
        var d, m;
        (d = t.current) != null && d.contains(i) && ((m = t.current) == null || m.removeChild(i)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var a, d;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((d = t.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, n, r, l, o]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Te(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return $(() => Te(e), [e]);
}
function je(e, n) {
  return e ? /* @__PURE__ */ p.jsx(h, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return r[e] ? (...o) => (n(e, o), je(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Be = ke(({
  slots: e,
  afterClose: n,
  afterOpenChange: r,
  getContainer: l,
  children: o,
  modalRender: t,
  setSlotParams: s,
  ...c
}) => {
  var a, d;
  const i = E(r), g = E(n), f = E(l), _ = E(t);
  return /* @__PURE__ */ p.jsx(te, {
    ...c,
    afterOpenChange: i,
    afterClose: g,
    okText: e.okText ? /* @__PURE__ */ p.jsx(h, {
      slot: e.okText
    }) : c.okText,
    okButtonProps: {
      ...c.okButtonProps || {},
      icon: e["okButtonProps.icon"] ? /* @__PURE__ */ p.jsx(h, {
        slot: e["okButtonProps.icon"]
      }) : (a = c.okButtonProps) == null ? void 0 : a.icon
    },
    cancelText: e.cancelText ? /* @__PURE__ */ p.jsx(h, {
      slot: e.cancelText
    }) : c.cancelText,
    cancelButtonProps: {
      ...c.cancelButtonProps || {},
      icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ p.jsx(h, {
        slot: e["cancelButtonProps.icon"]
      }) : (d = c.cancelButtonProps) == null ? void 0 : d.icon
    },
    closable: e["closable.closeIcon"] ? {
      ...typeof c.closable == "object" ? c.closable : {},
      closeIcon: /* @__PURE__ */ p.jsx(h, {
        slot: e["closable.closeIcon"]
      })
    } : c.closable,
    closeIcon: e.closeIcon ? /* @__PURE__ */ p.jsx(h, {
      slot: e.closeIcon
    }) : c.closeIcon,
    footer: e.footer ? M({
      slots: e,
      setSlotParams: s,
      key: "footer"
    }) : c.footer,
    title: e.title ? /* @__PURE__ */ p.jsx(h, {
      slot: e.title
    }) : c.title,
    modalRender: e.modalRender ? M({
      slots: e,
      setSlotParams: s,
      key: "modalRender"
    }) : _,
    getContainer: typeof l == "string" ? f : l,
    children: o
  });
});
export {
  Be as Modal,
  Be as default
};
