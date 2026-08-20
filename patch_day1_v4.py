#!/usr/bin/env python3
"""Day 1 v4: drop the Neil's Cove walk (user's call). With the 40 minutes of
walking gone, the pricier 12:30 Nautika is no longer needed - back to the cheap
13:15 Green Ocean (-Rs 1,200) and a relaxed Radhanagar sunset."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("03:45","04:15","Wake up & roll out (Chennai)","prep",place="maa",
   notes="Bags packed the night before. Keep each check-in bag at or under 15 kg (Akasa's free allowance; the ferries cap luggage at 15-20 kg too).",
   tips="Carry printed ferry tickets and DL photocopies for the scooter rentals.")
ev("04:15","05:15","Ride to Chennai Airport T1","travel",place="maa",
   notes="Own cab or Uber, roughly Rs 700 and outside the trip budget.")
ev("05:15","06:40","Check-in & security (Akasa)","prep",place="maa",
   notes="Akasa's domestic counters typically close 45-60 minutes before departure - confirm the exact cut-off on akasaair.com. Being at the desk by 05:15 clears any version of it.",
   tips="Web check-in the night before to skip the queue.")
ev("06:40","07:40","Gate & boarding","prep",place="maa")
ev("07:40","09:55","FLY — Akasa QP 1145 to Port Blair","travel",route="fly-maa-ixz",
   cost_inr=32163,cost_note="3 x Rs 10,721 (Cleartrip 3-adult search, 19 Aug)",
   notes="Boeing 737 MAX 8, 2h15m over the Bay of Bengal. Left-side windows get the island approach.")
ev("09:55","10:35","Land IXZ — bags & exit","prep",place="ixz",
   notes="No rush today: the ferry counter does not close until 13:00.")
ev("10:35","10:50","Cab to Junglighat","travel",route="cab-ixz-icyspicy",cost_inr=350,
   cost_note="airport taxi, ESTIMATE — no published tariff verified; carry Rs 500",
   notes="Icy Spicy sits about 3 minutes from the airport on the Junglighat side.")
ev("10:50","11:45","Veg lunch @ Icy Spicy","meal",place="icy-spicy",cost_inr=900,
   cost_note="ghee dosa Rs 149, mains Rs 250-350 (menu prices, 19 Aug)",
   notes="Port Blair's veg anchor, 4.2 stars from 3,491 reviews. A proper sit-down meal - the afternoon is unhurried.")
ev("11:45","12:00","Cab to the ferry jetty","travel",route="cab-icyspicy-phoenix",cost_inr=200,
   cost_note="short auto/taxi hop, ESTIMATE — no verified tariff",
   tips="CONFIRM THE JETTY ON YOUR TICKET. Private catamarans may sail from Haddo rather than Phoenix Bay — adjacent parts of the same harbour, but not the same gate.")
ev("12:00","13:15","Green Ocean check-in","prep",place="phoenix-bay",
   notes="The counter opens 60 minutes before sailing and shuts 15 minutes prior. A PRINTED ticket is mandatory on Green Ocean.",
   tips="Print the tickets in Chennai — do not rely on finding a printer here.")
ev("13:15","15:30","SAIL — Green Ocean 1 to Havelock","travel",route="ferry-pb-havelock",
   cost_inr=4200,cost_note="3 x Rs 1,400 all-in (Rs 1,050 + Rs 50 PMB + Rs 300 fuel)",
   notes="The cheapest verified sailing of the day.",
   tips="Take a motion-sickness tablet 30 minutes before if the sea looks up.")
ev("15:30","16:00","Scooters at the jetty, ride out","travel",route="ride-hljetty-bhuma",
   cost_inr=1000,cost_note="2 x Rs 500/24h (Go2Andaman off-season rate, valid to 30 Sep)",
   notes="Booked at least 48 h ahead with DL copies; two helmets included, fuel is not.",
   tips="Photograph both scooters at handover.")
ev("16:00","16:20","Check in @ Bhuma Homestay","prep",place="hotel-bhuma",cost_inr=6920,
   cost_note="family room for 3, breakfast incl., CASH only — rate quoted for a Sep 25-26 search; RECHECK for Sep 23-24",
   notes="9.5/10 from 226 reviews, 50 m from Govind Nagar Beach. Rs 5,000 refundable damage deposit.")
ev("16:20","16:50","Ride to Radhanagar (fuel en route)","travel",route="ride-bhuma-radhanagar",
   cost_inr=230,cost_note="~2 L petrol Rs 200 at Rs 88.66/L + parking Rs 30",
   notes="Fill both tanks at the IndianOil pump on the way — Havelock effectively has one working pump.",
   tips="Scooter parking at the beach entrance runs Rs 20-30.")
ev("16:50","17:45","RADHANAGAR BEACH — swim & sunset","scenic",place="radhanagar",
   notes="Sunset is 17:15 (verified). Blue Flag certified, with lifeguards, changing rooms and clean toilets. Get in the water first, then dry off for the sky.",
   tips="Optional if you feel like walking: Neil's Cove is about 1.2 km along the sand to the right — roughly 20 minutes each way, so only worth it if you skip the swim.")
ev("17:45","18:20","Night ride back to Govind Nagar","travel",route="ride-bhuma-radhanagar",
   notes="Dark by about 17:36. Easy pace and watch for oncoming high beams.")
ev("18:20","19:45","Dinner @ Something Different","meal",place="something-different",cost_inr=1600,
   cost_note="veg mains Rs 195-345 (TripAdvisor menu)",
   notes="Beachside cafe rated 4.4 from 5,224 reviews, a short hop from Bhuma.")
ev("19:45","21:30","Market stroll & wind down","buffer",place="hotel-bhuma",
   tips="Call Andaman Bliss tonight to confirm the 03:30 kayak. Full-moon week means they may decline — if so, sleep through to 05:30 and take Kala Pathar at dawn instead.")
ev("21:30","24:00","Sleep","sleep",place="hotel-bhuma")

it["days"][0]["events"] = E
it["days"][0]["theme"] = ("Chennai dawn flight, the catamaran to Swaraj Dweep, and an unhurried first "
                          "evening at Asia's most-photographed beach.")
it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day1 events:", len(E))
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
