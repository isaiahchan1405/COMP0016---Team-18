# Lookup tables for Ops Learning fields

The IFRC GO Ops Learning API stores several fields as numeric ids.
These CSVs turn those ids into names.

| Field in an Ops Learning record | Lookup file |
|---|---|
| `per_component_validated` | `per_components.csv` |
| `sector_validated` | `sectors.csv` |
| `type_validated` | `learning_types.csv` |
| `organization_validated` | `organization_types.csv` |

Example: `"per_component_validated": [5, 54]` means component 5
(Quality and accountability) and component 35 (Staff and volunteer management).

## PER component ids are not component numbers

`per_component_validated` holds GO's **database ids**, not the PER component
numbers (1-37). They only match for ids 1-13:

- Component 14 is a parent with 14 sub-components, 14A-14N (ids 15-28).
  This shifts every later id: component 15 has id 29, and so on.
- Ids 49-53 do not exist in the API, so components 35, 36 and 37 have
  ids 54, 55 and 56.

Always join on `id`. Use `component_code` (e.g. `14C`, `35`) when you need
the human-facing PER number.

The DREF-NLP repository (github.com/IFRCGo/DREF-NLP) uses component numbers,
with 34 split into 34-a to 34-e, so its tags do not line up with these ids.

## Source

Fetched from the GO API on 2026-11-24:

- `https://goadmin.ifrc.org/api/v2/per-formcomponent/?limit=200`
- `https://goadmin.ifrc.org/api/v2/primarysector/`
- `https://goadmin.ifrc.org/api/v2/global-enums/` (`per_learning_type`)
- `https://goadmin.ifrc.org/api/v2/ops-learning/organization-type/`

The area titles in `per_components.csv` (`area_title`) are not returned by
the component endpoint; they are the five PER areas, numbered 1-5.
Re-fetch if GO adds or removes components.
