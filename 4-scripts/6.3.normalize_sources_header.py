import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


ANCHOR_CSV = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "1.outputAnchor"
    / "sourcesAnchor.csv"
)
SOURCES_ALL = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "6.outputAddReferences_CSV"
    / "sources_all.csv"
)

OUTPUT_NORMALIZED = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "6.outputAddReferences_CSV"
    / "sources_all_normalized.csv"
)


with open(ANCHOR_CSV, encoding="utf8") as f:
    reader = csv.reader(f, delimiter=";")
    raw_header = next(reader)


anchor_header = [h.replace("\ufeff", "").strip() for h in raw_header]

print("Anchor header (cleaned):")
print(anchor_header)

rows = []
all_fields = set()

with open(SOURCES_ALL, encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        # normalize keys too (important!)
        clean_row = {k.replace("\ufeff", "").strip(): v for k, v in row.items()}
        rows.append(clean_row)
        all_fields.update(clean_row.keys())

print("\nFields in sources_all:")
print(all_fields)

# BUILD FINAL HEADER
final_header = anchor_header.copy()

for field in sorted(all_fields):
    if field not in final_header:
        final_header.append(field)

print("\nFinal normalized header:")
print(final_header)

# WRITE NORMALIZED FILE
os.makedirs(os.path.dirname(OUTPUT_NORMALIZED), exist_ok=True)

with open(OUTPUT_NORMALIZED, "w", encoding="utf8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=final_header, delimiter=";")
    writer.writeheader()

    for row in rows:
        normalized_row = {col: row.get(col, "") for col in final_header}
        writer.writerow(normalized_row)

# -------- REPORT --------

print("\nnormalize_sources_header.py finished")
print("-" * 50)
print(f"Rows written : {len(rows)}")
print(f"Saved to     : {OUTPUT_NORMALIZED}")
