#!/usr/bin/env python3
"""Space out the physical load.

Problem: Thursday had a 04:15 dawn wake + scuba + jet ski; Friday had a slippery
coral walk + the Munda Pahad trek on 5.75 h of sleep; and three pre-dawn starts
ran back to back (04:15, 04:30, 03:30).

Fix: Thursday's dawn wake goes. Kala Pathar moves to a relaxed late-morning
visit after the dive — same driftwood and black rocks, no 04:15 alarm — which
buys 2.5 h of sleep before Friday, the genuinely hard day. Friday's two items
are locked by tide and gate times and cannot move, so the lever is arriving
rested. Saturday is long but physically passive: a car, a boat and a short walk.
"""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("00:00","06:45","Sleep — a proper night","sleep",place="hotel-bhuma",
   notes="9h15m. Deliberately no dawn alarm today: Friday is the physically hard day and you want to reach it rested.")
ev("06:45","07:15","Slow start","prep",place="hotel-bhuma",
   tips="Light breakfast only — you are diving in an hour and a full stomach is uncomfortable underwater.")
ev("07:15","07:50","Breakfast @ Bhuma (included)","meal",place="hotel-bhuma")
ev("07:50","08:00","Walk to the dive shop","travel",place="govind-nagar",
   notes="Bhuma sits about 50 m off Govind Nagar Beach, so this is a walk — no scooter, no parking, no queue.")
ev("08:00","10:15","SCUBA — shore dive at Govind Nagar","activity",place="govind-nagar",
   cost_inr=10500,cost_note="3 x Rs 3,500 shore Try Dive (Dive Andaman, Govind Nagar)",
   notes=("Briefing, kit-up and a guided shore dive on the reef the reference video rates as Havelock's best. "
          "The Try Dive is the shorter beginner tier: about 30 minutes underwater. Non-swimmers can dive — "
          "you breathe, the instructor does the rest."),
   tips=("TODAY'S ONE DEMANDING THING. Book by phone a day ahead. No alcohol the night before; no flying for "
         "18-24 h after — Sunday's 10:35 departure is well clear."))
ev("10:15","10:45","Dry off & rest on the beach","buffer",place="govind-nagar",
   notes="Deliberate recovery gap. First dives leave most people pleasantly wrung out.",
   tips="Drink water — you dehydrate faster than you expect on a dive.")
ev("10:45","11:00","Ride to Kala Pathar","travel",route="ride-bhuma-kalapathar")
ev("11:00","12:00","Kala Pathar — driftwood & black rocks","scenic",place="kalapathar",
   notes=("The fallen trees and black-rock shoreline, at an hour that costs you nothing. You trade the dawn "
          "light for 2.5 hours of sleep — a deliberate swap, since Friday starts at 04:30 and ends with a trek. "
          "Flip it back to a 04:35 sunrise run if the crew would rather have the light."),
   tips="Free roadside parking. Walk south along the sand for the empty unnamed stretches.")
ev("12:00","12:15","Ride back to Govind Nagar","travel",route="ride-bhuma-kalapathar")
ev("12:15","13:15","Lunch @ Something Different","meal",place="something-different",cost_inr=1000,
   cost_note="keep it to mains — salads and sides run Rs 195-345 each",
   notes="Beachside cafe rated 4.4 from 5,224 reviews, a short hop up the strip.")
ev("13:15","13:35","Pack out, ride to the jetty, return scooters","travel",route="ride-hljetty-bhuma",
   cost_inr=0,cost_note="returned inside the 24h window — no second-slot charge",
   tips="Settle Bhuma's cash bill and collect the Rs 5,000 damage deposit before you go.")
ev("13:35","14:15","Nautika check-in","prep",place="havelock-jetty",
   notes="Nautika asks you to reach 45 minutes before departure; boarding shuts 15 minutes prior.")
ev("14:15","15:00","Jetty wait","buffer",place="havelock-jetty",
   tips="Last reliable wifi and a proper toilet before Neil.")
ev("15:00","15:45","SAIL — Nautika-Pro to Neil","travel",route="ferry-havelock-neil",
   cost_inr=4800,cost_note="3 x Rs 1,600 Luxury (live operator search)")
ev("15:45","16:05","Neil scooters at the jetty","travel",place="neil-jetty",cost_inr=1000,
   cost_note="2 x ~Rs 500/day",notes="Neil On Wheels, Neil Kendra, ph +91 94742 68205 — book ahead.")
ev("16:05","16:12","Ride to Bharatpur","travel",route="ride-neiljetty-bharatpur",
   notes="Barely a kilometre from the jetty — the closest beach on the island.")
ev("16:12","16:45","JET SKI @ Bharatpur","activity",place="bharatpur",cost_inr=2100,
   cost_note="3 x Rs 700 (walk-up counter rate Rs 500-700 for a ~10-min ride)",
   notes=("Gliding over the lagoon your notes and the video both rate above Goa. Ten minutes each and it is "
          "someone else's engine doing the work — an easy end to the day rather than another exertion."),
   tips="Beach hours 05:00-18:00, entry free, jet ski counter roughly 10:00-17:00. Stash bags in a locker.")
ev("16:45","17:00","Ride to Laxmanpur Beach 1","travel",route="ride-bharatpur-laxmanpur")
ev("17:00","17:40","SUNSET @ Laxmanpur Beach 1","scenic",place="laxmanpur",
   notes="Sunset is 17:14, so you are settled well before it goes. Dead-coral shore — watch rather than swim.")
ev("17:40","17:55","Ride to dinner","travel",route="ride-bluelagoon-pureveg",
   notes="Pure Veg sits on the Lakshmanpur side, minutes from the sunset beach.")
ev("17:55","19:05","Dinner @ Pure Veg Restaurant","meal",place="pure-veg-neil",cost_inr=800,
   cost_note="thali Rs 240 pp plus extras",notes="Neil's best-rated veg kitchen, 4.8 from 254 reviews.")
ev("19:05","19:30","Ride to Blue Lagoon & check in","travel",route="ride-bluelagoon-pureveg",
   cost_inr=4118,cost_note="stay Rs 3,968 (breakfast incl., free cancellation) + Rs 150 fuel",
   notes="Refuel at IndianOil Neil Kendra on the way if it is still open — the island's only pump.")
ev("19:30","21:00","Wind down early","buffer",place="hotel-bluelagoon",
   tips="Tomorrow is the hard day: 04:30 up, Sitapur sunrise, the coral walk at low tide, then the Munda Pahad trek. Get to bed.")
ev("21:00","24:00","Sleep","sleep",place="hotel-bluelagoon")

it["days"][1] = {"day": 2, "date": "2026-09-24",
  "title": "DIVE DAY → NEIL",
  "theme": "One demanding thing done well: a shore dive at Govind Nagar, then a deliberately easy afternoon — driftwood beach, a short ferry, ten minutes on a jet ski and a sunset.",
  "events": E}

# Friday: flag the load and protect the rest before it
d3 = it["days"][2]
for e in d3["events"]:
    if e["title"].startswith("MUNDA PAHAD TREK"):
        e["tips"] = ("THE TRIP'S HARDEST HOUR — 1.5 km each way on uneven ground with a few inclines, 30-60 min "
                     "up. You slept 7 h and did nothing strenuous yesterday afternoon, which is deliberate. "
                     "Trainers, water, repellent. Turn back at the gate time rather than pushing it.")
    if e["title"].startswith("NATURAL BRIDGE"):
        e["tips"] = ("Grip water-shoes are mandatory — 200 m over slippery dead coral. Take it slowly; this and "
                     "the afternoon trek are the day's two physical items and there is no prize for rushing either.")
    if e["title"].startswith("Sleep") and e["start"] == "00:00":
        e["notes"] = "7 hours. The pacing was rebuilt so you arrive at today's coral walk and trek rested."

it["sleep_hours"] = [9.25, 7.0, 5.67, 9.75]
it["philosophy"] += (" v9: physical load spaced on the user's request. Thursday's 04:15 dawn wake was cut and "
  "Kala Pathar moved to a relaxed late morning, so the dive is the only demanding item that day and Friday - "
  "whose coral walk and trek are locked to tide and gate times - is reached on 7 h of sleep instead of 5.75.")
it["risks"] = [r for r in it["risks"] if "PACING" not in r] + [
  "PACING: one demanding activity per day — Thu the dive, Fri the coral walk plus the trek (both locked to "
  "the 08:51 low tide and the 15:00 gate, so they cannot be separated), Sat a long but physically passive "
  "Baratang run. Sleep now averages 7h55m a night, min 5h40m before Baratang."]

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day2 events:", len(E))
print("sleep per night:", it["sleep_hours"], "avg", round(sum(it["sleep_hours"]) / 4, 2))
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
