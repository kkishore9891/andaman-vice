#!/usr/bin/env python3
"""Drop the paid Govind Nagar snorkel — the user's call, since the scuba dive
covers the same reef. The slot becomes free beach time so the day stays gapless."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))
d2 = it["days"][1]
out = []
for e in d2["events"]:
    if e["title"].startswith("SNORKEL at Govind Nagar"):
        out.append({
            "start": e["start"], "end": e["end"],
            "title": "Beach time at Govind Nagar", "category": "buffer",
            "place": "govind-nagar", "cost_inr": 0,
            "notes": ("Swim and dry off on the same beach after the dive. Snorkelling was dropped on your "
                      "call — the scuba covers that reef, and the dive itself is time spent looking at it."),
            "tips": ("If anyone still fancies a mask, the dive shop will usually lend gear cheaply — "
                     "ask when you book the dive.")})
    else:
        out.append(e)
d2["events"] = out
it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("snorkel removed; crew total: Rs", it["total_cost_inr"],
      "= Rs", round(it["total_cost_inr"] / 3), "pp")
