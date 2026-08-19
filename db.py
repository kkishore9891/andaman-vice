#!/usr/bin/env python3
"""Trip database layer. SQLite is the single source of truth.

Timeline architecture:
  - The trip is a contiguous minute ledger in IST.
  - `events` are hierarchical (parent_id): day -> phase -> event -> sub-step.
  - LEAF events must tile the ledger window with no gaps and no overlaps;
    `validate()` enforces this. Every minute maps to exactly one leaf event.
  - Times are stored as minutes since trip epoch (t0) plus ISO strings for humans.
"""
import json
import sqlite3
from datetime import datetime, timedelta

DB_PATH = __file__.rsplit("/", 1)[0] + "/trip.db"
IST = "+05:30"
# Trip epoch: Wed 2026-09-23 00:00 IST. Ledger window set after flights are final.
T0 = datetime(2026, 9, 23, 0, 0)

SCHEMA = """
CREATE TABLE IF NOT EXISTS places (
  id TEXT PRIMARY KEY,          -- slug
  name TEXT NOT NULL,
  island TEXT NOT NULL,         -- chennai | south_andaman | havelock | neil | baratang | sea | air
  lat REAL, lng REAL,
  kind TEXT,                    -- beach | jetty | airport | hotel | restaurant | cave | viewpoint | pump | other
  photo TEXT,                   -- assets/<slug>.jpg
  blurb TEXT,
  source_url TEXT
);
CREATE TABLE IF NOT EXISTS routes (
  id TEXT PRIMARY KEY,
  from_place TEXT REFERENCES places(id),
  to_place TEXT REFERENCES places(id),
  mode TEXT,                    -- flight | ferry | scooter | cab | walk | boat | trek | convoy
  distance_km REAL,
  duration_min INTEGER,
  polyline TEXT,                -- JSON [[lat,lng],...] for map drawing
  fuel_l REAL,                  -- computed for scooter legs (2 scooters combined)
  fuel_cost_inr REAL,
  notes TEXT,
  source_url TEXT
);
CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  parent_id TEXT REFERENCES events(id),
  day INTEGER,                  -- 1..5
  seq INTEGER,                  -- order among siblings
  title TEXT NOT NULL,
  category TEXT,                -- travel | activity | meal | sleep | prep | buffer | scenic
  start_min INTEGER,            -- minutes since T0 (IST)
  end_min INTEGER,
  place_id TEXT REFERENCES places(id),
  route_id TEXT REFERENCES routes(id),
  cost_inr REAL DEFAULT 0,      -- total for the 3-person crew
  cost_note TEXT,
  details TEXT,                 -- long-form: what/why/how, booking info
  tips TEXT,                    -- parking, what to wear/carry, pitfalls
  source_url TEXT
);
CREATE TABLE IF NOT EXISTS facts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT, value TEXT, source_url TEXT, as_of TEXT,
  verified TEXT DEFAULT 'reported'   -- reported | confirmed | refuted->corrected | unverifiable
);
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
"""


def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c


def m2iso(m: int) -> str:
    return (T0 + timedelta(minutes=m)).strftime("%Y-%m-%dT%H:%M") + IST


def iso2m(s: str) -> int:
    """'2026-09-23 04:40' -> minutes since T0."""
    dt = datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")
    return int((dt - T0).total_seconds() // 60)


def validate(c=None):
    """Leaf events must tile [ledger_start, ledger_end] exactly. Returns problem list."""
    c = c or conn()
    meta = {r["k"]: r["v"] for r in c.execute("SELECT * FROM meta")}
    if "ledger_start_min" not in meta:
        return ["meta.ledger_start_min/ledger_end_min not set yet"]
    lo, hi = int(meta["ledger_start_min"]), int(meta["ledger_end_min"])
    parents = {r["parent_id"] for r in c.execute(
        "SELECT DISTINCT parent_id FROM events WHERE parent_id IS NOT NULL")}
    leaves = [r for r in c.execute(
        "SELECT * FROM events WHERE start_min IS NOT NULL ORDER BY start_min")
        if r["id"] not in parents]
    probs, cur = [], lo
    for e in leaves:
        s, t = e["start_min"], e["end_min"]
        if s is None or t is None or t <= s:
            probs.append(f"{e['id']}: bad interval {s}..{t}")
            continue
        if s < cur:
            probs.append(f"{e['id']}: OVERLAP starts {m2iso(s)} before previous end {m2iso(cur)}")
        elif s > cur:
            probs.append(f"GAP {m2iso(cur)} -> {m2iso(s)} (before {e['id']})")
        cur = max(cur, t)
    if cur < hi:
        probs.append(f"GAP at end: {m2iso(cur)} -> {m2iso(hi)}")
    # parent envelopes must contain children
    for p in c.execute("SELECT * FROM events WHERE start_min IS NOT NULL"):
        kids = list(c.execute(
            "SELECT * FROM events WHERE parent_id=? AND start_min IS NOT NULL", (p["id"],)))
        if kids:
            if min(k["start_min"] for k in kids) < p["start_min"] or \
               max(k["end_min"] for k in kids) > p["end_min"]:
                probs.append(f"{p['id']}: children exceed parent envelope")
    return probs


def export(c=None):
    """Bake the whole DB to one JSON blob (for the API and the static/hosted build)."""
    c = c or conn()
    out = {"t0": T0.strftime("%Y-%m-%dT%H:%M") + IST}
    for table in ("places", "routes", "events", "facts", "meta"):
        out[table] = [dict(r) for r in c.execute(f"SELECT * FROM {table}")]
    out["validation"] = validate(c)
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        for p in validate():
            print("PROBLEM:", p)
        else:
            print("minute-ledger OK" if not validate() else "")
    elif len(sys.argv) > 1 and sys.argv[1] == "export":
        json.dump(export(), open(DB_PATH.rsplit("/", 1)[0] + "/data.json", "w"),
                  ensure_ascii=False)
        print("exported data.json")
    else:
        conn()
        print("db ready at", DB_PATH)
