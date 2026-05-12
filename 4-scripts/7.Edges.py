import json
import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

REFERENCES_JSON = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "5.outputBuildReferences"
    / "references.json"
)
SOURCES_ALL_CSV = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "6.outputAddReferences_CSV"
    / "sources_all_normalized.csv"
)

OUTPUT_DIR = BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "7.outputEdges"
OUTPUT_EDGES = os.path.join(OUTPUT_DIR, "edges_expanded.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

valid_ids = set()

with open(SOURCES_ALL_CSV, encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        sid = row.get("source_id", "").strip()
        if sid:
            valid_ids.add(sid)

print(f"Loaded sources_all.csv: {len(valid_ids)} source_ids")

with open(REFERENCES_JSON, encoding="utf8") as f:
    refs = json.load(f)


# Build edges
edges = []
total_refs = 0
used_refs = 0
skipped_unknown = 0
skipped_self = 0

for citing, items in refs.items():

    if citing not in valid_ids:
        continue

    for r in items:
        total_refs += 1

        target = r.get("target_id")

        if not target or target == "L_UNKNOWN":
            skipped_unknown += 1
            continue

        if target not in valid_ids:
            skipped_unknown += 1
            continue

        if citing == target:
            skipped_self += 1
            continue

        edges.append(
            {"citing": citing, "cited": target, "matched": r.get("matched", False)}
        )

        used_refs += 1

# Write edges_expanded.csv
if not edges:
    print("No edges created.")
    exit()

fieldnames = ["citing", "cited", "matched"]

with open(OUTPUT_EDGES, "w", encoding="utf8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for row in edges:
        writer.writerow(row)

# --------------------
# Report
# --------------------

print("\nrebuild_edges_expanded.py finished")
print("-" * 50)
print(f"Total references scanned : {total_refs}")
print(f"Edges created           : {len(edges)}")
print(f"Skipped L_UNKNOWN       : {skipped_unknown}")
print(f"Skipped self-citations  : {skipped_self}")
print(f"Saved to                : {OUTPUT_EDGES}")
