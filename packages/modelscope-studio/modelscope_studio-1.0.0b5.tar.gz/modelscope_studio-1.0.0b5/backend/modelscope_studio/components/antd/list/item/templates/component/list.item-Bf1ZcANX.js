import { g as $, w as y, d as ee, a as w } from "./Index-D2TGevjE.js";
const _ = window.ms_globals.React, W = window.ms_globals.React.useMemo, z = window.ms_globals.React.useState, F = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, C = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.List;
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
x.Fragment = oe;
x.jsx = U;
x.jsxs = U;
G.exports = x;
var I = G.exports;
const {
  SvelteComponent: ae,
  assign: k,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: ue,
  component_subscribe: P,
  compute_slots: de,
  create_slot: fe,
  detach: h,
  element: V,
  empty: T,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: E,
  safe_not_equal: ge,
  set_custom_element_data: q,
  space: we,
  transition_in: v,
  transition_out: R,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function j(n) {
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
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && be(
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
      r || (v(o, e), r = !0);
    },
    o(e) {
      R(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = V("react-portal-target"), r = we(), e && e.c(), s = T(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(h), r = ue(l), e && e.l(l), s = T(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      E(l, t, a), n[8](t), E(l, r, a), e && e.m(l, a), E(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && v(e, 1)) : (e = j(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (me(), R(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (v(e), o = !0);
    },
    o(l) {
      R(e), o = !1;
    },
    d(l) {
      l && (h(t), h(r), h(s)), n[8](null), e && e.d(l);
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
function Se(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: i
  } = t;
  const g = y(N(t)), f = y();
  P(n, f, (c) => r(0, s = c));
  const m = y();
  P(n, m, (c) => r(1, o = c));
  const u = [], d = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: B
  } = $() || {}, J = i({
    parent: d,
    props: g,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: B,
    onDestroy(c) {
      u.push(c);
    }
  });
  xe("$$ms-gr-react-wrapper", J), ye(() => {
    g.set(N(t));
  }), ve(() => {
    u.forEach((c) => c());
  });
  function Y(c) {
    L[c ? "unshift" : "push"](() => {
      s = c, f.set(s);
    });
  }
  function Q(c) {
    L[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = k(k({}, t), A(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = A(t), [s, o, f, m, a, i, l, e, Y, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const s = y(), o = new Ce({
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
          return a.nodes = [...a.nodes, l], D({
            createPortal: C,
            node: S
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: C,
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
  const [t, r] = z(() => w(n));
  return F(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function ke(n) {
  const t = W(() => ee(n, (r) => r), [n]);
  return Oe(t);
}
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Le.includes(r) ? t[r] = s + "px" : t[r] = s, t;
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
            clonedElement: l
          } = O(o.props.el);
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
      } = O(e);
      t.push(...a), r.appendChild(l);
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
const M = X(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = Z(), [l, a] = z([]);
  return F(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Te(o, u), r && u.classList.add(...r.split(" ")), s) {
        const d = Pe(s);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: d,
          clonedElement: p
        } = O(n);
        i = p, a(d), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, p;
        (d = e.current) != null && d.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), f.observe(n, {
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
  }, [n, t, r, s, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(n, t) {
  const r = W(() => _.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = w(e.props.node.slotIndex) || 0, i = w(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(l.props.node.subSlotIndex) || 0) : a - i;
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
  const s = Ae(t, "actions");
  return /* @__PURE__ */ I.jsx(te.Item, {
    ...r,
    extra: n.extra ? /* @__PURE__ */ I.jsx(M, {
      slot: n.extra
    }) : r.extra,
    actions: s.length > 0 ? s.map((o, e) => /* @__PURE__ */ I.jsx(M, {
      slot: o
    }, e)) : r.actions,
    children: t
  });
});
export {
  Ne as ListItem,
  Ne as default
};
