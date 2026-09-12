# Acessilia Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Test documents and expected extraction outputs for the [Acessilia](https://github.com/A11yDevs/acessilia) ecosystem.

## Overview

**Acessilia Dataset** provides a shared collection of test documents, intermediate processing artifacts, and expected accessible outputs for projects in the Acessilia ecosystem, including:

- [acessilia-structure-extractor](https://github.com/A11yDevs/acessilia-structure-extractor) — document structure extraction service
- [acessilia](https://github.com/A11yDevs/acessilia) — main accessibility processing platform

By maintaining documents, intermediate artifacts, and expected outputs in a single repository, all consuming projects can validate their extraction and accessibility pipelines against the same reference data, ensuring consistent behavior across the ecosystem.

## Repository Structure

```text
acessilia-dataset/
├── README.md
├── LICENSE
├── input/                           # Source documents (numbered sequentially)
│   ├── manifest.csv                 # Metadata per document
│   ├── 001.pdf                      # java-oo-3pgs (tutorial Java OO)
│   ├── 002.pdf                      # java-oo-369pgs (tutorial Java OO completo)
│   ├── 003.pdf                      # java-oo-caps-9-11-39pgs (capítulos 9-11)
│   ├── 004.pdf                      # java-oo-tables-pg26 (tabelas)
│   ├── 005.jpeg                     # sunset-skyline (fotografia)
│   ├── 006.pdf                      # grandezas-e-medidas-42pgs (apostila matemática)
│   ├── 007.pdf                      # grandezas-e-medidas-pg3-42 (fórmulas)
│   ├── 008.pdf                      # grandezas-e-medidas-pg7-42 (tabela)
│   └── formula-images/              # Formula extraction test fixtures
│       ├── ground_truth.csv         # Expected LaTeX per formula image
│       ├── *_limpa.png              # Clean formula renders (CodeCogs)
│       ├── *_degradada.jpg          # Degraded variants (rotation/blur/noise)
│       ├── *_limpa.pdf              # Synthetic A4 pages with formula image
│       ├── *_degradada.pdf          # Synthetic A4 pages with degraded image
│       ├── texto_paragrafo.png      # Non-formula: plain text paragraph
│       ├── diagrama_fluxo.png       # Non-formula: flow diagram
│       └── grafico_barras.png       # Non-formula: bar chart
├── intermediate/                    # Intermediate processing artifacts
│   ├── manifest.csv                 # Maps input_id → intermediate files
│   ├── processing-manifest/         # ProcessingManifest JSON snapshots
│   │   ├── 001.json
│   │   └── ...
│   ├── canonical-document/          # Canonical document (future)
│   │   ├── 001.json
│   │   └── ...
│   └── pddl-plan/                   # PDDL planning artifacts (future)
│       ├── 001.json
│       └── ...
└── outputs/                         # Expected accessible outputs
    ├── manifest.csv                 # Maps input_id → output files
    ├── txt/                         # Plain text
    │   ├── 001.txt
    │   └── ...
    ├── html/                        # Accessible HTML
    │   ├── 001.html
    │   └── ...
    ├── pdf/                         # PDF
    │   ├── 001.pdf
    │   └── ...
    ├── pdf_ua/                      # PDF/UA (accessible PDF)
    │   ├── 001.pdf
    │   └── ...
    ├── mp3/                         # Audio (text-to-speech)
    │   ├── 001.mp3
    │   └── ...
    └── epub/                        # EPUB
        ├── 001.epub
        └── ...
```

## Input Documents

| ID | Original filename | Format | Pages | Language | Domain | Notes |
|---|---|---|---|---|---|---|
| `001` | `java-oo-3pgs.pdf` | pdf | 3 | pt-BR | programming | Java OO tutorial |
| `002` | `java-oo-369pgs.pdf` | pdf | 369 | pt-BR | programming | Complete Java OO tutorial |
| `003` | `java-oo-caps-9-11-39pgs.pdf` | pdf | 39 | pt-BR | programming | Chapters 9-11 |
| `004` | `java-oo-tables-pg26.pdf` | pdf | 1 | pt-BR | programming | Example tables |
| `005` | `sunset-skyline.jpeg` | image | 1 | pt-BR | general | Photograph |
| `006` | `grandezas-e-medidas-42pgs.pdf` | pdf | 42 | pt-BR | chemistry | Presentation |
| `007` | `grandezas-e-medidas-pg3-42.pdf` | pdf | 1 | pt-BR | chemistry | Tables |
| `008` | `grandezas-e-medidas-pg7-42.pdf` | pdf | 1 | pt-BR | chemistry | Bar chart |
| `009` | `simples_limpa.png` | image | 1 | pt-BR | mathematics | E=mc² — clean formula render (CodeCogs) |
| `010` | `simples_degradada.jpg` | image | 1 | pt-BR | mathematics | E=mc² — degraded variant |
| `011` | `bhaskara_limpa.png` | image | 1 | pt-BR | mathematics | Bhaskara formula — clean render |
| `012` | `bhaskara_degradada.jpg` | image | 1 | pt-BR | mathematics | Bhaskara — degraded variant |
| `013` | `integral_limpa.png` | image | 1 | pt-BR | mathematics | Gaussian integral — clean render |
| `014` | `integral_degradada.jpg` | image | 1 | pt-BR | mathematics | Gaussian integral — degraded |
| `015` | `somatorio_limpa.png` | image | 1 | pt-BR | mathematics | Basel sum — clean render |
| `016` | `somatorio_degradada.jpg` | image | 1 | pt-BR | mathematics | Basel sum — degraded |
| `017` | `matriz_limpa.png` | image | 1 | pt-BR | mathematics | 2×2 matrix — clean render |
| `018` | `matriz_degradada.jpg` | image | 1 | pt-BR | mathematics | 2×2 matrix — degraded |
| `019` | `maxwell_limpa.png` | image | 1 | pt-BR | mathematics | Maxwell–Ampère — clean render |
| `020` | `maxwell_degradada.jpg` | image | 1 | pt-BR | mathematics | Maxwell–Ampère — degraded |
| `021` | `simples_limpa.pdf` | pdf | 1 | pt-BR | mathematics | E=mc² — synthetic A4 page |
| `022` | `simples_degradada.pdf` | pdf | 1 | pt-BR | mathematics | E=mc² — synthetic A4 degraded |
| `023` | `bhaskara_limpa.pdf` | pdf | 1 | pt-BR | mathematics | Bhaskara — synthetic A4 page |
| `024` | `bhaskara_degradada.pdf` | pdf | 1 | pt-BR | mathematics | Bhaskara — synthetic A4 degraded |
| `025` | `integral_limpa.pdf` | pdf | 1 | pt-BR | mathematics | Gaussian integral — synthetic A4 |
| `026` | `integral_degradada.pdf` | pdf | 1 | pt-BR | mathematics | Gaussian integral — synthetic A4 degraded |
| `027` | `somatorio_limpa.pdf` | pdf | 1 | pt-BR | mathematics | Basel sum — synthetic A4 |
| `028` | `somatorio_degradada.pdf` | pdf | 1 | pt-BR | mathematics | Basel sum — synthetic A4 degraded |
| `029` | `matriz_limpa.pdf` | pdf | 1 | pt-BR | mathematics | 2×2 matrix — synthetic A4 |
| `030` | `matriz_degradada.pdf` | pdf | 1 | pt-BR | mathematics | 2×2 matrix — synthetic A4 degraded |
| `031` | `maxwell_limpa.pdf` | pdf | 1 | pt-BR | mathematics | Maxwell–Ampère — synthetic A4 |
| `032` | `maxwell_degradada.pdf` | pdf | 1 | pt-BR | mathematics | Maxwell–Ampère — synthetic A4 degraded |
| `033` | `texto_paragrafo.png` | image | 1 | pt-BR | general | False positive: rendered paragraph |
| `034` | `diagrama_fluxo.png` | image | 1 | pt-BR | general | False positive: flow diagram |
| `035` | `grafico_barras.png` | image | 1 | pt-BR | general | False positive: bar chart |

## Manifests (CSV)

Each top-level directory contains a `manifest.csv` that serves as the index:

- **`input/manifest.csv`** — metadata per source document (id, original filename, format, media type, byte size, pages, language, domain, subdirectory, tables, formulas, images, callouts, chapters, notes)
  - `subdirectory`: subdirectory name for thematic groups (e.g., `formula-images`), empty for documents in `input/` root
- **`input/formula-images/ground_truth.csv`** — expected LaTeX for formula extraction test fixtures, linked to `input/manifest.csv` via `manifest_id` column
- **`intermediate/manifest.csv`** — maps `input_id` → intermediate artifacts (processing-manifest, canonical-document, pddl-plan) with extractor version and configuration
- **`outputs/manifest.csv`** — maps `input_id` → output files per format (txt, html, pdf, pdf_ua, mp3, epub) with generator version

## Usage

### As a git submodule

```bash
# In your project
git submodule add https://github.com/A11yDevs/acessilia-dataset.git tests/dataset
```

Then reference documents and expected outputs relative to the submodule path:

```python
from pathlib import Path
import csv

DATASET_DIR = Path("tests/dataset")


def get_inputs() -> list[Path]:
    """List all input files, recursing into subdirectories."""
    return sorted(
        p for p in DATASET_DIR.glob("input/**/*")
        if p.is_file() and p.name != "manifest.csv"
    )


def resolve_input_path(row: dict, dataset_dir: Path = DATASET_DIR) -> Path:
    """Resolve the full path of an input document from its manifest row.

    Handles documents in thematic subdirectories (e.g., formula-images/)
    via the ``subdirectory`` column.
    """
    subdir = (row.get("subdirectory") or "").strip()
    filename = row["original_filename"]
    if subdir:
        return dataset_dir / "input" / subdir / filename
    return dataset_dir / "input" / filename


def get_manifest(path: str) -> list[dict]:
    """Load a manifest.csv as a list of dicts."""
    with (DATASET_DIR / path).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))
```

### As a Python package (optional)

```bash
pip install acessilia-dataset@git+https://github.com/A11yDevs/acessilia-dataset.git
```

```python
from acessilia_dataset import get_inputs_dir, get_intermediate_dir, get_outputs_dir

for doc in get_inputs_dir().rglob("*"):
    print(doc)
```

## Contributing

Contributions of new test documents are welcome. Please follow these guidelines:

1. Add the source document to `input/` with the next sequential number (`036`, `037`, …)
2. If the document belongs to a thematic group (e.g., formula extraction fixtures), place it in a descriptive subdirectory under `input/` (e.g., `input/formula-images/`)
3. Record its metadata in `input/manifest.csv`:
   - `original_filename`: only the filename (e.g., `simples_limpa.png`)
   - `subdirectory`: the subdirectory name if placed in a thematic folder (e.g., `formula-images`), leave empty for documents in the root of `input/`
4. If the document has associated ground truth (e.g., expected LaTeX for formulas), add it to a `ground_truth.csv` in the same subdirectory, with a `manifest_id` column linking back to the central manifest
5. Generate the intermediate artifacts using the reference pipeline (see below)
6. Ensure the document is small (prefer under 1 MB) and does not contain copyrighted material unless properly licensed
7. Submit a pull request

### Generating intermediate artifacts

The intermediate artifacts (ProcessingManifest, PDDL plan, canonical document) are generated using the Acessilia pipeline with Docling + PDDL.

From the root of the `acessilia` repository, use the helper script:

```bash
# Process all documents (skipping those with >40 pages)
docker run --rm \
  -v $(pwd):/app -w /app \
  acessilia:test-pr24 \
  python scripts/generate_dataset_intermediates.py

# Process specific documents only
docker run --rm \
  -v $(pwd):/app -w /app \
  acessilia:test-pr24 \
  python scripts/generate_dataset_intermediates.py --ids 001 003 005

# Skip already-generated artifacts, just rewrite manifest.csv
docker run --rm \
  -v $(pwd):/app -w /app \
  acessilia:test-pr24 \
  python scripts/generate_dataset_intermediates.py --skip-existing

# Adjust max page threshold
docker run --rm \
  -v $(pwd):/app -w /app \
  acessilia:test-pr24 \
  python scripts/generate_dataset_intermediates.py --max-pages 50
```

The script reads `input/manifest.csv`, processes each document through the Docling → PDDL planner → canonical builder pipeline, and writes:

| Artifact | Directory | Format |
|---|---|---|
| ProcessingManifest | `intermediate/processing-manifest/` | JSON (schema v1.1.0) |
| PDDL NominalPlan | `intermediate/pddl-plan/` | JSON |
| Canonical Document | `intermediate/canonical-document/` | JSON (schema v1.0.0) |

The `intermediate/manifest.csv` is updated automatically after each run.

## Relationship with Acessilia

This repository is part of the [Acessilia](https://github.com/A11yDevs/acessilia) ecosystem. It provides shared test infrastructure for:

- **acessilia** — main accessibility processing platform
- **acessilia-structure-extractor** — standalone document structure extraction service
- Future projects that consume or produce Acessilia canonical structures

## Copyright and License

Copyright (c) 2026 Jhonata Fernandes Cordeiro
Copyright (c) 2026 Marcelo Inuzuka and Acessilia Dataset contributors

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for the full license text.
