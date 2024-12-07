import { g as ee, w as E, d as te, a as y } from "./Index-fO-yzN9g.js";
const _ = window.ms_globals.React, M = window.ms_globals.React.useMemo, W = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, Z = window.ms_globals.React.forwardRef, $ = window.ms_globals.React.useRef, R = window.ms_globals.ReactDOM.createPortal, P = window.ms_globals.antd.Card;
var F = {
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
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: le.current
  };
}
I.Fragment = oe;
I.jsx = U;
I.jsxs = U;
F.exports = I;
var h = F.exports;
const {
  SvelteComponent: ae,
  assign: j,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: de,
  component_subscribe: T,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: V,
  empty: A,
  exclude_internal_props: N,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: v,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: be,
  transition_in: C,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: xe,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function B(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = fe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(o, e), r = !0);
    },
    o(e) {
      O(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && B(n)
  );
  return {
    c() {
      t = V("react-portal-target"), r = be(), e && e.c(), s = A(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(g), r = de(l), e && e.l(l), s = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      v(l, t, a), n[8](t), v(l, r, a), e && e.m(l, a), v(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = B(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (me(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (C(e), o = !0);
    },
    o(l) {
      O(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ie(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = ue(e);
  let {
    svelteInit: i
  } = t;
  const b = E(D(t)), f = E();
  T(n, f, (c) => r(0, s = c));
  const m = E();
  T(n, m, (c) => r(1, o = c));
  const d = [], u = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: J
  } = ee() || {}, Y = i({
    parent: u,
    props: b,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: J,
    onDestroy(c) {
      d.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", Y), ye(() => {
    b.set(D(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function Q(c) {
    L[c ? "unshift" : "push"](() => {
      s = c, f.set(s);
    });
  }
  function X(c) {
    L[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = j(j({}, t), N(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = N(t), [s, o, f, m, a, i, l, e, Q, X];
}
class Se extends ae {
  constructor(t) {
    super(), he(this, t, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const s = E(), o = new Se({
      ...r,
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
          }, a = e.parent ?? S;
          return a.nodes = [...a.nodes, l], G({
            createPortal: R,
            node: S
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), G({
              createPortal: R,
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
      r(t);
    });
  });
}
function Oe(n) {
  const [t, r] = W(() => y(n));
  return z(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function ke(n) {
  const t = M(() => te(n, (r) => r), [n]);
  return Oe(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Pe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function k(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(R(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((o) => {
        if (_.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = k(o.props.el);
          return _.cloneElement(o, {
            ...o.props,
            el: l,
            children: [..._.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = k(e);
      t.push(...a), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const w = Z(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = $(), [l, a] = W([]);
  return z(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function b() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Le(o, d), r && d.classList.add(...r.split(" ")), s) {
        const u = je(s);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var x;
        const {
          portals: u,
          clonedElement: p
        } = k(n);
        i = p, a(u), i.style.display = "contents", b(), (x = e.current) == null || x.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, p;
        (u = e.current) != null && u.contains(i) && ((p = e.current) == null || p.removeChild(i)), d();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", b(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, s, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Te(n, t) {
  const r = M(() => _.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = y(e.props.node.slotIndex) || 0, i = y(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return ke(r);
}
const Ne = Re(({
  children: n,
  containsGrid: t,
  slots: r,
  ...s
}) => {
  const o = Te(n, "actions");
  return /* @__PURE__ */ h.jsxs(P, {
    ...s,
    title: r.title ? /* @__PURE__ */ h.jsx(w, {
      slot: r.title
    }) : s.title,
    extra: r.extra ? /* @__PURE__ */ h.jsx(w, {
      slot: r.extra
    }) : s.extra,
    cover: r.cover ? /* @__PURE__ */ h.jsx(w, {
      slot: r.cover
    }) : s.cover,
    tabBarExtraContent: r.tabBarExtraContent ? /* @__PURE__ */ h.jsx(w, {
      slot: r.tabBarExtraContent
    }) : s.tabBarExtraContent,
    actions: o.length > 0 ? o.map((e, l) => /* @__PURE__ */ h.jsx(w, {
      slot: e
    }, l)) : s.actions,
    children: [t ? /* @__PURE__ */ h.jsx(P.Grid, {
      style: {
        display: "none"
      }
    }) : null, n]
  });
});
export {
  Ne as Card,
  Ne as default
};
