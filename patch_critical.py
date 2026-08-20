#!/usr/bin/env python3
"""Apply the live critical-verification results.

1. HADDO JETTY (trip-critical): private catamarans sail from Haddo, not Phoenix
   Bay. Makruzz's own FAQ says "reach Haddo Jetty"; Green Ocean e-tickets print
   "Haddo (Gate-3)". Phoenix Bay is the GOVERNMENT ferry terminal ~1 km away.
2. Bharatpur 15:00 closing REFUTED - that figure came from a tour-package box,
   not counter hours. Jet ski runs ~10:00-17:00 at Rs 500-700 pp.
3. Baratang: real private-sedan rate is far below what we budgeted.
4. Cellular Jail on Saturday is HINDI-only, Rs 300/adult.
5. Munda Pahad: 1.5 km one way, 30-60 min, gate closes 15:00.
"""
import json
import re

IT = "data/itinerary.json"
BASE = "populate_base.py"

# ---------- 1. add Haddo Jetty place + routes ----------
src = open(BASE).read()
if "haddo-jetty" not in src:
    place = (' ("haddo-jetty", "Haddo Jetty (Gate 3)", "south_andaman", 11.6790, 92.7255, "jetty", None,\n'
             '  "Where the PRIVATE catamarans sail from — Makruzz, Nautika, Green Ocean. NOT Phoenix Bay, '
             'which is the government ferry terminal about 1 km away. Green Ocean e-tickets print '
             '\'Haddo (Gate-3)\'; reporting is 60 min before departure (Nautika 45). '
             '(Position approximate — confirm the gate printed on your ticket.)"),\n')
    src = src.replace(' ("aberdeen", "Aberdeen Bazaar"', place + ' ("aberdeen", "Aberdeen Bazaar"')
    routes = (
     '\n# --- Haddo jetty legs (private-ferry terminal, verified 2026-08-20) ---\n'
     'ROUTES_V3 = [\n'
     ' ("cab-icyspicy-haddo", "icy-spicy", "haddo-jetty", "cab", 2.8, 8,\n'
     '  [[11.6587633, 92.7313498], [11.668, 92.729], [11.6790, 92.7255]],\n'
     '  "Junglighat to Haddo Wharf. Makruzz says 15-20 min from the airport by taxi."),\n'
     ' ("ferry-haddo-havelock", "haddo-jetty", "havelock-jetty", "ferry", 74, 90,\n'
     '  [[11.6790, 92.7255], [11.82, 92.85], [12.0429471, 92.9835984]],\n'
     '  "Private catamaran from Haddo Gate 3 to Swaraj Dweep."),\n'
     ' ("ferry-neil-haddo", "neil-jetty", "haddo-jetty", "ferry", 60, 75,\n'
     '  [[11.8371487, 93.0311195], [11.75, 92.88], [11.6790, 92.7255]],\n'
     '  "Neil back to Haddo Wharf, Port Blair."),\n'
     ' ("ride-haddo-chidiyatapu", "haddo-jetty", "chidiya-tapu", "scooter", 27.0, 50,\n'
     '  [[11.6790, 92.7255], [11.62, 92.72], [11.56, 92.71], [11.5059682, 92.7014649]],\n'
     '  "NH 4 south from the jetty."),\n'
     ']\nR = R + ROUTES_V3\n')
    src = src.replace("\n\ndef main():", routes + "\n\ndef main():")
    open(BASE, "w").write(src)
    print("populate_base.py: added haddo-jetty + 4 routes")

it = json.load(open(IT))

def find(day, starts):
    for e in it["days"][day - 1]["events"]:
        if e["title"].startswith(starts):
            return e
    return None

# ---------- Day 1: repoint to Haddo ----------
e = find(1, "Cab to the ferry jetty")
if e:
    e["route"] = "cab-icyspicy-haddo"
    e["tips"] = ("Go to HADDO JETTY, Gate 3 — NOT Phoenix Bay. Phoenix Bay is the government ferry "
                 "terminal about 1 km away. Makruzz's own FAQ and Green Ocean's e-tickets both say Haddo.")
for t in ("Nautika check-in", "Green Ocean check-in"):
    e = find(1, t)
    if e:
        e["place"] = "haddo-jetty"
        e["notes"] = ("Reporting is 60 minutes before departure (Nautika asks 45). Check-in shuts 15 min "
                      "prior and boarding 10 min prior. A printed ticket and photo ID are mandatory.")
e = find(1, "SAIL")
if e: e["route"] = "ferry-haddo-havelock"

# ---------- Day 2: jet ski price + counter-hours myth ----------
e = find(2, "JET SKI @ Bharatpur")
if e:
    e["cost_inr"] = 2100
    e["cost_note"] = "3 x Rs 700 (walk-up counter rate Rs 500-700 for a ~10-min ride)"
    e["notes"] = ("Gliding over the lagoon your notes and the video both rate above Goa. Beach entry is free, "
                  "beach hours 05:00-18:00, and the jet ski counter runs roughly 10:00-17:00 — 16:12 is well inside it.")
    e["tips"] = ("The '15:00 closing' scare was a false alarm: that figure came from a tour-package box, not "
                 "the counter hours. Book at the beach desk, and stash bags in a locker while you ride.")

# ---------- Day 3: Munda Pahad + Haddo arrival ----------
e = find(3, "SAIL")
if e: e["route"] = "ferry-neil-haddo"
e = find(3, "PB scooters near jetty")
if e: e["place"] = "haddo-jetty"
e = find(3, "Ride south to Chidiya Tapu")
if e: e["route"] = "ride-haddo-chidiyatapu"
e = find(3, "MUNDA PAHAD TREK")
if e:
    e["notes"] = ("Gate entry must be BEFORE 15:00 (we arrive 14:10, a 50-minute margin). The trail is about "
                  "1.5 km one way and takes 30-60 minutes depending on pace, on an uneven path with a few "
                  "inclines. Entry is free; be back down by 16:15-16:30 when the area clears.")
    e["tips"] = "Trainers, water and mosquito repellent. Budget 2-2.5 hours for the round trip including time at the top."

# ---------- Day 4: Baratang real cost + Cellular Jail ----------
e = find(4, "Cab to Jirkatang")
if e:
    e["cost_inr"] = 5400
    e["cost_note"] = ("private sedan round trip, Rs 5,000-6,500 published range (ferrybooking.in lists Rs 5,400 "
                      "for up to 4 pax) — includes driver, tolls, parking and the Middle Strait vehicle ferry")
    e["notes"] = ("47 km in the dark to make the 06:00 first convoy. Two-wheelers are banned past the check post. "
                  "A shared joining tour is Rs 2,250 pp (Rs 6,750 for three) if you would rather split the cost "
                  "than have the car to yourselves.")
e = find(4, "Speedboat into the mangroves")
if e:
    e["cost_inr"] = 2700
    e["cost_note"] = "3 x Rs 900 (counter rate Rs 900-1,000 pp, booked on arrival at Nilambur)"
    e["notes"] = "A 6-8 seat motorboat, about 25 minutes each way through mangrove creeks. Half the show is the ride."
e = find(4, "Ferry back across")
if e: e["notes"] = "Vehicle ferry across Middle Strait — included in the private-cab rate."
e = find(4, "Return convoy")
if e:
    e["notes"] = ("Southbound convoys leave the Baratang side at roughly 12:00, 15:00 and 16:00 — the LAST one is "
                  "15:00 and missing it strands you overnight. Your driver knows the day's slot; confirm it on arrival.")
e = find(4, "Optional: Cellular Jail")
if e:
    e["title"] = "Optional: Cellular Jail light & sound (Hindi)"
    e["start"], e["end"] = "17:45", "19:15"
    e["cost_inr"] = 0
    e["cost_note"] = "Rs 300 per adult (Rs 900 for three) if you go — not counted in the trip budget"
    e["notes"] = ("On Saturday every show is in HINDI: 17:50, 18:50 and 19:50. English runs only Mon/Wed/Fri, so "
                  "there is no English option on the 26th. The 17:50 Hindi show fits this slot.")
    e["tips"] = ("Tickets are sold on the official Andaman Tourism e-Tourist portal. Skip it freely if the "
                 "04:00 start has flattened everyone — nothing downstream depends on it.")

it["risks"] = [r for r in it["risks"] if "Bharatpur watersports counter hours" not in r
               and "Baratang cab price" not in r] + [
  "VERIFIED: private ferries sail from HADDO JETTY (Gate 3), not Phoenix Bay — the plan now sends you to Haddo, but confirm the gate printed on your own ticket",
  "Late September is the tail of the SW monsoon: ferries run, but boat-based watersports at Bharatpur are weather-dependent on the day",
  "Saturday's Cellular Jail show is Hindi-only (English runs Mon/Wed/Fri)"]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
