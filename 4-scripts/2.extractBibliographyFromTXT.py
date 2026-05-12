import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_FOLDER = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "2.outputSnowball_extractBibliographyFromAnchorTxt"
)
INPUT_FOLDER = (
    BASE_DIR
    / "edubbaData"
    / "edubba2.0_DataTxtRaw"
    / "2.1.filterTxtWithBibliography_ForAnystyle"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def extract_source_id(text):
    match = re.search(r"Source_ID\s*:\s*(.+)", text)
    if match:
        return match.group(1).strip()
    return None


def extract_bibliography(text):
    headers = [
        "BIBLIOGRAPHY",
        "REFERENCES",
        "WORKS CITED",
        "LITERATURE",
        "SOURCES",
        "REFERENCES AND NOTES",
        "SELECTED BIBLIOGRAPHY",
        "BIBLIOGRAPHIC REFERENCES",
    ]

    headers_regex = "|".join(headers)

    # Case-sensitive, optional leading "#"
    pattern = rf"(?:^|\n)\s*#?\s*(?:{headers_regex})\s*\n(.*)$"

    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return None


processed = 0
skipped = 0

for filename in os.listdir(INPUT_FOLDER):
    if not filename.endswith(".txt"):
        continue

    path = os.path.join(INPUT_FOLDER, filename)

    with open(path, encoding="utf-8") as f:
        content = f.read()

    source_id = extract_source_id(content)
    bibliography = extract_bibliography(content)

    if not source_id or not bibliography:
        skipped += 1
        continue

    out_path = os.path.join(OUTPUT_FOLDER, f"{source_id}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(bibliography)

    processed += 1

print("Bibliography extraction finished")
print(f"Processed files: {processed}")
print(f"Skipped files (no Source_ID or no bibliography block): {skipped}")
print(f"Output folder: {OUTPUT_FOLDER}")
