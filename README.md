# Acessilia Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Test documents and evaluation references for the [Acessilia](https://github.com/A11yDevs/acessilia) ecosystem.

## Overview

**Acessilia Dataset** provides shared source documents and task-specific evaluation references for projects in the Acessilia ecosystem, including:

- [Acessilia Toolbox](https://github.com/A11yDevs/acessilia-toolbox) — document structure extraction and accessibility processing toolbox
- [acessilia](https://github.com/A11yDevs/acessilia) — main accessibility processing platform

The repository keeps source inputs separate from reference annotations, including partial ones. Coverage, provenance, review state and file paths are recorded per input and task so consumers can report what an evaluation does and does not cover.

## Repository Structure

`input/` contains source documents, fixtures and compatibility copies of the current ground truth files. `references/` contains the new task-oriented references, selectors, schema and coverage manifest. The two layouts coexist during consumer migration.

`intermediate/` is a legacy archive. It remains until Core and Toolbox have pinned the compatible Dataset revision, copied the snapshots required by their regression fixtures into consumer-owned fixtures and switched to those copies.

`outputs/` currently contains only legacy placeholders. Keep it through the compatibility release because the Toolbox provider still declares this split. Outputs created during processing belong to their individual runs. Remove the split and placeholders only in the later cleanup release, after the consumers have migrated.

```text
acessilia-dataset/
├── README.md
├── LICENSE
├── input/
│   ├── manifest.csv
│   ├── manifest.schema.json         # versioned source/provenance row schema (1.1.0)
│   ├── 001.pdf … 008.pdf / images
│   ├── formula-images/              # source fixtures for IDs 009-035
│   │   ├── ground_truth.csv         # legacy path; compatibility copy
│   │   └── formula images / PDFs
│   └── math-reference/
│       ├── velocidade-instantanea.pdf  # source document 036
│       ├── ground_truth.csv         # legacy path; compatibility copy
│       ├── expectations.json        # legacy path; compatibility copy
│       └── PERMISSIONS.md
├── input/presentation-reference/    # legacy paths; compatibility copies
│   ├── ground_truth.csv
│   └── expectations.json
├── outputs/                          # legacy placeholder split; retained for compatibility
│   └── manifest.csv
├── references/
│   ├── manifest.csv                 # availability, coverage and record selectors
│   ├── manifest.schema.json         # versioned CSV-row schema (1.2.0)
│   ├── migration-manifest.csv       # source revision and hashes for old/new copies
│   ├── schemas/                     # schemas for each referenced CSV/JSON document
│   │   ├── formula-image-ground-truth.schema.json
│   │   ├── math-036-ground-truth.schema.json
│   │   ├── math-036-expectations.schema.json
│   │   ├── presentation-006-ground-truth.schema.json
│   │   └── presentation-006-expectations.schema.json
│   ├── formula-images/
│   │   └── ground_truth.csv
│   ├── math/036/
│   │   ├── ground_truth.csv
│   │   └── expectations.json
│   └── presentation/006/
│       ├── ground_truth.csv
│       └── expectations.json
└── intermediate/                    # legacy snapshots; removal is pending fixture handoff
    ├── manifest.csv
    ├── processing-manifest/
    ├── canonical-document/
    └── pddl-plan/
```

The validator and its pull request workflow are in `scripts/validate_dataset.py` and `.github/workflows/validate-dataset.yml`; its pinned dependency is listed in `requirements-validation.txt`.

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
| `036` | `velocidade-instantanea.pdf` | pdf | 5 | pt-BR | mathematics | Calculus 1 handout (UnB) — math accessibility reference case |

## Manifests and evaluation coverage

`input/manifest.csv` catalogs source documents and fixtures. `input_path` is the authoritative repository-root-relative path, for example `input/formula-images/simples_limpa.png`. The original `id` values remain strings, including leading zeroes. `subdirectory` and `original_filename` remain for existing consumers.

The same input rows record `family_id` and `derived_from` for related excerpts, degraded images and synthetic PDFs. They also record source, creator, URL where known, license evidence, redistribution status and a short provenance note. `unknown` and `review_required` are explicit inventory states, not permission to redistribute.

`references/manifest.csv` is the authoritative catalog of reference availability and coverage. Each row identifies an input, an applicable task, a reference type, a format and a `record_selector`. Selectors are JSON values stored in CSV: `csv_filter` selects records by columns such as `manifest_id` and `kind`; `json_pointers` selects expectation rules by JSON Pointer. CSV selectors count `rows`; JSON selectors count list `items`, declared `rules`, or `units` (a list item, otherwise one selected value). A shared file must have a selector that isolates the records counted by that row. Paths are relative to the repository root.

The reference row contract is defined in [`references/manifest.schema.json`](references/manifest.schema.json), version `1.2.0`; `input/manifest.schema.json` defines the source inventory row contract. Each annotated row's `content_schema` points to the schema for its referenced file. The validator checks task/type/format/file/schema combinations, the content schema itself, file paths, input identities and sizes, selectors, selected record counts, page bounds, negative examples and cross-references. It also verifies that all five migrated files remain byte-identical at their legacy and new paths against the hashes in `references/migration-manifest.csv`. Dataset CI runs the validator on every pull request. A missing manifest is an error; a present header-only reference manifest is an empty collection; a task explicitly marked `unannotated` is a separate state.

| Column | Meaning |
|---|---|
| `input_id` | ID from `input/manifest.csv`. |
| `task` | Stable task identifier, such as `formula_image_recognition`. |
| `availability` | `complete`, `partial` or `unannotated` for the declared scope. |
| `coverage_scope` | Pages, objects, checks or other subset covered by the row. |
| `annotated_count`, `eligible_count`, `coverage_unit` | Covered and eligible units. Leave `eligible_count` empty when the denominator is not known. |
| `review_state`, `reviewer`, `reviewed_at` | Review status and reviewer metadata. Allowed review states are `reviewed`, `not_reviewed`, `not_recorded` and `not_applicable`. |
| `provenance` | Source or origin of the reference. Per-record provenance may remain in the referenced file. |
| `annotation_revision` | Content revision of the reference, starting at `1` for the migrated files. |
| `reference_type`, `format` | Current reference types are `ground_truth`, `expectations` and `expected_output`; `format` identifies CSV, JSON or the expected-output format. |
| `schema_version` | Version of this manifest contract; current rows use `1.2.0`. |
| `content_schema` | Repository-relative JSON Schema for the referenced file; empty only when the task is `unannotated`. |
| `file_path` | Repository-relative path. It is empty only when the applicable task is explicitly `unannotated`. |
| `record_selector` | JSON selector for the exact CSV rows or JSON rules counted by this entry; empty only for `unannotated`. |
| `notes` | Additional interpretation limits. |

When `review_state=reviewed`, record both `reviewer` and `reviewed_at`. Imported reference history is not inferred from file presence. Migrated reference files start at `annotation_revision=1`; increment that value when their content changes. Increment `schema_version` and update the JSON Schema when columns or meanings change. Selectors make shared-file row identity explicit; they do not change the meaning or contents of the underlying ground truth.

A row with `availability=unannotated` records a task that applies but has no reference file: `annotated_count` is zero and `file_path` is empty. A missing row means the task is not cataloged for that input; it must not be interpreted as an unannotated task. Negative examples with a ground-truth file are annotated references, not missing data. `complete` means all units in the declared scope are covered; `partial` means only a subset is covered. An unknown denominator stays empty.

Content schemas define the row fields and types for CSV references and the structure of JSON expectation documents. CSV values remain strings, and schema validation does not split or rewrite their contents. Preserve `|` alternatives, `;` terms, ` | ` table-cell separators, LaTeX and regular-expression patterns exactly as stored; consumers interpret those values according to their task contract.

Current inventory:

| Input/task | Availability and coverage |
|---|---|
| Formula-image recognition, IDs 009-035 | Complete per fixture: 27 references, including three explicit negative examples. |
| Math formula transcription, 036 | Complete: 91 formula records (16 display, 68 inline, 6 table headers and 1 table cell) across pages 1-5; eligible count is 91. |
| Math text quality, 036 | Partial: 14 selected checks; total eligible checks is unknown. |
| Math document structure, 036 | Partial: 14 selected expectation rules; total eligible rules is unknown. |
| Math formula speech, 036 | Partial: 8 lexical checks apply to a selected subset of the 16 display formulas. This row does not measure speech presence or verbalization quality across all 16. |
| Presentation slide content, 006 | Partial: 237 assertions across 42 slides; total eligible assertions is unknown. |
| Presentation output safety, structure and degraded-run behavior, 006 | Partial: 9 output-safety rules, 26 structure checks (14 expectation rules and 12 shared table-shape rows) and 2 degraded-run requirements; total eligible checks is unknown. |
| Expected accessible outputs, IDs 001-008 | Unannotated for each of six old formats (txt, html, pdf, pdf_ua, mp3, epub); the former manifest listed placeholders only. |

The source inventory counts and annotation counts use different units. In `input/manifest.csv`, `formulas=16` for 036 counts display formulas, while its reference file has 91 formula assertions; `tables=3` for 006 counts source-document tables, while its reference file has 12 `kind=table` shape assertions among 237 assertions. Do not add these counts or use one as the denominator for the other.

Ground-truth files:

- `references/formula-images/ground_truth.csv` contains expected LaTeX for the formula-image fixtures and identifies `manifest_id` values from `input/manifest.csv`. Its `filename` values remain basenames under `input/formula-images/`, not paths relative to the moved CSV. Resolve the input from `input_path`; the `source` column preserves per-record provenance.
- `references/math/036/ground_truth.csv` contains 91 formula transcriptions in reading order. The transcription follows the printed page, including its mistakes: equation (1) prints `2^8` where `2^3` is meant.
- `references/math/036/expectations.json` contains selected text, structure and spoken-form checks not covered by formula transcription. Its `negative-velocity` check keeps the sign-sensitive pattern and the accepted spoken form `menos`.
- `references/presentation/006/ground_truth.csv` contains selected text, image, chemical-structure, table and formula assertions for slides 1-42. Twelve table-shape rows are also cataloged for `presentation_structure`; they are shared rows, not extra unique CSV records. Values transcribe the source, including its mistakes. Matching is lenient on form and strict on content; superscripts and charges matter. The slide 27 image assertion retains the `granul` prefix used to match “granular.”
- `references/presentation/006/expectations.json` contains selected output-safety, slide-structure and degraded-provider checks.

The legacy copies under `input/`, `intermediate/` and `outputs/` are retained in the first compatibility phase. New processing artifacts belong to a run together with its configuration, not to the versioned reference dataset.

## Usage

### As a git submodule

```bash
git submodule add https://github.com/A11yDevs/acessilia-dataset.git tests/dataset
```

Read inputs from `input/manifest.csv` and evaluation references from `references/manifest.csv`. Reference paths are relative to the repository root; an unannotated row has an empty `file_path`.

```python
from pathlib import Path
import csv

DATASET_DIR = Path("tests/dataset")


def get_manifest(relative_path: str) -> list[dict[str, str]]:
    with (DATASET_DIR / relative_path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def resolve_input_path(row: dict[str, str]) -> Path:
    return DATASET_DIR / row["input_path"]


def get_references(input_id: str, task: str) -> list[dict[str, str]]:
    return [
        row for row in get_manifest("references/manifest.csv")
        if row["input_id"] == input_id and row["task"] == task
    ]


def resolve_reference_path(row: dict[str, str]) -> Path | None:
    relative_path = (row.get("file_path") or "").strip()
    return DATASET_DIR / relative_path if relative_path else None
```

## Contributing

Contributions of source documents and evaluation references are welcome.

1. Add a source document or fixture under `input/`; record its exact `input_path`, family, derivation, origin and license evidence in `input/manifest.csv`.
2. Keep source files in `input/`; store ground truth and task expectations under `references/<task-or-case>/`.
3. Add a row to `references/manifest.csv` for each applicable input, task and reference type. Shared files may be listed by multiple rows, but each row needs a selector for its records or rules.
4. Record the covered scope, unit, counts when known, review state, provenance, annotation revision, schema version and repository-relative path.
5. Use `availability=unannotated` with empty `file_path` and `record_selector` when a task applies but has no reference. Do not use an empty ground-truth value to mean missing annotation; a negative example must have an explicit selected ground-truth row.
6. Run `python scripts/validate_dataset.py`; the pull request CI runs the same validator.
7. Keep newly generated processing artifacts with their run and configuration. Do not remove compatibility paths until the staged migration below is complete.
8. Confirm source permissions before adding third-party documents, then submit a pull request.

### Three-repository migration and compatibility releases

The existing `input/` reference paths, `outputs/` split and `intermediate/` snapshots stay available during the transition. Do not merge a removal of any of these paths before both consumers have moved. The proposed tags name two distinct Dataset revisions; create and publish the first only after consumers have pinned the legacy revision, and the cleanup tag only after consumer CI passes.

| Phase | Dataset revision | Consumer action and gate |
|---|---|---|
| 0 — pin the legacy base | Existing layout at `9ed07b2` | Toolbox #141 replaces floating `main` with the exact legacy revision; Core #388 records that revision for `tests/dataset`. This happens before publishing the new layout. |
| 1 — dual-layout contract | Add `references/`, schema `1.2.0`, selectors, provenance, per-file content schemas and validation while preserving old `input/` references, `outputs/` and `intermediate/`; mark the compatible revision `dataset-references-v1.2.0`. | Both consumers point to the marked revision. The Dataset commit is the source revision they record. |
| 2 — consumer migration | No legacy paths removed. | Toolbox #141 reads explicit paths and selectors from the pinned revision. Core #388 migrates the 036/006 evaluators and fixtures and adds a CI smoke test that reads only the pinned manifests/references, without importing or calling the Toolbox. Preserve the 036/006 baselines and canonical comparison fixtures with source revision, hashes, schema and purpose. |
| 3 — cleanup release | In a later revision tagged `dataset-cleanup-v2.0.0`, remove old reference copies, `outputs/` and `intermediate/`. | Both consumers must use the phase-1 revision and pass the relevant tests with traceable fixtures. The Toolbox must ship at least one release advertising the deprecated API splits before removing them from the default revision. |

Phases 0 and 2 are cross-repository work. This local Dataset branch has not created or published either tag.

### Legacy intermediate snapshots

The existing `intermediate/` directory is a compatibility archive, not evaluation ground truth. Keep it until the required snapshots have been copied into consumer-owned regression fixtures and those consumers have switched to the copies.

| Consumer | Current dependency | Handoff before removing `intermediate/` |
|---|---|---|
| Core comparison | `scripts/compare_pipelines.py` and `tests/test_compare_pipelines_e2e.py` use five historical canonical documents for IDs `001`, `004`, `005`, `007` and `008`. | [Core #388](https://github.com/A11yDevs/acessilia/issues/388) preserves these documents in `tests/fixtures/pipeline-comparison/`, with the source revision, file and input hashes, schema `1.0.0` and regression purpose. |
| Toolbox snapshot tests | `tests/snapshot/test_structure_extract.py` uses six processing manifests for IDs `001`, `003`, `004`, `005`, `007` and `008`. | [Toolbox #141](https://github.com/A11yDevs/acessilia-toolbox/issues/141) preserves these snapshots in `tests/snapshot/references/`, with the source revision, hashes, ProcessingManifest schema `1.1.0`, Docling configuration and regression purpose. |
| Toolbox GitHub provider | `src/acessilia_toolbox/providers/dataset_github.py` currently exposes `intermediate` and `outputs` splits. | Retire those API splits as part of [Toolbox #141](https://github.com/A11yDevs/acessilia-toolbox/issues/141), while keeping the snapshot-test fixtures above available. |

The Dataset manifest records the completed processing runs with Docling `2.87.0`, OCR and table structure enabled, and remote services disabled. The embedded ProcessingManifest records schema `1.1.0` and the `docling-serve` endpoint. New run artifacts belong to the run that produced them; after the consumer-owned copies are in place and their tests pass, remove this legacy directory and its manifest in the phase-3 cleanup release.

## Relationship with Acessilia

This repository is part of the [Acessilia](https://github.com/A11yDevs/acessilia) ecosystem. It provides shared test infrastructure for:

- **acessilia** — main accessibility processing platform
- **Acessilia Toolbox** — document structure extraction and accessibility processing toolbox
- Future projects that consume or produce Acessilia canonical structures

## Copyright and License

Copyright (c) 2026 Jhonata Fernandes Cordeiro
Copyright (c) 2026 Marcelo Inuzuka and Acessilia Dataset contributors

Project-authored content is licensed under the [MIT License](LICENSE). Third-party inputs and material derived from them are subject to the terms applicable to their sources. The [input manifest](input/manifest.csv) records the available provenance and permission evidence for each input.

### Input source and permission inventory

- `001`–`004` — Redistribution permission is pending for Caelum's *Java e Orientação a Objetos* and its derivatives. The source PDF `002` contains a copyright notice restricting copying and distribution.
- `005`–`008` — License and redistribution terms are pending. The provenance of `005` is unverified. The PDF metadata for `006` names Patricia Confessori, and `007`–`008` derive from `006`.
- `009`–`032` — License and redistribution terms are pending for the formula images and their derivatives. The manifest records CodeCogs as the renderer for the source images. The account, rendering date, and terms applicable to those files remain unverified.
- `033`–`035` — The manifest identifies these locally generated negative fixtures as project-authored content under MIT.
- `036` — The [permission record](input/math-reference/PERMISSIONS.md) covers redistribution of *Cálculo 1: O problema da velocidade instantânea* in this repository as a test document. Contact the maintainers about use outside this scope.
