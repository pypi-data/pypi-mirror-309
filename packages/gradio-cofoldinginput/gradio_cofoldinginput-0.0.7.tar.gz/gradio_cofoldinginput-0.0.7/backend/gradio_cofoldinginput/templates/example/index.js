const {
  SvelteComponent: P,
  add_iframe_resize_listener: W,
  add_render_callback: j,
  append_hydration: d,
  attr: A,
  binding_callbacks: F,
  children: E,
  claim_element: g,
  claim_space: D,
  claim_text: b,
  destroy_each: G,
  detach: u,
  element: k,
  empty: z,
  ensure_array_like: V,
  get_svelte_dataset: J,
  init: K,
  insert_hydration: m,
  noop: R,
  safe_not_equal: O,
  set_data: w,
  space: S,
  text: p,
  toggle_class: M
} = window.__gradio__svelte__internal, { onMount: Q } = window.__gradio__svelte__internal;
function q(a, e, n) {
  const i = a.slice();
  return i[8] = e[n], i;
}
function C(a) {
  let e, n, i, l, t, s = (
    /*value*/
    a[0].covMods.length + ""
  ), f, c;
  function _(r, L) {
    return (
      /*value*/
      r[0].chains.length > 1 ? Y : X
    );
  }
  let y = _(a), o = y(a), I = V(
    /*value*/
    a[0].chains
  ), v = [];
  for (let r = 0; r < I.length; r += 1)
    v[r] = U(q(a, I, r));
  return {
    c() {
      o.c(), e = S(), n = k("ul");
      for (let r = 0; r < v.length; r += 1)
        v[r].c();
      i = S(), l = k("ul"), t = k("li"), f = p(s), c = p(" covalent modifications");
    },
    l(r) {
      o.l(r), e = D(r), n = g(r, "UL", {});
      var L = E(n);
      for (let B = 0; B < v.length; B += 1)
        v[B].l(L);
      L.forEach(u), i = D(r), l = g(r, "UL", {});
      var h = E(l);
      t = g(h, "LI", {});
      var N = E(t);
      f = b(N, s), c = b(N, " covalent modifications"), N.forEach(u), h.forEach(u);
    },
    m(r, L) {
      o.m(r, L), m(r, e, L), m(r, n, L);
      for (let h = 0; h < v.length; h += 1)
        v[h] && v[h].m(n, null);
      m(r, i, L), m(r, l, L), d(l, t), d(t, f), d(t, c);
    },
    p(r, L) {
      if (y === (y = _(r)) && o ? o.p(r, L) : (o.d(1), o = y(r), o && (o.c(), o.m(e.parentNode, e))), L & /*value, undefined*/
      1) {
        I = V(
          /*value*/
          r[0].chains
        );
        let h;
        for (h = 0; h < I.length; h += 1) {
          const N = q(r, I, h);
          v[h] ? v[h].p(N, L) : (v[h] = U(N), v[h].c(), v[h].m(n, null));
        }
        for (; h < v.length; h += 1)
          v[h].d(1);
        v.length = I.length;
      }
      L & /*value*/
      1 && s !== (s = /*value*/
      r[0].covMods.length + "") && w(f, s);
    },
    d(r) {
      r && (u(e), u(n), u(i), u(l)), o.d(r), G(v, r);
    }
  };
}
function X(a) {
  let e, n, i = (
    /*value*/
    a[0].chains.length + ""
  ), l, t, s;
  return {
    c() {
      e = k("b"), n = p("Input composed of "), l = p(i), t = p(" chain "), s = k("br");
    },
    l(f) {
      e = g(f, "B", {});
      var c = E(e);
      n = b(c, "Input composed of "), l = b(c, i), t = b(c, " chain "), c.forEach(u), s = g(f, "BR", {});
    },
    m(f, c) {
      m(f, e, c), d(e, n), d(e, l), d(e, t), m(f, s, c);
    },
    p(f, c) {
      c & /*value*/
      1 && i !== (i = /*value*/
      f[0].chains.length + "") && w(l, i);
    },
    d(f) {
      f && (u(e), u(s));
    }
  };
}
function Y(a) {
  let e, n, i = (
    /*value*/
    a[0].chains.length + ""
  ), l, t, s, f;
  return {
    c() {
      e = k("b"), n = p("Input composed of "), l = p(i), t = p(" chains"), s = S(), f = k("br");
    },
    l(c) {
      e = g(c, "B", {});
      var _ = E(e);
      n = b(_, "Input composed of "), l = b(_, i), t = b(_, " chains"), _.forEach(u), s = D(c), f = g(c, "BR", {});
    },
    m(c, _) {
      m(c, e, _), d(e, n), d(e, l), d(e, t), m(c, s, _), m(c, f, _);
    },
    p(c, _) {
      _ & /*value*/
      1 && i !== (i = /*value*/
      c[0].chains.length + "") && w(l, i);
    },
    d(c) {
      c && (u(e), u(s), u(f));
    }
  };
}
function H(a) {
  let e, n, i = (
    /*val*/
    a[8].class + ""
  ), l, t, s = (
    /*val*/
    a[8].sequence.length + ""
  ), f, c;
  return {
    c() {
      e = k("li"), n = k("div"), l = p(i), t = S(), f = p(s), c = p(" residues"), this.h();
    },
    l(_) {
      e = g(_, "LI", {});
      var y = E(e);
      n = g(y, "DIV", { class: !0 });
      var o = E(n);
      l = b(o, i), t = D(o), f = b(o, s), c = b(o, " residues"), o.forEach(u), y.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-1r1gryw");
    },
    m(_, y) {
      m(_, e, y), d(e, n), d(n, l), d(n, t), d(n, f), d(n, c);
    },
    p(_, y) {
      y & /*value*/
      1 && i !== (i = /*val*/
      _[8].class + "") && w(l, i), y & /*value*/
      1 && s !== (s = /*val*/
      _[8].sequence.length + "") && w(f, s);
    },
    d(_) {
      _ && u(e);
    }
  };
}
function T(a) {
  let e;
  function n(t, s) {
    return (
      /*val*/
      t[8].name != null ? $ : (
        /*val*/
        t[8].smiles != null ? x : Z
      )
    );
  }
  let i = n(a), l = i(a);
  return {
    c() {
      l.c(), e = z();
    },
    l(t) {
      l.l(t), e = z();
    },
    m(t, s) {
      l.m(t, s), m(t, e, s);
    },
    p(t, s) {
      i === (i = n(t)) && l ? l.p(t, s) : (l.d(1), l = i(t), l && (l.c(), l.m(e.parentNode, e)));
    },
    d(t) {
      t && u(e), l.d(t);
    }
  };
}
function Z(a) {
  let e, n = '<div class="svelte-1r1gryw">Ligand</div>';
  return {
    c() {
      e = k("li"), e.innerHTML = n;
    },
    l(i) {
      e = g(i, "LI", { "data-svelte-h": !0 }), J(e) !== "svelte-z73xb2" && (e.innerHTML = n);
    },
    m(i, l) {
      m(i, e, l);
    },
    p: R,
    d(i) {
      i && u(e);
    }
  };
}
function x(a) {
  let e, n, i, l = (
    /*val*/
    a[8].smiles.length + ""
  ), t, s;
  return {
    c() {
      e = k("li"), n = k("div"), i = p("Ligand SMILES with "), t = p(l), s = p(" atoms"), this.h();
    },
    l(f) {
      e = g(f, "LI", {});
      var c = E(e);
      n = g(c, "DIV", { class: !0 });
      var _ = E(n);
      i = b(_, "Ligand SMILES with "), t = b(_, l), s = b(_, " atoms"), _.forEach(u), c.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-1r1gryw");
    },
    m(f, c) {
      m(f, e, c), d(e, n), d(n, i), d(n, t), d(n, s);
    },
    p(f, c) {
      c & /*value*/
      1 && l !== (l = /*val*/
      f[8].smiles.length + "") && w(t, l);
    },
    d(f) {
      f && u(e);
    }
  };
}
function $(a) {
  let e, n, i, l = (
    /*val*/
    a[8].name + ""
  ), t;
  return {
    c() {
      e = k("li"), n = k("div"), i = p("Ligand "), t = p(l), this.h();
    },
    l(s) {
      e = g(s, "LI", {});
      var f = E(e);
      n = g(f, "DIV", { class: !0 });
      var c = E(n);
      i = b(c, "Ligand "), t = b(c, l), c.forEach(u), f.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-1r1gryw");
    },
    m(s, f) {
      m(s, e, f), d(e, n), d(n, i), d(n, t);
    },
    p(s, f) {
      f & /*value*/
      1 && l !== (l = /*val*/
      s[8].name + "") && w(t, l);
    },
    d(s) {
      s && u(e);
    }
  };
}
function U(a) {
  let e = ["protein", "DNA", "RNA"].includes(
    /*val*/
    a[8].class
  ), n, i, l = e && H(a), t = (
    /*val*/
    a[8].class == "ligand" && T(a)
  );
  return {
    c() {
      l && l.c(), n = S(), t && t.c(), i = z();
    },
    l(s) {
      l && l.l(s), n = D(s), t && t.l(s), i = z();
    },
    m(s, f) {
      l && l.m(s, f), m(s, n, f), t && t.m(s, f), m(s, i, f);
    },
    p(s, f) {
      f & /*value*/
      1 && (e = ["protein", "DNA", "RNA"].includes(
        /*val*/
        s[8].class
      )), e ? l ? l.p(s, f) : (l = H(s), l.c(), l.m(n.parentNode, n)) : l && (l.d(1), l = null), /*val*/
      s[8].class == "ligand" ? t ? t.p(s, f) : (t = T(s), t.c(), t.m(i.parentNode, i)) : t && (t.d(1), t = null);
    },
    d(s) {
      s && (u(n), u(i)), l && l.d(s), t && t.d(s);
    }
  };
}
function ee(a) {
  let e, n, i = (
    /*value*/
    a[0] && C(a)
  );
  return {
    c() {
      e = k("div"), i && i.c(), this.h();
    },
    l(l) {
      e = g(l, "DIV", { class: !0 });
      var t = E(e);
      i && i.l(t), t.forEach(u), this.h();
    },
    h() {
      A(e, "class", "svelte-1r1gryw"), j(() => (
        /*div_elementresize_handler*/
        a[5].call(e)
      )), M(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), M(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), M(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(l, t) {
      m(l, e, t), i && i.m(e, null), n = W(
        e,
        /*div_elementresize_handler*/
        a[5].bind(e)
      ), a[6](e);
    },
    p(l, [t]) {
      /*value*/
      l[0] ? i ? i.p(l, t) : (i = C(l), i.c(), i.m(e, null)) : i && (i.d(1), i = null), t & /*type*/
      2 && M(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && M(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && M(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: R,
    o: R,
    d(l) {
      l && u(e), i && i.d(), n(), a[6](null);
    }
  };
}
function le(a, e, n) {
  let { value: i } = e, { type: l } = e, { selected: t = !1 } = e, s, f;
  function c(o, I) {
    !o || !I || (f.style.setProperty("--local-text-width", `${I < 150 ? I : 200}px`), n(4, f.style.whiteSpace = "unset", f));
  }
  Q(() => {
    c(f, s);
  });
  function _() {
    s = this.clientWidth, n(3, s);
  }
  function y(o) {
    F[o ? "unshift" : "push"](() => {
      f = o, n(4, f);
    });
  }
  return a.$$set = (o) => {
    "value" in o && n(0, i = o.value), "type" in o && n(1, l = o.type), "selected" in o && n(2, t = o.selected);
  }, [i, l, t, s, f, _, y];
}
class te extends P {
  constructor(e) {
    super(), K(this, e, le, ee, O, { value: 0, type: 1, selected: 2 });
  }
}
export {
  te as default
};
