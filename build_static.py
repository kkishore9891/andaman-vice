#!/usr/bin/env python3
"""Bake the whole app into ONE self-contained HTML file for artifact hosting.

Inlines: CSS, JS, trip data (from SQLite), map geometry, and all referenced
photos as base64 data URIs. Output: dist/andaman-vice.html
"""
import base64
import json
import os
import re

import db

ROOT = os.path.dirname(os.path.abspath(__file__))


def slurp(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def main():
    data = db.export()
    geo = json.load(open(os.path.join(ROOT, "assets/map_geo.json")))

    # inline photos referenced by places as data URIs
    for p in data["places"]:
        ph = p.get("photo")
        if ph:
            fp = os.path.join(ROOT, ph)
            if os.path.exists(fp):
                p["photo"] = "data:image/jpeg;base64," + b64(fp)
            else:
                p["photo"] = None

    html = slurp("index.html")
    # drop external refs, inline everything
    html = re.sub(r'<link rel="manifest"[^>]*>\n?', "", html)
    html = html.replace('<link rel="stylesheet" href="css/app.css">',
                        "<style>\n" + slurp("css/app.css") + "\n</style>")
    inline_js = (
        "<script>\nwindow.TRIP_DATA = " + json.dumps(data, ensure_ascii=False) +
        ";\nwindow.MAP_GEO = " + json.dumps(geo) + ";\n</script>\n" +
        "<script>\n" + slurp("js/map.js") + "\n</script>\n" +
        "<script>\n" + slurp("js/app.js") + "\n</script>"
    )
    html = html.replace('<script src="js/map.js"></script>\n'
                        '<script src="js/app.js"></script>', inline_js)
    # no service worker in the artifact build
    outs = []
    for rel in ("dist/andaman-vice.html", "docs/index.html"):
        out = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        outs.append(out)
    print(f"baked {outs}: {os.path.getsize(outs[0])/1024:.0f} KB "
          f"(validation: {data['validation'] or 'OK'})")


if __name__ == "__main__":
    main()
