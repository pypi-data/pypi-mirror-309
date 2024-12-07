import { g as Z, w as y } from "./Index-DuelqC-a.js";
const p = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.List;
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
var ee = p, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) re.call(n, l) && !le.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: te,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: oe.current
  };
}
I.Fragment = ne;
I.jsx = D;
I.jsxs = D;
F.exports = I;
var w = F.exports;
const {
  SvelteComponent: se,
  assign: k,
  binding_callbacks: L,
  check_outros: ie,
  children: W,
  claim_element: z,
  claim_space: ce,
  component_subscribe: P,
  compute_slots: ae,
  create_slot: de,
  detach: h,
  element: G,
  empty: j,
  exclude_internal_props: T,
  get_all_dirty_from_scope: ue,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: E,
  safe_not_equal: pe,
  set_custom_element_data: U,
  space: he,
  transition_in: v,
  transition_out: S,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function N(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = de(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = G("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = z(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = W(n);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      E(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && ge(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? fe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ue(
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
      S(r, t), o = !1;
    },
    d(t) {
      t && h(n), r && r.d(t), e[9](null);
    }
  };
}
function ve(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && N(e)
  );
  return {
    c() {
      n = G("react-portal-target"), o = he(), t && t.c(), l = j(), this.h();
    },
    l(s) {
      n = z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), W(n).forEach(h), o = ce(s), t && t.l(s), l = j(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      E(s, n, c), e[8](n), E(s, o, c), t && t.m(s, c), E(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && v(t, 1)) : (t = N(s), t.c(), v(t, 1), t.m(l.parentNode, l)) : t && (_e(), S(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(s) {
      r || (v(t), r = !0);
    },
    o(s) {
      S(t), r = !1;
    },
    d(s) {
      s && (h(n), h(o), h(l)), e[8](null), t && t.d(s);
    }
  };
}
function A(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Ce(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = ae(t);
  let {
    svelteInit: i
  } = n;
  const g = y(A(n)), f = y();
  P(e, f, (a) => o(0, l = a));
  const m = y();
  P(e, m, (a) => o(1, r = a));
  const d = [], u = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H
  } = Z() || {}, K = i({
    parent: u,
    props: g,
    target: f,
    slot: m,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: H,
    onDestroy(a) {
      d.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", K), we(() => {
    g.set(A(n));
  }), ye(() => {
    d.forEach((a) => a());
  });
  function q(a) {
    L[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function V(a) {
    L[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, n = k(k({}, n), T(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = T(n), [l, r, f, m, c, i, s, t, q, V];
}
class Ie extends se {
  constructor(n) {
    super(), me(this, n, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(e) {
  function n(o) {
    const l = y(), r = new Ie({
      ...o,
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
          }, c = t.parent ?? x;
          return c.nodes = [...c.nodes, s], M({
            createPortal: R,
            node: x
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), M({
              createPortal: R,
              node: x
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
      o(n);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Re.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function O(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(R(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: p.Children.toArray(e._reactElement.props.children).map((r) => {
        if (p.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = O(r.props.el);
          return p.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...p.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = O(t);
      n.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Oe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const C = B(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = J(), [s, c] = Y([]);
  return Q(() => {
    var m;
    if (!t.current || !e)
      return;
    let i = e;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Oe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Se(l);
        Object.keys(u).forEach((_) => {
          d.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var b;
        const {
          portals: u,
          clonedElement: _
        } = O(e);
        i = _, c(u), i.style.display = "contents", g(), (b = t.current) == null || b.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, _;
        (u = t.current) != null && u.contains(i) && ((_ = t.current) == null || _.removeChild(i)), d();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = t.current) != null && d.contains(i) && ((u = t.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, n, o, l, r]), p.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Le(e) {
  return X(() => ke(e), [e]);
}
function Pe(e, n) {
  return e ? /* @__PURE__ */ w.jsx(C, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function je({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Pe(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ne = xe(({
  slots: e,
  renderItem: n,
  setSlotParams: o,
  ...l
}) => {
  const r = Le(n);
  return /* @__PURE__ */ w.jsx($, {
    ...l,
    footer: e.footer ? /* @__PURE__ */ w.jsx(C, {
      slot: e.footer
    }) : l.footer,
    header: e.header ? /* @__PURE__ */ w.jsx(C, {
      slot: e.header
    }) : l.header,
    loadMore: e.loadMore ? /* @__PURE__ */ w.jsx(C, {
      slot: e.loadMore
    }) : l.loadMore,
    renderItem: e.renderItem ? je({
      slots: e,
      setSlotParams: o,
      key: "renderItem"
    }) : r
  });
});
export {
  Ne as List,
  Ne as default
};
