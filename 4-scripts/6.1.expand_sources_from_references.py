import json
import csv
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

REFERENCES_JSON = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "5.outputBuildReferences"
    / "references.json"
)
OUTPUT_DIR = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "6.outputAddReferences_CSV"
)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "sources_external.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_text(s):
    if not s:
        return ""
    s = str(s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def normalize_year(y):
    if not y:
        return ""
    y = str(y)
    m = re.search(r"\d{4}", y)
    return m.group(0) if m else ""


with open(REFERENCES_JSON, encoding="utf8") as f:
    refs = json.load(f)

external_sources = {}
total_refs = 0

for citing, items in refs.items():
    for r in items:
        total_refs += 1

        if r.get("matched") is True:
            continue

        target_id = r.get("target_id")
        if not target_id or target_id == "L_UNKNOWN":
            continue

        if target_id in external_sources:
            continue

        author = clean_text(r.get("author", ""))
        title = clean_text(r.get("title", ""))
        year = normalize_year(r.get("year", ""))

        external_sources[target_id] = {
            "source_id": target_id,
            "author": author,
            "title": title,
            "year": year,
            "source_type": "",
            "source_book": "",
            "publication_place": "",
            "publisher": "",
            "pages": "",
            "language": "",
            "discipline": "",
            "urn_cts": "",
            "is_primary_text": "No",
            "has_translation": "No",
            "digital_source": "",
            "notes": "auto-extracted from references",
            "doi": "",
            "pdf_path": "",
            "has_pdf": "FALSE",
            "anchor_external": "external",
            "primary_source": "",
            "step_distance_all": "",
            "step_label": "",
            "reliable_source": 0,
        }

if not external_sources:
    print("No external sources found.")
    exit()

fieldnames = list(next(iter(external_sources.values())).keys())

with open(OUTPUT_CSV, "w", encoding="utf8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for row in external_sources.values():
        writer.writerow(row)

# --------------------
# Report
# --------------------

print("expand_sources_from_references.py finished")
print("-" * 50)
print(f"Total references scanned : {total_refs}")
print(f"External unique sources  : {len(external_sources)}")
print(f"Saved to                : {OUTPUT_CSV}")
