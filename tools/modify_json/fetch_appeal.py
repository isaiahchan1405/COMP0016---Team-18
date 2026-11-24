# This script reads learnings.jsonl and pulls out the "appeal" part of each record,
# saving each unique appeal to its own file in JSON Lines format.
#
# Many learning records belong to the same appeal, so each appeal is only written once
# (the first time its id is seen).

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN_FILE = ROOT / "data" / "big" / "learnings.jsonl"
OUT_FILE = ROOT / "data" / "big" / "test.jsonl"

appeals = {}

records = 0
missing = 0

with open(IN_FILE, encoding="utf-8") as inp:

    for line in inp:
        line = line.strip()
        if not line:
            continue

        records += 1
        rec = json.loads(line)
        appeal = rec.get("appeal")

        # Some records may not have an appeal attached
        if not appeal:
            missing += 1
            continue

        # If appeal_to_id.py has already run, appeal is just an id (no details to save)
        if not isinstance(appeal, dict):
            continue

        appeals.setdefault(appeal["id"], appeal)

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for appeal in appeals.values():
        out.write(json.dumps(appeal, ensure_ascii=False) + "\n")

print(f"Records: {records}, Missing Appeals: {missing}, Unique appeals: {len(appeals)}")