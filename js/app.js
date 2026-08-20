/* Andaman Vice — app: data, day tabs, minute timeline, simulation, briefing panel. */
(async () => {
  const $ = (s) => document.querySelector(s);
  const CAT = { travel: "--cat-travel", activity: "--cat-activity", meal: "--cat-meal",
    sleep: "--cat-sleep", prep: "--cat-prep", buffer: "--cat-prep", scenic: "--cat-scenic" };
  const catColor = (c) =>
    getComputedStyle(document.documentElement).getPropertyValue(CAT[c] || "--cat-prep").trim();

  /* ---------- data ---------- */
  async function loadData() {
    if (window.TRIP_DATA) return window.TRIP_DATA;
    for (const u of ["/api/trip", "data.json"]) {
      try { const r = await fetch(u); if (r.ok) return await r.json(); } catch (e) {}
    }
    return null;
  }
  const D = await loadData();
  if (!D || !D.events || !D.events.length) {
    $("#boot").textContent = "NO TRIP DATA YET — RESEARCH IN PROGRESS";
    return;
  }

  const places = Object.fromEntries(D.places.map(p => [p.id, p]));
  const routesById = Object.fromEntries(D.routes.map(r => [r.id, r]));
  const ev = Object.fromEntries(D.events.map(e => [e.id, e]));
  const kids = {};
  for (const e of D.events) (kids[e.parent_id || "_root"] ||= []).push(e);
  for (const k in kids) kids[k].sort((a, b) => (a.seq || 0) - (b.seq || 0) ||
    (a.start_min || 0) - (b.start_min || 0));
  const isLeaf = (e) => !(kids[e.id] && kids[e.id].length);
  const leaves = D.events.filter(e => isLeaf(e) && e.start_min != null)
    .sort((a, b) => a.start_min - b.start_min);
  const meta = Object.fromEntries((D.meta || []).map(m => [m.k, m.v]));
  const T0 = new Date(D.t0.replace("+05:30", ""));  // treat as wall-clock IST
  const L0 = +meta.ledger_start_min || 0, L1 = +meta.ledger_end_min || 0;

  const fmtT = (m) => {
    const d = new Date(T0.getTime() + m * 60000);
    return String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
  };
  const fmtDur = (mins) => {
    const h = Math.floor(mins / 60), m = mins % 60;
    return (h ? h + "h " : "") + (m || !h ? m + "m" : "");
  };
  const INR = (v) => "₹" + Math.round(v).toLocaleString("en-IN");
  const dayStart = (day) => (day - 1) * 1440;   // day 1 = Sep 23 00:00 IST
  const DAYNAMES = ["WED 23", "THU 24", "FRI 25", "SAT 26", "SUN 27"];

  /* ---------- map ---------- */
  let geo = null;
  try { const r = await fetch("assets/map_geo.json"); if (r.ok) geo = await r.json(); } catch (e) {}
  if (!geo && window.MAP_GEO) geo = window.MAP_GEO;
  if (!geo) geo = { bbox: [92.3, 11.3, 93.2, 12.45], islands: [] };
  VMap.init($("#map"), geo, { onPlace: (id) => openPlace(id) });
  VMap.markers(D.places);
  VMap.routes(D.routes);

  /* ---------- day tabs ---------- */
  let curDay = 1, simMin = L0, playing = false, selBlock = null;
  const daysEl = $("#days");
  for (let d = 1; d <= 5; d++) {
    const b = document.createElement("button");
    b.className = "daytab"; b.innerHTML = `<span class="d">${d}</span>${DAYNAMES[d - 1]}`;
    b.onclick = () => setDay(d, true);
    daysEl.appendChild(b);
  }

  /* ---------- timeline ---------- */
  const strip = $("#tl-strip"), blocksEl = $("#tl-blocks"), cursor = $("#tl-cursor");
  function setDay(d, jump) {
    curDay = d;
    [...daysEl.children].forEach((b, i) => b.classList.toggle("on", i === d - 1));
    blocksEl.innerHTML = "";
    const s = dayStart(d), e = s + 1440;
    for (const lf of leaves) {
      if (lf.end_min <= s || lf.start_min >= e) continue;
      const a = Math.max(lf.start_min, s), b = Math.min(lf.end_min, e);
      const div = document.createElement("div");
      div.className = "blk";
      div.style.left = ((a - s) / 1440 * 100) + "%";
      div.style.width = (Math.max(b - a, 4) / 1440 * 100) + "%";
      div.style.background = catColor(lf.category);
      div.title = fmtT(lf.start_min) + "–" + fmtT(lf.end_min) + "  " + lf.title;
      div.dataset.id = lf.id;
      div.onclick = (evx) => { evx.stopPropagation(); setMinute(a); openBrief(lf.id); };
      blocksEl.appendChild(div);
    }
    const hrs = $("#tl-hours"); hrs.innerHTML = "";
    for (let h = 0; h <= 24; h += 3) {
      const sp = document.createElement("span");
      sp.style.left = (h / 24 * 100) + "%";
      sp.textContent = String(h).padStart(2, "0");
      hrs.appendChild(sp);
    }
    if (jump) setMinute(Math.max(s, Math.min(e - 1, Math.max(L0, s))));
  }
  strip.onclick = (e) => {
    const r = strip.getBoundingClientRect();
    setMinute(dayStart(curDay) + Math.round((e.clientX - r.left) / r.width * 1440));
  };

  function leafAt(t) {
    for (const lf of leaves) if (lf.start_min <= t && lf.end_min > t) return lf;
    return null;
  }

  function setMinute(t) {
    simMin = Math.max(L0, Math.min(L1 - 1, t));
    const d = Math.floor(simMin / 1440) + 1;
    if (d !== curDay && d >= 1 && d <= 5) setDay(d, false);
    cursor.style.left = ((simMin - dayStart(curDay)) / 1440 * 100) + "%";
    $("#tl-clock").textContent = fmtT(simMin);
    const lf = leafAt(simMin);
    if (lf) {
      $("#tl-now").textContent = lf.title;
      if (selBlock) selBlock.classList.remove("sel");
      selBlock = blocksEl.querySelector(`[data-id="${lf.id}"]`);
      if (selBlock) selBlock.classList.add("sel");
      // position marker
      const r = lf.route_id && routesById[lf.route_id];
      if (r && r.polyline) {
        const f = (simMin - lf.start_min) / (lf.end_min - lf.start_min);
        if (r.mode === "flight") {
          // plane glyph traces the projected flight line, nose on true bearing
          const pose = VMap.poseAlong(r, f);
          if (pose) {
            VMap.you(pose.lat, pose.lng, pose.heading, "flight");
            const ixz = places.ixz;   // keep plane + the islands in frame
            VMap.fitPoints([[pose.lat, pose.lng], [ixz.lat, ixz.lng]]);
          }
        } else {
          const p = VMap.pointAlong(r, f);
          if (p) VMap.you(p[0], p[1]);
        }
        VMap.activeRoute(lf.route_id); VMap.activePlace(null);
      } else {
        const pl = lf.place_id && places[lf.place_id];
        if (pl && pl.lat != null) VMap.you(pl.lat, pl.lng);
        VMap.activeRoute(null); VMap.activePlace(lf.place_id);
      }
    }
  }

  /* ---------- simulation ---------- */
  let lastTs = 0, raf = 0;
  const playBtn = $("#tl-play");
  playBtn.onclick = () => { playing ? stop() : play(); };
  function play() {
    playing = true; playBtn.textContent = "❚❚"; playBtn.classList.add("playing");
    lastTs = performance.now(); raf = requestAnimationFrame(tick);
  }
  function stop() {
    playing = false; playBtn.textContent = "▶"; playBtn.classList.remove("playing");
    cancelAnimationFrame(raf);
  }
  function tick(ts) {
    if (!playing) return;
    const sp = +$("#tl-speed").value;             // sim-minutes per real minute
    const dm = (ts - lastTs) / 60000 * sp;
    lastTs = ts;
    if (simMin + dm >= L1 - 1) { setMinute(L1 - 1); stop(); return; }
    setMinute(simMin + dm);
    raf = requestAnimationFrame(tick);
  }

  /* ---------- briefing panel ---------- */
  const brief = $("#brief");
  $("#brief-close").onclick = () => brief.classList.add("hidden");

  function watchBtn(url) {
    if (!url || !/youtu/.test(url)) return null;
    const a = document.createElement("a");
    a.className = "watch-btn"; a.href = url; a.target = "_blank"; a.rel = "noopener";
    a.textContent = "▶ WATCH THIS SPOT IN THE VIDEO";
    return a;
  }

  function receipts(container, e, r, pl) {
    // per-event receipts: facts that mention this place/route/activity + sources
    const keys = [];
    if (pl) keys.push(...pl.name.toLowerCase().split(/[^a-z]+/).filter(w => w.length > 3));
    if (r) keys.push(r.mode);
    keys.push(...e.title.toLowerCase().split(/[^a-z]+/).filter(w => w.length > 4));
    const uniq = [...new Set(keys)];
    const scored = (D.facts || []).map(f => {
      const hay = (f.topic + " " + f.value).toLowerCase();
      return [uniq.reduce((n, k) => n + (hay.includes(k) ? 1 : 0), 0), f];
    }).filter(([n]) => n >= 2).sort((a, b) => b[0] - a[0]).slice(0, 3);
    if (!scored.length && !e.source_url) return;
    const box = document.createElement("div");
    box.className = "receipts";
    box.innerHTML = "<div class='rc-h'>RECEIPTS</div>" + scored.map(([, f]) =>
      `<div class="rc"><span>${f.verified === "confirmed" ? "✅" : "📋"} ${f.value.slice(0, 150)}</span>
       ${f.source_url ? `<a href="${f.source_url}" target="_blank" rel="noopener">source</a>` : ""}</div>`
    ).join("");
    container.appendChild(box);
  }

  /* events at a place: direct place_id matches + travel legs touching it */
  function placeEvents(id) {
    return leaves.filter(l => l.place_id === id ||
      (l.route_id && routesById[l.route_id] &&
       (routesById[l.route_id].from_place === id || routesById[l.route_id].to_place === id)));
  }

  /* ---------- place card (map pin click) ---------- */
  function openPlace(id) {
    const pl = places[id]; if (!pl) return;
    const here0 = placeEvents(id);
    if (here0.length === 1) { openBrief(here0[0].id); return; }  // jump straight in
    $("#brief-nav").style.visibility = "hidden";                 // no stale ◀ ▶
    brief.classList.remove("hidden");
    const cr = $("#brief-crumbs"); cr.innerHTML = "";
    const s = document.createElement("span");
    s.className = "crumb"; s.textContent = "MAP · " + (pl.island || "").replace("_", " ");
    cr.appendChild(s);
    const b = $("#brief-body"); b.innerHTML = "";
    const h = document.createElement("h1"); h.textContent = pl.name; b.appendChild(h);
    const chip = document.createElement("span");
    chip.className = "cat-chip"; chip.textContent = pl.kind || "place";
    chip.style.background = catColor("scenic"); b.appendChild(chip);
    if (pl.photo) {
      const img = document.createElement("img");
      img.className = "photo"; img.src = pl.photo; img.alt = pl.name; b.appendChild(img);
    }
    if (pl.blurb) { const p = document.createElement("p"); p.textContent = pl.blurb; b.appendChild(p); }
    const wb = watchBtn(pl.source_url); if (wb) b.appendChild(wb);
    const here = placeEvents(id);
    const kd = document.createElement("div"); kd.className = "kids";
    if (here.length) {
      const hh = document.createElement("p"); hh.className = "mut";
      hh.textContent = "On the itinerary here:"; b.appendChild(hh);
      for (const k of here) {
        const row = document.createElement("div"); row.className = "kid";
        row.innerHTML = `<span class="t">D${Math.floor(k.start_min / 1440) + 1} ${fmtT(k.start_min)}</span>
          <span class="n">${k.title}</span><span class="arr">▸</span>`;
        row.onclick = () => openBrief(k.id);
        kd.appendChild(row);
      }
    } else {
      const p = document.createElement("p"); p.className = "mut";
      p.textContent = "Not scheduled on this trip — kept on the map for orientation (see the blurb for why/when it's worth it).";
      b.appendChild(p);
    }
    b.appendChild(kd);
    VMap.activePlace(id); VMap.activeRoute(null);
    if (pl.lat != null) VMap.focusLatLng(pl.lat, pl.lng, 5);
  }
  function crumbs(e) {
    const c = [];
    let cur = e;
    while (cur) { c.unshift(cur); cur = cur.parent_id ? ev[cur.parent_id] : null; }
    return c;
  }
  function openBrief(id) {
    const e = ev[id]; if (!e) return;
    brief.classList.remove("hidden");
    const cr = $("#brief-crumbs"); cr.innerHTML = "";
    for (const c of crumbs(e)) {
      const s = document.createElement("span");
      s.className = "crumb"; s.textContent = c.title;
      if (c.id !== e.id) s.onclick = () => openBrief(c.id);
      cr.appendChild(s);
    }
    const b = $("#brief-body"); b.innerHTML = "";
    const h = document.createElement("h1"); h.textContent = e.title; b.appendChild(h);
    if (e.category) {
      const chip = document.createElement("span");
      chip.className = "cat-chip"; chip.textContent = e.category;
      chip.style.background = catColor(e.category); b.appendChild(chip);
    }
    const r = e.route_id && routesById[e.route_id];
    const pl = e.place_id && places[e.place_id];
    const stats = [];
    if (e.start_min != null) {
      stats.push(["Start", fmtT(e.start_min)], ["End", fmtT(e.end_min)],
        ["Duration", fmtDur(e.end_min - e.start_min)]);
    }
    if (r) {
      if (r.distance_km) stats.push(["Distance", r.distance_km + " km"]);
      if (r.duration_min) stats.push(["Travel time", fmtDur(r.duration_min)]);
      if (r.fuel_l) stats.push(["Fuel (2 scooters)",
        r.fuel_l.toFixed(2) + " L <small>" + INR(r.fuel_cost_inr || 0) + "</small>"]);
      stats.push(["Mode", r.mode]);
    }
    if (e.cost_inr) stats.push(["Cost (3 pax)", INR(e.cost_inr)]);
    const sg = document.createElement("div"); sg.className = "statgrid";
    for (const [k, v] of stats) {
      const d = document.createElement("div"); d.className = "stat";
      d.innerHTML = `<div class="k">${k}</div><div class="v">${v}</div>`;
      sg.appendChild(d);
    }
    b.appendChild(sg);
    if (pl && pl.photo) {
      const img = document.createElement("img");
      img.className = "photo"; img.src = pl.photo; img.alt = pl.name;
      b.appendChild(img);
    }
    for (const txt of [e.details, pl && pl.blurb]) {
      if (!txt) continue;
      for (const para of String(txt).split(/\n\n+/)) {
        const p = document.createElement("p"); p.textContent = para; b.appendChild(p);
      }
    }
    if (e.cost_note) {
      const p = document.createElement("p"); p.className = "mut";
      p.textContent = "Cost detail: " + e.cost_note; b.appendChild(p);
    }
    if (e.tips) {
      const t = document.createElement("div"); t.className = "tips";
      t.textContent = e.tips; b.appendChild(t);
    }
    if (kids[e.id]) {
      const kd = document.createElement("div"); kd.className = "kids";
      for (const k of kids[e.id]) {
        const row = document.createElement("div"); row.className = "kid";
        row.innerHTML = `<span class="t">${k.start_min != null ? fmtT(k.start_min) : ""}</span>
          <span class="n">${k.title}</span><span class="arr">▸</span>`;
        row.onclick = () => openBrief(k.id);
        kd.appendChild(row);
      }
      b.appendChild(kd);
    }
    const wb = watchBtn(pl && pl.source_url); if (wb) b.appendChild(wb);
    receipts(b, e, r, pl);
    // prev/next across the chronological leaf sequence
    const li = leaves.findIndex(l => l.id === e.id);
    const nav = $("#brief-nav");
    nav.style.visibility = li >= 0 ? "visible" : "hidden";
    if (li >= 0) {
      $("#bn-prev").disabled = li <= 0;
      $("#bn-next").disabled = li >= leaves.length - 1;
      $("#bn-prev").onclick = () => li > 0 && openBrief(leaves[li - 1].id);
      $("#bn-next").onclick = () => li < leaves.length - 1 && openBrief(leaves[li + 1].id);
    }
    // focus map
    if (r && r.polyline) {
      VMap.activeRoute(r.id);
      const p = VMap.pointAlong(r, 0.5); if (p) VMap.focusLatLng(p[0], p[1], 2);
    } else if (pl && pl.lat != null) {
      VMap.activePlace(pl.id); VMap.focusLatLng(pl.lat, pl.lng, 5);
    }
    if (e.start_min != null && (simMin < e.start_min || simMin >= e.end_min))
      setMinute(e.start_min);
  }

  /* ---------- sheets ---------- */
  const sheets = { legend: $("#legend"), budget: $("#budget"), intel: $("#intel"), kit: $("#kit") };
  function toggleSheet(name) {
    for (const k in sheets) sheets[k].classList.toggle("hidden", k !== name || !sheets[k].classList.contains("hidden"));
  }
  $("#btn-legend").onclick = () => toggleSheet("legend");
  $("#btn-budget").onclick = () => toggleSheet("budget");
  $("#btn-intel").onclick = () => toggleSheet("intel");
  $("#btn-kit").onclick = () => toggleSheet("kit");
  $("#btn-tilt").onclick = () => {
    $("#tilt").classList.toggle("on");
    $("#btn-tilt").classList.toggle("on");
  };

  // legend
  sheets.legend.innerHTML = "<h2>Legend</h2>" +
    Object.entries({ travel: "Travel leg", activity: "Mission / activity", meal: "Food stop",
      sleep: "Sleep", prep: "Prep · buffer · check-in", scenic: "Scenic / sunset / sunrise" })
      .map(([c, l]) => `<div class="legend-row"><span class="swatch" style="background:${catColor(c)}"></span>${l}</div>`)
      .join("") +
    `<h3>Map</h3>
     <div class="legend-row"><span class="swatch" style="background:var(--route)"></span>Neon line = your route (animated = live leg)</div>
     <div class="legend-row"><span class="swatch" style="background:var(--sand)"></span>Chips = places (letter = kind: B beach, J jetty, A airport, H hotel, R restaurant…)</div>
     <p class="mut">Scroll / pinch to zoom · drag to pan · click any chip or timeline block for the mission briefing.</p>`;

  // budget rollup
  function buildBudget() {
    const rows = leaves.filter(e => e.cost_inr > 0);
    const byDay = {}; let total = 0;
    for (const e of rows) {
      const d = Math.floor(e.start_min / 1440) + 1;
      (byDay[d] ||= []).push(e); total += e.cost_inr;
    }
    let html = "<h2>Budget — crew of 3</h2>";
    for (let d = 1; d <= 5; d++) {
      if (!byDay[d]) continue;
      const sub = byDay[d].reduce((s, e) => s + e.cost_inr, 0);
      html += `<h3>Day ${d} · ${DAYNAMES[d - 1]} — ${INR(sub)}</h3><table>` +
        byDay[d].map(e => `<tr><td>${fmtT(e.start_min)}</td><td>${e.title}</td>
          <td class="n">${INR(e.cost_inr)}</td></tr>`).join("") + "</table>";
    }
    html += `<h3>Total</h3><table><tr><th>Grand total (3 pax, ex-shopping)</th>
      <th class="n">${INR(total)}</th></tr></table>
      <p class="mut">Every figure carries its source in the event briefing. Prices captured live; recheck before paying.</p>`;
    sheets.budget.innerHTML = html;
  }
  buildBudget();

  // intel (facts & verification)
  function buildIntel() {
    const badge = (v) => ({ confirmed: "✅", reported: "📋", unverifiable: "❓" }[v] || "🛠");
    sheets.intel.innerHTML = "<h2>Intel — verified facts</h2><table>" +
      (D.facts || []).map(f => `<tr><td>${badge(f.verified)}</td>
        <td>${f.topic}<br><span class="mut">${f.value}</span><br>
        <a class="mut" href="${f.source_url}" target="_blank" rel="noopener">source</a>
        <span class="mut"> · ${f.as_of || ""}</span></td></tr>`).join("") + "</table>";
  }
  buildIntel();

  // kit (packing) — authored into meta.kit as JSON [[section,[items]],...]
  function buildKit() {
    let kit = [];
    try { kit = JSON.parse(meta.kit || "[]"); } catch (e) {}
    sheets.kit.innerHTML = "<h2>Kit — what to wear &amp; carry</h2>" +
      (kit.length ? kit.map(([sec, items]) =>
        `<h3>${sec}</h3><ul>` + items.map(i => `<li>${i}</li>`).join("") + "</ul>").join("")
        : "<p class='mut'>Packing list lands after weather research.</p>");
  }
  buildKit();

  /* ---------- boot ---------- */
  $("#boot").remove();
  setDay(1, false);
  setMinute(L0);
  if ("serviceWorker" in navigator && location.protocol.startsWith("http"))
    navigator.serviceWorker.register("sw.js").catch(() => {});
})();
