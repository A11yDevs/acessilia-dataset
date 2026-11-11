#!/usr/bin/env python3
"""Validate Dataset manifests, reference selectors, and compatibility copies."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: set[str] = set()
CONTENT_SCHEMA_BY_FILE = {
    "references/formula-images/ground_truth.csv": "references/schemas/formula-image-ground-truth.schema.json",
    "references/math/036/ground_truth.csv": "references/schemas/math-036-ground-truth.schema.json",
    "references/math/036/expectations.json": "references/schemas/math-036-expectations.schema.json",
    "references/presentation/006/ground_truth.csv": "references/schemas/presentation-006-ground-truth.schema.json",
    "references/presentation/006/expectations.json": "references/schemas/presentation-006-expectations.schema.json",
}
LEGACY_SOURCE_REVISION = "9ed07b28aeddb69721228f2dd66de6f9794c0001"
# Blob digests from the legacy revision, also available to exported trees.
LEGACY_REFERENCE_BLOBS = {
    ("input/formula-images/ground_truth.csv", "references/formula-images/ground_truth.csv"):
        "eb1f77a7a28b83d736a1fecaa52de2fac20b43a4595882829b84e2c3e34dde0d",
    ("input/math-reference/ground_truth.csv", "references/math/036/ground_truth.csv"):
        "d0027c3f152ff016d03b70e6360f4b6422c3dc46b55af9b5d547e140b58493ed",
    ("input/math-reference/expectations.json", "references/math/036/expectations.json"):
        "a2b5de74715de260103bb5bbfd8f4424a080f9accea2efa57af2c80c5f32bb48",
    ("input/presentation-reference/ground_truth.csv", "references/presentation/006/ground_truth.csv"):
        "ce3b3de211832b4b9406ffd8e19e4436b2d51bcda1a6339cfba912acb0e6926a",
    ("input/presentation-reference/expectations.json", "references/presentation/006/expectations.json"):
        "ed68fe8c9a94e89ab2507676e590a7500c25dc2b9336853d6dfb9b7f8c8fa737",
}


def content_contract(reference_type: str, format_name: str, file_path: str) -> tuple[str, str, str, str]:
    return (reference_type, format_name, file_path, CONTENT_SCHEMA_BY_FILE[file_path])


TASK_CONTENT_CONTRACTS = {
    "formula_image_recognition": {
        content_contract("ground_truth", "csv", "references/formula-images/ground_truth.csv")
    },
    "math_formula_transcription": {
        content_contract("ground_truth", "csv", "references/math/036/ground_truth.csv")
    },
    "math_text_quality": {
        content_contract("expectations", "json", "references/math/036/expectations.json")
    },
    "math_document_structure": {
        content_contract("expectations", "json", "references/math/036/expectations.json")
    },
    "math_formula_speech": {
        content_contract("expectations", "json", "references/math/036/expectations.json")
    },
    "presentation_slide_content": {
        content_contract("ground_truth", "csv", "references/presentation/006/ground_truth.csv")
    },
    "presentation_output_safety": {
        content_contract("expectations", "json", "references/presentation/006/expectations.json")
    },
    "presentation_structure": {
        content_contract("ground_truth", "csv", "references/presentation/006/ground_truth.csv"),
        content_contract("expectations", "json", "references/presentation/006/expectations.json"),
    },
    "presentation_degraded_run_behavior": {
        content_contract("expectations", "json", "references/presentation/006/expectations.json")
    },
    "accessible_output_reference": {
        ("expected_output", format_name, "", "")
        for format_name in ("txt", "html", "pdf", "pdf_ua", "mp3", "epub")
    },
}

TASK_JSON_SELECTORS = {
    "math_text_quality": ("rules", {"/text"}),
    "math_document_structure": ("rules", {"/structure"}),
    "math_formula_speech": ("items", {"/speech/formulas"}),
    "presentation_output_safety": ("items", {"/text/must_not_match"}),
    "presentation_structure": (
        "rules", {"/structure/slide_titles", "/structure/deck_title", "/structure/slide_count"}
    ),
    "presentation_degraded_run_behavior": ("rules", {"/degraded"}),
}


def error(message: str) -> None:
    ERRORS.append(message)


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(f"{path.relative_to(ROOT)}: cannot read JSON: {exc}")
        return None


def load_csv(path: Path, required: bool = True) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        if required:
            error(f"{path.relative_to(ROOT)}: required manifest is missing")
        return [], []
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                error(f"{path.relative_to(ROOT)}: CSV header is missing")
                return [], []
            fields = list(reader.fieldnames)
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        error(f"{path.relative_to(ROOT)}: cannot read CSV: {exc}")
        return [], []
    if any(None in row for row in rows):
        error(f"{path.relative_to(ROOT)}: one or more rows have extra columns")
    if any(value is None for row in rows for value in row.values()):
        error(f"{path.relative_to(ROOT)}: one or more rows have missing columns")
    return fields, rows


def validate_schema_document(schema_path: Path) -> dict[str, Any] | None:
    schema = load_json(schema_path)
    if isinstance(schema, dict):
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # jsonschema exposes several schema-error types
            error(f"{schema_path.relative_to(ROOT)}: invalid JSON Schema: {exc}")
            return None
    else:
        error(f"{schema_path.relative_to(ROOT)}: schema must be a JSON object")
        return None
    return schema


def validate_manifest_rows(
    path: Path,
    schema_path: Path,
    rows: list[dict[str, str]],
    fields: list[str],
) -> dict[str, Any] | None:
    schema = validate_schema_document(schema_path)
    if schema is None:
        return None
    expected_fields = schema.get("x-csv-columns")
    if fields != expected_fields:
        error(
            f"{path.relative_to(ROOT)}: CSV columns do not match schema; "
            f"expected {expected_fields}, got {fields}"
        )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for line_number, row in enumerate(rows, start=2):
        for issue in validator.iter_errors(row):
            location = ".".join(str(part) for part in issue.absolute_path) or "row"
            error(f"{path.relative_to(ROOT)}:{line_number} {location}: {issue.message}")
    return schema


def validate_content_schema(path: Path, schema_path: Path) -> None:
    schema = validate_schema_document(schema_path)
    if schema is None:
        return
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    if path.suffix.lower() == ".csv":
        fields, rows = load_csv(path)
        expected_fields = schema.get("x-csv-columns")
        if fields != expected_fields:
            error(
                f"{path.relative_to(ROOT)}: columns do not match {schema_path.relative_to(ROOT)}; "
                f"expected {expected_fields}, got {fields}"
            )
        for line_number, row in enumerate(rows, start=2):
            for issue in validator.iter_errors(row):
                location = ".".join(str(part) for part in issue.absolute_path) or "row"
                error(f"{path.relative_to(ROOT)}:{line_number} {location}: {issue.message}")
        return
    document = load_json(path)
    if document is None:
        return
    for issue in validator.iter_errors(document):
        location = ".".join(str(part) for part in issue.absolute_path) or "document"
        error(f"{path.relative_to(ROOT)} {location}: {issue.message}")


def repo_file(relative: str, *, prefix: str | None = None) -> Path | None:
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "\\" in relative:
        error(f"unsafe repository-relative path: {relative!r}")
        return None
    if prefix and (not candidate.parts or candidate.parts[0] != prefix):
        error(f"path {relative!r} must be under {prefix}/")
        return None
    resolved = (ROOT / Path(*candidate.parts)).resolve()
    if ROOT not in resolved.parents:
        error(f"path escapes the repository: {relative!r}")
        return None
    return resolved


def validate_input_rows(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_id: dict[str, dict[str, str]] = {}
    for line_number, row in enumerate(rows, start=2):
        identifier = row.get("id", "")
        if identifier in by_id:
            error(f"input/manifest.csv:{line_number}: duplicate input id {identifier!r}")
        by_id[identifier] = row

        if identifier in {f"{number:03d}" for number in range(1, 9)}:
            expected = Path("input") / f"{identifier}{Path(row.get('original_filename', '')).suffix}"
        else:
            expected = Path("input")
            if row.get("subdirectory"):
                expected /= row["subdirectory"]
            expected /= row.get("original_filename", "")
        if row.get("input_path") != expected.as_posix():
            error(
                f"input/manifest.csv:{line_number}: input_path {row.get('input_path')!r} "
                f"does not match the declared input path convention {expected.as_posix()!r}"
            )

        file_path = repo_file(row.get("input_path", ""), prefix="input")
        if file_path is not None:
            if not file_path.is_file():
                error(f"input/manifest.csv:{line_number}: missing input file {row['input_path']}")
            else:
                try:
                    actual_size = file_path.stat().st_size
                    if actual_size != int(row.get("byte_size", "0")):
                        error(
                            f"input/manifest.csv:{line_number}: byte_size is {row.get('byte_size')}, "
                            f"but {row['input_path']} is {actual_size} bytes"
                        )
                except (OSError, ValueError) as exc:
                    error(f"input/manifest.csv:{line_number}: cannot check input size: {exc}")

        status = row.get("license_status")
        redistribution = row.get("redistribution_status")
        if status == "restricted" and redistribution != "permission_required":
            error(f"input {identifier}: restricted source must require permission")
        if status == "unknown" and redistribution != "review_required":
            error(f"input {identifier}: unknown source terms must require review")
        if redistribution in {"permission_required", "review_required"}:
            WARNINGS.add(
                f"input {identifier}: rights follow-up required "
                f"({redistribution}; {row.get('license_summary', '')})"
            )

    if not rows:
        error("input/manifest.csv: input inventory must contain at least one row")

    for identifier, row in by_id.items():
        parent = row.get("derived_from", "")
        if parent:
            if parent not in by_id:
                error(f"input {identifier}: derived_from references unknown input {parent}")
            elif by_id[parent].get("family_id") != row.get("family_id"):
                error(f"input {identifier}: derived_from parent {parent} is in another family")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            error(f"input family derivation cycle includes {identifier}")
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        parent = by_id.get(identifier, {}).get("derived_from", "")
        if parent in by_id:
            visit(parent)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in by_id:
        visit(identifier)
    return by_id


def parse_selector(raw: str, row_number: int, selector_schema: dict[str, Any]) -> dict[str, Any] | None:
    try:
        selector = json.loads(raw)
    except json.JSONDecodeError as exc:
        error(f"references/manifest.csv:{row_number}: record_selector is invalid JSON: {exc}")
        return None
    validator = Draft202012Validator(selector_schema)
    issues = list(validator.iter_errors(selector))
    for issue in issues:
        error(f"references/manifest.csv:{row_number}: invalid record_selector: {issue.message}")
    return None if issues else selector


def validate_task_selector(
    task: str, format_name: str, selector: dict[str, Any], row_number: int
) -> bool:
    if format_name == "json":
        mode, allowed_pointers = TASK_JSON_SELECTORS[task]
        matches = (
            selector["type"] == "json_pointers"
            and selector["count_mode"] == mode
            and set(selector["pointers"]) <= allowed_pointers
        )
    else:
        matches = selector["type"] == "csv_filter" and (
            task != "presentation_structure" or selector["filters"].get("kind") == "table"
        )
    if not matches:
        error(f"references/manifest.csv:{row_number}: selector does not match task {task!r}")
    return matches


def resolve_json_pointer(document: Any, pointer: str) -> Any:
    current = document
    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[token]
        elif isinstance(current, list):
            current = current[int(token)]
        else:
            raise KeyError(f"cannot resolve {pointer!r} at {token!r}")
    return current


def count_rules(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        meaningful = {
            key: child
            for key, child in value.items()
            if key not in {"description", "notes", "why", "language"}
        }
        if not meaningful:
            return 0
        if "description" not in value and not any(isinstance(child, list) for child in meaningful.values()):
            return 1
        return sum(len(child) if isinstance(child, list) else 1 for child in meaningful.values())
    return 1


def selector_count(path: Path, selector: dict[str, Any], input_id: str, row_number: int) -> int | None:
    mode = selector.get("count_mode")
    if selector.get("type") == "csv_filter":
        fields, records = load_csv(path)
        filters = selector.get("filters", {})
        if filters.get("manifest_id") != input_id:
            error(f"references/manifest.csv:{row_number}: CSV selector must filter manifest_id={input_id}")
        missing = sorted(set(filters) - set(fields))
        if missing:
            error(f"references/manifest.csv:{row_number}: selector columns missing from {path}: {missing}")
            return None
        selected = [record for record in records if all(record.get(k) == v for k, v in filters.items())]
        if not selected:
            error(f"references/manifest.csv:{row_number}: selector matches no records in {path}")
        for record in selected:
            if "manifest_id" in record and record["manifest_id"] != input_id:
                error(
                    f"references/manifest.csv:{row_number}: selected record belongs to "
                    f"input {record['manifest_id']}, expected {input_id}"
                )
        if mode != "rows":
            error(f"references/manifest.csv:{row_number}: CSV selector count_mode must be rows")
        return len(selected)

    if selector.get("type") == "json_pointers":
        document = load_json(path)
        if document is None:
            return None
        if isinstance(document, dict) and document.get("manifest_id") != input_id:
            error(
                f"references/manifest.csv:{row_number}: JSON manifest_id is "
                f"{document.get('manifest_id')!r}, expected {input_id}"
            )
        total = 0
        for pointer in selector.get("pointers", []):
            try:
                value = resolve_json_pointer(document, pointer)
            except (KeyError, IndexError, ValueError, TypeError) as exc:
                error(f"references/manifest.csv:{row_number}: invalid JSON pointer {pointer!r}: {exc}")
                continue
            if mode == "items":
                if not isinstance(value, list):
                    error(f"references/manifest.csv:{row_number}: {pointer} must select a list for items")
                else:
                    total += len(value)
            elif mode == "rules":
                total += count_rules(value)
            else:  # units
                total += len(value) if isinstance(value, list) else 1
        return total
    return None


def validate_reference_records(
    path: Path,
    records_cache: dict[Path, tuple[list[str], list[dict[str, str]]]],
    input_by_id: dict[str, dict[str, str]],
) -> None:
    if path.suffix.lower() != ".csv":
        return
    if path not in records_cache:
        records_cache[path] = load_csv(path)
    fields, records = records_cache[path]
    seen: set[str] = set()
    for line_number, record in enumerate(records, start=2):
        record_id = record.get("id", "")
        if record_id:
            if record_id in seen:
                error(f"{path.relative_to(ROOT)}:{line_number}: duplicate record id {record_id!r}")
            seen.add(record_id)
        manifest_id = record.get("manifest_id", "")
        if manifest_id and manifest_id not in input_by_id:
            error(f"{path.relative_to(ROOT)}:{line_number}: unknown manifest_id {manifest_id!r}")
        if "page" in record and record["page"]:
            try:
                page = int(record["page"])
                max_pages = int(input_by_id[manifest_id]["pages"])
                if not 1 <= page <= max_pages:
                    error(f"{path.relative_to(ROOT)}:{line_number}: page {page} outside 1..{max_pages}")
            except (KeyError, ValueError):
                error(f"{path.relative_to(ROOT)}:{line_number}: invalid page or missing manifest_id")
        if "kind" in record and not record["kind"]:
            error(f"{path.relative_to(ROOT)}:{line_number}: kind is required")

    if path == ROOT / "references/formula-images/ground_truth.csv":
        required = {"id", "manifest_id", "filename", "kind", "format", "expected_latex"}
        if not required.issubset(fields):
            error(f"{path.relative_to(ROOT)}: formula references missing columns {sorted(required - set(fields))}")
        for line_number, record in enumerate(records, start=2):
            if record.get("kind") not in {"formula", "formula_pdf", "non_formula"}:
                error(f"{path.relative_to(ROOT)}:{line_number}: unsupported formula fixture kind {record.get('kind')!r}")
            input_row = input_by_id.get(record.get("manifest_id", ""))
            if input_row:
                expected_name = Path(input_row["input_path"]).name
                if record.get("filename") != expected_name:
                    error(
                        f"{path.relative_to(ROOT)}:{line_number}: filename must remain the basename "
                        f"of {input_row['input_path']} (got {record.get('filename')!r})"
                    )
                if not input_row["input_path"].startswith("input/formula-images/"):
                    error(f"{path.relative_to(ROOT)}:{line_number}: formula fixture is outside input/formula-images/")

    if path == ROOT / "references/math/036/ground_truth.csv":
        required = {"id", "manifest_id", "page", "kind", "expected_latex", "context", "notes"}
        if not required.issubset(fields):
            error(f"{path.relative_to(ROOT)}: math references missing columns {sorted(required - set(fields))}")
        for line_number, record in enumerate(records, start=2):
            if record.get("kind") not in {"inline", "display", "table-header", "table-cell"}:
                error(f"{path.relative_to(ROOT)}:{line_number}: unsupported formula kind {record.get('kind')!r}")
            if not record.get("expected_latex", "").strip():
                error(f"{path.relative_to(ROOT)}:{line_number}: expected_latex is required for 036 formulas")

    if path == ROOT / "references/presentation/006/ground_truth.csv":
        required = {"id", "manifest_id", "page", "kind", "expected", "context", "notes"}
        if not required.issubset(fields):
            error(f"{path.relative_to(ROOT)}: presentation references missing columns {sorted(required - set(fields))}")
        for line_number, record in enumerate(records, start=2):
            if record.get("kind") not in {"text", "image", "chemical-structure", "table", "table-header", "table-row", "formula"}:
                error(f"{path.relative_to(ROOT)}:{line_number}: unsupported presentation kind {record.get('kind')!r}")
            if not record.get("expected", "").strip():
                error(f"{path.relative_to(ROOT)}:{line_number}: expected value is required")


def validate_special_fixtures(
    input_by_id: dict[str, dict[str, str]],
    reference_rows: list[dict[str, str]],
    records_cache: dict[Path, tuple[list[str], list[dict[str, str]]]],
) -> None:
    formula_path = ROOT / "references/formula-images/ground_truth.csv"
    if formula_path in records_cache:
        _, formula_rows = records_cache[formula_path]
        formulas = {row.get("manifest_id"): row for row in formula_rows}
        for identifier in ("033", "034", "035"):
            row = formulas.get(identifier)
            if not row or row.get("kind") != "non_formula" or row.get("expected_latex") != "":
                error(f"formula negative {identifier} must remain a non_formula row with blank expected_latex")
        for identifier in (f"{number:03d}" for number in range(9, 33)):
            row = formulas.get(identifier)
            if row and not row.get("expected_latex", "").strip():
                error(f"positive formula fixture {identifier} must have expected_latex")

    math_path = ROOT / "references/math/036/ground_truth.csv"
    math_rows: list[dict[str, str]] = []
    if math_path in records_cache:
        _, math_rows = records_cache[math_path]
        counts = Counter(row.get("kind") for row in math_rows)
        expected = {"display": 16, "inline": 68, "table-header": 6, "table-cell": 1}
        if len(math_rows) != 91 or dict(counts) != expected:
            error(f"036 formula inventory must remain 91 records by kind {expected}; got {len(math_rows)} {dict(counts)}")
        if "036" in input_by_id and input_by_id["036"].get("formulas") != "16":
            error("input 036 formulas must remain the 16 display formulas, separate from 91 GT assertions")
        math_ids = {row.get("id") for row in math_rows}
        expectations = load_json(ROOT / "references/math/036/expectations.json")
        if isinstance(expectations, dict):
            spoken = expectations.get("speech", {}).get("formulas", [])
            spoken_ids = [entry.get("formula") for entry in spoken if isinstance(entry, dict)]
            if len(spoken_ids) != len(set(spoken_ids)) or set(spoken_ids) - math_ids:
                error("036 speech formula references must be unique and resolve to ground-truth IDs")
            display_ids = {row.get("id") for row in math_rows if row.get("kind") == "display"}
            if len(spoken_ids) != 8 or set(spoken_ids) - display_ids:
                error("036 speech word checks must remain 8 unique references within the 16 display formulas")
            speech_rows = [
                row
                for row in reference_rows
                if row.get("input_id") == "036" and row.get("task") == "math_formula_speech"
            ]
            if len(speech_rows) != 1:
                error("036 must have exactly one math_formula_speech coverage row")
            elif (
                speech_rows[0].get("availability") != "partial"
                or speech_rows[0].get("annotated_count") != "8"
                or speech_rows[0].get("eligible_count") != "16"
                or speech_rows[0].get("coverage_unit") != "formula"
            ):
                error("036 speech coverage must distinguish 8 lexical checks from the 16-formula display scope")
            equation_numbers = expectations.get("structure", {}).get("equation_numbers", [])
            eq_ids = [entry.get("formula") for entry in equation_numbers if isinstance(entry, dict)]
            if set(eq_ids) - math_ids:
                error("036 equation-number references must resolve to ground-truth IDs")
            eq_values = [entry.get("number") for entry in equation_numbers if isinstance(entry, dict)]
            if any(not value for value in eq_values) or len(eq_values) != len(set(eq_values)):
                error("036 equation numbers must be present and unique")
            for section in (expectations.get("text", {}).get("must_match", []), expectations.get("text", {}).get("must_not_match", [])):
                for item in section:
                    try:
                        re.compile(item["pattern"])
                    except (KeyError, re.error) as exc:
                        error(f"036 expectation has an invalid regular expression: {exc}")

    presentation_path = ROOT / "references/presentation/006/ground_truth.csv"
    if presentation_path in records_cache:
        _, rows = records_cache[presentation_path]
        kinds = Counter(row.get("kind") for row in rows)
        if kinds.get("table") != 12:
            error(f"006 must retain 12 kind=table shape assertions; got {kinds.get('table', 0)}")
        if "006" in input_by_id and input_by_id["006"].get("tables") != "3":
            error("input 006 tables must remain 3; this catalog count is distinct from 12 table assertions")

    permission_row = input_by_id.get("036")
    permission_path = ROOT / "input/math-reference/PERMISSIONS.md"
    if permission_row:
        if permission_row.get("license_status") != "documented_limited_permission":
            error("input 036 must retain its documented limited permission status")
        if permission_row.get("redistribution_status") != "permitted_for_repository_test_only":
            error("input 036 permission must remain limited to repository test use")
        if permission_row.get("license_reference") != "input/math-reference/PERMISSIONS.md":
            error("input 036 must link its permission record at input/math-reference/PERMISSIONS.md")
        if not permission_path.is_file():
            error("input 036 permission record is missing")
        else:
            permission_text = permission_path.read_text(encoding="utf-8")
            input_file = repo_file(permission_row.get("input_path", ""), prefix="input")
            actual_hash = hashlib.sha256(input_file.read_bytes()).hexdigest() if input_file and input_file.is_file() else ""
            if "036" not in permission_text or not actual_hash or actual_hash not in permission_text:
                error("input 036 permission record must identify the fixture and match its SHA-256")


def validate_migration_manifest() -> int:
    path = ROOT / "references/migration-manifest.csv"
    expected_fields = ["source_revision", "legacy_path", "reference_path", "sha256", "annotation_revision"]
    fields, rows = load_csv(path)
    if fields != expected_fields:
        error(f"{path.relative_to(ROOT)}: expected columns {expected_fields}, got {fields}")
    found: set[tuple[str, str]] = set()
    for line_number, row in enumerate(rows, start=2):
        pair = (row.get("legacy_path", ""), row.get("reference_path", ""))
        if pair in found:
            error(f"{path.relative_to(ROOT)}:{line_number}: duplicate path pair {pair}")
        found.add(pair)
        if row.get("source_revision") != LEGACY_SOURCE_REVISION:
            error(f"{path.relative_to(ROOT)}:{line_number}: source_revision must be {LEGACY_SOURCE_REVISION}")
        if row.get("annotation_revision") != "1":
            error(f"{path.relative_to(ROOT)}:{line_number}: annotation_revision must be 1 for migrated references")
        legacy = repo_file(row.get("legacy_path", ""), prefix="input")
        reference = repo_file(row.get("reference_path", ""), prefix="references")
        if legacy is None or reference is None or not legacy.is_file() or not reference.is_file():
            error(f"{path.relative_to(ROOT)}:{line_number}: legacy/reference compatibility file missing")
            continue
        legacy_hash = hashlib.sha256(legacy.read_bytes()).hexdigest()
        reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
        if not (row.get("sha256") == reference_hash == legacy_hash == LEGACY_REFERENCE_BLOBS.get(pair)):
            error(f"{path.relative_to(ROOT)}:{line_number}: compatibility copy hash mismatch with source blob")
    if differences := found ^ LEGACY_REFERENCE_BLOBS.keys():
        error(f"{path.relative_to(ROOT)}: path pairs differ from expected migration set: {differences}")
    return len(rows)


def validate_compatibility_layout() -> None:
    output_extensions = {"epub": "epub", "html": "html", "mp3": "mp3", "pdf": "pdf", "pdf_ua": "pdf", "txt": "txt"}
    for format_name in output_extensions:
        relative = f"outputs/{format_name}/.gitkeep"
        if not (ROOT / relative).is_file():
            error(f"compatibility layout is missing {relative}")

    manifest = "outputs/manifest.csv"
    fields, rows = load_csv(ROOT / manifest)
    if fields != ["input_id", "format", "file_path", "byte_size", "generator_version", "status"]:
        error(f"{manifest}: columns differ from the legacy output inventory")
    else:
        # The transition keeps all legacy placeholders, with their status empty.
        expected = Counter(
            (input_id, format_name, f"outputs/{format_name}/{input_id}.{extension}", "", "", "")
            for input_id in (f"{number:03d}" for number in range(1, 9))
            for format_name, extension in output_extensions.items()
        )
        actual = Counter(tuple(row[field] for field in fields) for row in rows)
        if actual != expected:
            error(f"{manifest}: legacy output inventory differs "
                  f"({sum((expected - actual).values())} missing, "
                  f"{sum((actual - expected).values())} unexpected rows)")

    manifest = "intermediate/manifest.csv"
    fields, rows = load_csv(ROOT / manifest)
    required_fields = {"input_id", "intermediate_type", "file_path", "status"}
    if missing_fields := required_fields - set(fields):
        error(f"{manifest}: missing columns {sorted(missing_fields)}")
        return

    # Preserve the completed snapshots from the legacy compatibility baseline.
    required_snapshots = {
        (input_id, kind, f"intermediate/{kind}/{input_id}.json")
        for input_id in ("001", "003", "004", "005", "007", "008")
        for kind in ("canonical-document", "processing-manifest", "pddl-plan")
    }
    for line_number, row in enumerate(rows, start=2):
        if (row.get("status") or "").strip().lower() not in {"available", "complete", "completed", "present"}:
            continue
        relative = row.get("file_path") or ""
        if not relative:
            error(f"{manifest}:{line_number}: completed artifact has no file_path")
            continue
        if not relative.startswith("intermediate/"):
            relative = (PurePosixPath("intermediate") / relative).as_posix()
        required_snapshots.discard((row["input_id"], row["intermediate_type"], relative))
        path = repo_file(relative, prefix="intermediate")
        if path is not None and not path.is_file():
            error(f"{manifest}:{line_number}: missing completed artifact {relative}")
    for _, _, relative in sorted(required_snapshots):
        error(f"{manifest}: missing completed manifest entry for {relative}")


def validate_required_references(keys: set[tuple[str, str, str, str]]) -> None:
    """Keep the migrated coverage inventory from silently shrinking."""
    required = {
        (f"{number:03d}", "formula_image_recognition", "ground_truth", "csv")
        for number in range(9, 36)
    }
    required.update(
        (f"{number:03d}", "accessible_output_reference", "expected_output", format_name)
        for number in range(1, 9)
        for _, format_name, _, _ in TASK_CONTENT_CONTRACTS["accessible_output_reference"]
    )
    required.update(
        (input_id, task, reference_type, format_name)
        for input_id, prefix in (("036", "math_"), ("006", "presentation_"))
        for task, contracts in TASK_CONTENT_CONTRACTS.items()
        if task.startswith(prefix)
        for reference_type, format_name, _, _ in contracts
    )
    for key in sorted(required - keys):
        error(f"references/manifest.csv: missing required reference row {key}")


def main() -> int:
    input_manifest = ROOT / "input/manifest.csv"
    reference_manifest = ROOT / "references/manifest.csv"
    input_fields, input_rows = load_csv(input_manifest)
    input_schema = validate_manifest_rows(
        input_manifest, ROOT / "input/manifest.schema.json", input_rows, input_fields
    )
    reference_fields, reference_rows = load_csv(reference_manifest)
    reference_schema = validate_manifest_rows(
        reference_manifest, ROOT / "references/manifest.schema.json", reference_rows, reference_fields
    )

    input_by_id = validate_input_rows(input_rows) if input_schema else {}
    selector_schema = (reference_schema or {}).get("$defs", {}).get("recordSelector", {})
    unique_reference_keys: set[tuple[str, str, str, str]] = set()
    records_cache: dict[Path, tuple[list[str], list[dict[str, str]]]] = {}
    validated_content: set[tuple[Path, Path]] = set()

    for line_number, row in enumerate(reference_rows, start=2):
        identifier = row.get("input_id", "")
        if identifier not in input_by_id:
            error(f"references/manifest.csv:{line_number}: unknown input_id {identifier!r}")
        if row.get("task") not in TASK_CONTENT_CONTRACTS:
            error(f"references/manifest.csv:{line_number}: unknown task {row.get('task')!r}")
        contract = (
            row.get("reference_type", ""),
            row.get("format", ""),
            row.get("file_path", ""),
            row.get("content_schema", ""),
        )
        expected_contracts = TASK_CONTENT_CONTRACTS.get(row.get("task", ""))
        if expected_contracts is not None and contract not in expected_contracts:
            error(
                f"references/manifest.csv:{line_number}: task/type/format/file/content_schema "
                f"combination is not supported for {row.get('task')!r}: {contract}"
            )
        key = (identifier, row.get("task", ""), row.get("reference_type", ""), row.get("format", ""))
        if key in unique_reference_keys:
            error(f"references/manifest.csv:{line_number}: duplicate reference key {key}")
        unique_reference_keys.add(key)

        try:
            annotated = int(row.get("annotated_count", "0"))
            eligible = int(row["eligible_count"]) if row.get("eligible_count") else None
        except (KeyError, ValueError):
            continue
        if eligible is not None and eligible < annotated:
            error(f"references/manifest.csv:{line_number}: eligible_count is smaller than annotated_count")
        if row.get("availability") == "complete" and eligible != annotated:
            error(f"references/manifest.csv:{line_number}: complete scope needs eligible_count = annotated_count")

        if row.get("availability") == "unannotated":
            continue
        path = repo_file(row.get("file_path", ""), prefix="references")
        if path is None:
            continue
        if not path.is_file():
            error(f"references/manifest.csv:{line_number}: missing reference file {row.get('file_path')}")
            continue
        expected_schema = CONTENT_SCHEMA_BY_FILE.get(row.get("file_path", ""))
        if expected_schema is None:
            error(f"references/manifest.csv:{line_number}: no content schema is registered for {row.get('file_path')!r}")
            continue
        schema_relative = row.get("content_schema", "")
        if schema_relative != expected_schema:
            error(
                f"references/manifest.csv:{line_number}: {row.get('file_path')!r} "
                f"must use content schema {expected_schema!r}"
            )
            continue
        content_schema_path = repo_file(schema_relative, prefix="references")
        if content_schema_path is None:
            continue
        if not content_schema_path.is_file():
            error(f"references/manifest.csv:{line_number}: missing content schema {schema_relative!r}")
            continue
        content_key = (path, content_schema_path)
        if content_key not in validated_content:
            validate_content_schema(path, content_schema_path)
            validated_content.add(content_key)
        selector = parse_selector(row.get("record_selector", ""), line_number, selector_schema)
        if selector is None:
            continue
        if expected_contracts is not None and contract in expected_contracts:
            if not validate_task_selector(row["task"], row["format"], selector, line_number):
                continue
        count = selector_count(path, selector, identifier, line_number)
        if count is not None and count != annotated:
            error(
                f"references/manifest.csv:{line_number}: selector resolves to {count} units, "
                f"but annotated_count is {annotated}"
            )
        validate_reference_records(path, records_cache, input_by_id)

    validate_required_references(unique_reference_keys)
    validate_special_fixtures(input_by_id, reference_rows, records_cache)
    migration_count = validate_migration_manifest()
    validate_compatibility_layout()

    if ERRORS:
        print(f"Dataset validation failed with {len(ERRORS)} error(s):", file=sys.stderr)
        for issue in ERRORS:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    available = sum(row.get("availability") != "unannotated" for row in reference_rows)
    empty = len(reference_rows) - available
    print(
        f"Dataset validation passed: {len(input_rows)} inputs, {len(reference_rows)} reference rows "
        f"({available} annotated, {empty} unannotated); {migration_count} compatibility copies hash-verified."
    )
    print("Legacy outputs and intermediate snapshots are present for the compatibility phase.")
    for warning in sorted(WARNINGS):
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
