import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN_FILE = ROOT / "data" / "big" / "appeals.jsonl"
OUT_FILE = ROOT / "data" / "big" / "event_details.jsonl"

events = {}

records = 0
missing = 0

with open(IN_FILE, encoding="utf-8") as inp:
    for line in inp:
        line = line.strip()
        if not line:
            continue

        records += 1
        rec = json.loads(line)
        event_details = rec.get("event_details")

        # Some records may not have an event_details attached
        if not event_details:
            missing += 1
            continue

        # If appeal_to_id.py has already run, event_details is just an id (no details to save)
        if not isinstance(event_details, dict):
            continue

        events.setdefault(event_details["id"], event_details)

with open(OUT_FILE, "w", encoding="utf-8") as out:
    for event in events.values():
        out.write(json.dumps(event) + "\n")

print(f"Records: {records}, Missing Events: {missing}, Unique Events: {len(events)}")