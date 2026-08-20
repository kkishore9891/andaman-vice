#!/usr/bin/env python3
"""Apply live Booking.com re-pricing (20 Aug 2026, 3 adults, exact nights) and
the confirmed scuba rate.

- Port Blair: Hotel Atlanta -> Pibo Homestay. Rs 5,250 vs Rs 8,845 for the same
  2 nights, 9.3 vs 7.9, breakfast included, free cancellation to 24 Sep.
- Havelock: same Bhuma, but the Rs 5,685 Family Room rather than the Rs 6,920
  Family Double that was previously quoted.
- Scuba at Govind Nagar is Rs 4,500 pp (Dive Andaman shore Discover Scuba),
  not the Rs 3,500 previously carried.
"""
import json

BASE = "populate_base.py"
IT = "data/itinerary.json"

src = open(BASE).read()
if "hotel-pibo" not in src:
    place = (' ("hotel-pibo", "Pibo Homestay", "south_andaman", 11.6540, 92.7300, "hotel", None,\n'
             '  "Port Blair base — 9.3/10 from 138 reviews. Family room sleeping 3 (1 full + 1 king), '
             'breakfast included, free cancellation to 24 Sep. Rs 5,250 for both nights: Rs 875 per person '
             'per night, well under the Rs 2,000 target and Rs 3,595 cheaper than Hotel Atlanta. '
             '(Position approximate — 2.9 km from downtown, 1.2 km from the beach.)"),\n')
    src = src.replace(' ("hotel-atlanta",', place + ' ("hotel-atlanta",')
    routes = ('\n# --- Pibo Homestay legs (live re-pricing, 2026-08-20) ---\n'
              'ROUTES_V4 = [\n'
              ' ("ride-chidiyatapu-pibo", "chidiya-tapu", "hotel-pibo", "scooter", 24.0, 45,\n'
              '  [[11.5059682, 92.7014649], [11.56, 92.71], [11.62, 92.72], [11.6540, 92.7300]],\n'
              '  "NH 4 back north in the dark."),\n'
              ' ("cab-pibo-jirkatang", "hotel-pibo", "jirkatang", "cab", 48.0, 78,\n'
              '  [[11.6540, 92.7300], [11.70, 92.70], [11.78, 92.67], [11.8396935, 92.6538333]],\n'
              '  "NH 4. Two-wheelers are barred beyond the check post."),\n'
              ' ("cab-pibo-ixz", "hotel-pibo", "ixz", "cab", 2.0, 6,\n'
              '  [[11.6540, 92.7300], [11.641656, 92.730243]],\n'
              '  "A short hop — the homestay sits close to the airport side of town."),\n'
              ' ("walk-pibo-marina", "hotel-pibo", "marina-park", "walk", 2.6, 9, None,\n'
              '  "Short auto ride or a walk down to the waterfront."),\n'
              ' ("cab-pibo-icyspicy", "hotel-pibo", "icy-spicy", "cab", 1.2, 5, None,\n'
              '  "Junglighat is the neighbouring area."),\n'
              ']\nR = R + ROUTES_V4\n')
    src = src.replace("\n\ndef main():", routes + "\n\ndef main():")
    open(BASE, "w").write(src)
    print("populate_base.py: added hotel-pibo + 5 routes")

it = json.load(open(IT))

def find(day, starts):
    for e in it["days"][day - 1]["events"]:
        if e["title"].startswith(starts):
            return e
    return None

# ---- Havelock: cheaper room at the same homestay ----
e = find(1, "Check in @ Bhuma")
if e:
    e["cost_inr"] = 5685
    e["cost_note"] = ("Family Room 23 m² (1 full + 1 king + 1 sofa bed), breakfast incl., CASH only — "
                      "live Booking.com quote 20 Aug for these exact nights")
    e["notes"] = ("9.5/10 from 226 reviews, 50 m from Govind Nagar Beach. Rs 5,000 refundable damage deposit.")
    e["tips"] = ("Book this one early: only 1 of these rooms left and it is non-refundable. The larger Family "
                 "Double (33 m², a third proper bed and a kitchenette) is Rs 6,920 with 3 left if this one goes.")

# ---- Thursday scuba: confirmed rate ----
e = find(2, "SCUBA")
if e:
    e["cost_inr"] = 13500
    e["cost_note"] = "3 x Rs 4,500 shore Discover Scuba (Dive Andaman, Govind Nagar) — CONFIRMED live 20 Aug"
    e["tips"] = ("Book by phone a day ahead. No alcohol the night before. No flying for 18-24 h after a dive — "
                 "Sunday's 10:35 departure is comfortably clear. Turquoise Dream on Neil is the same Rs 4,500 "
                 "but MORNINGS ONLY, which is why the dive sits here on Havelock rather than after Thursday's ferry.")

# ---- Port Blair: swap Atlanta -> Pibo ----
e = find(3, "Check in @ Hotel Atlanta")
if e:
    e["title"] = "Check in @ Pibo Homestay"
    e["place"] = "hotel-pibo"
    e["cost_inr"] = 5250
    e["cost_note"] = ("Family Room for 3 (1 full + 1 king), 2 nights, breakfast incl., free cancellation to "
                      "24 Sep — live Booking.com quote 20 Aug")
    e["notes"] = ("9.3/10 from 138 reviews. Rs 875 per person per night — Rs 3,595 cheaper than Hotel Atlanta, "
                  "which scores 7.9, charges extra for breakfast and has no sea view despite the name.")
    e["tips"] = "Only 1 room left at this rate — book it before the flights if you want it."

for day, starts, route, place in (
        (3, "Night ride back to Port Blair", "ride-chidiyatapu-pibo", None),
        (3, "Dinner @ Annapurna", None, None),
        (4, "Cab to Jirkatang", "cab-pibo-jirkatang", None),
        (4, "Drive back to Port Blair", "cab-pibo-jirkatang", None),
        (4, "Marina Park", "walk-pibo-marina", None),
        (4, "Farewell dinner @ Icy Spicy", "cab-pibo-icyspicy", None),
        (5, "Cab to the airport", "cab-pibo-ixz", None)):
    e = find(day, starts)
    if e and route:
        e["route"] = route

# any remaining references to the old hotel place
for d in it["days"]:
    for e in d["events"]:
        if e.get("place") == "hotel-atlanta":
            e["place"] = "hotel-pibo"

e = find(5, "Breakfast + pack out")
if e:
    e["cost_inr"] = 0
    e["cost_note"] = "breakfast included at Pibo"
    e["notes"] = "Breakfast is included here, so no need to hunt for an early cafe before the airport run."

it["risks"] = [r for r in it["risks"] if "lodging costs" not in r.lower()] + [
  "Bhuma's Rs 5,685 room and Pibo's Rs 5,250 rate each show only 1 left as of 20 Aug — book the rooms before the flights",
  "Bhuma is non-refundable and cash-only; Pibo and Blue Lagoon both allow free cancellation (24 Sep and 17 Sep respectively)"]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
