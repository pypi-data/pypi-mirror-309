import { g as fe, w as x } from "./Index-DonQ-lwo.js";
const y = window.ms_globals.React, J = window.ms_globals.React.useMemo, ae = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, pe = window.ms_globals.React.useEffect, T = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.Upload;
var Y = {
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
var me = y, _e = Symbol.for("react.element"), he = Symbol.for("react.fragment"), ve = Object.prototype.hasOwnProperty, Ie = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, be = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, o, r) {
  var s, n = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), o.key !== void 0 && (t = "" + o.key), o.ref !== void 0 && (l = o.ref);
  for (s in o) ve.call(o, s) && !be.hasOwnProperty(s) && (n[s] = o[s]);
  if (e && e.defaultProps) for (s in o = e.defaultProps, o) n[s] === void 0 && (n[s] = o[s]);
  return {
    $$typeof: _e,
    type: e,
    key: t,
    ref: l,
    props: n,
    _owner: Ie.current
  };
}
S.Fragment = he;
S.jsx = Q;
S.jsxs = Q;
Y.exports = S;
var X = Y.exports;
const {
  SvelteComponent: ye,
  assign: M,
  binding_callbacks: W,
  check_outros: Ee,
  children: Z,
  claim_element: V,
  claim_space: ge,
  component_subscribe: q,
  compute_slots: Re,
  create_slot: xe,
  detach: R,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Ue,
  get_slot_changes: Le,
  group_outros: Se,
  init: Fe,
  insert_hydration: U,
  safe_not_equal: ke,
  set_custom_element_data: ee,
  space: Oe,
  transition_in: L,
  transition_out: j,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: Te,
  onDestroy: je,
  setContext: De
} = window.__gradio__svelte__internal;
function H(e) {
  let o, r;
  const s = (
    /*#slots*/
    e[7].default
  ), n = xe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      o = $("svelte-slot"), n && n.c(), this.h();
    },
    l(t) {
      o = V(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = Z(o);
      n && n.l(l), l.forEach(R), this.h();
    },
    h() {
      ee(o, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      U(t, o, l), n && n.m(o, null), e[9](o), r = !0;
    },
    p(t, l) {
      n && n.p && (!r || l & /*$$scope*/
      64) && Pe(
        n,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? Le(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : Ue(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (L(n, t), r = !0);
    },
    o(t) {
      j(n, t), r = !1;
    },
    d(t) {
      t && R(o), n && n.d(t), e[9](null);
    }
  };
}
function Ne(e) {
  let o, r, s, n, t = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      o = $("react-portal-target"), r = Oe(), t && t.c(), s = z(), this.h();
    },
    l(l) {
      o = V(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(o).forEach(R), r = ge(l), t && t.l(l), s = z(), this.h();
    },
    h() {
      ee(o, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      U(l, o, a), e[8](o), U(l, r, a), t && t.m(l, a), U(l, s, a), n = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, a), a & /*$$slots*/
      16 && L(t, 1)) : (t = H(l), t.c(), L(t, 1), t.m(s.parentNode, s)) : t && (Se(), j(t, 1, 1, () => {
        t = null;
      }), Ee());
    },
    i(l) {
      n || (L(t), n = !0);
    },
    o(l) {
      j(t), n = !1;
    },
    d(l) {
      l && (R(o), R(r), R(s)), e[8](null), t && t.d(l);
    }
  };
}
function K(e) {
  const {
    svelteInit: o,
    ...r
  } = e;
  return r;
}
function Ae(e, o, r) {
  let s, n, {
    $$slots: t = {},
    $$scope: l
  } = o;
  const a = Re(t);
  let {
    svelteInit: i
  } = o;
  const b = x(K(o)), w = x();
  q(e, w, (d) => r(0, s = d));
  const f = x();
  q(e, f, (d) => r(1, n = d));
  const c = [], p = Te("$$ms-gr-react-wrapper"), {
    slotKey: u,
    slotIndex: _,
    subSlotIndex: F
  } = fe() || {}, k = i({
    parent: p,
    props: b,
    target: w,
    slot: f,
    slotKey: u,
    slotIndex: _,
    subSlotIndex: F,
    onDestroy(d) {
      c.push(d);
    }
  });
  De("$$ms-gr-react-wrapper", k), Ce(() => {
    b.set(K(o));
  }), je(() => {
    c.forEach((d) => d());
  });
  function m(d) {
    W[d ? "unshift" : "push"](() => {
      s = d, w.set(s);
    });
  }
  function O(d) {
    W[d ? "unshift" : "push"](() => {
      n = d, f.set(n);
    });
  }
  return e.$$set = (d) => {
    r(17, o = M(M({}, o), G(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, o = G(o), [s, n, w, f, a, i, l, t, m, O];
}
class Me extends ye {
  constructor(o) {
    super(), Fe(this, o, Ae, Ne, ke, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, C = window.ms_globals.tree;
function We(e) {
  function o(r) {
    const s = x(), n = new Me({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? C;
          return a.nodes = [...a.nodes, l], B({
            createPortal: T,
            node: C
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), B({
              createPortal: T,
              node: C
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(o);
    });
  });
}
function qe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function v(e) {
  return J(() => qe(e), [e]);
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((o, r) => {
    const s = e[r];
    return typeof s == "number" && !ze.includes(r) ? o[r] = s + "px" : o[r] = s, o;
  }, {}) : {};
}
function D(e) {
  const o = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return o.push(T(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: y.Children.toArray(e._reactElement.props.children).map((n) => {
        if (y.isValidElement(n) && n.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = D(n.props.el);
          return y.cloneElement(n, {
            ...n.props,
            el: l,
            children: [...y.Children.toArray(n.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: o
    };
  Object.keys(e.getEventListeners()).forEach((n) => {
    e.getEventListeners(n).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let n = 0; n < s.length; n++) {
    const t = s[n];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = D(t);
      o.push(...a), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: o
  };
}
function He(e, o) {
  e && (typeof e == "function" ? e(o) : e.current = o);
}
const Ke = ae(({
  slot: e,
  clone: o,
  className: r,
  style: s
}, n) => {
  const t = de(), [l, a] = ue([]);
  return pe(() => {
    var f;
    if (!t.current || !e)
      return;
    let i = e;
    function b() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), He(n, c), r && c.classList.add(...r.split(" ")), s) {
        const p = Ge(s);
        Object.keys(p).forEach((u) => {
          c.style[u] = p[u];
        });
      }
    }
    let w = null;
    if (o && window.MutationObserver) {
      let c = function() {
        var _;
        const {
          portals: p,
          clonedElement: u
        } = D(e);
        i = u, a(p), i.style.display = "contents", b(), (_ = t.current) == null || _.appendChild(i);
      };
      c(), w = new window.MutationObserver(() => {
        var p, u;
        (p = t.current) != null && p.contains(i) && ((u = t.current) == null || u.removeChild(i)), c();
      }), w.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", b(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var c, p;
      i.style.display = "", (c = t.current) != null && c.contains(i) && ((p = t.current) == null || p.removeChild(i)), w == null || w.disconnect();
    };
  }, [e, o, r, s, n]), y.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Be(e, o) {
  return e ? /* @__PURE__ */ X.jsx(Ke, {
    slot: e,
    clone: o == null ? void 0 : o.clone
  }) : null;
}
function g({
  key: e,
  setSlotParams: o,
  slots: r
}, s) {
  return r[e] ? (...n) => (o(e, n), Be(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function Je(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Qe = We(({
  slots: e,
  upload: o,
  showUploadList: r,
  progress: s,
  beforeUpload: n,
  customRequest: t,
  previewFile: l,
  isImageUrl: a,
  itemRender: i,
  iconRender: b,
  data: w,
  onChange: f,
  onValueChange: c,
  onRemove: p,
  fileList: u,
  setSlotParams: _,
  ...F
}) => {
  const k = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", m = Je(r), O = v(m.showPreviewIcon), d = v(m.showRemoveIcon), te = v(m.showDownloadIcon), N = v(n), oe = v(t), ne = v(s == null ? void 0 : s.format), re = v(l), se = v(a), le = v(i), ie = v(b), ce = v(w), A = J(() => (u == null ? void 0 : u.map((h) => ({
    ...h,
    name: h.orig_name || h.path,
    uid: h.url || h.path,
    status: "done"
  }))) || [], [u]);
  return /* @__PURE__ */ X.jsx(we, {
    ...F,
    fileList: A,
    data: ce || w,
    previewFile: re,
    isImageUrl: se,
    itemRender: e.itemRender ? g({
      slots: e,
      setSlotParams: _,
      key: "itemRender"
    }) : le,
    iconRender: e.iconRender ? g({
      slots: e,
      setSlotParams: _,
      key: "iconRender"
    }) : ie,
    onRemove: (h) => {
      p == null || p(h);
      const P = A.findIndex((I) => I.uid === h.uid), E = u.slice();
      E.splice(P, 1), c == null || c(E), f == null || f(E.map((I) => I.path));
    },
    beforeUpload: async (h, P) => {
      if (N && !await N(h, P))
        return !1;
      const E = (await o([h])).filter((I) => I);
      return c == null || c([...u, ...E]), f == null || f([...u.map((I) => I.path), ...E.map((I) => I.path)]), !1;
    },
    customRequest: oe,
    progress: s && {
      ...s,
      format: ne
    },
    showUploadList: k ? {
      ...m,
      showDownloadIcon: te || m.showDownloadIcon,
      showRemoveIcon: d || m.showRemoveIcon,
      showPreviewIcon: O || m.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? g({
        slots: e,
        setSlotParams: _,
        key: "showUploadList.downloadIcon"
      }) : m.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? g({
        slots: e,
        setSlotParams: _,
        key: "showUploadList.removeIcon"
      }) : m.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? g({
        slots: e,
        setSlotParams: _,
        key: "showUploadList.previewIcon"
      }) : m.previewIcon,
      extra: e["showUploadList.extra"] ? g({
        slots: e,
        setSlotParams: _,
        key: "showUploadList.extra"
      }) : m.extra
    } : r
  });
});
export {
  Qe as Upload,
  Qe as default
};
