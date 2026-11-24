"""Convert data/big/*.jsonl into a SQLite database (data/big.db)."""
import json
import sqlite3
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "big"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA.parent / "big.db"

SCHEMA = """
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    dtype INTEGER,
    name TEXT,
    start_date TEXT,
    emergency_response_contact_email TEXT,
    translation_module_original_language TEXT
);
CREATE TABLE countries (
    id INTEGER PRIMARY KEY,
    iso TEXT,
    iso3 TEXT,
    name TEXT,
    society_name TEXT,
    region INTEGER,
    record_type INTEGER,
    record_type_display TEXT,
    independent INTEGER,
    is_deprecated INTEGER,
    fdrs TEXT,
    average_household_size REAL,
    translation_module_original_language TEXT
);
CREATE TABLE event_countries (
    event_id INTEGER REFERENCES events(id),
    country INTEGER REFERENCES countries(id),
    PRIMARY KEY (event_id, country)
);
CREATE TABLE appeals (
    id INTEGER PRIMARY KEY,
    code TEXT,
    name TEXT,
    atype TEXT,
    event_id INTEGER REFERENCES events(id),
    country INTEGER,
    start_date TEXT
);
CREATE TABLE learnings (
    id INTEGER PRIMARY KEY,
    appeal INTEGER REFERENCES appeals(id),
    appeal_code TEXT,
    appeal_document_id INTEGER,
    document_url TEXT,
    document_name TEXT,
    learning_en TEXT, learning_es TEXT, learning_fr TEXT, learning_ar TEXT,
    learning_validated TEXT,
    learning_validated_en TEXT, learning_validated_es TEXT,
    learning_validated_fr TEXT, learning_validated_ar TEXT,
    type_validated INTEGER,
    is_validated INTEGER,
    modified_at TEXT,
    created_at TEXT,
    translation_module_original_language TEXT,
    translation_module_skip_auto_translation INTEGER
);
CREATE TABLE learning_organizations (learning_id INTEGER REFERENCES learnings(id), organization INTEGER, PRIMARY KEY (learning_id, organization));
CREATE TABLE learning_sectors (learning_id INTEGER REFERENCES learnings(id), sector INTEGER, PRIMARY KEY (learning_id, sector));
CREATE TABLE learning_per_components (learning_id INTEGER REFERENCES learnings(id), per_component INTEGER, PRIMARY KEY (learning_id, per_component));
CREATE INDEX idx_appeals_event ON appeals(event_id);
CREATE INDEX idx_learnings_appeal ON learnings(appeal);
"""

LIST_TABLES = {
    "organization_validated": ("learning_organizations", "organization"),
    "sector_validated": ("learning_sectors", "sector"),
    "per_component_validated": ("learning_per_components", "per_component"),
}


def rows(name):
    with open(DATA / f"{name}.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def insert(db, table, row):
    cols = ", ".join(row)
    marks = ", ".join("?" * len(row))
    db.execute(f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({marks})", list(row.values()))


def main():
    OUT.unlink(missing_ok=True)
    db = sqlite3.connect(OUT)
    db.executescript(SCHEMA)

    for e in rows("event_details"):
        for c in e.pop("countries_for_preview") or []:
            insert(db, "countries", c)
            insert(db, "event_countries", {"event_id": e["id"], "country": c["id"]})
        for k in ("slug", "parent_event"):
            e.pop(k, None)
        insert(db, "events", e)

    for a in rows("appeals"):
        ev = a.pop("event_details")
        a["event_id"] = ev["id"] if ev else None
        insert(db, "appeals", a)

    for l in rows("learnings"):
        for key, (table, col) in LIST_TABLES.items():
            for v in l.pop(key) or []:
                insert(db, table, {"learning_id": l["id"], col: v})
        insert(db, "learnings", l)

    db.commit()
    for t in ("countries", "events", "event_countries", "appeals", "learnings",
              "learning_organizations", "learning_sectors", "learning_per_components"):
        print(t, db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    db.close()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
