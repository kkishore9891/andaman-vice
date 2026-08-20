#!/usr/bin/env python3
"""Day 2 v3: all underwater activity moves to Neil (Bharatpur) per user direction.
Elephant Beach dropped; earlier cheap ferry buys a full Neil afternoon so SCUBA +
snorkel + jet ski all land around the verified 14:32 high tide."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("00:00","03:00","Sleep","sleep",place="hotel-bhuma")
ev("03:00","03:20","Up in the dark (kayak kit)","prep",place="hotel-bhuma",
   tips="Dry bag, quick-dry clothes, headlamp. If the operator cancelled, sleep to 05:30 instead.")
ev("03:20","03:30","Ride to the kayak launch","travel",route="ride-bhuma-kayak",place="kayak-point")
ev("03:30","05:45","NIGHT KAYAK — dark-window glow attempt + sunrise on the water","activity",
   place="kayak-point",cost_inr=10500,cost_note="3 x Rs 3,500 (Andaman Bliss, all taxes)",
   notes="The trip's ONLY true darkness: moonset 02:54, civil dawn 04:47. Expect a mild sparkle at the paddle strokes, not new-moon fireworks - then sunrise 05:09 from the kayaks.",
   tips="Basic swimming required (operator's age 13-45 rule). Phones in a dry bag only.")
ev("05:45","06:10","Ride to Kala Pathar","travel",route="ride-bhuma-kalapathar",
   notes="Golden hour runs to about 06:45 - go straight there while the light is soft.")
ev("06:10","06:50","Kala Pathar — fallen trees & black rocks","scenic",place="kalapathar",
   notes="The driftwood-and-jungle shoreline from the video. Free roadside parking.")
ev("06:50","07:05","Ride back to Bhuma","travel",route="ride-bhuma-kalapathar")
ev("07:05","07:40","Breakfast @ Bhuma (included)","meal",place="hotel-bhuma",
   tips="Ask the night before for an early serving.")
ev("07:40","07:55","Pack & checkout","prep",place="hotel-bhuma",
   tips="Settle the cash bill and collect the Rs 5,000 damage deposit.")
ev("07:55","08:15","Ride to the jetty, return scooters","travel",route="ride-hljetty-bhuma",
   notes="Hand the scooters back at the jetty gate (drop-off is included in the rental).")
ev("08:15","09:15","Green Ocean check-in","prep",place="havelock-jetty",
   notes="Counter opens 60 min before sailing; a PRINTED ticket is mandatory on Green Ocean.")
ev("09:15","10:30","SAIL — Green Ocean 1 to Neil","travel",route="ferry-havelock-neil",
   cost_inr=4200,cost_note="3 x Rs 1,400 all-in (Rs 1,050 + Rs 50 PMB + Rs 300 fuel)",
   notes="Cheapest of the six verified Thursday sailings, and the early slot is what buys the full Neil afternoon.")
ev("10:30","10:50","Neil scooters at the jetty","travel",place="neil-jetty",cost_inr=1000,
   cost_note="2 x ~Rs 500/day",notes="Neil On Wheels, Neil Kendra (5.0-rated), ph +91 94742 68205 - book ahead.")
ev("10:50","11:10","Ride to Blue Lagoon via the pump","travel",route="ride-neiljetty-bluelagoon",
   cost_inr=4118,cost_note="stay Rs 3,968 (breakfast incl., free cancellation) + Rs 150 fuel",
   notes="Top up at IndianOil Neil Kendra on the way - it is the island's only pump and shuts around 18:00.")
ev("11:10","11:30","Check in & drop bags","prep",place="hotel-bluelagoon",
   notes="8.6/10, on the Sitapur side - tomorrow's sunrise beach is a 3-minute ride away.")
ev("11:30","12:30","Veg thali lunch @ Pure Veg Restaurant","meal",place="pure-veg-neil",
   route="ride-bluelagoon-pureveg",cost_inr=720,cost_note="3 x Rs 240 thali",
   notes="Neil's best-rated veg kitchen (4.8). Eat light - you are diving in an hour.")
ev("12:30","12:45","Ride to Bharatpur","travel",route="ride-bluelagoon-bharatpur")
ev("12:45","15:00","SCUBA DIVE @ Bharatpur","activity",place="bharatpur",cost_inr=10500,
   cost_note="3 x Rs 3,500 shore try-dive (DiveIndia's Neil branch sits 50 m from the jetty)",
   notes="Briefing, kit-up and a guided shore dive on Neil's coral garden, timed to the 14:32 high tide. Non-swimmers can dive - the instructor handles everything but breathing.",
   tips="Book by phone a day ahead. No alcohol the night before and no flying for 18 h after - Sunday's 10:35 flight is well clear.")
ev("15:00","15:45","SNORKEL the coral garden","activity",place="bharatpur",cost_inr=3000,
   cost_note="~Rs 1,000 pp guided boat snorkel, booked on the beach",
   notes="The transcript's best snorkel in the Andamans - better than Elephant Beach or North Bay - and the tide is still high.",
   tips="Book at the beach counter, never prepaid online.")
ev("15:45","16:15","JET SKI runs","activity",place="bharatpur",cost_inr=2400,
   cost_note="3 x Rs 800 (10-15 min each; verified range 800-1,200)",
   notes="Glassy high-tide water over the lagoon.")
ev("16:15","16:40","Dry off & beach time","buffer",place="bharatpur",
   notes="Beach is open till 18:00, entry free.")
ev("16:40","16:55","Ride to Laxmanpur Beach 1","travel",route="ride-bharatpur-laxmanpur")
ev("16:55","17:50","SUNSET @ Laxmanpur Beach 1","scenic",place="laxmanpur",
   notes="Sunset 17:14 - Neil's sunset stage. Dead-coral shore, so watch rather than swim.")
ev("17:50","19:00","Dinner @ Pure Veg Restaurant","meal",place="pure-veg-neil",cost_inr=800,
   cost_note="thali Rs 240 pp plus extras")
ev("19:00","19:20","Ride home","travel",route="ride-bluelagoon-pureveg")
ev("19:20","21:30","Wind down","buffer",place="hotel-bluelagoon",
   tips="Tomorrow: 04:30 up for the Sitapur sunrise, then Natural Bridge at the 08:51 low tide.")
ev("21:30","24:00","Sleep","sleep",place="hotel-bluelagoon")

it["days"][1] = {"day": 2, "date": "2026-09-24",
  "title": "GLOW RUN → NEIL UNDERWATER",
  "theme": "Night kayak in the only dark window, Kala Pathar driftwood dawn, then the early ferry to Neil for scuba, snorkel and jet ski on the same high tide.",
  "events": E}

it["philosophy"] += (" v3: on the user's call, ALL underwater activity moved to Neil/Bharatpur "
  "(their own notes and the reference video both rate it above Elephant Beach) and Elephant Beach "
  "was dropped entirely. Taking the cheap 09:15 Green Ocean instead of the 15:00 Nautika buys a full "
  "Neil afternoon, so scuba, snorkel and jet ski all sit on the verified 14:32 high tide.")
it["risks"] = [r for r in it["risks"] if "Elephant Beach trek" not in r and "v2 cost" not in r] + [
  "Scuba must be phone-booked a day ahead; no flying for 18 h after a dive - Sunday's 10:35 departure is comfortably clear",
  "Monsoon visibility on Neil is variable; if the dive is called off for sea state, the snorkel and jet ski still run and the money is refunded",
  "COST: this version runs about Rs 47,500/person, over the Rs 40,000 worst-case line. Trims listed in the app: drop the full-moon kayak (-Rs 3,500/person), swap Hotel Atlanta for Ananya Residency (-Rs 1,563/person), take Green Ocean instead of Makruzz on Friday (-Rs 775/person), shared instead of private Baratang cab (-Rs 250/person)"]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day2 events:", len(E))
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "per person")
