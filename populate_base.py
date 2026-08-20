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


def main():
    c = db.conn()
    c.execute("DELETE FROM places"); c.execute("DELETE FROM routes"); c.execute("DELETE FROM facts")
    for (pid, name, isl, lat, lng, kind, photo, blurb) in P:
        # fallback Maps link by coordinates; canonical listing URLs applied below
        murl = (f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
                if lat is not None else None)
        c.execute("INSERT INTO places (id,name,island,lat,lng,kind,photo,blurb,source_url,maps_url) "
                  "VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (pid, name, isl, lat, lng, kind, photo, blurb, None, murl))
    for (rid, a, b, mode, km, mins, poly, note) in R:
        fuel_l = round(2 * km / KMPL, 3) if mode == "scooter" else None   # 2 scooters
        fuel_c = round(fuel_l * PETROL, 1) if fuel_l else None
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
    c.execute("INSERT OR REPLACE INTO meta VALUES ('kit', ?)", (json.dumps(kit, ensure_ascii=False),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('petrol_inr_l', ?)", (str(PETROL),))
    c.execute("INSERT OR REPLACE INTO meta VALUES ('scooter_kmpl', ?)", (str(KMPL),))
    c.commit()
    print("places:", c.execute("SELECT COUNT(*) FROM places").fetchone()[0],
          "routes:", c.execute("SELECT COUNT(*) FROM routes").fetchone()[0],
          "facts:", c.execute("SELECT COUNT(*) FROM facts").fetchone()[0])


if __name__ == "__main__":
    main()
