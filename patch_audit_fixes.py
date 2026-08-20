#!/usr/bin/env python3
"""Apply the per-event audit's non-browser fixes.

Biggest change: Day 1 moves to the Nautika-Pro 12:30 sailing (arr 14:00) instead
of Green Ocean 13:15 (arr 15:30). The old clock made Neil's Cove impossible - a
1.2 km/20-min walk each way squeezed into 20 minutes, with sunset back at
Radhanagar at the same instant. +Rs 1,200 for the crew buys 90 real minutes.
"""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

# ---------------- Day 1 rebuild ----------------
E = []
def ev(s, t, title, cat, **kw):
    E.append(dict({"start": s, "end": t, "title": title, "category": cat}, **kw))

ev("03:45","04:15","Wake up & roll out (Chennai)","prep",place="maa",
   notes="Bags packed the night before. Keep each check-in bag at or under 15 kg (Akasa's free allowance; the Nautika ferry caps luggage at 15 kg too).",
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
   notes="Tight-ish turnaround today: the ferry check-in closes at 11:45, so move briskly.")
ev("10:35","10:50","Cab to Junglighat","travel",route="cab-ixz-icyspicy",cost_inr=350,
   cost_note="airport taxi, ESTIMATE — no published tariff verified; carry Rs 500",
   notes="Icy Spicy sits about 3 minutes from the airport on the Junglighat side.")
ev("10:50","11:30","Quick veg lunch @ Icy Spicy","meal",place="icy-spicy",cost_inr=900,
   cost_note="ghee dosa Rs 149, mains Rs 250-350 (menu prices, 19 Aug)",
   notes="Port Blair's veg anchor, 4.2 stars from 3,491 reviews. Order dosas - they arrive fastest.",
   tips="Ask for the bill when the food lands; the ferry counter closes at 11:45.")
ev("11:30","11:45","Cab to the ferry jetty","travel",route="cab-icyspicy-phoenix",cost_inr=200,
   cost_note="short auto/taxi hop, ESTIMATE — no verified tariff",
   tips="CONFIRM THE JETTY ON YOUR TICKET. Private catamarans may sail from Haddo rather than Phoenix Bay — the two are adjacent parts of the same harbour but not the same gate.")
ev("11:45","12:30","Nautika check-in","prep",place="phoenix-bay",
   notes="Nautika asks you to reach 45 minutes before departure; boarding shuts 15 minutes prior.",
   tips="Luggage is capped at 15 kg per person, with excess at Rs 100/kg.")
ev("12:30","14:00","SAIL — Nautika-Pro to Havelock","travel",route="ferry-pb-havelock",
   cost_inr=5400,cost_note="3 x Rs 1,800 Luxury (live operator search, 19 Aug)",
   notes="Chosen over the cheaper 13:15 Green Ocean because arriving 14:00 instead of 15:30 is what makes Neil's Cove and the Radhanagar sunset both possible today.",
   tips="Take a motion-sickness tablet 30 minutes before if the sea looks up.")
ev("14:00","14:30","Scooters at the jetty, ride out","travel",route="ride-hljetty-bhuma",
   cost_inr=1000,cost_note="2 x Rs 500/24h (Go2Andaman off-season rate, valid to 30 Sep)",
   notes="Booked at least 48 h ahead with DL copies; two helmets included, fuel is not.",
   tips="Photograph both scooters at handover.")
ev("14:30","14:50","Check in @ Bhuma Homestay","prep",place="hotel-bhuma",cost_inr=6920,
   cost_note="family room for 3, breakfast incl., CASH only — rate quoted for a Sep 25-26 search; RECHECK for Sep 23-24",
   notes="9.5/10 from 226 reviews, 50 m from Govind Nagar Beach. Rs 5,000 refundable damage deposit.")
ev("14:50","15:20","Ride to Radhanagar (fuel en route)","travel",route="ride-bhuma-radhanagar",
   cost_inr=230,cost_note="~2 L petrol Rs 200 at Rs 88.66/L + parking Rs 30",
   notes="Fill both tanks at the IndianOil pump on the way — Havelock effectively has one working pump.",
   tips="Scooter parking at the beach entrance runs Rs 20-30.")
ev("15:20","15:40","Walk to Neil's Cove","travel",route="walk-radhanagar-cove",
   notes="About 1.2 km along the sand to the right of the main beach.",
   tips="Barefoot is fine on sand; carry water.")
ev("15:40","16:50","Neil's Cove — the quiet lagoon","scenic",place="neils-cove",
   notes="The crowd stays behind at the main beach. Swim, float, and have the water largely to yourselves.",
   tips="Exact position is approximate — there is no Google Maps listing for the cove; just keep the sea on your left walking north-west.")
ev("16:50","17:10","Walk back to Radhanagar","travel",route="walk-radhanagar-cove")
ev("17:10","17:45","SUNSET @ Radhanagar Beach","scenic",place="radhanagar",
   notes="Sunset is 17:15 (verified). Radhanagar holds Blue Flag certification; the beach is patrolled and has changing rooms.",
   tips="Stay for the afterglow — the sky keeps working for about 20 minutes after the sun goes.")
ev("17:45","18:20","Night ride back to Govind Nagar","travel",route="ride-bhuma-radhanagar",
   notes="Dark by about 17:36. Easy pace and watch for oncoming high beams.")
ev("18:20","19:45","Dinner @ Something Different","meal",place="something-different",cost_inr=1600,
   cost_note="veg mains Rs 195-345 (TripAdvisor menu)",
   notes="Beachside cafe rated 4.4 from 5,224 reviews, a short hop from Bhuma.")
ev("19:45","21:30","Market stroll & wind down","buffer",place="hotel-bhuma",
   tips="Call Andaman Bliss tonight to confirm the 03:30 kayak. Full-moon week means they may decline — if so, sleep through to 05:30 and take Kala Pathar at dawn instead.")
ev("21:30","24:00","Sleep","sleep",place="hotel-bhuma")

it["days"][0]["events"] = E
it["days"][0]["theme"] = ("Chennai dawn flight, the fast catamaran to Swaraj Dweep, then a full "
                          "afternoon at the quiet end of Asia's most-photographed beach.")

# ---------------- targeted fixes on other days ----------------
def find(day, title_startswith):
    for e in it["days"][day - 1]["events"]:
        if e["title"].startswith(title_startswith):
            return e
    return None

# D2: sunset block must start BEFORE the 17:14 sun, not after
e = find(2, "SUNSET @ Laxmanpur")
if e:
    e["start"] = "16:45"; e["end"] = "17:40"
    e["notes"] = ("Sunset is 17:14 (verified) — be on the sand by 16:45 so you are settled before it goes. "
                  "Dead-coral shore, so watch rather than swim.")
for t, s, en in (("JET SKI runs", "15:45", "16:15"), ("Dry off & beach time", "16:15", "16:30"),
                 ("Ride to Laxmanpur Beach 1", "16:30", "16:45")):
    e = find(2, t)
    if e: e["start"], e["end"] = s, en
e = find(2, "Dinner @ Pure Veg")
if e: e["start"] = "17:40"

# D4: convoy arithmetic, unsupported legal claim, cave specifics, food gap, marina walk
e = find(4, "Return convoy")
if e:
    e["start"], e["end"] = "12:10", "13:35"
    e["notes"] = ("Convoy departure times vary by source (12:00 or 12:30) — your driver knows the day's slot. "
                  "The escorted run back to Jirkatang takes about 83 minutes.")
e = find(4, "CONVOY through the Jarawa")
if e:
    e["tips"] = ("You may glimpse Jarawa people. Cameras stay packed — operators are absolute about it: "
                 "no photographs, no stopping, windows up when asked.")
e = find(4, "LIMESTONE CAVES")
if e:
    e["notes"] = ("A walk inland from the boat drop through mangrove and forest to the sculpted chambers. "
                  "Operators schedule roughly 09:00-10:00 at the caves.")
    e["tips"] = "A headlamp beats a phone torch; the floor is wet and uneven."
e = find(4, "Drive back to Port Blair")
if e: e["start"] = "13:35"
e = find(4, "Marina Park")
if e:
    e["notes"] = ("Flag Point on the Marina Park waterfront — where the first tricolour was raised on Indian "
                  "soil on 30 Dec 1943, per the reference video. A five-minute walk from the hotel door.")
e = find(4, "Early lunch @ Baratang")
if e:
    e["cost_note"] = "simple jetty meals for 3, ESTIMATE — no verified Baratang food prices"
    e["notes"] = "Basic canteen fare at the jetty. Confirm a veg option with your driver — carry backup snacks."

# D5: unsupported counter-closing time
e = find(5, "Check-in + security")
if e:
    e["notes"] = ("Akasa's domestic counters typically close 45-60 minutes before departure — confirm on "
                  "akasaair.com. Arriving 08:05 for a 10:35 flight clears any version of the rule.")

# hotel rate provenance
e = find(3, "Check in @ Hotel Atlanta")
if e: e["cost_note"] = ("family room, 2 nights, free cancellation — Booking.com quote captured for these dates "
                        "on 19 Aug; RECHECK before booking")
e = find(2, "Ride to Blue Lagoon")
if e: e["cost_note"] = ("stay Rs 3,968 (breakfast incl., free cancellation) + Rs 150 fuel — rate quoted for a "
                        "Sep 26-27 search; RECHECK for Sep 24-25")

it["total_cost_inr"] = sum(e.get("cost_inr", 0) or 0 for d in it["days"] for e in d["events"])
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("day1 events:", len(E))
print("crew total: Rs", it["total_cost_inr"], "= Rs", round(it["total_cost_inr"] / 3), "pp")
