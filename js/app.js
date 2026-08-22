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
    b.onclick = () => { setDay(d, true); openDayAgenda(d); };
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
    // label only today's places while zoomed out (declutters dense clusters)
    const todays = new Set();
    for (const lf of leaves) {
      if (lf.end_min <= s || lf.start_min >= e) continue;
      if (lf.place_id) todays.add(lf.place_id);
      const rr = lf.route_id && routesById[lf.route_id];
      if (rr) { todays.add(rr.from_place); todays.add(rr.to_place); }
    }
    VMap.setDayPlaces(todays);
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
          // plane glyph traces the drawn approach corridor, nose on true bearing
          const pose = VMap.poseAlong(r, f);
          if (pose) VMap.you(pose.lat, pose.lng, pose.heading, "flight");
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

  function mapsBtn(pl) {
    if (!pl || !pl.maps_url) return null;
    const a = document.createElement("a");
    a.className = "watch-btn maps-btn"; a.href = pl.maps_url;
    a.target = "_blank"; a.rel = "noopener";
    a.textContent = "📍 OPEN IN GOOGLE MAPS";
    return a;
  }

  function linkRow(...btns) {
    const row = document.createElement("div");
    row.className = "linkrow";
    let any = false;
    for (const b of btns) if (b) { row.appendChild(b); any = true; }
    return any ? row : null;
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

  /* ---------- whole-day agenda (what a date tap opens) ---------- */
  function dayLeaves(day) {
    const s = dayStart(day), e = s + 1440;
    return leaves.filter(l => l.end_min > s && l.start_min < e);
  }

  function openDayAgenda(day) {
    const parent = ev["d" + day];
    brief.classList.remove("hidden");
    $("#brief-nav").style.visibility = "hidden";
    const cr = $("#brief-crumbs"); cr.innerHTML = "";
    const s = document.createElement("span");
    s.className = "crumb";
    s.textContent = `DAY ${day} · ${DAYNAMES[day - 1]}`;
    cr.appendChild(s);

    const b = $("#brief-body"); b.innerHTML = "";
    const h = document.createElement("h1");
    h.textContent = (parent && parent.title) || `Day ${day}`;
    b.appendChild(h);
    if (parent && parent.details) {
      const p = document.createElement("p"); p.className = "theme";
      p.textContent = parent.details; b.appendChild(p);
    }

    const list = dayLeaves(day);
    const cost = list.reduce((n, e) => n + (e.cost_inr || 0), 0);
    const sleep = list.filter(e => e.category === "sleep")
      .reduce((n, e) => n + (e.end_min - e.start_min), 0);
    const sg = document.createElement("div"); sg.className = "statgrid";
    for (const [k, v] of [["Events", list.length], ["Day cost (3 pax)", INR(cost)],
                          ["Sleep", fmtDur(sleep)], ["Date", DAYNAMES[day - 1] + " Sep 2026"]]) {
      const d = document.createElement("div"); d.className = "stat";
      d.innerHTML = `<div class="k">${k}</div><div class="v">${v}</div>`;
      sg.appendChild(d);
    }
    b.appendChild(sg);

    // the whole day, top to bottom — no next-next-next
    const ag = document.createElement("div"); ag.className = "agenda";
    for (const lf of list) {
      const row = document.createElement("div");
      row.className = "ag-row cat-" + (lf.category || "prep");
      const pl = lf.place_id && places[lf.place_id];
      const r = lf.route_id && routesById[lf.route_id];
      const bits = [];
      if (r && r.distance_km) bits.push(`${r.distance_km} km`);
      if (lf.cost_inr) bits.push(INR(lf.cost_inr));
      if (pl) bits.push(pl.name);
      row.innerHTML =
        `<div class="ag-time">${fmtT(lf.start_min)}<span>${fmtDur(lf.end_min - lf.start_min)}</span></div>
         <div class="ag-main">
           <div class="ag-title">${lf.title}</div>
           ${bits.length ? `<div class="ag-meta">${bits.join(" · ")}</div>` : ""}
           ${lf.details ? `<div class="ag-note">${String(lf.details).slice(0, 150)}${String(lf.details).length > 150 ? "…" : ""}</div>` : ""}
         </div><div class="arr">▸</div>`;
      row.onclick = () => { setMinute(lf.start_min); openBrief(lf.id); };
      ag.appendChild(row);
    }
    b.appendChild(ag);
    b.scrollTop = 0;
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
    const lr = linkRow(mapsBtn(pl), watchBtn(pl.source_url)); if (lr) b.appendChild(lr);
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
      // the day crumb reopens the whole-day agenda, not a single event
      if (c.id !== e.id) {
        s.onclick = /^d\d+$/.test(c.id)
          ? () => openDayAgenda(+c.id.slice(1))
          : () => openBrief(c.id);
      }
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
    const dest = pl || (r && places[r.to_place]);
    const lr = linkRow(mapsBtn(dest), watchBtn(dest && dest.source_url));
    if (lr) b.appendChild(lr);
    receipts(b, e, r, pl);
    // prev/next across the chronological leaf sequence
    const li = leaves.findIndex(l => l.id === e.id);
    const nav = $("#brief-nav");
    nav.style.visibility = li >= 0 ? "visible" : "hidden";
    if (li >= 0) {
      const day = Math.floor(e.start_min / 1440) + 1;
      $("#bn-prev").disabled = li <= 0;
      $("#bn-next").disabled = li >= leaves.length - 1;
      $("#bn-prev").onclick = () => li > 0 && openBrief(leaves[li - 1].id);
      $("#bn-next").onclick = () => li < leaves.length - 1 && openBrief(leaves[li + 1].id);
      $("#bn-day").disabled = false;
      $("#bn-day").onclick = () => openDayAgenda(day);
      $("#bn-day").title = `Back to all of ${DAYNAMES[day - 1]}`;
    }
    // focus map
    if (r && r.polyline) {
      VMap.activeRoute(r.id);
      if (r.mode === "flight") {
        VMap.focusAll();   // keep the whole archipelago framed during air legs
      } else {
        const p = VMap.pointAlong(r, 0.5); if (p) VMap.focusLatLng(p[0], p[1], 2);
      }
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

  /* ---------- printable / PDF itinerary ---------- */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>]/g,
      (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  }

  function linkList(e, pl, r) {
    const out = [];
    if (pl && pl.maps_url) out.push(`<a href="${esc(pl.maps_url)}">Google Maps</a>`);
    if (pl && pl.source_url) out.push(`<a href="${esc(pl.source_url)}">Video clip</a>`);
    if (e.source_url) out.push(`<a href="${esc(e.source_url)}">Source</a>`);
    if (r && r.source_url) out.push(`<a href="${esc(r.source_url)}">Route source</a>`);
    return out;
  }

  function buildPrintDoc() {
    const meta2 = meta;
    const total = leaves.reduce((n, e) => n + (e.cost_inr || 0), 0);
    let sleepArr = [];
    try { sleepArr = JSON.parse(meta2.sleep_hours || "[]"); } catch (err) {}
    let H = [];
    H.push(`<header class="pd-cover">
      <div class="pd-kicker">Trip dossier · generated ${new Date().toISOString().slice(0, 10)}</div>
      <h1>Andaman Vice</h1>
      <p class="pd-sub">Chennai → Port Blair → Havelock → Neil → Port Blair → Chennai<br>
      Wednesday 23 – Sunday 27 September 2026 · 3 travellers (vegetarian)</p>
      <table class="pd-summary">
        <tr><th>Total cost (3 people)</th><td>${INR(total)}</td></tr>
        <tr><th>Per person</th><td>${INR(total / 3)}</td></tr>
        <tr><th>Nights</th><td>Havelock ×1 · Neil ×1 · Port Blair ×2</td></tr>
        <tr><th>Sleep per night</th><td>${sleepArr.length ? sleepArr.map(h => h + " h").join(" · ") : "—"}</td></tr>
        <tr><th>Outbound</th><td>Akasa QP 1145 · MAA 07:40 → IXZ 09:55</td></tr>
        <tr><th>Return</th><td>Akasa QP 1146 · IXZ 10:35 → MAA 12:55</td></tr>
      </table>
      <p class="pd-warn"><strong>Before you travel:</strong> private ferries sail from <strong>Haddo Jetty (Gate 3)</strong>, not Phoenix Bay — confirm the gate printed on your ticket. Re-check every price and sailing time before booking; figures were captured live in August 2026.</p>
    </header>`);

    for (let d = 1; d <= 5; d++) {
      const parent = ev["d" + d];
      const list = dayLeaves(d);
      if (!list.length) continue;
      const dayCost = list.reduce((n, e) => n + (e.cost_inr || 0), 0);
      H.push(`<section class="pd-day">
        <h2><span class="pd-daynum">Day ${d}</span> ${esc((parent && parent.title) || "")}</h2>
        <p class="pd-date">${DAYNAMES[d - 1]} September 2026 · ${list.length} events · ${INR(dayCost)}</p>
        ${parent && parent.details ? `<p class="pd-theme">${esc(parent.details)}</p>` : ""}`);
      for (const lf of list) {
        const pl = lf.place_id && places[lf.place_id];
        const r = lf.route_id && routesById[lf.route_id];
        const facts = [];
        if (r) {
          if (r.distance_km) facts.push(`${r.distance_km} km`);
          if (r.duration_min) facts.push(fmtDur(r.duration_min) + " travel");
          if (r.mode) facts.push(r.mode);
          if (r.fuel_l) facts.push(`fuel ${r.fuel_l.toFixed(2)} L (${INR(r.fuel_cost_inr || 0)})`);
        }
        if (lf.cost_inr) facts.push(`<strong>${INR(lf.cost_inr)}</strong>`);
        const links = linkList(lf, pl, r);
        H.push(`<div class="pd-ev cat-${esc(lf.category || "prep")}">
          <div class="pd-time">${fmtT(lf.start_min)}–${fmtT(lf.end_min)}<br>
            <span>${fmtDur(lf.end_min - lf.start_min)}</span></div>
          <div class="pd-body">
            <div class="pd-title">${esc(lf.title)}</div>
            ${pl ? `<div class="pd-place">${esc(pl.name)}</div>` : ""}
            ${facts.length ? `<div class="pd-facts">${facts.join(" · ")}</div>` : ""}
            ${lf.cost_note ? `<div class="pd-cost">Cost: ${esc(lf.cost_note)}</div>` : ""}
            ${lf.details ? `<p>${esc(lf.details)}</p>` : ""}
            ${lf.tips ? `<p class="pd-tip"><strong>Tip:</strong> ${esc(lf.tips)}</p>` : ""}
            ${links.length ? `<div class="pd-links">${links.join(" · ")}</div>` : ""}
          </div></div>`);
      }
      H.push(`</section>`);
    }

    // budget appendix
    const paid = leaves.filter(e => e.cost_inr > 0);
    H.push(`<section class="pd-day pd-appendix"><h2>Budget breakdown</h2><table class="pd-table">
      <tr><th>Day</th><th>Item</th><th class="n">Cost (3 pax)</th></tr>` +
      paid.map(e => `<tr><td>D${Math.floor(e.start_min / 1440) + 1} ${fmtT(e.start_min)}</td>
        <td>${esc(e.title)}${e.cost_note ? `<br><span class="pd-small">${esc(e.cost_note)}</span>` : ""}</td>
        <td class="n">${INR(e.cost_inr)}</td></tr>`).join("") +
      `<tr class="pd-total"><td></td><th>Total</th><th class="n">${INR(total)}</th></tr>
       <tr class="pd-total"><td></td><th>Per person</th><th class="n">${INR(total / 3)}</th></tr>
       </table></section>`);

    // packing list
    let kit = [];
    try { kit = JSON.parse(meta2.kit || "[]"); } catch (err) {}
    if (kit.length) {
      H.push(`<section class="pd-day pd-appendix"><h2>What to pack</h2>` +
        kit.map(([sec, items]) => `<h3>${esc(sec)}</h3><ul>` +
          items.map(i => `<li>${esc(i)}</li>`).join("") + `</ul>`).join("") + `</section>`);
    }

    // risks / things to confirm
    let risks = [];
    try { risks = JSON.parse(meta2.risks || "[]"); } catch (err) {}
    if (!risks.length && window.TRIP_RISKS) risks = window.TRIP_RISKS;
    if (risks.length) {
      H.push(`<section class="pd-day pd-appendix"><h2>Confirm before you go</h2><ul class="pd-risks">` +
        risks.map(r => `<li>${esc(r)}</li>`).join("") + `</ul></section>`);
    }

    // sources
    const verified = (D.facts || []).filter(f => f.verified === "confirmed").slice(0, 40);
    H.push(`<section class="pd-day pd-appendix"><h2>Verified facts &amp; sources</h2>
      <p class="pd-small">Every figure in this dossier was read from a live web page in August 2026.
      ${(D.facts || []).length} facts recorded, ${verified.length} independently re-verified.</p>
      <table class="pd-table">` +
      verified.map(f => `<tr><td>${esc(f.topic)}</td><td>${esc(String(f.value).slice(0, 220))}
        ${f.source_url ? `<br><a class="pd-small" href="${esc(f.source_url)}">${esc(f.source_url.slice(0, 80))}</a>` : ""}</td></tr>`).join("") +
      `</table></section>`);

    $("#printdoc").innerHTML = H.join("");
  }

  $("#btn-pdf").onclick = () => {
    buildPrintDoc();
    document.body.classList.add("printing");
    setTimeout(() => {
      window.print();
      setTimeout(() => document.body.classList.remove("printing"), 500);
    }, 120);
  };

  /* ---------- boot ---------- */
  $("#boot").remove();
  setDay(1, false);
  setMinute(L0);
  if ("serviceWorker" in navigator && location.protocol.startsWith("http"))
    navigator.serviceWorker.register("sw.js").catch(() => {});
})();
