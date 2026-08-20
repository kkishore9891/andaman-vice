#!/usr/bin/env python3
"""Bring the trip under the hard Rs 40,000/person ceiling.

Flights are Rs 19,927 pp and immovable (cheapest nonstops both ways), so the
whole ground budget must fit Rs 20,073 pp. Five cuts, cheapest-pain first:
  1. Kayak dropped        -Rs 10,500  (full-moon week: mild glow at best)
  2. Scuba -> Try Dive     -Rs 3,000  (same reef, shorter dive)
  3. Friday ferry -> GO    -Rs 2,325  (15 min less buffer, still 35 min spare)
  4. Baratang -> shared    -Rs 1,350  (joining tour incl. boat + permits)
  5. Meal/scooter trims    -Rs 1,100
Everything the user called non-negotiable survives: Radhanagar + Neil's Cove,
scuba, jet ski, Natural Bridge, Sitapur, limestone caves, Munda Pahad.
"""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

def find(day, starts):
    for e in it["days"][day - 1]["events"]:
        if e["title"].startswith(starts):
            return e
    return None

# ---- 1. drop the kayak; Thursday now starts at Kala Pathar ----
d2 = it["days"][1]
keep = []
for e in d2["events"]:
    if e["title"] in ("Up in the dark (kayak kit)", "Ride to the kayak launch") or \
       e["title"].startswith("NIGHT KAYAK"):
        continue
    keep.append(e)
# stretch sleep to the new 04:15 start and re-open the morning
for e in keep:
    if e["title"] == "Sleep" and e["start"] == "00:00":
        e["end"] = "04:15"
d2["events"] = [keep[0]] + [
    {"start": "04:15", "end": "04:35", "title": "Up in the dark", "category": "prep",
     "place": "hotel-bhuma",
     "notes": "A gentler start than the kayak version — 6h45m of sleep behind you.",
     "tips": "Headlamp and a warm layer; it is properly dark until about 04:47."},
    {"start": "04:35", "end": "05:00", "title": "Ride to Kala Pathar", "category": "travel",
     "route": "ride-bhuma-kalapathar",
     "notes": "Sunrise is 05:09, so this puts you on the sand with minutes to spare."},
    {"start": "05:00", "end": "06:30", "title": "SUNRISE @ Kala Pathar Beach", "category": "scenic",
     "place": "kalapathar",
     "notes": ("Sunrise 05:09 over the driftwood-and-black-rock shoreline the reference video calls the "
               "best sunrise in the Andamans. With the kayak dropped this becomes the morning's centrepiece "
               "and you get a full 90 minutes of it instead of a rushed 40."),
     "tips": "Free roadside parking. Walk south along the sand for the empty unnamed stretches."},
    {"start": "06:30", "end": "06:50", "title": "Ride back to Bhuma", "category": "travel",
     "route": "ride-bhuma-kalapathar"},
] + [e for e in keep[1:] if not (
        e["title"].startswith("Ride to Kala Pathar") or
        e["title"].startswith("Kala Pathar") or
        e["title"].startswith("Ride back to Bhuma"))]
# breakfast now starts right after the ride back
for e in d2["events"]:
    if e["title"].startswith("Breakfast @ Bhuma"):
        e["start"] = "06:50"; e["end"] = "07:45"

# ---- 2. scuba: the shorter Try Dive tier ----
e = find(2, "SCUBA")
if e:
    e["cost_inr"] = 10500
    e["cost_note"] = "3 x Rs 3,500 shore Try Dive (Dive Andaman, Govind Nagar) — the shorter beginner tier"
    e["notes"] = ("Briefing, kit-up and a guided shore dive on the reef the reference video rates as "
                  "Havelock's best. The Try Dive is the shorter option: about 30 minutes underwater against "
                  "the Rs 4,500 Discover Scuba. Same reef, same instructor ratio.")
    e["tips"] = ("Book by phone a day ahead. No alcohol the night before; no flying for 18-24 h after — "
                 "Sunday's 10:35 flight is clear. Upgrade to the Rs 4,500 Discover Scuba on the day if "
                 "the budget feels comfortable when you get there.")

# ---- 3. Friday ferry: Green Ocean instead of Makruzz ----
e = find(3, "SAIL")
if e:
    e["start"] = "11:00"; e["end"] = "12:45"
    e["cost_inr"] = 4200
    e["cost_note"] = "3 x Rs 1,400 all-in (Green Ocean 1, Rs 1,050 + Rs 50 PMB + Rs 300 fuel)"
    e["notes"] = ("Rs 2,325 cheaper than the Makruzz sailing. Lands 12:45 instead of 12:30, which still "
                  "leaves a 35-minute margin on the Munda Pahad gate.")
e = find(3, "Makruzz check-in")
if e:
    e["title"] = "Green Ocean check-in"; e["start"] = "10:00"; e["end"] = "11:00"
    e["notes"] = "Counter opens 60 min before sailing and shuts 15 min prior. PRINTED ticket mandatory."
e = find(3, "Jetty wait")
if e: e["start"] = "11:00"; e["end"] = "11:00"
for e in d2["events"]:
    pass
# shift the Friday afternoon 15 min later to match the later arrival
for t, s, en in (("PB scooters near jetty", "12:45", "13:25"),
                 ("Ride south to Chidiya Tapu", "13:25", "14:15"),
                 ("On to Munda Pahad Beach", "14:15", "14:25"),
                 ("MUNDA PAHAD TREK", "14:25", "16:00")):
    e = find(3, t)
    if e: e["start"], e["end"] = s, en

# ---- 4. Baratang: shared joining tour ----
e = find(4, "Cab to Jirkatang")
if e:
    e["cost_inr"] = 6750
    e["cost_note"] = ("3 x Rs 2,250 shared joining tour (Andaman Ocean) — includes A/C shared cab with hotel "
                      "pickup, convoy permit assistance, shared speedboat tickets, tolls and parking")
    e["notes"] = ("A shared vehicle rather than your own car: Rs 1,350 cheaper and it folds the speedboat and "
                  "permits into one price. Hotel pickup around 04:00 to make the 06:00 convoy.")
    e["tips"] = "Excludes the Rs 14 pp vehicle-ferry ticket and all meals. A private sedan is Rs 5,400 + boat if you would rather not share."
e = find(4, "Speedboat into the mangroves")
if e:
    e["cost_inr"] = 0
    e["cost_note"] = "included in the shared tour price"

# ---- 5. small trims ----
e = find(2, "Lunch @ Something Different")
if e:
    e["cost_inr"] = 1000
    e["cost_note"] = "keep it to mains — salads and sides here run Rs 195-345 each"
e = find(2, "Ride to the jetty, return scooters")
if e:
    e["cost_inr"] = 0
    e["cost_note"] = "returned inside the 24h window — no second-slot charge"
    e["tips"] = "Return by the 10am rental boundary to avoid a second day's charge."

it["sleep_hours"] = [6.75, 7.0, 5.75, 9.75]
it["philosophy"] += (" v8: trimmed to the user's hard Rs 40,000/person ceiling. Flights are Rs 19,927 pp and "
  "immovable, so the ground budget had to fit Rs 20,073 pp. The kayak was the casualty - full-moon week made "
  "it a mild-glow gamble at Rs 3,500 a head - and Kala Pathar sunrise inherits the morning.")
it["risks"] = [r for r in it["risks"] if "kayak" not in r.lower()] + [
  "KAYAK DROPPED to meet the Rs 40,000 ceiling. If you decide with your cousins that you want it back, it is Rs 3,500 pp and pushes the trip to about Rs 43,500 pp",
  "Friday's Green Ocean sailing lands 12:45, leaving a 35-minute margin on the 15:00 Munda Pahad gate - if the ferry runs late, skip the trek and go straight to Chidiya Tapu for sunset"]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
pp = it["total_cost_inr"] / 3
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(pp), "pp")
print("UNDER Rs 40,000 ceiling:", pp <= 40000)
