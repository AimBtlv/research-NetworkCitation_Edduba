import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


SOURCES_ANCHOR = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "1.outputAnchor"
    / "sourcesAnchor.csv"
)
SOURCES_EXTERNAL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "6.outputAddReferences_CSV"
    / "sources_external.csv"
)

OUTPUT_DIR = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "6.outputAddReferences_CSV"
)
OUTPUT_ALL = os.path.join(OUTPUT_DIR, "sources_all.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_csv_dict(path):
    rows = []
    with open(path, encoding="utf8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            rows.append(r)
    return rows


anchors = load_csv_dict(SOURCES_ANCHOR)
external = load_csv_dict(SOURCES_EXTERNAL)

print(f"Anchor sources  : {len(anchors)}")
print(f"External sources: {len(external)}")


# Merge + deduplicate


merged = {}
order = []

for row in anchors + external:
    sid = row.get("source_id", "").strip()
    if not sid:
        continue

    if sid not in merged:
        merged[sid] = row
        order.append(sid)


# Write merged CSV


if not merged:
    print("No data to write.")
    exit()

# collect all columns
fieldnames = set()
for row in merged.values():
    fieldnames.update(row.keys())

fieldnames = list(fieldnames)

with open(OUTPUT_ALL, "w", encoding="utf8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for sid in order:
        writer.writerow(merged[sid])
# --------------------
# Report
# --------------------

print("\nmerge_sources.py finished")
print("-" * 50)
print(f"Total unique sources : {len(merged)}")
print(f"Saved to             : {OUTPUT_ALL}")
