# This script rewrites ops_learning.jsonl so that each record's "appeal" field
# holds only the appeal's id instead of the full appeal object.
#
#   before: "appeal": {"id": 3766, "code": "MDRMR015", "name": "...", ...}
#   after:  "appeal": 3766
#
# The full appeal details live in appeals.jsonl (made by fetch_appeal.py),
# so run fetch_appeal.py FIRST, before running this script.
#
# Safe to run more than once: records whose appeal is already an id are left as they are.

import json
import os
from pathlib import Path

# Build paths relative to this script so it works from any folder.
# This file lives in tools/modify_json/, so the repo root is two levels up.
ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "data" / "big" / "ops_learning.jsonl"

# Write to a temporary file first, then swap it in at the end.
# That way, if something goes wrong halfway, the original file is untouched.
TMP_FILE = FILE.with_suffix(".jsonl.tmp")

records = 0
changed = 0

with open(FILE, encoding="utf-8") as inp, open(TMP_FILE, "w", encoding="utf-8") as out:

    for line in inp:
        line = line.strip()
        if not line:
            continue

        records += 1
        rec = json.loads(line)

        # Only replace the appeal if it is still a full object (a dict)
        if isinstance(rec.get("appeal"), dict):
            rec["appeal"] = rec["appeal"]["id"]
            changed += 1

        out.write(json.dumps(rec, ensure_ascii=False) + "\n")

# Replace the original file with the new one
os.replace(TMP_FILE, FILE)

print(f"Read {records} records")
print(f"Replaced appeal with its id in {changed} records")
