"""Classify the lesson 2 terrain polygons into broad land-cover types with TypeSafe.

The polygons only carry a numeric CLASS code. The code -> name lookup is exact
(it comes from the NLS feature model spreadsheet in figs/), so it stays in code.
TypeSafe only makes the semantic judgment: which broad land-cover type does each
class name belong to. That is one request per class (21), not one per polygon.

Run with the course environment, from lesson-2/:
    TYPESAFE_API_KEY=... ~/miniconda3/envs/autogis/bin/python classify_terrain.py
"""
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

import geopandas
import pandas

API_URL = "https://api.typesafe.ai/v1/systemone"
DATA_DIRECTORY = pathlib.Path(__file__).resolve().parent / "data"
TOPOGRAPHIC_DATABASE_DIRECTORY = DATA_DIRECTORY / "finland_topographic_database"
CACHE_FILE = TOPOGRAPHIC_DATABASE_DIRECTORY / "terrain_class_categories.json"
REVIEW_THRESHOLD = 0.7  # below this confidence, flag the class for a human check

# Official English names, from figs/maastotietokanta_kohdemalli_eng_2019.xlsx
CLASS_NAMES = {
    32111: "Mineral resources extraction area, coarse-grained material",
    32112: "Mineral resources extraction area, fine-grained material",
    32200: "Cemetery",
    32417: "Other air traffic area, paved",
    32421: "Motor traffic area",
    32500: "Quarry",
    32611: "Field",
    32612: "Garden",
    32800: "Meadow",
    32900: "Park",
    33000: "Earth fill",
    33100: "Sports and recreation area",
    34100: "Rock - area",
    34300: "Sand",
    34700: "Rocky area",
    35300: "Paludified land",
    35411: "Open bog, easy to traverse treeless",
    35412: "Bog, easy to traverse forested",
    35421: "Open fen, difficult to traverse treeless",
    36200: "Lake water",
    36313: "Watercourse area",
}

LAND_COVER_QUESTION = {
    "type": "choice",
    "instructions": (
        "Which broad land-cover type does the terrain class `class_name` from the "
        "Finnish topographic database belong to?"
    ),
    "criteria": {
        "water": "Open water: lakes, rivers, streams, watercourses",
        "wetland": "Bogs, fens, mires and other paludified or peat land, with or without trees",
        "agriculture": "Cultivated fields, meadows and other farmed or grazed land",
        "urban_green": "Vegetated land kept for people in built-up areas: parks, gardens, cemeteries, sports grounds",
        "built_up": "Sealed or constructed surfaces: roads, traffic areas, airports, fills",
        "extraction": "Land dug for material: quarries, gravel and sand pits, mineral extraction areas",
        "bare_natural": "Natural surfaces with little vegetation: bedrock, boulder fields, natural sand",
        "other": "None of the above fits",
    },
}


def ask_typesafe(api_key, class_code, class_name):
    payload = {
        "state": {"class_code": class_code, "class_name": class_name},
        "model": "jev-latest",
        "questions": {"land_cover": LAND_COVER_QUESTION},
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
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["answers"]["land_cover"]


def classify_all_classes():
    # Cache answers so re-running the script does not call the API again
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())

    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        sys.exit("TYPESAFE_API_KEY is not set in this shell.")

    answers = {}
    for class_code, class_name in CLASS_NAMES.items():
        try:
            answer = ask_typesafe(api_key, class_code, class_name)
        except urllib.error.HTTPError as err:
            sys.exit(f"HTTP {err.code} for class {class_code}: {err.read().decode()}")
        answers[str(class_code)] = {
            "category": answer["choice"],
            "confidence": answer["confidence"],
        }
        print(f"{class_code} {class_name:<60} -> {answer['choice']} ({answer['confidence']:.2f})")

    CACHE_FILE.write_text(json.dumps(answers, indent=2))
    return answers


answers = classify_all_classes()

categories = pandas.DataFrame(
    [
        {
            "CLASS": int(class_code),
            "class_name": CLASS_NAMES[int(class_code)],
            "category": answer["category"],
            "confidence": answer["confidence"],
            "needs_review": answer["confidence"] < REVIEW_THRESHOLD,
        }
        for class_code, answer in answers.items()
    ]
)

# Attach the categories to every polygon
terrain = pandas.concat(
    geopandas.read_file(TOPOGRAPHIC_DATABASE_DIRECTORY / f"terrain_{class_code}.shp")
    for class_code in CLASS_NAMES
)
terrain = terrain.merge(categories, on="CLASS", how="left")
terrain["area"] = terrain.area

terrain.to_file(TOPOGRAPHIC_DATABASE_DIRECTORY / "terrain_classified.gpkg")

print()
print(categories.sort_values(["category", "CLASS"]).to_string(index=False))
print()
print("Area by land-cover category (km²):")
print((terrain.groupby("category").area.sum() / 1e6).sort_values(ascending=False).round(2))

if categories.needs_review.any():
    print(f"\nClasses below {REVIEW_THRESHOLD} confidence, check by hand:")
    print(categories[categories.needs_review].to_string(index=False))
