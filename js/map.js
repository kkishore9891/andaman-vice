/* VMap — neon SVG map: real coastline polys, markers, routes, sim marker, pan/zoom. */
const VMap = (() => {
  const NS = "http://www.w3.org/2000/svg";
  let svg, gIsl, gRoute, gMk, gYou, proj, vb, cb = {};
  let W = 1000, H = 1000;

  function el(n, at, parent) {
    const e = document.createElementNS(NS, n);
    for (const k in at) e.setAttribute(k, at[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  function makeProj(bbox) {
    const [x0, y0, x1, y1] = bbox;                 // lon/lat
    const midLat = (y0 + y1) / 2;
    const kx = Math.cos(midLat * Math.PI / 180);
    const aspect = ((x1 - x0) * kx) / (y1 - y0);
    W = 1000; H = W / aspect;
    return (lat, lng) => [
      (lng - x0) / (x1 - x0) * W,
      (y1 - lat) / (y1 - y0) * H,
    ];
  }

  function init(svgEl, geo, opts = {}) {
    svg = svgEl; cb = opts;
    // pad bbox 4%
    const b = geo.bbox.slice();
    const px = (b[2] - b[0]) * 0.04, py = (b[3] - b[1]) * 0.04;
    proj = makeProj([b[0] - px, b[1] - py, b[2] + px, b[3] + py]);
    vb = { x: 0, y: 0, w: W, h: H };
    apply();
    svg.innerHTML = "";
    const gWater = el("g", {}, svg);
    gIsl = el("g", {}, svg);
    gRoute = el("g", {}, svg);
    gMk = el("g", {}, svg);
    gYou = el("g", {}, svg);
    // sea name
    el("text", { class: "water-name", x: W * 0.55, y: H * 0.5, "font-size": W / 34 },
      gWater).textContent = "ANDAMAN SEA";
    for (const isl of geo.islands) {
      const d = isl.points.map((p, i) => {
        const [x, y] = proj(p[1], p[0]);
        return (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1);
      }).join("") + "Z";
      el("path", { class: "island", d }, gIsl);
    }
    bindPanZoom();
  }

  function apply() {
    svg.setAttribute("viewBox", `${vb.x} ${vb.y} ${vb.w} ${vb.h}`);
    // keep marker/label sizes readable at any zoom
    const s = vb.w / W;
    svg.style.setProperty("--zs", s);
    for (const t of svg.querySelectorAll(".mk circle"))
      t.setAttribute("r", 8 * s + "");
    for (const t of svg.querySelectorAll(".mk text"))
      t.setAttribute("font-size", 9 * s + "");
    for (const t of svg.querySelectorAll(".mklabel"))
      t.setAttribute("font-size", 10.5 * s + "");
    for (const t of svg.querySelectorAll(".you"))
      t.setAttribute("r", 5.5 * s + "");
  }

  function markers(places) {
    gMk.innerHTML = "";
    for (const p of places) {
      if (p.lat == null || p.island === "chennai" || p.island === "air") continue;
      const [x, y] = proj(p.lat, p.lng);
      const g = el("g", { class: "mk", "data-id": p.id }, gMk);
      el("circle", { cx: x, cy: y, r: 8 }, g);
      const ic = el("text", { x, y: y + 3 }, g);
      ic.textContent = (p.kind || "?")[0].toUpperCase();
      const lb = el("text", { class: "mklabel", x: x + 12, y: y + 4 }, g);
      lb.textContent = p.name;
      g.addEventListener("click", () => cb.onPlace && cb.onPlace(p.id));
    }
    apply();
  }

  function routes(rs) {
    gRoute.innerHTML = "";
    for (const r of rs) {
      let pts = [];
      try { pts = JSON.parse(r.polyline || "[]"); } catch (e) {}
      if (pts.length < 2) continue;
      const d = pts.map((p, i) => {
        const [x, y] = proj(p[0], p[1]);
        return (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1);
      }).join("");
      const cls = "route" + (["ferry", "boat", "flight"].includes(r.mode) ? " sea" : "");
      el("path", { class: cls, d, "data-id": r.id }, gRoute);
    }
  }

  function activeRoute(id) {
    for (const p of gRoute.querySelectorAll(".route"))
      p.classList.toggle("active", p.dataset.id === id);
  }
  function activePlace(id) {
    for (const m of gMk.querySelectorAll(".mk"))
      m.classList.toggle("active", m.dataset.id === id);
  }

  function you(lat, lng) {
    gYou.innerHTML = "";
    if (lat == null) return;
    const [x, y] = proj(lat, lng);
    el("circle", { class: "you-ring", cx: x, cy: y, r: 6 }, gYou);
    el("circle", { class: "you", cx: x, cy: y, r: 5.5 }, gYou);
    apply();
  }

  function focusLatLng(lat, lng, zoom = 3) {
    const [x, y] = proj(lat, lng);
    const w = W / zoom, h = H / zoom;
    vb = { x: x - w / 2, y: y - h / 2, w, h };
    apply();
  }
  function focusAll() { vb = { x: 0, y: 0, w: W, h: H }; apply(); }

  /* --- interpolate along a route polyline, t in 0..1 → [lat,lng] --- */
  function pointAlong(r, t) {
    let pts = [];
    try { pts = JSON.parse(r.polyline || "[]"); } catch (e) { return null; }
    if (pts.length < 2) return null;
    const segs = []; let total = 0;
    for (let i = 1; i < pts.length; i++) {
      const d = Math.hypot(pts[i][0] - pts[i - 1][0],
        (pts[i][1] - pts[i - 1][1]) * Math.cos(pts[i][0] * Math.PI / 180));
      segs.push(d); total += d;
    }
    let want = t * total;
    for (let i = 0; i < segs.length; i++) {
      if (want <= segs[i] || i === segs.length - 1) {
        const f = segs[i] ? want / segs[i] : 0;
        return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f];
      }
      want -= segs[i];
    }
    return pts[pts.length - 1];
  }

  /* --- pan / zoom --- */
  function bindPanZoom() {
    let drag = null, pinch = null;
    svg.addEventListener("wheel", (e) => {
      e.preventDefault();
      const f = e.deltaY > 0 ? 1.15 : 1 / 1.15;
      zoomAt(e.clientX, e.clientY, f);
    }, { passive: false });
    svg.addEventListener("pointerdown", (e) => {
      svg.setPointerCapture(e.pointerId);
      drag = { x: e.clientX, y: e.clientY, vb: { ...vb } };
    });
    svg.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const r = svg.getBoundingClientRect();
      const sc = vb.w / r.width;
      vb.x = drag.vb.x - (e.clientX - drag.x) * sc;
      vb.y = drag.vb.y - (e.clientY - drag.y) * sc;
      apply();
    });
    svg.addEventListener("pointerup", () => drag = null);
    svg.addEventListener("touchstart", (e) => {
      if (e.touches.length === 2) {
        drag = null;
        pinch = { d: dist(e.touches), vb: { ...vb } };
      }
    }, { passive: true });
    svg.addEventListener("touchmove", (e) => {
      if (pinch && e.touches.length === 2) {
        const f = pinch.d / dist(e.touches);
        const cx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const cy = (e.touches[0].clientY + e.touches[1].clientY) / 2;
        vb = { ...pinch.vb };
        zoomAt(cx, cy, f);
      }
    }, { passive: true });
    svg.addEventListener("touchend", () => pinch = null);
    function dist(t) { return Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY); }
  }
  function zoomAt(cx, cy, f) {
    const r = svg.getBoundingClientRect();
    const mx = vb.x + (cx - r.left) / r.width * vb.w;
    const my = vb.y + (cy - r.top) / r.height * vb.h;
    let w = vb.w * f;
    w = Math.max(W / 40, Math.min(W * 1.6, w));
    const h = w * vb.h / vb.w;
    vb = { x: mx - (mx - vb.x) * (w / vb.w), y: my - (my - vb.y) * (h / vb.h), w, h };
    apply();
  }

  return { init, markers, routes, activeRoute, activePlace, you,
           focusLatLng, focusAll, pointAlong, proj: (a, b) => proj(a, b) };
})();
