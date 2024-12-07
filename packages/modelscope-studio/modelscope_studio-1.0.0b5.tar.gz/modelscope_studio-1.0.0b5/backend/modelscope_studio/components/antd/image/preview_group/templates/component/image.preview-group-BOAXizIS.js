import { g as Z, w as b } from "./Index-CTePWVOB.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Image;
var D = {
  exports: {}
}, E = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(t, n, s) {
  var o, r = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (o in n) re.call(n, o) && !se.hasOwnProperty(o) && (r[o] = n[o]);
  if (t && t.defaultProps) for (o in n = t.defaultProps, n) r[o] === void 0 && (r[o] = n[o]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: oe.current
  };
}
E.Fragment = ne;
E.jsx = G;
E.jsxs = G;
D.exports = E;
var C = D.exports;
const {
  SvelteComponent: le,
  assign: S,
  binding_callbacks: O,
  check_outros: ie,
  children: M,
  claim_element: W,
  claim_space: ce,
  component_subscribe: P,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: z,
  empty: L,
  exclude_internal_props: T,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: he,
  transition_in: y,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function j(t) {
  let n, s;
  const o = (
    /*#slots*/
    t[7].default
  ), r = ue(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = z("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = W(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = M(n);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, n, l), r && r.m(n, null), t[9](n), s = !0;
    },
    p(e, l) {
      r && r.p && (!s || l & /*$$scope*/
      64) && ge(
        r,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (y(r, e), s = !0);
    },
    o(e) {
      k(r, e), s = !1;
    },
    d(e) {
      e && h(n), r && r.d(e), t[9](null);
    }
  };
}
function Ee(t) {
  let n, s, o, r, e = (
    /*$$slots*/
    t[4].default && j(t)
  );
  return {
    c() {
      n = z("react-portal-target"), s = he(), e && e.c(), o = L(), this.h();
    },
    l(l) {
      n = W(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), M(n).forEach(h), s = ce(l), e && e.l(l), o = L(), this.h();
    },
    h() {
      U(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, n, c), t[8](n), v(l, s, c), e && e.m(l, c), v(l, o, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && y(e, 1)) : (e = j(l), e.c(), y(e, 1), e.m(o.parentNode, o)) : e && (pe(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (y(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (h(n), h(s), h(o)), t[8](null), e && e.d(l);
    }
  };
}
function N(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function Ce(t, n, s) {
  let o, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const g = b(N(n)), f = b();
  P(t, f, (a) => s(0, o = a));
  const _ = b();
  P(t, _, (a) => s(1, r = a));
  const u = [], d = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H
  } = Z() || {}, K = i({
    parent: d,
    props: g,
    target: f,
    slot: _,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: H,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", K), we(() => {
    g.set(N(n));
  }), ve(() => {
    u.forEach((a) => a());
  });
  function q(a) {
    O[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  function V(a) {
    O[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  return t.$$set = (a) => {
    s(17, n = S(S({}, n), T(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, l = a.$$scope);
  }, n = T(n), [o, r, f, _, c, i, l, e, q, V];
}
class Ie extends le {
  constructor(n) {
    super(), _e(this, n, Ce, Ee, me, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(t) {
  function n(s) {
    const o = b(), r = new Ie({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], A({
            createPortal: R,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), A({
              createPortal: R,
              node: I
            });
          }), l;
        },
        ...s.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(n);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const o = t[s];
    return typeof o == "number" && !ke.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function x(t) {
  const n = [], s = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(R(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = x(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const e = o[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = x(e);
      n.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: n
  };
}
function Se(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const F = B(({
  slot: t,
  clone: n,
  className: s,
  style: o
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Se(r, u), s && u.classList.add(...s.split(" ")), o) {
        const d = xe(o);
        Object.keys(d).forEach((p) => {
          u.style[p] = d[p];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var w;
        const {
          portals: d,
          clonedElement: p
        } = x(t);
        i = p, c(d), i.style.display = "contents", g(), (w = e.current) == null || w.appendChild(i);
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
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, d;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, s, o, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Pe(t) {
  return X(() => Oe(t), [t]);
}
function Le(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const je = Re(({
  slots: t,
  preview: n,
  ...s
}) => {
  const o = Le(n), r = t["preview.mask"] || t["preview.closeIcon"] || n !== !1, e = Pe(o.getContainer);
  return /* @__PURE__ */ C.jsx($.PreviewGroup, {
    ...s,
    preview: r ? {
      ...o,
      getContainer: e,
      ...t["preview.mask"] || Reflect.has(o, "mask") ? {
        mask: t["preview.mask"] ? /* @__PURE__ */ C.jsx(F, {
          slot: t["preview.mask"]
        }) : o.mask
      } : {},
      closeIcon: t["preview.closeIcon"] ? /* @__PURE__ */ C.jsx(F, {
        slot: t["preview.closeIcon"]
      }) : o.closeIcon
    } : !1
  });
});
export {
  je as ImagePreviewGroup,
  je as default
};
