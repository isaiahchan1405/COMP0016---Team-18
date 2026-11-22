# This script reads ops_learning.jsonl and pulls out the "appeal" part of each record,
# saving each unique appeal to its own file in JSON Lines format.
#
# Many learning records belong to the same appeal, so each appeal is only written once
# (the first time its id is seen).

import json
from pathlib import Path

# Build paths relative to this script so it works from any folder.
# This file lives in tools/modify_json/, so the repo root is two levels up.
ROOT = Path(__file__).resolve().parents[2]
IN_FILE = ROOT / "data" / "big" / "ops_learning.jsonl"
OUT_FILE = ROOT / "data" / "big" / "appeals.jsonl"

# Unique appeals, keyed by id, in the order they are first seen
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

print(f"Read {records} records")

# Only write the file if we actually found full appeal objects,
# so we never wipe an existing appeals.jsonl with an empty one.
if not appeals:
    print("No full appeal objects found (ops_learning.jsonl may already contain only ids).")
    print(f"Left {OUT_FILE} unchanged.")
else:
    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for appeal in appeals.values():
            out.write(json.dumps(appeal, ensure_ascii=False) + "\n")
    print(f"Wrote {len(appeals)} unique appeals to {OUT_FILE}")

if missing:
    print(f"{missing} records had no appeal")
