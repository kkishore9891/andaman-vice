#!/usr/bin/env python3
"""Day 2 v5: water activity moves to GOVIND NAGAR (user's call) - snorkel and
scuba both happen on the beach the homestay sits on, so the Elephant Beach trek,
its speedboat and all that travel disappear. Jet ski stays at Bharatpur on Neil.
"""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("00:00","03:00","Sleep","sleep",place="hotel-bhuma")
ev("03:00","03:20","Up in the dark (kayak kit)","prep",place="hotel-bhuma",
   tips="Dry bag, quick-dry clothes, headlamp. If the operator declined, sleep to 05:30 and start at Kala Pathar instead.")
ev("03:20","03:30","Ride to the kayak launch","travel",route="ride-bhuma-kayak",place="kayak-point")
ev("03:30","05:45","NIGHT KAYAK — dark-window glow attempt + sunrise on the water","activity",
   place="kayak-point",cost_inr=10500,cost_note="3 x Rs 3,500 (Andaman Bliss, all taxes)",
   notes="The trip's only true darkness: moonset 02:54, civil dawn 04:47. Expect a mild sparkle at the paddle strokes rather than new-moon fireworks - then sunrise 05:09 from the kayaks.",
   tips="Basic swimming required (the operator's age 13-45 rule). Phones in a dry bag only.")
ev("05:45","06:10","Ride to Kala Pathar","travel",route="ride-bhuma-kalapathar",
   notes="Golden hour runs to about 06:45 - go straight there while the light is soft.")
ev("06:10","06:50","Kala Pathar — fallen trees & black rocks","scenic",place="kalapathar",
   notes="The driftwood-and-jungle shoreline from the reference video. Free roadside parking.")
ev("06:50","07:05","Ride back to Bhuma","travel",route="ride-bhuma-kalapathar")
ev("07:05","07:45","Breakfast @ Bhuma (included)","meal",place="hotel-bhuma",
   tips="Ask the night before for an early serving - you are in the water by 08:00.")
ev("07:45","08:00","Walk to the dive shop","travel",place="govind-nagar",
   notes="Bhuma sits about 50 m off Govind Nagar Beach, so this is a walk, not a ride - no scooter, no parking, no jetty queue.")
ev("08:00","10:15","SCUBA — shore dive at Govind Nagar","activity",place="govind-nagar",
   cost_inr=10500,cost_note="3 x Rs 3,500 shore Try Dive (Dive Andaman, Beach No.2 Govind Nagar) — PRICE BEING RE-CONFIRMED LIVE",
   notes="Briefing, kit-up and a guided shore dive on the reef the reference video rates as Havelock's best - a massive coral bed with clownfish among it. Non-swimmers can dive: you breathe, the instructor handles the rest.",
   tips="Book by phone a day ahead. No alcohol the night before. No flying for 18-24 h after a dive - Sunday's 10:35 departure is comfortably clear.")
ev("10:15","11:30","SNORKEL at Govind Nagar","activity",place="govind-nagar",
   cost_inr=1800,cost_note="~Rs 600 pp gear hire on the beach, ESTIMATE — being confirmed",
   notes="Straight back in off the same beach with a mask once the tanks are off. Shallow coral close to shore, and no boat transfer to pay for.",
   tips="Rent gear from the dive shop you just dived with - they will usually throw it in cheap.")
ev("11:30","12:15","Shower, pack & checkout","prep",place="hotel-bhuma",
   notes="Settle the cash bill and collect the Rs 5,000 damage deposit.")
ev("12:15","13:15","Lunch @ Something Different","meal",place="something-different",cost_inr=1600,
   cost_note="veg mains Rs 195-345 (TripAdvisor menu)",
   notes="Beachside cafe rated 4.4 from 5,224 reviews, a short hop up the strip.")
ev("13:15","13:35","Ride to the jetty, return scooters","travel",route="ride-hljetty-bhuma",
   cost_inr=500,cost_note="possible second-slot charge (rentals run on 10am-10am windows)",
   tips="Hand the scooters back with the agreed fuel level.")
ev("13:35","14:15","Nautika check-in","prep",place="havelock-jetty",
   notes="Nautika asks you to reach 45 minutes before departure; boarding shuts 15 minutes prior.")
ev("14:15","15:00","Jetty wait","buffer",place="havelock-jetty",
   tips="Last reliable wifi and a proper toilet before Neil.")
ev("15:00","15:45","SAIL — Nautika-Pro to Neil","travel",route="ferry-havelock-neil",
   cost_inr=4800,cost_note="3 x Rs 1,600 Luxury (live operator search, 19 Aug)")
ev("15:45","16:05","Neil scooters at the jetty","travel",place="neil-jetty",cost_inr=1000,
   cost_note="2 x ~Rs 500/day",
   notes="Neil On Wheels, Neil Kendra (5.0-rated), ph +91 94742 68205 - book ahead.")
ev("16:05","16:12","Ride to Bharatpur","travel",route="ride-neiljetty-bharatpur",
   notes="Bharatpur is barely a kilometre from the jetty - the closest beach on the island.")
ev("16:12","16:45","JET SKI @ Bharatpur","activity",place="bharatpur",cost_inr=2400,
   cost_note="3 x Rs 800 (10-15 min each; verified range 800-1,200)",
   notes="Gliding over the lagoon your notes and the video both rate above Goa. Beach is free to enter and open to 18:00.",
   tips="CHECK COUNTER HOURS when booking - one source says the watersports desks close at 15:00, which would push this to Friday morning. Stash the bags in a beach locker while you ride.")
ev("16:45","17:00","Ride to Laxmanpur Beach 1","travel",route="ride-bharatpur-laxmanpur")
ev("17:00","17:40","SUNSET @ Laxmanpur Beach 1","scenic",place="laxmanpur",
   notes="Sunset is 17:14 (verified), so you are settled well before it goes. Dead-coral shore - watch rather than swim.")
ev("17:40","17:55","Ride to dinner","travel",route="ride-bluelagoon-pureveg",
   notes="Pure Veg sits on the Lakshmanpur side, minutes from the sunset beach.")
ev("17:55","19:05","Dinner @ Pure Veg Restaurant","meal",place="pure-veg-neil",cost_inr=800,
   cost_note="thali Rs 240 pp plus extras",
   notes="Neil's best-rated veg kitchen, 4.8 stars from 254 reviews.")
ev("19:05","19:30","Ride to Blue Lagoon & check in","travel",route="ride-bluelagoon-pureveg",
   cost_inr=4118,cost_note="stay Rs 3,968 (breakfast incl., free cancellation) + Rs 150 fuel — RE-PRICING LIVE for Sep 24-25",
   notes="Refuel at IndianOil Neil Kendra on the way if it is still open - it is the island's only pump.",
   tips="Tomorrow starts at 04:30 for the Sitapur sunrise, so unpack only what you need.")
ev("19:30","21:30","Wind down","buffer",place="hotel-bluelagoon",
   tips="Tomorrow: Sitapur sunrise, then Natural Bridge at the 08:51 low tide.")
ev("21:30","24:00","Sleep","sleep",place="hotel-bluelagoon")

it["days"][1] = {"day": 2, "date": "2026-09-24",
  "title": "GLOW RUN → GOVIND NAGAR REEF → NEIL",
  "theme": "Night kayak in the only dark window, driftwood dawn at Kala Pathar, then scuba and snorkel straight off the beach the homestay sits on - and jet ski at Bharatpur before the Neil sunset.",
  "events": E}

it["philosophy"] += (" v5: snorkelling and scuba both moved to Govind Nagar on the user's call - the "
  "homestay is 50 m from that beach, which deletes the Elephant Beach trek, its speedboat fare and "
  "roughly two hours of travel. Jet ski stays at Bharatpur.")
it["risks"] = [r for r in it["risks"] if "Elephant Beach" not in r] + [
  "Govind Nagar scuba price (Rs 3,500 pp shore Try Dive, Dive Andaman) and the snorkel gear rate are being re-confirmed live - treat Thursday's water costs as provisional",
  "Bharatpur watersports counter hours are disputed (one source says 08:00-15:00): if they shut at 15:00 the 16:12 jet ski must move to Friday morning after Natural Bridge"]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day2 events:", len(E))
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
