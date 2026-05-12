import os
import csv
from pathlib import Path

print(">>> fromTXT_Metadata_toCSV.py - SCRIPT VERSION 2026-01-23 <<<")
BASE_DIR = Path(__file__).resolve().parent

TXT_FOLDER = (
    BASE_DIR
    / "edubbaData"
    / "edubba2.0_DataTxtRaw"
    / "2.0.datacollectTXT_AnchorArticles"
)
CSV_FILE = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "1.outputAnchor"
    / "sourcesAnchor.csv"
)


CSV_FIELDS = [
    "source_id",
    "author",
    "title",
    "year",
    "source_type",
    "source_book",
    "publication_place",
    "publisher",
    "pages",
    "language",
    "discipline",
    "urn_cts",
    "is_primary_text",
    "has_translation",
    "digital_source",
    "notes",
    "doi",
    "pdf_path",
    "has_pdf",
]


def parse_metadata(txt_path):
    metadata = {}

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_metadata = False

    for line in lines:
        line = line.strip()

        if line.startswith("# METADATA"):
            in_metadata = True
            continue

        if line.startswith("#") and in_metadata:
            break

        if in_metadata and ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip().lower()] = value.strip()

    return metadata


def parse_source_type(raw_source_type):
    if not raw_source_type:
        return "", ""

    if raw_source_type.lower().startswith("article in book"):
        parts = raw_source_type.split(":", 1)
        if len(parts) == 2:
            return "Article in Book", parts[1].strip()
        else:
            return "Article in Book", ""

    return raw_source_type, ""


def main():
    total_processed = 0

    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS, delimiter=";")

        if not file_exists:
            writer.writeheader()

        for filename in os.listdir(TXT_FOLDER):
            if not filename.endswith(".txt"):
                continue

            txt_path = os.path.join(TXT_FOLDER, filename)
            meta = parse_metadata(txt_path)

            raw_source_type = meta.get("source_type", "")
            source_type, source_book = parse_source_type(raw_source_type)

            row = {
                "source_id": meta.get("source_id", ""),
                "author": meta.get("author", ""),
                "title": meta.get("title", ""),
                "year": meta.get("year", ""),
                "source_type": source_type,
                "source_book": source_book,
                "publication_place": meta.get("publication_place", ""),
                "publisher": meta.get("published", ""),
                "pages": meta.get("pages", ""),
                "language": meta.get("language", ""),
                "discipline": meta.get("discipline", ""),
                "urn_cts": "",
                "is_primary_text": "No",
                "has_translation": "No",
                "digital_source": meta.get("web", ""),
                "notes": "",
                "doi": meta.get("doi", ""),
                "pdf_path": "",
                "has_pdf": "TRUE",
            }

            writer.writerow(row)
            total_processed += 1
            print(f"Added: {filename}")

    print(f"\n Total files processed: {total_processed}")


if __name__ == "__main__":
    main()
