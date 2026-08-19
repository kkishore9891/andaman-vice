# Andaman Vice 🌴

GTA-style minute-by-minute trip companion for a Chennai → Port Blair → Havelock → Neil
run, **Sep 23–27 2026**, crew of 3. Neon 2.5D map built from real OSM coastline,
mission-timeline with a minute scrubber, drill-down briefings with live-researched
prices, fuel math, tide/moon/sunrise data — every fact browser-verified with sources.

## Architecture
- `trip.db` — SQLite, single source of truth. The itinerary is a **minute ledger**:
  hierarchical events whose leaves tile every minute from Chennai takeoff to landing
  back (enforced by `python3 db.py validate`).
- `server.py` — zero-dependency local server: static frontend + `/api/trip`, `/api/minute?t=N`.
- `js/` + `css/` — vanilla-JS frontend (SVG map, timeline sim, briefing panels). PWA-ready.
- `build_static.py` — bakes DB + geometry + photos into one self-contained HTML
  (`docs/index.html` → GitHub Pages, `dist/andaman-vice.html`).

## Run locally
```bash
python3 server.py          # http://localhost:8765
```

## Deploy
```bash
python3 build_static.py && git add -A && git commit -m "bake" && git push
```
GitHub Pages serves `docs/` on `main`.
