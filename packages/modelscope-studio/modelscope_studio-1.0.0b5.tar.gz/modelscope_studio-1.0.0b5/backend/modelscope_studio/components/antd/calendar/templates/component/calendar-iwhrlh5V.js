import { g as re, w as R } from "./Index-DScmnEra.js";
const w = window.ms_globals.React, E = window.ms_globals.React.useMemo, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, F = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Calendar, N = window.ms_globals.dayjs;
var q = {
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
var le = w, se = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(t, n, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ce.call(n, l) && !ue.hasOwnProperty(l) && (r[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: se,
    type: t,
    key: e,
    ref: s,
    props: r,
    _owner: ae.current
  };
}
x.Fragment = ie;
x.jsx = B;
x.jsxs = B;
q.exports = x;
var J = q.exports;
const {
  SvelteComponent: de,
  assign: M,
  binding_callbacks: W,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: _e,
  component_subscribe: z,
  compute_slots: pe,
  create_slot: me,
  detach: g,
  element: X,
  empty: G,
  exclude_internal_props: U,
  get_all_dirty_from_scope: he,
  get_slot_changes: we,
  group_outros: be,
  init: ge,
  insert_hydration: C,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: ve,
  transition_in: O,
  transition_out: P,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: Ce,
  onDestroy: Oe,
  setContext: xe
} = window.__gradio__svelte__internal;
function V(t) {
  let n, o;
  const l = (
    /*#slots*/
    t[7].default
  ), r = me(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = X("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(n);
      r && r.l(s), s.forEach(g), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, n, s), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Ee(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? we(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : he(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (O(r, e), o = !0);
    },
    o(e) {
      P(r, e), o = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function Ie(t) {
  let n, o, l, r, e = (
    /*$$slots*/
    t[4].default && V(t)
  );
  return {
    c() {
      n = X("react-portal-target"), o = ve(), e && e.c(), l = G(), this.h();
    },
    l(s) {
      n = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(n).forEach(g), o = _e(s), e && e.l(s), l = G(), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, n, a), t[8](n), C(s, o, a), e && e.m(s, a), C(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && O(e, 1)) : (e = V(s), e.c(), O(e, 1), e.m(l.parentNode, l)) : e && (be(), P(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      r || (O(e), r = !0);
    },
    o(s) {
      P(e), r = !1;
    },
    d(s) {
      s && (g(n), g(o), g(l)), t[8](null), e && e.d(s);
    }
  };
}
function H(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Se(t, n, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const a = pe(e);
  let {
    svelteInit: i
  } = n;
  const h = R(H(n)), f = R();
  z(t, f, (u) => o(0, l = u));
  const p = R();
  z(t, p, (u) => o(1, r = u));
  const c = [], d = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: I
  } = re() || {}, S = i({
    parent: d,
    props: h,
    target: f,
    slot: p,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: I,
    onDestroy(u) {
      c.push(u);
    }
  });
  xe("$$ms-gr-react-wrapper", S), Re(() => {
    h.set(H(n));
  }), Oe(() => {
    c.forEach((u) => u());
  });
  function k(u) {
    W[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function L(u) {
    W[u ? "unshift" : "push"](() => {
      r = u, p.set(r);
    });
  }
  return t.$$set = (u) => {
    o(17, n = M(M({}, n), U(u))), "svelteInit" in u && o(5, i = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = U(n), [l, r, f, p, a, i, s, e, k, L];
}
class ke extends de {
  constructor(n) {
    super(), ge(this, n, Se, Ie, ye, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, j = window.ms_globals.tree;
function Le(t) {
  function n(o) {
    const l = R(), r = new ke({
      ...o,
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
          }, a = e.parent ?? j;
          return a.nodes = [...a.nodes, s], K({
            createPortal: F,
            node: j
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), K({
              createPortal: F,
              node: j
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
function je(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function v(t) {
  return E(() => je(t), [t]);
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const l = t[o];
    return typeof l == "number" && !Te.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function D(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(F(w.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: w.Children.toArray(t._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = D(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...e]
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(e);
      n.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Fe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const Pe = $(({
  slot: t,
  clone: n,
  className: o,
  style: l
}, r) => {
  const e = ee(), [s, a] = te([]);
  return ne(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(r, c), o && c.classList.add(...o.split(" ")), l) {
        const d = Ae(l);
        Object.keys(d).forEach((_) => {
          c.style[_] = d[_];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var b;
        const {
          portals: d,
          clonedElement: _
        } = D(t);
        i = _, a(d), i.style.display = "contents", h(), (b = e.current) == null || b.appendChild(i);
      };
      c(), f = new window.MutationObserver(() => {
        var d, _;
        (d = e.current) != null && d.contains(i) && ((_ = e.current) == null || _.removeChild(i)), c();
      }), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", h(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var c, d;
      i.style.display = "", (c = e.current) != null && c.contains(i) && ((d = e.current) == null || d.removeChild(i)), f == null || f.disconnect();
    };
  }, [t, n, o, l, r]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function De(t, n) {
  return t ? /* @__PURE__ */ J.jsx(Pe, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function T({
  key: t,
  setSlotParams: n,
  slots: o
}, l) {
  return o[t] ? (...r) => (n(t, r), De(o[t], {
    clone: !0,
    ...l
  })) : void 0;
}
function A(t) {
  return N(typeof t == "number" ? t * 1e3 : t);
}
const Me = Le(({
  disabledDate: t,
  value: n,
  defaultValue: o,
  validRange: l,
  onChange: r,
  onPanelChange: e,
  onSelect: s,
  onValueChange: a,
  setSlotParams: i,
  cellRender: h,
  fullCellRender: f,
  headerRender: p,
  slots: c,
  ...d
}) => {
  const _ = v(t), b = v(h), I = v(f), S = v(p), k = E(() => n ? A(n) : void 0, [n]), L = E(() => o ? A(o) : void 0, [o]), u = E(() => Array.isArray(l) ? l.map((m) => A(m)) : void 0, [l]);
  return /* @__PURE__ */ J.jsx(oe, {
    ...d,
    value: k,
    defaultValue: L,
    validRange: u,
    disabledDate: _,
    cellRender: c.cellRender ? T({
      slots: c,
      setSlotParams: i,
      key: "cellRender"
    }) : b,
    fullCellRender: c.fullCellRender ? T({
      slots: c,
      setSlotParams: i,
      key: "fullCellRender"
    }) : I,
    headerRender: c.headerRender ? T({
      slots: c,
      setSlotParams: i,
      key: "headerRender"
    }) : S,
    onChange: (m, ...y) => {
      a(m.valueOf() / 1e3), r == null || r(m.valueOf() / 1e3, ...y);
    },
    onPanelChange: (m, ...y) => {
      e == null || e(m.valueOf() / 1e3, ...y);
    },
    onSelect: (m, ...y) => {
      s == null || s(m.valueOf() / 1e3, ...y);
    }
  });
});
export {
  Me as Calendar,
  Me as default
};
