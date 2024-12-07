import { g as $, w as v, d as ee, a as b } from "./Index-YfCEmPBU.js";
const _ = window.ms_globals.React, k = window.ms_globals.React.useMemo, W = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Carousel;
var G = {
  exports: {}
}, x = {};
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
function U(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) se.call(n, l) && !ie.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: re,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
x.Fragment = oe;
x.jsx = U;
x.jsxs = U;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: ae,
  assign: P,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: h,
  element: V,
  empty: j,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: E,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: we,
  transition_in: C,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: ve,
  onDestroy: Ee,
  setContext: Ce
} = window.__gradio__svelte__internal;
function F(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = fe(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(n);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      E(e, n, s), o && o.m(n, null), t[9](n), r = !0;
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
      r || (C(o, e), r = !0);
    },
    o(e) {
      R(o, e), r = !1;
    },
    d(e) {
      e && h(n), o && o.d(e), t[9](null);
    }
  };
}
function xe(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = V("react-portal-target"), r = we(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      n = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(h), r = ue(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      E(s, n, a), t[8](n), E(s, r, a), e && e.m(s, a), E(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = F(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (me(), R(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      R(e), o = !1;
    },
    d(s) {
      s && (h(n), h(r), h(l)), t[8](null), e && e.d(s);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Ie(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const a = de(e);
  let {
    svelteInit: i
  } = n;
  const g = v(N(n)), f = v();
  T(t, f, (c) => r(0, l = c));
  const m = v();
  T(t, m, (c) => r(1, o = c));
  const u = [], d = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: y,
    subSlotIndex: B
  } = $() || {}, J = i({
    parent: d,
    props: g,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: y,
    subSlotIndex: B,
    onDestroy(c) {
      u.push(c);
    }
  });
  Ce("$$ms-gr-react-wrapper", J), ye(() => {
    g.set(N(n));
  }), Ee(() => {
    u.forEach((c) => c());
  });
  function Y(c) {
    L[c ? "unshift" : "push"](() => {
      l = c, f.set(l);
    });
  }
  function Q(c) {
    L[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return t.$$set = (c) => {
    r(17, n = P(P({}, n), A(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, n = A(n), [l, o, f, m, a, i, s, e, Y, Q];
}
class Se extends ae {
  constructor(n) {
    super(), he(this, n, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(t) {
  function n(r) {
    const l = v(), o = new Se({
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
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], D({
            createPortal: S,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: S,
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
      r(n);
    });
  });
}
function Oe(t) {
  const [n, r] = W(() => b(t));
  return z(() => {
    let l = !0;
    return t.subscribe((e) => {
      l && (l = !1, e === n) || r(e);
    });
  }, [t]), n;
}
function ke(t) {
  const n = k(() => ee(t, (r) => r), [t]);
  return Oe(n);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Pe.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function O(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(S(_.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: _.Children.toArray(t._reactElement.props.children).map((o) => {
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
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = O(e);
      n.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Te(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const je = X(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Z(), [s, a] = W([]);
  return z(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Te(o, u), r && u.classList.add(...r.split(" ")), l) {
        const d = Le(l);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y;
        const {
          portals: d,
          clonedElement: p
        } = O(t);
        i = p, a(d), i.style.display = "contents", g(), (y = e.current) == null || y.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, r, l, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function M(t) {
  return k(() => Ae(t), [t]);
}
function Fe(t, n) {
  const r = k(() => _.Children.toArray(t).filter((e) => e.props.node && (!e.props.nodeSlotKey || n)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(s.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(s.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return ke(r);
}
const De = Re(({
  afterChange: t,
  beforeChange: n,
  children: r,
  ...l
}) => {
  const o = M(t), e = M(n), s = Fe(r);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ w.jsx(te, {
      ...l,
      afterChange: o,
      beforeChange: e,
      children: s.map((a, i) => /* @__PURE__ */ w.jsx(je, {
        clone: !0,
        slot: a
      }, i))
    })]
  });
});
export {
  De as Carousel,
  De as default
};
