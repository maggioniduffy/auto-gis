"""Dumb smoke test for the TypeSafe API: one Noul, one Choice and one Score question.

Run: python typesafe_test.py   (needs TYPESAFE_API_KEY in the environment)
"""
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.typesafe.ai/v1/systemone"

api_key = os.environ.get("TYPESAFE_API_KEY")
if not api_key:
    sys.exit("TYPESAFE_API_KEY is not set in this shell.")

payload = {
    "state": {
        "feature_name": "Laguna del Diamante",
        "description": "High-altitude lake at the foot of the Maipo volcano, "
                       "surrounded by wetlands and grazing land. Access road "
                       "is closed in winter due to snow.",
    },
    "model": "jev-latest",
    "questions": {
        "is_water_body": {
            "type": "noul",
            "instructions": "Is the feature described in `description` a body of water?",
        },
        "terrain_class": {
            "type": "choice",
            "instructions": "Which land-cover class best fits the feature in `description`?",
            "criteria": {
                "water": "Lakes, rivers, reservoirs, lagoons",
                "urban": "Built-up areas, cities, towns",
                "forest": "Dense tree cover",
                "agriculture": "Crops or pasture",
                "barren": "Rock, sand, ice, bare ground",
            },
        },
        "accessibility": {
            "type": "score",
            "instructions": "How easy is it to reach the feature in `description` year-round?",
            "criteria": [
                "Unreachable for much of the year",
                "Reachable only seasonally or with difficulty",
                "Easily reachable all year",
            ],
        },
    },
}

request = urllib.request.Request(
    API_URL,
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
except urllib.error.HTTPError as err:
    sys.exit(f"HTTP {err.code}: {err.read().decode()}")

print(json.dumps(result, indent=2))
