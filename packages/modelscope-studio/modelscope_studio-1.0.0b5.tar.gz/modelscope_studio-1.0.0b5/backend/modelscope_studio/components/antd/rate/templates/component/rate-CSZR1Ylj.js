import { g as Q, w as y } from "./Index-BU1ZxO6l.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, S = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Rate;
var D = {
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) te.call(t, s) && !re.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: ne.current
  };
}
R.Fragment = ee;
R.jsx = F;
R.jsxs = F;
D.exports = R;
var w = D.exports;
const {
  SvelteComponent: oe,
  assign: O,
  binding_callbacks: k,
  check_outros: se,
  children: W,
  claim_element: z,
  claim_space: le,
  component_subscribe: P,
  compute_slots: ie,
  create_slot: ce,
  detach: h,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ae,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: E,
  safe_not_equal: _e,
  set_custom_element_data: U,
  space: pe,
  transition_in: v,
  transition_out: x,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function j(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ce(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = G("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && me(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (v(r, e), o = !0);
    },
    o(e) {
      x(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && j(n)
  );
  return {
    c() {
      t = G("react-portal-target"), o = pe(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      t = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(t).forEach(h), o = le(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      U(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, t, c), n[8](t), E(l, o, c), e && e.m(l, c), E(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = j(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (ue(), x(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      x(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function N(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ee(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = y(N(t)), f = y();
  P(n, f, (a) => o(0, s = a));
  const p = y();
  P(n, p, (a) => o(1, r = a));
  const d = [], u = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H
  } = Q() || {}, K = i({
    parent: u,
    props: g,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H,
    onDestroy(a) {
      d.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", K), he(() => {
    g.set(N(t));
  }), we(() => {
    d.forEach((a) => a());
  });
  function M(a) {
    k[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function q(a) {
    k[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = O(O({}, t), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = T(t), [s, r, f, p, c, i, l, e, M, q];
}
class ve extends oe {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, C = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = y(), r = new ve({
      ...o,
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
          }, c = e.parent ?? C;
          return c.nodes = [...c.nodes, l], A({
            createPortal: S,
            node: C
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), A({
              createPortal: S,
              node: C
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Ce.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function I(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(S(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = I(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...m.Children.toArray(r.props.children), ...e]
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = I(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = V(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = B(), [l, c] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(r, d), o && d.classList.add(...o.split(" ")), s) {
        const u = Se(s);
        Object.keys(u).forEach((_) => {
          d.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b;
        const {
          portals: u,
          clonedElement: _
        } = I(n);
        i = _, c(u), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, _;
        (u = e.current) != null && u.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((u = e.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, t, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(n, t) {
  return n ? /* @__PURE__ */ w.jsx(Ie, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ke({
  key: n,
  setSlotParams: t,
  slots: o
}, s) {
  return o[n] ? (...r) => (t(n, r), Oe(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Le = Re(({
  slots: n,
  children: t,
  onValueChange: o,
  character: s,
  onChange: r,
  setSlotParams: e,
  elRef: l,
  ...c
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ w.jsx(X, {
    ...c,
    ref: l,
    onChange: (i) => {
      r == null || r(i), o(i);
    },
    character: n.character ? ke({
      slots: n,
      setSlotParams: e,
      key: "character"
    }) : s
  })]
}));
export {
  Le as Rate,
  Le as default
};
