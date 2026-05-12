import json
import pandas as pd
import re
from unidecode import unidecode
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sources_normalized = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "1.outputAnchor"
    / "sourcesAnchor.csv"
)
yamlAnchors = BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "4.outputAnystyle"
refs_path = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "5.outputBuildReferences"
    / "references.json"
)

os.makedirs(os.path.dirname(refs_path), exist_ok=True)


sources = pd.read_csv(sources_normalized, delimiter=";")


def make_global_id(author, year, title):
    author_key = unidecode(str(author).split()[0]) if author else "Unknown"
    year_key = str(int(year)) if str(year).isdigit() else "0000"

    title_clean = unidecode(str(title))
    title_clean = re.sub(r"[^A-Za-z0-9]", "", title_clean)
    title_key = title_clean[:10]

    return f"{author_key}{year_key}_{title_key}"


anchors_list = sources["source_id"].dropna().unique().tolist()

print(f"Total anchors: {len(anchors_list)}")


ref_data = {}

processed = 0
skipped = 0

for anchor in anchors_list:

    path = os.path.join(yamlAnchors, f"bibl{anchor}.json")

    if not os.path.exists(path):
        skipped += 1
        continue

    with open(path, encoding="utf8") as f:
        refs = json.load(f)

    ref_data[anchor] = []

    for r in refs:
        authors = r.get("author", [])
        author = authors[0].get("family", "Unknown") if authors else "Unknown"
        year = r.get("date", ["0000"])[0]
        title = r.get("title", [""])[0]

        found = sources[
            sources["title"]
            .astype(str)
            .str.contains(title[:20], case=False, na=False, regex=False)
        ]

        if not found.empty:
            target = found.iloc[0]["source_id"]
            matched = True
        else:
            target = make_global_id(author, year, title)
            matched = False

        ref_data[anchor].append(
            {
                "raw": r,
                "author": author,
                "year": year,
                "title": title,
                "target_id": target,
                "matched": matched,
            }
        )

    processed += 1


with open(refs_path, "w", encoding="utf8") as f:
    json.dump(ref_data, f, indent=2, ensure_ascii=False)

# ---------- REPORT ----------
total_refs = sum(len(v) for v in ref_data.values())

print("references.json rebuilt for ALL sources")
print(f"Anchors processed: {processed}")
print(f"Anchors skipped (no Anystyle file): {skipped}")
print(f"Total references extracted: {total_refs}")
print(f"Saved to: {refs_path}")
