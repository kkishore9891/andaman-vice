#!/usr/bin/env python3
"""Load the arbiter's final itinerary (data/itinerary.json, DESIGN_SCHEMA shape)
into the events table as a validated minute ledger.

- One parent event per day (d1..d5), leaves under it (d1-e01...).
- Leaf times come from the itinerary's HH:MM strings on each day's date.
- Ledger bounds = first leaf start .. last leaf end; db.validate() must pass.
"""
import json
import sys
import db

IT = db.DB_PATH.rsplit("/", 1)[0] + "/data/itinerary.json"
DATES = {1: "2026-09-23", 2: "2026-09-24", 3: "2026-09-25", 4: "2026-09-26", 5: "2026-09-27"}


def t2m(day, hhmm):
    """HH:MM on a given day -> minutes since T0. '24:00' = end of that day."""
    if hhmm.strip() == "24:00":
        return (day - 1) * 1440 + 1440
    return db.iso2m(f"{DATES[day]} {hhmm}")


def main():
    it = json.load(open(IT))
    c = db.conn()
    c.execute("DELETE FROM events")
    place_ids = {r["id"] for r in c.execute("SELECT id FROM places")}
    route_ids = {r["id"] for r in c.execute("SELECT id FROM routes")}
    bad_refs = []
    lo = hi = None
    for d in it["days"]:
        day = d["day"]
        evs = d["events"]
        dstart = t2m(day, evs[0]["start"])
        dend = t2m(day, evs[-1]["end"])
        if dend <= dstart:               # day ends past midnight
            dend += 1440
        c.execute("INSERT INTO events (id,parent_id,day,seq,title,category,start_min,end_min,details) "
                  "VALUES (?,?,?,?,?,?,?,?,?)",
                  (f"d{day}", None, day, day, d.get("title") or f"Day {day}", "prep",
                   dstart, dend, d.get("theme") or ""))
        prev_end = None
        for i, e in enumerate(evs, 1):
            s = t2m(day, e["start"])
            t = t2m(day, e["end"])
            if prev_end is not None and s < prev_end - 720:   # crossed midnight
                s += 1440
            if t < s:
                t += 1440
            prev_end = t
            pid = e.get("place") or None
            rid = e.get("route") or None
            if pid and pid not in place_ids:
                bad_refs.append(f"d{day}-e{i:02d} place '{pid}'"); pid = None
            if rid and rid not in route_ids:
                bad_refs.append(f"d{day}-e{i:02d} route '{rid}'"); rid = None
            c.execute("INSERT INTO events (id,parent_id,day,seq,title,category,start_min,end_min,"
                      "place_id,route_id,cost_inr,cost_note,details,tips) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (f"d{day}-e{i:02d}", f"d{day}", day, i, e["title"], e.get("category") or "prep",
                       s, t, pid, rid, e.get("cost_inr") or 0, e.get("cost_note") or None,
                       e.get("notes") or None, e.get("tips") or None))
            lo = s if lo is None else min(lo, s)
            hi = t if hi is None else max(hi, t)
    c.execute("INSERT OR REPLACE INTO meta VALUES ('ledger_start_min', ?)", (str(lo),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('ledger_end_min', ?)", (str(hi),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('sleep_hours', ?)",
              (json.dumps(it.get("sleep_hours") or []),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('total_cost_inr', ?)",
              (str(it.get("total_cost_inr") or 0),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('philosophy', ?)", (it.get("philosophy") or "",))
    c.commit()
    print("events:", c.execute("SELECT COUNT(*) FROM events").fetchone()[0],
          "| ledger:", db.m2iso(lo), "->", db.m2iso(hi))
    if bad_refs:
        print("UNRESOLVED REFS (cleared):", *bad_refs, sep="\n  ")
    probs = db.validate(c)
    for p in probs:
        print("PROBLEM:", p)
    if probs:
        sys.exit(1)
    print("minute-ledger OK — every minute mapped")


if __name__ == "__main__":
    main()
