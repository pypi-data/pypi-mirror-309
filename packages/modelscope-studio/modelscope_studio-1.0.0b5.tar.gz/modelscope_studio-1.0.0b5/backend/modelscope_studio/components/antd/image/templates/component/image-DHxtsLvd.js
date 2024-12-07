import { g as ee, w as v } from "./Index-GjvtT8Rc.js";
const _ = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Image;
var U = {
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
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) le.call(n, l) && !ie.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = W;
C.jsxs = W;
U.exports = C;
var w = U.exports;
const {
  SvelteComponent: ce,
  assign: P,
  binding_callbacks: j,
  check_outros: ae,
  children: z,
  claim_element: G,
  claim_space: de,
  component_subscribe: L,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: H,
  empty: T,
  exclude_internal_props: F,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: _e,
  init: ge,
  insert_hydration: y,
  safe_not_equal: he,
  set_custom_element_data: K,
  space: we,
  transition_in: E,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: ye,
  onDestroy: Ee,
  setContext: Re
} = window.__gradio__svelte__internal;
function N(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = G(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = z(n);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      y(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && be(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? me(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (E(r, t), o = !0);
    },
    o(t) {
      k(r, t), o = !1;
    },
    d(t) {
      t && g(n), r && r.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && N(e)
  );
  return {
    c() {
      n = H("react-portal-target"), o = we(), t && t.c(), l = T(), this.h();
    },
    l(s) {
      n = G(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), z(n).forEach(g), o = de(s), t && t.l(s), l = T(), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      y(s, n, c), e[8](n), y(s, o, c), t && t.m(s, c), y(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && E(t, 1)) : (t = N(s), t.c(), E(t, 1), t.m(l.parentNode, l)) : t && (_e(), k(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      r || (E(t), r = !0);
    },
    o(s) {
      k(t), r = !1;
    },
    d(s) {
      s && (g(n), g(o), g(l)), e[8](null), t && t.d(s);
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
function Ie(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = ue(t);
  let {
    svelteInit: i
  } = n;
  const h = v(A(n)), f = v();
  L(e, f, (a) => o(0, l = a));
  const m = v();
  L(e, m, (a) => o(1, r = a));
  const d = [], u = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: q
  } = ee() || {}, V = i({
    parent: u,
    props: h,
    target: f,
    slot: m,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(a) {
      d.push(a);
    }
  });
  Re("$$ms-gr-react-wrapper", V), ve(() => {
    h.set(A(n));
  }), Ee(() => {
    d.forEach((a) => a());
  });
  function B(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function J(a) {
    j[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return e.$$set = (a) => {
    o(17, n = P(P({}, n), F(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = F(n), [l, r, f, m, c, i, s, t, B, J];
}
class xe extends ce {
  constructor(n) {
    super(), ge(this, n, Ie, Ce, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(e) {
  function n(o) {
    const l = v(), r = new xe({
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
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, s], D({
            createPortal: S,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: S,
              node: I
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
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !ke.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function O(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(S(_.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: _.Children.toArray(e._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = O(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: s,
            children: [..._.Children.toArray(r.props.children), ...t]
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
function Pe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const R = Y(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var m;
    if (!t.current || !e)
      return;
    let i = e;
    function h() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Pe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const u = Oe(l);
        Object.keys(u).forEach((p) => {
          d.style[p] = u[p];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var b;
        const {
          portals: u,
          clonedElement: p
        } = O(e);
        i = p, c(u), i.style.display = "contents", h(), (b = t.current) == null || b.appendChild(i);
      };
      d(), f = new window.MutationObserver(() => {
        var u, p;
        (u = t.current) != null && u.contains(i) && ((p = t.current) == null || p.removeChild(i)), d();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var d, u;
      i.style.display = "", (d = t.current) != null && d.contains(i) && ((u = t.current) == null || u.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, n, o, l, r]), _.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function x(e) {
  return $(() => je(e), [e]);
}
function Le(e) {
  return Object.keys(e).reduce((n, o) => (e[o] !== void 0 && (n[o] = e[o]), n), {});
}
function Te(e, n) {
  return e ? /* @__PURE__ */ w.jsx(R, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Te(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function Fe(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Ae = Se(({
  slots: e,
  preview: n,
  setSlotParams: o,
  ...l
}) => {
  const r = Fe(n), t = e["preview.mask"] || e["preview.closeIcon"] || e["preview.toolbarRender"] || e["preview.imageRender"] || n !== !1, s = x(r.getContainer), c = x(r.toolbarRender), i = x(r.imageRender);
  return /* @__PURE__ */ w.jsx(te, {
    ...l,
    preview: t ? Le({
      ...r,
      getContainer: s,
      toolbarRender: e["preview.toolbarRender"] ? M({
        slots: e,
        setSlotParams: o,
        key: "preview.toolbarRender"
      }) : c,
      imageRender: e["preview.imageRender"] ? M({
        slots: e,
        setSlotParams: o,
        key: "preview.imageRender"
      }) : i,
      ...e["preview.mask"] || Reflect.has(r, "mask") ? {
        mask: e["preview.mask"] ? /* @__PURE__ */ w.jsx(R, {
          slot: e["preview.mask"]
        }) : r.mask
      } : {},
      closeIcon: e["preview.closeIcon"] ? /* @__PURE__ */ w.jsx(R, {
        slot: e["preview.closeIcon"]
      }) : r.closeIcon
    }) : !1,
    placeholder: e.placeholder ? /* @__PURE__ */ w.jsx(R, {
      slot: e.placeholder
    }) : l.placeholder
  });
});
export {
  Ae as Image,
  Ae as default
};
