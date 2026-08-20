#!/usr/bin/env python3
"""Repair routes whose polyline was stored as "null".

Two Pibo routes were added with None as the polyline, which json.dumps turns
into the string "null". JSON.parse("null") returns null, not [], so the frontend
threw and the whole app failed to boot. Build the missing geometry from the
endpoint coordinates, then assert no null geometry survives."""
import json
import sys

import db

c = db.conn()
coords = {r["id"]: (r["lat"], r["lng"])
          for r in c.execute("SELECT id, lat, lng FROM places")}

bad = []
for r in c.execute("SELECT id, from_place, to_place, polyline FROM routes"):
    try:
        pts = json.loads(r["polyline"] or "[]")
    except Exception:
        pts = None
    if not isinstance(pts, list) or len(pts) < 2:
        bad.append(dict(r))

print("routes with unusable geometry:", len(bad))
fixed = 0
for r in bad:
    a, b = coords.get(r["from_place"]), coords.get(r["to_place"])
    if not a or not b or a[0] is None or b[0] is None:
        print("  CANNOT FIX (missing coords):", r["id"])
        continue
    poly = [[a[0], a[1]], [b[0], b[1]]]
    c.execute("UPDATE routes SET polyline=? WHERE id=?", (json.dumps(poly), r["id"]))
    print(f"  fixed {r['id']}: {r['from_place']} -> {r['to_place']}")
    fixed += 1
c.commit()

# hard assertion: nothing unusable may remain
remaining = []
for r in c.execute("SELECT id, polyline FROM routes"):
    try:
        pts = json.loads(r["polyline"] or "[]")
    except Exception:
        pts = None
    if not isinstance(pts, list) or len(pts) < 2:
        remaining.append(r["id"])
print(f"\nfixed {fixed}; unusable remaining: {remaining or 'none'}")
if remaining:
    sys.exit(1)
