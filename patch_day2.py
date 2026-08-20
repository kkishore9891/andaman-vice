#!/usr/bin/env python3
"""Itinerary v2: night-kayak attempt (only true-dark window of the trip),
Elephant Beach trek + snorkel, Nautika 15:00 to Neil, jetski late-afternoon."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

it["sleep_hours"] = [5.5, 7.0, 5.75, 9.75]
it["philosophy"] += (" v2 additions on user request: the 03:30 Thu kayak is scheduled in the trip's only "
  "true-dark window (moonset 02:54, dawn 04:47) as a confirm-by-phone attempt, and the Elephant Beach "
  "forest trek + coral-garden snorkel fills Thursday morning, pushing the Neil ferry to the verified "
  "15:00 Nautika and the jet ski to 16:35 (beach open to 18:00).")
it["risks"] = [r for r in it["risks"] if "Bioluminescence" not in r] + [
  "Night kayak (Thu 03:30) MUST be phone-confirmed Wed evening - operators often refuse full-moon week; glow will be mild, sunrise-from-kayak is the sure part. Fallback: sleep to 04:15 + Kala Pathar sunrise",
  "Elephant Beach trek is officially open but monsoon-muddy; the stream crossing needs water shoes. Fallback: Rs 1,250 pp speedboat from the jetty",
  "v2 cost is ~Rs 44,300/person - Rs 4,300 over the worst-case line. Trims if wanted: drop kayak (-Rs 3,500), Ananya hotel swap in PB (-Rs 940), Green Ocean Friday ferry (-Rs 775)"]

d1 = it["days"][0]
for e in d1["events"]:
    if e["start"] == "19:45":
        e["tips"] = ("CALL Andaman Bliss TONIGHT to confirm the 03:30 kayak (full-moon week needs explicit "
                     "operator sign-off). If refused: sleep till 04:15 and do Kala Pathar at sunrise instead.")

E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("00:00","03:00","Sleep","sleep",place="hotel-bhuma")
ev("03:00","03:20","Up in the dark (kayak kit)","prep",place="hotel-bhuma",
   tips="Dry bag, quick-dry clothes, headlamp. Skip if the operator cancelled - sleep to 04:15.")
ev("03:20","03:30","Ride to the kayak launch","travel",place="kayak-point")
ev("03:30","05:45","NIGHT KAYAK — dark-window glow attempt + sunrise on the water","activity",
   place="kayak-point",cost_inr=10500,cost_note="3 x Rs 3,500 (Andaman Bliss, all taxes)",
   notes="The trip's ONLY true darkness: moonset 02:54, civil dawn 04:47. Expect a mild sparkle at paddle-strokes, not the new-moon fireworks - then sunrise 05:09 from the kayaks.",
   tips="Basic swimming required (age 13-45 rule). Phones in dry bag only.")
ev("05:45","06:10","Ride to Kala Pathar","travel",route="ride-govind-kalapathar",
   notes="Golden hour is 05:45-06:45 - straight there while the light is soft.")
ev("06:10","06:50","Kala Pathar — fallen trees & black rocks","scenic",place="kalapathar",
   notes="The rustic driftwood-and-jungle shoreline from the video. Free roadside parking.")
ev("06:50","07:05","Ride back to Bhuma","travel",route="ride-govind-kalapathar")
ev("07:05","07:55","Breakfast @ Bhuma (incl.)","meal",place="hotel-bhuma")
ev("07:55","08:15","Checkout — bags stored at Bhuma","prep",place="hotel-bhuma",
   tips="Homestay holds luggage till the 13:00 pickup; settle the cash bill now.")
ev("08:15","08:35","Ride to the Elephant Beach trailhead","travel",route="ride-govind-elephant")
ev("08:35","09:15","TREK — giant trees to Elephant Beach","activity",route="walk-elephant",
   notes="1.7 km forest trail past enormous buttress-root trees; stream crossing near the end.",
   tips="Clogs/water shoes, mosquito repellent. Trail is flat but monsoon-muddy.")
ev("09:15","11:00","ELEPHANT BEACH — snorkel the coral garden","activity",place="elephant-beach",
   cost_inr=2400,cost_note="~Rs 800 pp gear+guide on the beach (on-spot rate, estimate)",
   notes="Shallow reef right off the sand - the transcript's favourite snorkel. Book water sports ON the beach, never prepaid.",
   tips="No restaurants here - carry water/fruit. Lockers/showers at small extra cost.")
ev("11:00","11:40","Trek back to the trailhead","travel",route="walk-elephant")
ev("11:40","12:00","Ride back to Govind Nagar","travel",route="ride-govind-elephant")
ev("12:00","13:00","Lunch @ Something Different","meal",place="something-different",cost_inr=1600,
   notes="Opens 11:30 - beachside table, veg mains Rs 195-345.")
ev("13:00","13:20","Bags + jetty, return scooters","travel",route="ride-jetty-govind",cost_inr=500,
   cost_note="possible 2nd-slot charge (10am-10am rental windows)",
   tips="Hand scooters back with the agreed fuel level.")
ev("13:20","14:15","Nautika check-in (45 min)","prep",place="havelock-jetty")
ev("14:15","15:00","Jetty wait","buffer",place="havelock-jetty")
ev("15:00","15:45","SAIL — Nautika-Pro to Neil","travel",route="ferry-havelock-neil",
   cost_inr=4800,cost_note="3 x Rs 1,600 Luxury (verified live)")
ev("15:45","16:05","Neil scooters @ jetty","travel",place="neil-jetty",cost_inr=1000,
   cost_note="2 x ~Rs 500/day",notes="Neil On Wheels, ph +91 94742 68205 - book ahead.")
ev("16:05","16:20","Ride via the pump — flash check-in @ Blue Lagoon","travel",
   route="ride-neiljetty-sitapur",cost_inr=4118,
   cost_note="stay Rs 3,968 (breakfast incl., free cancel) + Rs 150 fuel",
   notes="Top up at IndianOil Neil Kendra (closes ~18:00) on the way; drop bags, straight back out.")
ev("16:20","16:35","Ride to Bharatpur","travel",route="ride-neiljetty-bharatpur")
ev("16:35","17:05","JET SKI @ Bharatpur","activity",place="bharatpur",cost_inr=2400,
   cost_note="3 x Rs 800 (10-15 min each; verified range 800-1,200)",
   notes="Beach open till 18:00; tide still ~1.5 m - plenty of water in the lagoon.")
ev("17:05","17:15","Hop to Laxmanpur","travel",route="ride-neiljetty-laxmanpur")
ev("17:15","17:50","SUNSET @ Laxmanpur Beach 1","scenic",place="laxmanpur",
   notes="Sunset 17:14 - Neil's sunset stage.")
ev("17:50","19:00","Dinner @ Pure Veg Restaurant","meal",place="pure-veg-neil",cost_inr=800,
   cost_note="thali Rs 240 pp + extras")
ev("19:00","19:20","Ride home","travel",route="ride-neiljetty-sitapur")
ev("19:20","21:30","Wind down","buffer",place="hotel-bluelagoon",
   tips="Tomorrow: 04:30 wake for Sitapur sunrise, then Natural Bridge at the 08:51 low tide.")
ev("21:30","24:00","Sleep","sleep",place="hotel-bluelagoon")

it["days"][1] = {"day": 2, "date": "2026-09-24",
  "title": "GLOW RUN → SHAHEED DWEEP",
  "theme": "Night kayak in the only dark window, Kala Pathar driftwood dawn, the giant-tree trek to Elephant Beach, then Neil by 15:45 for jet ski and sunset.",
  "events": E}

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day2 events:", len(E), "| new crew total: Rs", it["total_cost_inr"])
