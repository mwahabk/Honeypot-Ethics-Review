# Honeypot Ethics Taxonomy (v0.1, basic)

Ethical risks of honeypot research and open-source honeypot tools, stored in a lightweight SQLite database and browsable in a small web page (Meeting 12: "Taxonomy in the database", "create some GUI to connect with the database", "start with the basic one").

Pipeline: literature -> dataset -> coding -> taxonomy.

## Contents

| File | What it is |
|---|---|
| `taxonomy.sqlite` | The taxonomy database (6 stages, 6 categories, 31 risks, 62 mitigations, 69 codes, 239 entries, 1,145 evidence quotes) |
| `index.html` | List view: reads `taxonomy.sqlite` in the browser; lifecycle-stage and risk-category views; click any item to expand |
| `tree.html` | Tree view (Meeting 13): root -> 6 risk categories (or 6 lifecycle stages) -> 31 risks -> 62 mitigations, drawn as connected boxes; click a risk for its details; print or save as PDF |
| `taxonomy_content.py` | The taxonomy itself: stages, categories and risks (definition, how it appears, mitigations, trade-off, linked codes, dataset indicator) |
| `build_taxonomy.py` | Rebuilds `taxonomy.sqlite` from the content file, the codebook, the final open coding and the dataset |

## Open the GUI

Browsers block reading a local file from a page opened with a double-click, so serve the folder:

```
cd taxonomy
python -m http.server 8000
```

Then open http://localhost:8000 (list view) or http://localhost:8000/tree.html (tree view). The two pages link to each other. (Opened directly, the page offers a file picker for `taxonomy.sqlite` instead.)

## Rebuild the database

```
python build_taxonomy.py --codebook ../taguette/codebook.csv --dataset ../dataset/honeypot_ethics_dataset.csv \
  --papers ../taguette/scientific-pdf-coding-final-2026-11-16.sqlite3 \
  --tools ../taguette/ns-tool-documentation-final-2026-11-16.sqlite3 --out taxonomy.sqlite
```

The build stops if any of the 69 codebook codes is not mapped to a risk (or marked as context), or if the dataset is not the unified 239-row file.

## Database tables

`stage`, `category`, `risk`, `risk_stage` (risk-to-stage, many-to-many), `mitigation`, `code`, `risk_code`, `entry` (the 239 dataset rows), `evidence` (coded quotes per entry and code), `risk_entry` (entries where the risk's dataset indicator holds), `meta`.

Prevalence counts describe what papers and tool documentation report, not what authors did in practice.
