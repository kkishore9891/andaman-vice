#!/usr/bin/env python3
"""Populate places, routes, facts, meta from the verified fact base.
Events are inserted later by populate_events.py once the itinerary is final.
All coordinates from live Google Maps reads (see data/factbase.json)."""
import json
import db

PETROL = 88.66          # Rs/L, A&N, 2026-08-19 (NDTV fuel prices)
KMPL = 45.0             # Honda Activa-class real-world (BikeWale owner-reported 47-50)
FB = db.DB_PATH.rsplit("/", 1)[0] + "/data/factbase.json"

P = [  # id, name, island, lat, lng, kind, photo, blurb
 ("maa", "Chennai Airport (MAA)", "chennai", None, None, "airport", None,
  "Kamaraj Domestic Terminal. Akasa QP 1145 departs 07:40 — be at bag-drop by 06:10."),
 ("ixz", "Veer Savarkar Intl Airport", "south_andaman", 11.641656, 92.730243, "airport", None,
  "Port Blair / Sri Vijaya Puram airport (IXZ). 3.4 km from Phoenix Bay Jetty."),
 ("phoenix-bay", "Phoenix Bay Jetty", "south_andaman", 11.6726921, 92.7345295, "jetty", None,
  "Private ferry terminal (Makruzz/Nautika/Green Ocean). Check-in ~60 min before sailing."),
 ("haddo-jetty", "Haddo Jetty (Gate 3)", "south_andaman", 11.6790, 92.7255, "jetty", None,
  "Where the PRIVATE catamarans sail from — Makruzz, Nautika, Green Ocean. NOT Phoenix Bay, which is the government ferry terminal about 1 km away. Green Ocean e-tickets print 'Haddo (Gate-3)'; reporting is 60 min before departure (Nautika 45). (Position approximate — confirm the gate printed on your ticket.)"),
 ("aberdeen", "Aberdeen Bazaar", "south_andaman", 11.6675019, 92.7412765, "other", None,
  "Port Blair city hub — hotels, food, market."),
 ("cellular-jail", "Cellular Jail", "south_andaman", 11.6747447, 92.7478601, "viewpoint", "assets/cellular-jail.jpg",
  "National memorial. Optional evening light-and-sound show."),
 ("marina-park", "Marina Park / Flag Point", "south_andaman", 11.6698312, 92.7474232, "viewpoint", "assets/marina-flag-point.jpg",
  "Where Netaji hoisted the first tricolour on Indian soil (30 Dec 1943). Scenic evening walk."),
 ("chidiya-tapu", "Chidiya Tapu Beach", "south_andaman", 11.5059682, 92.7014649, "beach", "assets/chidiya-tapu.jpg",
  "Sunset amphitheatre of South Andaman. No swimming — saltwater crocodiles are spotted here."),
 ("munda-pahad", "Munda Pahad", "south_andaman", 11.4914543, 92.7087511, "viewpoint", None,
  "1.3 km clifftop trek (~30 min each way) from Munda Pahad Beach. Trek entry closes 15:00, area by 16:00."),
 ("jirkatang", "Jirkatang Check Post", "south_andaman", 11.8396935, 92.6538333, "other", None,
  "Jarawa reserve convoy gate. First convoy 06:00 — no photography beyond this point."),
 ("middle-strait", "Middle Strait Jetty", "south_andaman", 12.1599132, 92.7557293, "jetty", None,
  "Vehicle-ferry point to Baratang (Nilambur) across the strait."),
 ("nilambur", "Nilambur Jetty, Baratang", "baratang", 12.1702177, 92.7624788, "jetty", None,
  "Baratang side. Speedboats to the limestone-cave drop point (₹900 pp round trip)."),
 ("limestone-caves", "Limestone Caves", "baratang", 12.0959029, 92.7454867, "cave", "assets/limestone-caves-baratang.jpg",
  "Sedimentary cathedral shaped over millions of years. Speedboat + ~1.2 km walk through mangrove."),
 ("wandoor", "Wandoor Jetty", "south_andaman", 11.5936441, 92.6093126, "jetty", None,
  "Gateway to Mahatma Gandhi Marine NP (Red Skin / Jolly Buoy). Forest permit issued a day ahead."),
 ("red-skin", "Red Skin Island", "south_andaman", 11.5559255, 92.5916443, "beach", "assets/jolly-buoy.jpg",
  "MGMNP island OPEN in September (Jolly Buoy closed 16 May–14 Nov). Monsoon sailings weather-dependent. (Photo: neighbouring Jolly Buoy.)"),
 ("havelock-jetty", "Havelock Jetty", "havelock", 12.0429471, 92.9835984, "jetty", "assets/ferry-makruzz.jpg",
  "Swaraj Dweep ferry terminal. Scooter delivery at the gate (Go2Andaman, ₹500/day off-season)."),
 ("govind-nagar", "Govind Nagar Beach", "havelock", 12.0306216, 93.000842, "beach", "assets/govind-nagar-beach.jpg",
  "Beach No.3 strip — dive schools, cafés, the island's working petrol pump nearby."),
 ("radhanagar", "Radhanagar Beach", "havelock", 11.9844552, 92.9508454, "beach", "assets/radhanagar-beach.jpg",
  "Blue-Flag certified, among Asia's best beaches. Sunset 17:14. Scooter parking ₹20–30."),
 ("neils-cove", "Neil's Cove", "havelock", 11.9922, 92.9430, "beach", "assets/neils-cove.jpg",
  "Secluded lagoon ~1.2 km walk right of Radhanagar. (Position approximate — no Maps listing exists.)"),
 ("kalapathar", "Kala Pathar Beach", "havelock", 12.0006111, 93.0070952, "beach", "assets/kalapathar-beach.jpg",
  "Sunrise beach with fallen trees and black rocks. Be there 04:45; sunrise 05:09. Free roadside parking."),
 ("elephant-beach", "Elephant Beach", "havelock", 12.0081083, 92.9416061, "beach", "assets/elephant-beach.jpg",
  "Watersports hub reached by speedboat (₹1,250 pp incl. snorkel dip, from 1 Sep 2026) or 1.5 km trek."),
 ("elephant-trek", "Elephant Beach Trailhead", "havelock", 12.0087171, 92.9635124, "other", None,
  "'Walking Path to Elephant Beach' on the Radhanagar road (SH4)."),
 ("hl-pump", "IndianOil Havelock (Radhanagar road)", "havelock", 12.008853, 92.97162, "pump", None,
  "The island's working petrol pump (opens 06:00) — conveniently ON the Radhanagar road (SH4)."),
 ("kayak-point", "Kayak Night Launch (Beach No.5 area)", "havelock", 12.026, 93.003, "other", "assets/bioluminescence.jpg",
  "Andaman Bliss night-kayak meet point (exact spot confirmed on booking, ₹3,500 pp). On THIS trip the only true-dark window is 03:00–04:47 on the night of Sep 23→24 (moonset 02:54) — glow will be mild near full moon; sunrise from the kayak is the guaranteed part. (Position approximate.)"),
 ("neil-jetty", "Shaheed Dweep Jetty", "neil", 11.8371487, 93.0311195, "jetty", None,
  "Neil Island ferry terminal. Everything on the island is within 6 km."),
 ("bharatpur", "Bharatpur Beach", "neil", 11.8361324, 93.034197, "beach", "assets/bharatpur-beach.jpg",
  "Jet ski + snorkelling lagoon, 1.1 km from jetty. Best at HIGH tide. Open 05:00–18:00, free entry."),
 ("natural-bridge", "Natural Bridge", "neil", 11.8320292, 93.0139828, "beach", "assets/natural-bridge-neil.jpg",
  "Howrah Bridge coral arch at Laxmanpur Beach 2. Walk 200 m over dead coral — LOW tide only, wear grip shoes."),
 ("laxmanpur", "Laxmanpur Beach 1", "neil", 11.847006, 93.0156096, "beach", "assets/laxmanpur-beach.jpg",
  "Neil's sunset beach. Dead-coral shore — watch the sky, not a swim."),
 ("sitapur", "Sitapur Beach", "neil", 11.8261573, 93.0650936, "beach", "assets/sitapur-beach.jpg",
  "Sunrise point of Neil; pink-tinged sand, photo cave + shipwreck a 500 m walk along the shore."),
 ("neil-pump", "IndianOil Neil Kendra", "neil", 11.832, 93.031, "pump", None,
  "Neil's ONLY pump (~1 km from jetty). Practical hours ~07:00–18:00 — refuel by evening. (Position from plus code.)"),
 # stays (live Booking.com picks, 2026-08-19; positions approximate from listed distances)
 ("hotel-pibo", "Pibo Homestay", "south_andaman", 11.6540, 92.7300, "hotel", None,
  "Port Blair base — 9.3/10 from 138 reviews. Family room sleeping 3 (1 full + 1 king), breakfast included, free cancellation to 24 Sep. Rs 5,250 for both nights: Rs 875 per person per night, well under the Rs 2,000 target and Rs 3,595 cheaper than Hotel Atlanta. (Position approximate — 2.9 km from downtown, 1.2 km from the beach.)"),
 ("hotel-atlanta", "Hotel Atlanta — A Seaview Hotel", "south_andaman", 11.6721653, 92.7455293, "hotel", None,
  "Port Blair base. Beachfront block opposite the Marina Park–Phoenix Bay stretch (location score 9.3). Family room for 3 ≈ ₹4,423/night, free cancellation."),
 ("hotel-bhuma", "Bhuma Homestay", "havelock", 12.0314836, 92.9960689, "hotel", None,
  "Havelock base — 9.5/10 from 226 reviews. 50 m to Govind Nagar Beach, breakfast included. ₹6,920/night for 3. Cash-only, non-refundable, ₹5,000 damage deposit."),
 ("hotel-bluelagoon", "Blue Lagoon Resort", "neil", 11.8178389, 93.0530135, "hotel", None,
  "Neil base — 8.6/10 from 256 reviews, on the SITAPUR side: sunrise beach is a 3-min ride. King room w/ balcony + breakfast ≈ ₹3,968/night, free cancellation."),
 # veg food (live Google Maps/Zomato research, 2026-08-19; pin positions pending QA pass)
 ("icy-spicy", "Icy Spicy — Pure Veg", "south_andaman", 11.6587633, 92.7313498, "restaurant", None,
  "Port Blair's veg anchor (4.2★, 3,491 reviews), Junglighat. Ghee dosa ₹149, Veg Manchurian ₹280. Dinner for 3 ≈ ₹700–1,100."),
 ("annapurna", "Annapurna Cafeteria", "south_andaman", 11.6671159, 92.7423254, "restaurant", None,
  "Veg South-Indian stalwart in Aberdeen Bazaar (3.7★, 4,487 reviews). Opens 07:00 — the pre-ferry breakfast stop."),
 ("something-different", "Something Different — A Beachside Cafe", "havelock", 12.035727, 92.989741, "restaurant", None,
  "Havelock beachside dinner (4.4★, 5,224 reviews), Beach No.2. Veg mains ₹195–345; ~₹1,400–1,800 for 3. Opens 11:30."),
 ("pure-veg-neil", "Pure Veg Restaurant (Lakshmanpur)", "neil", 11.8414615, 93.0197503, "restaurant", None,
  "Neil's top veg spot (4.8★, 254 reviews), near Hotel Samsaara, Lakshmanpur. Thali ≈ ₹240. Opens 08:00."),
]

# id, from, to, mode, km, min, polyline([[lat,lng],..]), note
R = [
 # Chennai is 12° of longitude off-map, so the drawn line is the final APPROACH
 # corridor (the plane traces it); the full 1,355 km sits in the stats.
 ("fly-maa-ixz", "maa", "ixz", "flight", 1355, 135,
  [[12.35, 92.52], [12.10, 92.56], [11.90, 92.61], [11.75, 92.66], [11.641656, 92.730243]],
  "Akasa QP 1145 (Boeing 737 MAX 8), 07:40→09:55, 2h15m over the Bay of Bengal. "
  "The line on the map is the final approach into Port Blair from the west — the full 1,355 km crossing starts far off-map at Chennai."),
 ("fly-ixz-maa", "ixz", "maa", "flight", 1355, 130,
  [[11.641656, 92.730243], [11.75, 92.66], [11.90, 92.61], [12.10, 92.56], [12.35, 92.52]],
  "Return over the Bay of Bengal to Chennai. The map shows the departure corridor heading west-north-west; Chennai lies 1,355 km beyond the frame."),
 ("cab-ixz-phoenix", "ixz", "phoenix-bay", "cab", 3.4, 8, [[11.641656, 92.730243], [11.658, 92.729], [11.6726921, 92.7345295]],
  "Via VIP Rd."),
 ("cab-ixz-aberdeen", "ixz", "aberdeen", "cab", 2.7, 7, [[11.641656, 92.730243], [11.655, 92.737], [11.6675019, 92.7412765]],
  "Via VIP Rd."),
 ("ride-pb-chidiyatapu", "aberdeen", "chidiya-tapu", "scooter", 24.0, 44,
  [[11.6675019, 92.7412765], [11.62, 92.72], [11.56, 92.71], [11.5059682, 92.7014649]], "NH4 south."),
 ("ride-chidiyatapu-munda", "chidiya-tapu", "munda-pahad", "scooter", 2.2, 8,
  [[11.5059682, 92.7014649], [11.4914543, 92.7087511]], "Munda Pahad Beach Rd."),
 ("cab-pb-jirkatang", "aberdeen", "jirkatang", "cab", 47.4, 72,
  [[11.6675019, 92.7412765], [11.70, 92.70], [11.78, 92.67], [11.8396935, 92.6538333]],
  "NH4. Two-wheelers NOT allowed beyond the check post — closed cab only."),
 ("cab-jirkatang-middlestrait", "jirkatang", "middle-strait", "convoy", 47.7, 83,
  [[11.8396935, 92.6538333], [11.95, 92.67], [12.05, 92.71], [12.1599132, 92.7557293]],
  "Escorted convoy through Jarawa reserve. No photos, no stops."),
 ("boat-middlestrait-nilambur", "middle-strait", "nilambur", "ferry", 1.5, 15,
  [[12.1599132, 92.7557293], [12.1702177, 92.7624788]], "Vehicle ferry across Middle Strait."),
 ("boat-nilambur-caves", "nilambur", "limestone-caves", "boat", 8, 30,
  [[12.1702177, 92.7624788], [12.13, 92.74], [12.0959029, 92.7454867]],
  "Speedboat through mangrove creeks (₹900 pp) + 1.2 km walk."),
 ("ride-pb-wandoor", "aberdeen", "wandoor", "scooter", 24.8, 42,
  [[11.6675019, 92.7412765], [11.63, 92.68], [11.5936441, 92.6093126]], "VIP Rd → NH4 → SH8."),
 ("boat-wandoor-redskin", "wandoor", "red-skin", "boat", 8, 45,
  [[11.5936441, 92.6093126], [11.5559255, 92.5916443]], "MGMNP boat (Forest permit needed, issued day before)."),
 ("ferry-pb-havelock", "phoenix-bay", "havelock-jetty", "ferry", 74, 90,
  [[11.6726921, 92.7345295], [11.82, 92.85], [12.0429471, 92.9835984]],
  "Private catamaran (Makruzz/Nautika). Grab upper-deck sea-facing seats if offered."),
 ("ferry-havelock-neil", "havelock-jetty", "neil-jetty", "ferry", 40, 60,
  [[12.0429471, 92.9835984], [11.94, 93.01], [11.8371487, 93.0311195]], "Short hop south."),
 ("ferry-neil-pb", "neil-jetty", "phoenix-bay", "ferry", 60, 75,
  [[11.8371487, 93.0311195], [11.75, 92.88], [11.6726921, 92.7345295]], "Nautika 09:30→10:45 verified for Sun Sep 27."),
 ("ride-jetty-govind", "havelock-jetty", "govind-nagar", "scooter", 3.0, 7,
  [[12.0429471, 92.9835984], [12.0306216, 93.000842]], "SH4 along the east coast."),
 ("ride-govind-radhanagar", "govind-nagar", "radhanagar", "scooter", 9.6, 22,
  [[12.0306216, 93.000842], [12.038, 92.985], [12.0087171, 92.9635124], [11.9844552, 92.9508454]],
  "Back past the jetty, then SH4 southwest — the island's prettiest ride."),
 ("ride-govind-elephant", "govind-nagar", "elephant-trek", "scooter", 6.4, 14,
  [[12.0306216, 93.000842], [12.038, 92.985], [12.0087171, 92.9635124]],
  "SH4 toward Radhanagar; the trailhead ('Walking Path to Elephant Beach') is on the right."),
 ("walk-elephant", "elephant-trek", "elephant-beach", "trek", 1.7, 35,
  [[12.0087171, 92.9635124], [12.010, 92.952], [12.0081083, 92.9416061]],
  "Forest trek past giant buttress-root trees; a stream crossing near the end — wear clogs/water shoes, not sneakers."),
 ("ride-govind-kalapathar", "govind-nagar", "kalapathar", "scooter", 3.7, 8,
  [[12.0306216, 93.000842], [12.0006111, 93.0070952]], "SH5 south along the coast."),
 ("walk-radhanagar-cove", "radhanagar", "neils-cove", "walk", 1.2, 20,
  [[11.9844552, 92.9508454], [11.9922, 92.9430]], "Walk right (north-west) along the sand."),
 ("ride-neiljetty-bharatpur", "neil-jetty", "bharatpur", "scooter", 1.1, 3,
  [[11.8371487, 93.0311195], [11.8361324, 93.034197]], "Bharatpur Beach Rd."),
 ("ride-neiljetty-bridge", "neil-jetty", "natural-bridge", "scooter", 2.1, 4,
  [[11.8371487, 93.0311195], [11.8320292, 93.0139828]], "Village road; last stretch on foot over shore rock."),
 ("ride-neiljetty-sitapur", "neil-jetty", "sitapur", "scooter", 5.6, 10,
  [[11.8371487, 93.0311195], [11.828, 93.048], [11.8261573, 93.0650936]], "SH6 east — sunrise run."),
 ("ride-neiljetty-laxmanpur", "neil-jetty", "laxmanpur", "scooter", 2.7, 5,
  [[11.8371487, 93.0311195], [11.847006, 93.0156096]], "Village road."),
 ("ride-laxmanpur-sitapur", "laxmanpur", "sitapur", "scooter", 7.4, 12,
  [[11.847006, 93.0156096], [11.8371487, 93.0311195], [11.8261573, 93.0650936]], "Via SH6."),
]

# --- v2.3: hotel/restaurant-anchored legs, distances read live from Google
# Maps (2026-08-20) and independently re-verified with reversed queries. ---
ROUTES_V2 = [
 ("cab-ixz-icyspicy", "ixz", "icy-spicy", "cab", 0.65, 2,
  [[11.641656, 92.730243], [11.6587633, 92.7313498]],
  "Great Andaman Trunk Rd — the Junglighat side of the airport."),
 ("cab-icyspicy-phoenix", "icy-spicy", "phoenix-bay", "cab", 2.6, 7,
  [[11.6587633, 92.7313498], [11.6726921, 92.7345295]],
  "Great Andaman Trunk Rd north to the ferry terminal."),
 ("ride-phoenix-chidiyatapu", "phoenix-bay", "chidiya-tapu", "scooter", 26.5, 49,
  [[11.6726921, 92.7345295], [11.62, 92.72], [11.56, 92.71], [11.5059682, 92.7014649]],
  "NH 4 south from the jetty."),
 ("ride-chidiyatapu-atlanta", "chidiya-tapu", "hotel-atlanta", "scooter", 24.6, 46,
  [[11.5059682, 92.7014649], [11.56, 92.71], [11.62, 92.72], [11.6721653, 92.7455293]],
  "NH 4 back north in the dark."),
 ("cab-atlanta-jirkatang", "hotel-atlanta", "jirkatang", "cab", 48.3, 79,
  [[11.6721653, 92.7455293], [11.7, 92.7], [11.78, 92.67], [11.8396935, 92.6538333]],
  "NH 4. Two-wheelers are barred beyond the check post."),
 ("walk-atlanta-annapurna", "hotel-atlanta", "annapurna", "walk", 1.1, 4,
  [[11.6721653, 92.7455293], [11.6671159, 92.7423254]],
  "Rina Rd."),
 ("walk-atlanta-marina", "hotel-atlanta", "marina-park", "walk", 0.4, 6,
  [[11.6721653, 92.7455293], [11.6698312, 92.7474232]],
  "A short walk down to the waterfront. (Google Maps 1.4 km figure is the DRIVING route; on foot it is ~400 m.)"),
 ("cab-atlanta-ixz", "hotel-atlanta", "ixz", "cab", 3.2, 8,
  [[11.6721653, 92.7455293], [11.641656, 92.730243]],
  "VIP Rd."),
 ("cab-atlanta-icyspicy", "hotel-atlanta", "icy-spicy", "cab", 2.9, 9,
  [[11.6721653, 92.7455293], [11.6587633, 92.7313498]],
  "Rina Rd."),
 ("ride-hljetty-bhuma", "havelock-jetty", "hotel-bhuma", "scooter", 2.5, 7,
  [[12.0429471, 92.9835984], [12.0314836, 92.9960689]],
  "SH4 along the east coast."),
 ("ride-bhuma-radhanagar", "hotel-bhuma", "radhanagar", "scooter", 9.1, 19,
  [[12.0314836, 92.9960689], [12.038, 92.985], [12.0087171, 92.9635124], [11.9844552, 92.9508454]],
  "SH4 southwest — the island's prettiest ride."),
 ("ride-bhuma-kalapathar", "hotel-bhuma", "kalapathar", "scooter", 4.1, 8,
  [[12.0314836, 92.9960689], [12.0006111, 93.0070952]],
  "SH5 south."),
 ("ride-bhuma-elephant", "hotel-bhuma", "elephant-trek", "scooter", 6.0, 12,
  [[12.0314836, 92.9960689], [12.038, 92.985], [12.0087171, 92.9635124]],
  "SH4 toward Radhanagar; trailhead on the right."),
 ("ride-bhuma-kayak", "hotel-bhuma", "kayak-point", "scooter", 0.6, 3,
  [[12.0314836, 92.9960689], [12.026, 93.003]],
  "A few hundred metres up the beach road in the dark."),
 ("ride-neiljetty-bluelagoon", "neil-jetty", "hotel-bluelagoon", "scooter", 4.2, 7,
  [[11.8371487, 93.0311195], [11.828, 93.045], [11.8178389, 93.0530135]],
  "SH6 east toward the Sitapur side."),
 ("ride-bluelagoon-sitapur", "hotel-bluelagoon", "sitapur", "scooter", 1.4, 3,
  [[11.8178389, 93.0530135], [11.8261573, 93.0650936]],
  "SH6 — the sunrise beach is minutes from the room."),
 ("ride-bluelagoon-bharatpur", "hotel-bluelagoon", "bharatpur", "scooter", 3.9, 7,
  [[11.8178389, 93.0530135], [11.828, 93.045], [11.8361324, 93.034197]],
  "SH6 west to the watersports lagoon."),
 ("ride-bluelagoon-bridge", "hotel-bluelagoon", "natural-bridge", "scooter", 5.4, 8,
  [[11.8178389, 93.0530135], [11.8371487, 93.0311195], [11.8320292, 93.0139828]],
  "SH6 then the village road."),
 ("ride-bluelagoon-pureveg", "hotel-bluelagoon", "pure-veg-neil", "scooter", 5.1, 8,
  [[11.8178389, 93.0530135], [11.8371487, 93.0311195], [11.8414615, 93.0197503]],
  "SH6 then the village road to Lakshmanpur."),
 ("ride-bharatpur-laxmanpur", "bharatpur", "laxmanpur", "scooter", 3.5, 7,
  [[11.8361324, 93.034197], [11.8371487, 93.0311195], [11.847006, 93.0156096]],
  "Via the jetty junction. (Distance derived from the two verified jetty legs.)"),
 ("ride-bridge-neiljetty", "natural-bridge", "neil-jetty", "scooter", 2.1, 4,
  [[11.8320292, 93.0139828], [11.8371487, 93.0311195]],
  "Village road."),
]
R = R + ROUTES_V2

# --- Haddo jetty legs (private-ferry terminal, verified 2026-08-20) ---
ROUTES_V3 = [
 ("cab-icyspicy-haddo", "icy-spicy", "haddo-jetty", "cab", 2.8, 8,
  [[11.6587633, 92.7313498], [11.668, 92.729], [11.6790, 92.7255]],
  "Junglighat to Haddo Wharf. Makruzz says 15-20 min from the airport by taxi."),
 ("ferry-haddo-havelock", "haddo-jetty", "havelock-jetty", "ferry", 74, 90,
  [[11.6790, 92.7255], [11.82, 92.85], [12.0429471, 92.9835984]],
  "Private catamaran from Haddo Gate 3 to Swaraj Dweep."),
 ("ferry-neil-haddo", "neil-jetty", "haddo-jetty", "ferry", 60, 75,
  [[11.8371487, 93.0311195], [11.75, 92.88], [11.6790, 92.7255]],
  "Neil back to Haddo Wharf, Port Blair."),
 ("ride-haddo-chidiyatapu", "haddo-jetty", "chidiya-tapu", "scooter", 27.0, 50,
  [[11.6790, 92.7255], [11.62, 92.72], [11.56, 92.71], [11.5059682, 92.7014649]],
  "NH 4 south from the jetty."),
]
R = R + ROUTES_V3

# --- Pibo Homestay legs (live re-pricing, 2026-08-20) ---
ROUTES_V4 = [
 ("ride-chidiyatapu-pibo", "chidiya-tapu", "hotel-pibo", "scooter", 24.0, 45,
  [[11.5059682, 92.7014649], [11.56, 92.71], [11.62, 92.72], [11.6540, 92.7300]],
  "NH 4 back north in the dark."),
 ("cab-pibo-jirkatang", "hotel-pibo", "jirkatang", "cab", 48.0, 78,
  [[11.6540, 92.7300], [11.70, 92.70], [11.78, 92.67], [11.8396935, 92.6538333]],
  "NH 4. Two-wheelers are barred beyond the check post."),
 ("cab-pibo-ixz", "hotel-pibo", "ixz", "cab", 2.0, 6,
  [[11.6540, 92.7300], [11.641656, 92.730243]],
  "A short hop — the homestay sits close to the airport side of town."),
 ("walk-pibo-marina", "hotel-pibo", "marina-park", "walk", 2.6, 9, None,
  "Short auto ride or a walk down to the waterfront."),
 ("cab-pibo-icyspicy", "hotel-pibo", "icy-spicy", "cab", 1.2, 5, None,
  "Junglighat is the neighbouring area."),
]
R = R + ROUTES_V4


def main():
    c = db.conn()
    c.execute("DELETE FROM places"); c.execute("DELETE FROM routes"); c.execute("DELETE FROM facts")
    for (pid, name, isl, lat, lng, kind, photo, blurb) in P:
        # Fallback = NAME search (opens the business listing with menu/photos/
        # reviews), never a bare coordinate pin. Canonical listing URLs below win.
        import urllib.parse as _u
        area = {"havelock": " Havelock Swaraj Dweep", "neil": " Neil Island Shaheed Dweep",
                "south_andaman": " Port Blair", "baratang": " Baratang"}.get(isl, "")
        murl = ("https://www.google.com/maps/search/?api=1&query="
                + _u.quote_plus(name + area)) if lat is not None else None
        c.execute("INSERT INTO places (id,name,island,lat,lng,kind,photo,blurb,source_url,maps_url) "
                  "VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (pid, name, isl, lat, lng, kind, photo, blurb, None, murl))
    coords = {p[0]: (p[3], p[4]) for p in P}
    for (rid, a, b, mode, km, mins, poly, note) in R:
        fuel_l = round(2 * km / KMPL, 3) if mode == "scooter" else None   # 2 scooters
        fuel_c = round(fuel_l * PETROL, 1) if fuel_l else None
        # Never store null geometry: a stored "null" parses to null in the
        # frontend and used to take the whole app down. Fall back to a straight
        # line between the endpoints.
        if not poly or len(poly) < 2:
            pa, pb = coords.get(a), coords.get(b)
            if pa and pb and pa[0] is not None and pb[0] is not None:
                poly = [[pa[0], pa[1]], [pb[0], pb[1]]]
            else:
                raise SystemExit(f"route {rid}: no geometry and no usable endpoint coords")
        c.execute("INSERT INTO routes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (rid, a, b, mode, km, mins, json.dumps(poly), fuel_l, fuel_c, note, None))
    fb = json.load(open(FB))
    for topic, blob in fb["research"].items():
        for f in blob.get("facts", []):
            c.execute("INSERT INTO facts (topic,value,source_url,as_of,verified) VALUES (?,?,?,?,?)",
                      (f"{topic}: {f['topic']}", f["value"][:600], f["source_url"], f.get("as_of", "2026-08-19"), "reported"))
    for v in fb["verification"]:
        status = {"confirmed": "confirmed", "refuted": "refuted->corrected"}.get(v.get("verdict"), "unverifiable")
        val = v.get("corrected_value") or v.get("claim", "")
        c.execute("INSERT INTO facts (topic,value,source_url,as_of,verified) VALUES (?,?,?,?,?)",
                  (f"VERIFIED[{v.get('from', '')}]", val[:600], v.get("evidence_url", ""), "2026-08-19", status))
    kit = [
      ["Clothing (Sept = wettest month: 388 mm rain, 29°/24°C, 90% humidity)", [
        "Quick-dry tees + shorts (3–4 sets) — cotton stays wet here",
        "Light rain poncho or packable rain jacket (daily thundershower regime)",
        "One warm layer for AC ferries and the 4 AM cab",
        "Swimwear ×2 (one drying, one wearing) + light cover-up",
        "Cap/hat + sunglasses (UV is fierce between showers)"]],
      ["Feet", [
        "Water shoes / floaters with grip — REQUIRED for Natural Bridge dead-coral walk + Elephant Beach stream",
        "Flip-flops for beaches",
        "One pair of light trainers for the Munda Pahad trek"]],
      ["Gear", [
        "Waterproof phone pouch + dry bag (kayak, jet ski, speedboat spray)",
        "Reef-safe sunscreen SPF50 + after-sun aloe",
        "Mosquito repellent (dawn/dusk, forest treks)",
        "Headlamp or phone torch (04:30 starts: Kalapathar / Baratang / Sitapur)",
        "Power bank ≥10,000 mAh (long days, patchy power)",
        "Motion-sickness tablets (catamaran crossings, monsoon swell)"]],
      ["Documents & money", [
        "Driving licence (physical) for both riders + photocopies for scooter rental",
        "Photo-ID for ferry check-ins and Forest permits",
        "Cash ₹8–10k (pumps, parking, stalls and small eateries are cash-first; island ATMs can't be trusted)"]],
    ]
    # timestamped deep-links into the user's reference video (Sakre Cubes, watched live)
    YT = "https://www.youtube.com/watch?v=NhLrrne5jXM&t="
    yt_links = {
        "radhanagar": 211, "neils-cove": 240, "elephant-beach": 271, "elephant-trek": 271,
        "kalapathar": 376, "govind-nagar": 442, "kayak-point": 532, "bharatpur": 671,
        "natural-bridge": 723, "laxmanpur": 770, "sitapur": 784, "cellular-jail": 821,
        "marina-park": 897, "red-skin": 930, "wandoor": 930, "limestone-caves": 1144,
        "nilambur": 1144, "chidiya-tapu": 1218, "munda-pahad": 1218,
        "havelock-jetty": 95, "phoenix-bay": 95, "neil-jetty": 627,
    }
    for pid, t in yt_links.items():
        c.execute("UPDATE places SET source_url=? WHERE id=?", (f"{YT}{t}s", pid))
    # Canonical Google Maps LISTING urls (opened + name-verified in the browser).
    # These open the place card itself - menu, photos, hours, reviews - not a pin.
    G = "https://www.google.com/maps/place/"
    canonical = {
      "icy-spicy": G + "Icy+Spicy+-+Pure+Veg/@11.6587633,92.7313498,1563m/data=!3m2!1e3!4b1!4m6!3m5!1s0x308895a508bcbd15:0xc50f513f8d030e5d!8m2!3d11.6587633!4d92.7313498!16s%2Fg%2F11r8s7820",
      "annapurna": G + "Annapurna+Cafeteria+Pure+Veg/@11.6671159,92.7423254,1563m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088950b9112bb31:0x9abee36ad549492e!8m2!3d11.6671159!4d92.7423254!16s%2Fg%2F1tdr5mfx",
      "something-different": G + "Something+Different+-+A+Beachside+Cafe/@12.035727,92.989741,1561m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d33db6b96377:0x838400de2bff7381!8m2!3d12.035727!4d92.989741!16s%2Fg%2F11cnhpr3t_",
      "pure-veg-neil": G + "PURE+VEG+RESTAURANT/@11.8414615,93.0197503,1562m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d97bd787643f:0x55211e18a164b49!8m2!3d11.8414615!4d93.0197503!16s%2Fg%2F11pkht8c0z",
      "hl-pump": G + "IndianOil/@12.008853,92.97162,1561m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d25615405c53:0x29abaf986f9af813!8m2!3d12.008853!4d92.97162!16s%2Fg%2F11dfpqs462",
      "hotel-atlanta": G + "Hotel+Atlanta+-+A+Seaview+Hotel/@11.6721653,92.7455293,1563m/data=!3m1!1e3!4m9!3m8!1s0x30889544245cffc3:0x4857634e89b86650!5m2!4m1!1i2!8m2!3d11.6721653!4d92.7455293!16s%2Fg%2F11ldkm5j04",
      "hotel-bhuma": G + "Bhuma+Homestay/@12.0314836,92.9960689,1561m/data=!3m1!1e3!4m9!3m8!1s0x3088d398856370e3:0x5787c47a082dfc03!5m2!4m1!1i2!8m2!3d12.0314836!4d92.9960689!16s%2Fg%2F11vcw8309g",
      "hotel-bluelagoon": G + "Blue+Lagoon+Resort,+Neil+Island/@11.8178389,93.0530135,1562m/data=!3m1!1e3!4m9!3m8!1s0x3088d9dc90b059e9:0xd0c5192b3088e7bd!5m2!4m1!1i2!8m2!3d11.8178389!4d93.0530135!16s%2Fg%2F11h6t76ln3",
    }
    canonical.update({"icy-spicy": "https://www.google.com/maps/place/Icy+Spicy+-+Pure+Veg/@11.6587633,92.7313498,1563m/data=!3m2!1e3!4b1!4m6!3m5!1s0x308895a508bcbd15:0xc50f513f8d030e5d!8m2!3d11.6587633!4d92.7313498!16s%2Fg%2F11r8s7820", "annapurna": "https://www.google.com/maps/place/Annapurna+Cafeteria+Pure+Veg/@11.6671159,92.7423254,1563m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088950b9112bb31:0x9abee36ad549492e!8m2!3d11.6671159!4d92.7423254!16s%2Fg%2F1tdr5mfx", "something-different": "https://www.google.com/maps/place/Something+Different+-+A+Beachside+Cafe/@12.035727,92.989741,1561m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d33db6b96377:0x838400de2bff7381!8m2!3d12.035727!4d92.989741!16s%2Fg%2F11cnhpr3t_", "pure-veg-neil": "https://www.google.com/maps/place/PURE+VEG+RESTAURANT/@11.8414615,93.0197503,1562m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d97bd787643f:0x55211e18a164b49!8m2!3d11.8414615!4d93.0197503!16s%2Fg%2F11pkht8c0z", "hotel-atlanta": "https://www.google.com/maps/place/Hotel+Atlanta+-+A+Seaview+Hotel/@11.6721653,92.7455293,1563m/data=!3m1!1e3!4m9!3m8!1s0x30889544245cffc3:0x4857634e89b86650!5m2!4m1!1i2!8m2!3d11.6721653!4d92.7455293!16s%2Fg%2F11ldkm5j04", "hotel-bhuma": "https://www.google.com/maps/place/Bhuma+Homestay/@12.0314836,92.9960689,1561m/data=!3m1!1e3!4m9!3m8!1s0x3088d398856370e3:0x5787c47a082dfc03!5m2!4m1!1i2!8m2!3d12.0314836!4d92.9960689!16s%2Fg%2F11vcw8309g", "hotel-bluelagoon": "https://www.google.com/maps/place/Blue+Lagoon+Resort,+Neil+Island/@11.8178389,93.0530135,1562m/data=!3m1!1e3!4m9!3m8!1s0x3088d9dc90b059e9:0xd0c5192b3088e7bd!5m2!4m1!1i2!8m2!3d11.8178389!4d93.0530135!16s%2Fg%2F11h6t76ln3", "hl-pump": "https://www.google.com/maps/place/IndianOil/@12.008853,92.97162,1561m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d25615405c53:0x29abaf986f9af813!8m2!3d12.008853!4d92.97162!16s%2Fg%2F11dfpqs462", "neil-pump": "https://www.google.com/maps/place/IndianOil/@11.831935,93.030909,1562m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d90d4368cdef:0x28ac3f7f603df382!8m2!3d11.831935!4d93.030909!16s%2Fg%2F11h01t5032", "phoenix-bay": "https://www.google.com/maps/place/Phoenix+Bay+Jetty/@11.6726985,92.7345305,3126m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088959f150bf0fd:0x14d92975608ce055!8m2!3d11.6726985!4d92.7345305!16s%2Fg%2F11gc8tc2ft", "havelock-jetty": "https://www.google.com/maps/place/Havelock+Jetty/@12.0429471,92.9835984,1561m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d3fa1cc2605b:0x3297a66752f5150a!8m2!3d12.0429471!4d92.9835984!16s%2Fg%2F11q1trvx7l", "neil-jetty": "https://www.google.com/maps/place/Shaheed+Dweep+Jetty/@11.8371487,93.0311195,3125m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d99a3137bbd1:0xffbc8324237261d3!8m2!3d11.8371487!4d93.0311195!16s%2Fg%2F11c6dzms82", "radhanagar": "https://www.google.com/maps/place/Radhanagar+Beach/@11.9830678,92.9484492,6246m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d212164bb773:0x9715637d9a7265b3!8m2!3d11.9844552!4d92.9508454!16s%2Fg%2F1hc18h9zw", "kalapathar": "https://www.google.com/maps/place/Kala+Pathar+Beach/@12.0002055,93.0079768,6245m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d39ad246aa93:0xa562a45e499c1abd!8m2!3d12.0006111!4d93.0070952!16s%2Fg%2F12hrhkb0v", "bharatpur": "https://www.google.com/maps/place/Bharatpur+Beach,+Neil+Island/@11.8361324,93.034197,3125m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d9990d90cc03:0x8384b4367470fc0a!8m2!3d11.8361324!4d93.034197!16s%2Fg%2F11cjhkd_l5", "natural-bridge": "https://www.google.com/maps/place/Natural+bridge+1/@11.8320292,93.0139828,1562m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088db0000e788ef:0x8df2a078f6e76a0f!8m2!3d11.8320292!4d93.0139828!16s%2Fg%2F11wxjq724g", "sitapur": "https://www.google.com/maps/place/Sitapur+Beach/@11.8262966,93.0656817,3003m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d8f863b86131:0x6d7b01e475bf3549!8m2!3d11.8261573!4d93.0650936!16s%2Fg%2F11h0wf7z0", "laxmanpur": "https://www.google.com/maps/place/Laxmanpur+Beach+No+1/@11.8470058,93.0156096,6249m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088da20a18f8a61:0xa0d515ea579c8453!8m2!3d11.847006!4d93.0156096!16s%2Fg%2F1tfd9wxl", "elephant-beach": "https://www.google.com/maps/place/Elephant+Beach/@12.008108,92.9416061,6002m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d27d470f1f33:0xbe96fc275b9105fa!8m2!3d12.0081083!4d92.9416061!16s%2Fg%2F1q5blvb_h", "elephant-trek": "https://www.google.com/maps/place/Walking+Path+To+Elephant+Beach/@12.0087171,92.9635124,1501m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088d25dec04ebb9:0xcfca19e5821243f0!8m2!3d12.0087171!4d92.9635124!16s%2Fg%2F11f03_bshq", "chidiya-tapu": "https://www.google.com/maps/place/Chidiya+Tapu+Beach/@11.5059679,92.7014649,6257m/data=!3m2!1e3!4b1!4m6!3m5!1s0x30888dfc24f0eccf:0x8f3a8242f0ef351!8m2!3d11.5059682!4d92.7014649!16s%2Fg%2F1tdjtg0m", "munda-pahad": "https://www.google.com/maps/place/Munda+Pahad+Beach/@11.4914543,92.7087511,1503m/data=!3m2!1e3!4b1!4m6!3m5!1s0x30888de86b12401b:0x8a33420ae35be5cd!8m2!3d11.4914543!4d92.7087511!16s%2Fg%2F113hbmhrs", "limestone-caves": "https://www.google.com/maps/place/Limestone+Cave+Baratang/@12.0959029,92.7454867,1500m/data=!3m2!1e3!4b1!4m6!3m5!1s0x308f4afbac8bd9c7:0xa1e372f97c60eb89!8m2!3d12.0959029!4d92.7454867!16s%2Fg%2F1tfhx0db", "jirkatang": "https://www.google.com/maps/place/Jirkatang+Check+Post/@11.8396966,92.6537788,1502m/data=!3m2!1e3!4b1!4m6!3m5!1s0x3088baf978690e8b:0x3f386f20dd94b2de!8m2!3d11.8396966!4d92.6537788!16s%2Fg%2F11g6bhncfg", "ixz": "https://www.google.com/maps/place/Veer+Savarkar+International+Airport/@11.641656,92.730243,1563m/data=!3m2!1e3!4b1!4m6!3m5!1s0x30889451c7104cff:0x692277584b73d9f0!8m2!3d11.641656!4d92.730243!16zL20vMDl3cjFw"})
    for pid, url in canonical.items():
        c.execute("UPDATE places SET maps_url=? WHERE id=?", (url, pid))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('kit', ?)", (json.dumps(kit, ensure_ascii=False),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('petrol_inr_l', ?)", (str(PETROL),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('scooter_kmpl', ?)", (str(KMPL),))
    c.commit()
    print("places:", c.execute("SELECT COUNT(*) FROM places").fetchone()[0],
          "routes:", c.execute("SELECT COUNT(*) FROM routes").fetchone()[0],
          "facts:", c.execute("SELECT COUNT(*) FROM facts").fetchone()[0])


if __name__ == "__main__":
    main()
