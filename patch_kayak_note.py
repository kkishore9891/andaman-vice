#!/usr/bin/env python3
"""Record the verified kayak findings so the decision is documented in the app."""
import json

IT = "data/itinerary.json"
it = json.load(open(IT))

it["risks"] = [r for r in it["risks"] if "KAYAK DROPPED" not in r] + [
  "KAYAK — VERIFIED, AND DROPPING IT WAS RIGHT: operators sell bioluminescence as a NO-MOON product. "
  "Thrillophilia states it runs only '5 days before, on, and 5 days after the no-moon night'; 23-24 Sep is "
  "~13 days after the 11 Sep new moon, i.e. outside that window. The Dive Master Havelock says a half moon "
  "already cuts the glow to 30-40%. Operators will still take the booking and paddle you out at 03:30 — the "
  "mangroves and sunrise are real — but almost none claim you would see meaningful glow in a full-moon week.",
  "KAYAK PRICING — Andaman Bliss's Rs 3,500 pp is at the expensive end. The Dive Master Havelock (local, "
  "WhatsApp +91 70872 88214) lists Rs 2,000 pp for the same 03:30-06:00 slot: Rs 6,000 for three, not "
  "Rs 10,500. The 'Rs 2,800' Go2Andaman figure is a DAYTIME floor price, not a night quote.",
  "KAYAK ALTERNATIVE if the crew still wants to paddle: a daytime or sunrise mangrove kayak runs about "
  "Rs 1,999-2,500 pp, is genuinely good in late September, and does not depend on the moon at all.",
]
json.dump(it, open(IT, "w"), ensure_ascii=False, indent=1)
print("kayak findings recorded;  crew total unchanged: Rs", it["total_cost_inr"],
      "= Rs", round(it["total_cost_inr"] / 3), "pp")
