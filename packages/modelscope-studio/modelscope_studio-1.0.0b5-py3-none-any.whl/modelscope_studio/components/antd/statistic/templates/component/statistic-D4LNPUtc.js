import { g as Z, w as y } from "./Index-wQNS__ug.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Statistic;
var D = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, e, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) re.call(e, s) && !se.hasOwnProperty(s) && (r[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: te,
    type: n,
    key: t,
    ref: l,
    props: r,
    _owner: oe.current
  };
}
C.Fragment = ne;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var p = D.exports;
const {
  SvelteComponent: le,
  assign: k,
  binding_callbacks: P,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: G,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: v,
  transition_out: I,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function N(n) {
  let e, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = G("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = z(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = W(e);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      U(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      E(t, e, l), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? fe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : de(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (v(r, t), o = !0);
    },
    o(t) {
      I(r, t), o = !1;
    },
    d(t) {
      t && g(e), r && r.d(t), n[9](null);
    }
  };
}
function ve(n) {
  let e, o, s, r, t = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      e = G("react-portal-target"), o = he(), t && t.c(), s = L(), this.h();
    },
    l(l) {
      e = z(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(e).forEach(g), o = ce(l), t && t.l(l), s = L(), this.h();
    },
    h() {
      U(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, e, c), n[8](e), E(l, o, c), t && t.m(l, c), E(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = N(l), t.c(), v(t, 1), t.m(s.parentNode, s)) : t && (_e(), I(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(l) {
      r || (v(t), r = !0);
    },
    o(l) {
      I(t), r = !1;
    },
    d(l) {
      l && (g(e), g(o), g(s)), n[8](null), t && t.d(l);
    }
  };
}
function A(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function xe(n, e, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ae(t);
  let {
    svelteInit: i
  } = e;
  const w = y(A(e)), f = y();
  j(n, f, (a) => o(0, s = a));
  const m = y();
  j(n, m, (a) => o(1, r = a));
  const u = [], d = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H
  } = Z() || {}, K = i({
    parent: d,
    props: w,
    target: f,
    slot: m,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", K), we(() => {
    w.set(A(e));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function q(a) {
    P[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  function V(a) {
    P[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, e = k(k({}, e), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, e = T(e), [s, r, f, m, c, i, l, t, q, V];
}
class Ce extends le {
  constructor(e) {
    super(), pe(this, e, xe, ve, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(n) {
  function e(o) {
    const s = y(), r = new Ce({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? S;
          return c.nodes = [...c.nodes, l], F({
            createPortal: R,
            node: S
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: R,
              node: S
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
      o(e);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const s = n[o];
    return typeof s == "number" && !Re.includes(o) ? e[o] = s + "px" : e[o] = s, e;
  }, {}) : {};
}
function O(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(R(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = O(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...h.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
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
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(t);
      e.push(...c), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const x = B(({
  slot: n,
  clone: e,
  className: o,
  style: s
}, r) => {
  const t = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!t.current || !n)
      return;
    let i = n;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const d = Ie(s);
        Object.keys(d).forEach((_) => {
          u.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var b;
        const {
          portals: d,
          clonedElement: _
        } = O(n);
        i = _, c(d), i.style.display = "contents", w(), (b = t.current) == null || b.appendChild(i);
      };
      u(), f = new window.MutationObserver(() => {
        var d, _;
        (d = t.current) != null && d.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", w(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((d = t.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [n, e, o, s, r]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ke(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Pe(n) {
  return X(() => ke(n), [n]);
}
function je(n, e) {
  return n ? /* @__PURE__ */ p.jsx(x, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: o
}, s) {
  return o[n] ? (...r) => (e(n, r), je(o[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Se(({
  children: n,
  slots: e,
  setSlotParams: o,
  formatter: s,
  ...r
}) => {
  const t = Pe(s);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx($, {
      ...r,
      formatter: e.formatter ? Le({
        slots: e,
        setSlotParams: o,
        key: "formatter"
      }) : t,
      title: e.title ? /* @__PURE__ */ p.jsx(x, {
        slot: e.title
      }) : r.title,
      prefix: e.prefix ? /* @__PURE__ */ p.jsx(x, {
        slot: e.prefix
      }) : r.prefix,
      suffix: e.suffix ? /* @__PURE__ */ p.jsx(x, {
        slot: e.suffix
      }) : r.suffix
    })]
  });
});
export {
  Ne as Statistic,
  Ne as default
};
