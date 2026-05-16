import pandas as pd
import subprocess
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sources_csv = (
    BASE_DIR
    / "edubbaData"
    / "edubba3_DataSourceFile"
    / "1.outputAnchor"
    / "sourcesAnchor.csv"
)
anystyle_out = BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "4.outputAnystyle"
biblio_txt_dir = (
    BASE_DIR / "edubbaData" / "edubba3_DataSourceFile" / "3.outputNormalizeBibliography"
)

os.makedirs(anystyle_out, exist_ok=True)

sources = pd.read_csv(sources_csv, delimiter=";")

processed = 0
skipped = 0
errors = 0

total = len(sources)

print(f"Total sources: {total}")
print(f"Anystyle output folder: {anystyle_out}")
print("-" * 50)


for idx, row in sources.iterrows():

    source_id = str(row["source_id"]).strip()

    file_path = None

    candidate_txt = os.path.join(biblio_txt_dir, f"{source_id}.txt")
    if os.path.exists(candidate_txt):
        file_path = candidate_txt
    else:
        pdf_path = row.get("pdf_path")
        if isinstance(pdf_path, str) and pdf_path and os.path.exists(pdf_path):
            file_path = pdf_path

    if not file_path:
        skipped += 1
        continue

    out_file = os.path.join(anystyle_out, f"bibl{source_id}.json")

    if os.path.exists(out_file):
        print(f" already exists: {source_id}")
        continue

    cmd = ["anystyle", "parse", file_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f" Anystyle error for {source_id}")
            print(result.stderr[:300])
            errors += 1
            continue

        if result.stdout.strip():
            with open(out_file, "w", encoding="utf8") as f:
                f.write(result.stdout)

            processed += 1
            print(f" {source_id}")
        else:
            skipped += 1

    except Exception as e:
        print(f" Exception for {source_id}: {e}")
        errors += 1


# ---------- REPORT ----------
print("\nFinished")
print("-" * 50)
print(f"Processed successfully : {processed}")
print(f"Skipped (no file)      : {skipped}")
print(f"Errors                 : {errors}")
print(f"Total sources          : {total}")
