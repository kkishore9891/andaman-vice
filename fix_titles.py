#!/usr/bin/env python3
"""Tidy leftovers from the budget pass: the Friday sailing is Green Ocean now,
and drop any zero-length events the shifts left behind."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

for e in it["days"][2]["events"]:
    if e["title"].startswith("SAIL — Makruzz to Port Blair"):
        e["title"] = "SAIL — Green Ocean 1 to Port Blair"

removed = []
for d in it["days"]:
    kept = []
    for e in d["events"]:
        if e["start"] == e["end"]:
            removed.append(f"D{d['day']} {e['start']} {e['title']}")
            continue
        kept.append(e)
    d["events"] = kept

json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("zero-length events removed:", removed or "none")
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
