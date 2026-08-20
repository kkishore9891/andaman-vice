#!/usr/bin/env python3
"""Apply the route audit: add hotel/restaurant-anchored routes with real Google
Maps distances, repoint every mismatched event, and swap in canonical Maps
listing URLs. Source: data/route_audit.json (live Maps, independently verified).
"""
import json
import re

BASE = "populate_base.py"
IT = "data/itinerary.json"
AUDIT = json.load(open("data/route_audit.json"))

# id, from, to, mode, km, min, via-waypoints (lat,lng) or None, note
NEW = [
 ("cab-ixz-icyspicy", "ixz", "icy-spicy", "cab", 0.65, 2, None,
  "Great Andaman Trunk Rd — the Junglighat side of the airport."),
 ("cab-icyspicy-phoenix", "icy-spicy", "phoenix-bay", "cab", 2.6, 7, None,
  "Great Andaman Trunk Rd north to the ferry terminal."),
 ("ride-phoenix-chidiyatapu", "phoenix-bay", "chidiya-tapu", "scooter", 26.5, 49,
  [(11.62, 92.72), (11.56, 92.71)], "NH 4 south from the jetty."),
 ("ride-chidiyatapu-atlanta", "chidiya-tapu", "hotel-atlanta", "scooter", 24.6, 46,
  [(11.56, 92.71), (11.62, 92.72)], "NH 4 back north in the dark."),
 ("cab-atlanta-jirkatang", "hotel-atlanta", "jirkatang", "cab", 48.3, 79,
  [(11.70, 92.70), (11.78, 92.67)], "NH 4. Two-wheelers are barred beyond the check post."),
 ("walk-atlanta-annapurna", "hotel-atlanta", "annapurna", "walk", 1.1, 4, None, "Rina Rd."),
 ("walk-atlanta-marina", "hotel-atlanta", "marina-park", "walk", 1.4, 3, None,
  "Rajiv Gandhi Rd and Rina Rd — the waterfront is minutes from the hotel."),
 ("cab-atlanta-ixz", "hotel-atlanta", "ixz", "cab", 3.2, 8, None, "VIP Rd."),
 ("cab-atlanta-icyspicy", "hotel-atlanta", "icy-spicy", "cab", 2.9, 9, None, "Rina Rd."),
 ("ride-hljetty-bhuma", "havelock-jetty", "hotel-bhuma", "scooter", 2.5, 7, None,
  "SH4 along the east coast."),
 ("ride-bhuma-radhanagar", "hotel-bhuma", "radhanagar", "scooter", 9.1, 19,
  [(12.038, 92.985), (12.0087171, 92.9635124)], "SH4 southwest — the island's prettiest ride."),
 ("ride-bhuma-kalapathar", "hotel-bhuma", "kalapathar", "scooter", 4.1, 8, None, "SH5 south."),
 ("ride-bhuma-elephant", "hotel-bhuma", "elephant-trek", "scooter", 6.0, 12,
  [(12.038, 92.985)], "SH4 toward Radhanagar; trailhead on the right."),
 ("ride-bhuma-kayak", "hotel-bhuma", "kayak-point", "scooter", 0.6, 3, None,
  "A few hundred metres up the beach road in the dark."),
 ("ride-neiljetty-bluelagoon", "neil-jetty", "hotel-bluelagoon", "scooter", 4.2, 7,
  [(11.828, 93.045)], "SH6 east toward the Sitapur side."),
 ("ride-bluelagoon-sitapur", "hotel-bluelagoon", "sitapur", "scooter", 1.4, 3, None,
  "SH6 — the sunrise beach is minutes from the room."),
 ("ride-bluelagoon-bharatpur", "hotel-bluelagoon", "bharatpur", "scooter", 3.9, 7,
  [(11.828, 93.045)], "SH6 west to the watersports lagoon."),
 ("ride-bluelagoon-bridge", "hotel-bluelagoon", "natural-bridge", "scooter", 5.4, 8,
  [(11.8371487, 93.0311195)], "SH6 then the village road."),
 ("ride-bluelagoon-pureveg", "hotel-bluelagoon", "pure-veg-neil", "scooter", 5.1, 8,
  [(11.8371487, 93.0311195)], "SH6 then the village road to Lakshmanpur."),
 ("ride-bharatpur-laxmanpur", "bharatpur", "laxmanpur", "scooter", 3.5, 7,
  [(11.8371487, 93.0311195)], "Via the jetty junction. (Distance derived from the two verified jetty legs.)"),
 ("ride-bridge-neiljetty", "natural-bridge", "neil-jetty", "scooter", 2.1, 4, None, "Village road."),
]

# event title -> new route id (per day)
REPOINT = {
 1: {"Cab toward town (Junglighat)": "cab-ixz-icyspicy",
     "Auto to Phoenix Bay Jetty": "cab-icyspicy-phoenix",
     "Scooters at the jetty → ride out": "ride-hljetty-bhuma",
     "Ride to Radhanagar (fuel en route)": "ride-bhuma-radhanagar",
     "Night ride back to Govind Nagar": "ride-bhuma-radhanagar"},
 2: {"Ride to the kayak launch": "ride-bhuma-kayak",
     "Ride to Kala Pathar": "ride-bhuma-kalapathar",
     "Ride back to Bhuma": "ride-bhuma-kalapathar",
     "Ride to the Elephant Beach trailhead": "ride-bhuma-elephant",
     "Ride back to Govind Nagar": "ride-bhuma-elephant",
     "Bags + jetty, return scooters": "ride-hljetty-bhuma",
     "Ride via the pump — flash check-in @ Blue Lagoon": "ride-neiljetty-bluelagoon",
     "Ride to Bharatpur": "ride-bluelagoon-bharatpur",
     "Hop to Laxmanpur": "ride-bharatpur-laxmanpur",
     "Ride home": "ride-bluelagoon-pureveg"},
 3: {"3-minute ride to Sitapur": "ride-bluelagoon-sitapur",
     "Ride back": "ride-bluelagoon-sitapur",
     "Ride to Natural Bridge": "ride-bluelagoon-bridge",
     "Jetty: return scooters + refuel-as-agreed": "ride-bridge-neiljetty",
     "Ride south to Chidiya Tapu": "ride-phoenix-chidiyatapu",
     "Night ride back to Port Blair": "ride-chidiyatapu-atlanta"},
 4: {"Cab to Jirkatang Check Post": "cab-atlanta-jirkatang",
     "Drive back to Port Blair": "cab-atlanta-jirkatang",
     "Marina Park + Flag Point at dusk": "walk-atlanta-marina",
     "Farewell dinner @ Icy Spicy": "cab-atlanta-icyspicy"},
 5: {"Cab to the airport": "cab-atlanta-ixz"},
}


def patch_base():
    src = open(BASE).read()
    if "ROUTES_V2" in src:
        print("populate_base.py already patched"); return
    coords = dict(re.findall(r'\("([\w-]+)", "[^"]*", "\w+", ([\d.]+, [\d.]+)', src))
    lines = []
    for (rid, a, b, mode, km, mins, waypts, note) in NEW:
        if a not in coords or b not in coords:
            print("  !! missing coords for", rid, a, b); continue
        pts = [tuple(float(x) for x in coords[a].split(", "))]
        pts += list(waypts or [])
        pts.append(tuple(float(x) for x in coords[b].split(", ")))
        poly = "[" + ", ".join(f"[{la}, {lo}]" for la, lo in pts) + "]"
        lines.append(f' ("{rid}", "{a}", "{b}", "{mode}", {km}, {mins},\n  {poly},\n  "{note}"),')
    block = ("\n# --- v2.3: hotel/restaurant-anchored legs, distances read live from Google\n"
             "# Maps (2026-08-20) and independently re-verified with reversed queries. ---\n"
             "ROUTES_V2 = [\n" + "\n".join(lines) + "\n]\nR = R + ROUTES_V2\n")
    src = src.replace("\n\ndef main():", block + "\n\ndef main():")
    # canonical Google Maps listing links from the audit
    links = {p["id"]: p["maps_url"] for p in AUDIT["maps"]["place_links"] if p.get("maps_url")}
    src = src.replace("    for pid, url in canonical.items():",
                      "    canonical.update(" + json.dumps(links, ensure_ascii=False) + ")\n"
                      "    for pid, url in canonical.items():")
    open(BASE, "w").write(src)
    print(f"populate_base.py: +{len(lines)} routes, {len(links)} canonical listing links")


def patch_itinerary():
    it = json.load(open(IT))
    n = 0
    for d in it["days"]:
        m = REPOINT.get(d["day"], {})
        for e in d["events"]:
            if e["title"] in m:
                if e.get("route") != m[e["title"]]:
                    e["route"] = m[e["title"]]; n += 1
    json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
    print(f"itinerary.json: {n} events repointed at correct routes")


if __name__ == "__main__":
    patch_base()
    patch_itinerary()
