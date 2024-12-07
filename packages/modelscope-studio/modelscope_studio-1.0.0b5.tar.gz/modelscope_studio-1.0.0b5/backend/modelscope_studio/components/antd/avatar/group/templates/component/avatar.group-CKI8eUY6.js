import { g as $, w as x, d as ee, a as w } from "./Index-BrSm6UgU.js";
const h = window.ms_globals.React, F = window.ms_globals.React.useMemo, M = window.ms_globals.React.useState, W = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, R = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Avatar;
var z = {
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
var ne = h, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ie.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
I.Fragment = re;
I.jsx = U;
I.jsxs = U;
z.exports = I;
var g = z.exports;
const {
  SvelteComponent: ae,
  assign: P,
  binding_callbacks: A,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: de,
  component_subscribe: j,
  compute_slots: ue,
  create_slot: pe,
  detach: v,
  element: V,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: y,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: ve,
  transition_in: E,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: xe,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function N(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = pe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      y(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
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
      o || (E(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && v(t), r && r.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = V("react-portal-target"), o = ve(), e && e.c(), l = L(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(v), o = de(s), e && e.l(s), l = L(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      y(s, t, a), n[8](t), y(s, o, a), e && e.m(s, a), y(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && E(e, 1)) : (e = N(s), e.c(), E(e, 1), e.m(l.parentNode, l)) : e && (me(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (E(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (v(t), v(o), v(l)), n[8](null), e && e.d(s);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ue(e);
  let {
    svelteInit: i
  } = t;
  const m = x(D(t)), u = x();
  j(n, u, (c) => o(0, l = c));
  const f = x();
  j(n, f, (c) => o(1, r = c));
  const d = [], p = xe("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: B
  } = $() || {}, J = i({
    parent: p,
    props: m,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: B,
    onDestroy(c) {
      d.push(c);
    }
  });
  Ee("$$ms-gr-react-wrapper", J), be(() => {
    m.set(D(t));
  }), ye(() => {
    d.forEach((c) => c());
  });
  function Y(c) {
    A[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function Q(c) {
    A[c ? "unshift" : "push"](() => {
      r = c, f.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = P(P({}, t), T(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = T(t), [l, r, u, f, a, i, s, e, Y, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const l = x(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? S;
          return a.nodes = [...a.nodes, s], G({
            createPortal: R,
            node: S
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), G({
              createPortal: R,
              node: S
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = M(() => w(n));
  return W(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function ke(n) {
  const t = F(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Pe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = k(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const C = X(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Z(), [s, a] = M([]);
  return W(() => {
    var f;
    if (!e.current || !n)
      return;
    let i = n;
    function m() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), je(r, d), o && d.classList.add(...o.split(" ")), l) {
        const p = Ae(l);
        Object.keys(p).forEach((_) => {
          d.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b;
        const {
          portals: p,
          clonedElement: _
        } = k(n);
        i = _, a(p), i.style.display = "contents", m(), (b = e.current) == null || b.appendChild(i);
      };
      d(), u = new window.MutationObserver(() => {
        var p, _;
        (p = e.current) != null && p.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (f = e.current) == null || f.appendChild(i);
    return () => {
      var d, p;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n, t) {
  const o = F(() => h.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = w(e.props.node.slotIndex) || 0, i = w(s.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(s.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return ke(o);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...o
}) => {
  var r, e, s, a, i, m;
  const l = Le(t);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(te.Group, {
      ...o,
      max: {
        ...o.max,
        popover: n["max.popover.title"] || n["max.popover.content"] ? {
          ...((e = o.max) == null ? void 0 : e.popover) || {},
          title: n["max.popover.title"] ? /* @__PURE__ */ g.jsx(C, {
            slot: n["max.popover.title"]
          }) : (a = (s = o.max) == null ? void 0 : s.popover) == null ? void 0 : a.title,
          content: n["max.popover.content"] ? /* @__PURE__ */ g.jsx(C, {
            slot: n["max.popover.content"]
          }) : (m = (i = o.max) == null ? void 0 : i.popover) == null ? void 0 : m.content
        } : (r = o.max) == null ? void 0 : r.popover
      },
      children: l.map((u, f) => /* @__PURE__ */ g.jsx(C, {
        slot: u
      }, f))
    })]
  });
});
export {
  Ne as AvatarGroup,
  Ne as default
};
