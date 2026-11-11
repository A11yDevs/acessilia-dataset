import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ValidateDatasetTest(unittest.TestCase):
    def test_legacy_output_inventory_and_reference_provenance_are_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = Path(__file__).resolve().parents[1]
            for name in ("input", "references", "intermediate", "outputs", "scripts"):
                shutil.copytree(source / name, root / name)

            outputs = root / "outputs/manifest.csv"
            migration = root / "references/migration-manifest.csv"
            legacy = root / "input/formula-images/ground_truth.csv"
            reference = root / "references/formula-images/ground_truth.csv"
            original = legacy.read_bytes()
            edited = b"\xef\xbb\xbf" + original
            migration_bytes = migration.read_bytes()
            with migration.open(newline="", encoding="utf-8") as stream:
                first_row = next(csv.DictReader(stream))

            scenarios = [
                ({outputs: outputs.read_bytes().splitlines(keepends=True)[0]},
                 "legacy output inventory differs (48 missing"),
                ({migration: migration_bytes.replace(first_row["source_revision"].encode(), b"a" * 40)},
                 "source_revision must be"),
                ({
                    legacy: edited,
                    reference: edited,
                    migration: migration_bytes.replace(first_row["sha256"].encode(),
                                                       hashlib.sha256(edited).hexdigest().encode()),
                }, "compatibility copy hash mismatch with source blob"),
            ]
            for changes, expected_error in scenarios:
                with self.subTest(expected_error=expected_error):
                    originals = {path: path.read_bytes() for path in changes}
                    for path, contents in changes.items():
                        path.write_bytes(contents)
                    result = subprocess.run(
                        [sys.executable, str(root / "scripts" / "validate_dataset.py")],
                        capture_output=True, text=True, check=False,
                    )
                    for path, contents in originals.items():
                        path.write_bytes(contents)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(expected_error, result.stderr)

    def test_missing_completed_intermediate_artifact_fails_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = Path(__file__).resolve().parents[1]
            for name in ("input", "references", "intermediate", "outputs", "scripts"):
                shutil.copytree(source / name, root / name)
            missing = "intermediate/processing-manifest/001.json"
            (root / missing).unlink()

            result = subprocess.run(
                [sys.executable, str(root / "scripts" / "validate_dataset.py")],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(f"missing completed artifact {missing}", result.stderr)

    def test_removing_completed_intermediate_row_and_file_fails_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = Path(__file__).resolve().parents[1]
            for name in ("input", "references", "intermediate", "outputs", "scripts"):
                shutil.copytree(source / name, root / name)

            missing = "processing-manifest/001.json"
            (root / "intermediate" / missing).unlink()
            manifest = root / "intermediate" / "manifest.csv"
            with manifest.open(newline="", encoding="utf-8") as stream:
                reader = csv.DictReader(stream)
                fields = reader.fieldnames
                rows = [row for row in reader if row["file_path"] != missing]
            with manifest.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

            result = subprocess.run(
                [sys.executable, str(root / "scripts" / "validate_dataset.py")],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(f"missing completed manifest entry for intermediate/{missing}", result.stderr)

    def test_matching_count_cannot_substitute_another_tasks_selector(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = Path(__file__).resolve().parents[1]
            for name in ("input", "references", "intermediate", "outputs", "scripts"):
                shutil.copytree(source / name, root / name)

            manifest = root / "references" / "manifest.csv"
            with manifest.open(newline="", encoding="utf-8") as stream:
                reader = csv.DictReader(stream)
                fields, rows = reader.fieldnames, list(reader)
            text = next(row for row in rows if row["task"] == "math_text_quality")
            structure = next(row for row in rows if row["task"] == "math_document_structure")
            self.assertEqual(text["annotated_count"], structure["annotated_count"])
            text["record_selector"] = structure["record_selector"]
            with manifest.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

            result = subprocess.run(
                [sys.executable, str(root / "scripts" / "validate_dataset.py")],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("selector does not match task 'math_text_quality'", result.stderr)
