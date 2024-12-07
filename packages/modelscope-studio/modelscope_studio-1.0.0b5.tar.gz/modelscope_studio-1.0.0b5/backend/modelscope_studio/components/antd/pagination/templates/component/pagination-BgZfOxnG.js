import { g as $, w as y } from "./Index-x0KMbTcJ.js";
const h = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Pagination;
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !le.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = M;
R.jsxs = M;
D.exports = R;
var g = D.exports;
const {
  SvelteComponent: ie,
  assign: k,
  binding_callbacks: O,
  check_outros: ce,
  children: W,
  claim_element: z,
  claim_space: ae,
  component_subscribe: P,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: B,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: E,
  safe_not_equal: he,
  set_custom_element_data: G,
  space: ge,
  transition_in: v,
  transition_out: S,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function j(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = de(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = B("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = z(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(n);
      r && r.l(l), l.forEach(w), this.h();
    },
    h() {
      G(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && we(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
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
      S(r, e), o = !1;
    },
    d(e) {
      e && w(n), r && r.d(e), t[9](null);
    }
  };
}
function Re(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && j(t)
  );
  return {
    c() {
      n = B("react-portal-target"), o = ge(), e && e.c(), s = L(), this.h();
    },
    l(l) {
      n = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(n).forEach(w), o = ae(l), e && e.l(l), s = L(), this.h();
    },
    h() {
      G(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, n, c), t[8](n), E(l, o, c), e && e.m(l, c), E(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && v(e, 1)) : (e = j(l), e.c(), v(e, 1), e.m(s.parentNode, s)) : e && (pe(), S(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      r || (v(e), r = !0);
    },
    o(l) {
      S(e), r = !1;
    },
    d(l) {
      l && (w(n), w(o), w(s)), t[8](null), e && e.d(l);
    }
  };
}
function F(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function xe(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const m = y(F(n)), d = y();
  P(t, d, (a) => o(0, s = a));
  const _ = y();
  P(t, _, (a) => o(1, r = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: U
  } = $() || {}, H = i({
    parent: f,
    props: m,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: U,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", H), be(() => {
    m.set(F(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function K(a) {
    O[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function Q(a) {
    O[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = k(k({}, n), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, n = T(n), [s, r, d, _, c, i, l, e, K, Q];
}
class Ce extends ie {
  constructor(n) {
    super(), me(this, n, xe, Re, he, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, x = window.ms_globals.tree;
function Se(t) {
  function n(o) {
    const s = y(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, l], N({
            createPortal: C,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), N({
              createPortal: C,
              node: x
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
      o(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !Ie.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function I(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(C(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = I(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = I(e);
      n.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Oe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const J = q(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = V(), [l, c] = Y([]);
  return X(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function m() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: f,
          clonedElement: p
        } = I(t);
        i = p, c(f), i.style.display = "contents", m(), (b = e.current) == null || b.appendChild(i);
      };
      u(), d = new window.MutationObserver(() => {
        var f, p;
        (f = e.current) != null && f.contains(i) && ((p = e.current) == null || p.removeChild(i)), u();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", m(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, o, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function A(t) {
  return Z(() => Pe(t), [t]);
}
function Le(t, n) {
  return t ? /* @__PURE__ */ g.jsx(J, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Te({
  key: t,
  setSlotParams: n,
  slots: o
}, s) {
  return o[t] ? (...r) => (n(t, r), Le(o[t], {
    clone: !0,
    ...s
  })) : void 0;
}
const Fe = Se(({
  slots: t,
  showTotal: n,
  showQuickJumper: o,
  onChange: s,
  children: r,
  itemRender: e,
  setSlotParams: l,
  ...c
}) => {
  const i = A(e), m = A(n);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ g.jsx(ee, {
      ...c,
      showTotal: n ? m : void 0,
      itemRender: t.itemRender ? Te({
        slots: t,
        setSlotParams: l,
        key: "itemRender"
      }, {
        clone: !0
      }) : i,
      onChange: (d, _) => {
        s == null || s(d, _);
      },
      showQuickJumper: t["showQuickJumper.goButton"] ? {
        goButton: /* @__PURE__ */ g.jsx(J, {
          slot: t["showQuickJumper.goButton"]
        })
      } : o
    })]
  });
});
export {
  Fe as Pagination,
  Fe as default
};
