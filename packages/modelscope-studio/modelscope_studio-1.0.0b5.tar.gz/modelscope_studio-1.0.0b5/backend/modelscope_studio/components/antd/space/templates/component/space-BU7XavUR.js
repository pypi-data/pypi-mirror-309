import { g as $, w as E, d as ee, a as b } from "./Index-DiPBwryR.js";
const _ = window.ms_globals.React, M = window.ms_globals.React.useMemo, W = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, C = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Space;
var G = {
  exports: {}
}, S = {};
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
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ie.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
S.Fragment = oe;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var h = G.exports;
const {
  SvelteComponent: ae,
  assign: k,
  binding_callbacks: P,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: de,
  component_subscribe: L,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: V,
  empty: T,
  exclude_internal_props: j,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: v,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: we,
  transition_in: x,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function A(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = fe(
    l,
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
      var s = H(t);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && be(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (x(o, e), r = !0);
    },
    o(e) {
      R(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      t = V("react-portal-target"), r = we(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(g), r = de(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      v(s, t, a), n[8](t), v(s, r, a), e && e.m(s, a), v(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && x(e, 1)) : (e = A(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (me(), R(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      R(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function N(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ie(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ue(e);
  let {
    svelteInit: i
  } = t;
  const w = E(N(t)), f = E();
  L(n, f, (c) => r(0, l = c));
  const m = E();
  L(n, m, (c) => r(1, o = c));
  const d = [], u = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: B
  } = $() || {}, J = i({
    parent: u,
    props: w,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: B,
    onDestroy(c) {
      d.push(c);
    }
  });
  xe("$$ms-gr-react-wrapper", J), ye(() => {
    w.set(N(t));
  }), ve(() => {
    d.forEach((c) => c());
  });
  function Y(c) {
    P[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function Q(c) {
    P[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = k(k({}, t), j(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = j(t), [l, o, f, m, a, i, s, e, Y, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Ie, Se, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const l = E(), o = new Ce({
      ...r,
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
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], D({
            createPortal: C,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: C,
              node: I
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
function Oe(n) {
  const [t, r] = W(() => b(n));
  return z(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function ke(n) {
  const t = M(() => ee(n, (r) => r), [n]);
  return Oe(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Pe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function O(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(C(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((o) => {
        if (_.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = O(o.props.el);
          return _.cloneElement(o, {
            ...o.props,
            el: s,
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = O(e);
      t.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Te(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const F = X(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Z(), [s, a] = W([]);
  return z(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Te(o, d), r && d.classList.add(...r.split(" ")), l) {
        const u = Le(l);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y;
        const {
          portals: u,
          clonedElement: p
        } = O(n);
        i = p, a(u), i.style.display = "contents", w(), (y = e.current) == null || y.appendChild(i);
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
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, r, l, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(n, t) {
  const r = M(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(s.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(s.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return ke(r);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...r
}) => {
  const l = je(t);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(te, {
      ...r,
      split: n.split ? /* @__PURE__ */ h.jsx(F, {
        slot: n.split,
        clone: !0
      }) : r.split,
      children: l.map((o, e) => /* @__PURE__ */ h.jsx(F, {
        slot: o
      }, e))
    })]
  });
});
export {
  Ne as Space,
  Ne as default
};
