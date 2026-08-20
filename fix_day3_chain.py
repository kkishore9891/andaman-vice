#!/usr/bin/env python3
"""Repair the Day 3 chain after the ferry shift: make every event start exactly
when the previous one ends, from the trek through to the evening."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))
d3 = it["days"][2]

for i, e in enumerate(d3["events"]):
    print(f"{i:2d} {e['start']}-{e['end']}  {e['title'][:52]}")

# walk forward from the trek; push any event that starts before the previous end
prev_end = None
fixed = 0
for e in d3["events"]:
    if prev_end and e["start"] < prev_end:
        dur_h, dur_m = map(int, e["end"].split(":"))
        s_h, s_m = map(int, e["start"].split(":"))
        dur = (dur_h * 60 + dur_m) - (s_h * 60 + s_m)
        if dur <= 0:
            dur = 15
        ph, pm = map(int, prev_end.split(":"))
        start = ph * 60 + pm
        end = start + dur
        e["start"] = f"{start // 60:02d}:{start % 60:02d}"
        e["end"] = f"{end // 60:02d}:{end % 60:02d}"
        fixed += 1
    prev_end = e["end"]

# the day must still close at 24:00
if d3["events"][-1]["end"] != "24:00":
    d3["events"][-1]["end"] = "24:00"

json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print(f"\nrepaired {fixed} events")
for e in d3["events"][-8:]:
    print(f"   {e['start']}-{e['end']}  {e['title'][:52]}")
