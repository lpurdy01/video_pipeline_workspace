import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import io
from datetime import date
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("assurance_compiler", Path(__file__).parents[1] / "compile.py")
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)
TODAY = date(2026, 9, 8)


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("out/sources/original.txt", "Original source context, including its limits.")
        self.write("out/sources/context.txt", "Original source context, including its limits.")
        self.source = {"id": "S-TEST-001", "title": "Test source", "url": "https://example.org/source",
                       "source_type": "research_paper", "jurisdiction": "example", "accessed_at": "2026-09-08",
                       "inspection_scope": "test", "limitations": "test", "independence_group": "test",
                       "refresh_days": 30, "regions": [{"id": "S-TEST-001-R1", "locator": "p1",
                       "excerpt": "Original source context", "context_status": "full_context",
                       "snapshot_path": "out/sources/original.txt",
                       "snapshot_sha256": compiler.file_hash(self.root / "out/sources/original.txt"),
                       "context_path": "out/sources/context.txt"}]}
        self.claim = {"id": "C-TEST-001", "text": "Test scoped claim", "kind": "fact", "status": "provisional",
                      "scope": "example", "challenge": "Test limits", "evidence": [
                      {"region_id": "S-TEST-001-R1", "relation": "supports"}]}
        self.save("research/sources.json", {"schema_version": 1, "sources": [self.source]})
        self.save("verification/claims.json", {"schema_version": 1, "claims": [self.claim]})
        self.artifacts = [{"id": "A-TEST", "path": "paper.md", "kind": "paper", "depends_on": []}]
        self.save("verification/artifacts.json", {"schema_version": 1, "artifacts": self.artifacts})
        self.write("paper.md", "Scoped claim in context. [C-TEST-001]")

    def write(self, path, text):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)

    def save(self, path, value):
        self.write(path, json.dumps(value))

    def build(self, **kwargs):
        return compiler.compile_project(self.root, today=TODAY, **kwargs)

    def set_assurance_case(self):
        self.artifacts[0]["claim_ids"] = ["C-TEST-001"]
        self.save("verification/artifacts.json", {"schema_version": 1, "artifacts": self.artifacts})
        self.case = {
            "schema_version": 1,
            "system_releases": [{"id": "REL-TEST-001", "label": "Frozen fixture release",
                                 "release_version": "r0", "learning_mode": "frozen_trained",
                                 "release_status": "released"}],
            "assumptions": [{"id": "AS-TEST-001", "text": "Fixture assumption",
                             "status": "supported", "release_ids": ["REL-TEST-001"]}],
            "hazards": [{"id": "H-TEST-001", "title": "Fixture hazard",
                         "release_id": "REL-TEST-001", "assumption_ids": ["AS-TEST-001"],
                         "obligation_ids": ["O-TEST-001"]}],
            "evidence_artifacts": [{"id": "EA-TEST-001", "title": "Fixture evidence",
                                    "kind": "test", "status": "verified", "release_id": "REL-TEST-001",
                                    "claim_ids": ["C-TEST-001"]}],
            "obligations": [{"id": "O-TEST-001", "title": "Fixture obligation",
                             "description": "Fixture obligation description", "status": "closed",
                             "hazard_ids": ["H-TEST-001"], "assumption_ids": ["AS-TEST-001"],
                             "evidence_artifact_ids": ["EA-TEST-001"], "claim_ids": ["C-TEST-001"]}]
        }
        self.save("assurance/assurance_case.json", self.case)

    def set_method_crosswalk(self):
        self.set_assurance_case()
        self.crosswalk = {
            "schema_version": 1,
            "methods": [{
                "id": "M-TEST-001", "title": "Fixture method", "status": "guidance",
                "scope": "Fixture scope", "claim_ids": ["C-TEST-001"],
                "mappings": [{"obligation_id": "O-TEST-001", "coverage": "partial",
                              "note": "Fixture mapping", "claim_ids": ["C-TEST-001"]}]
            }]
        }
        self.save("assurance/method_crosswalk.json", self.crosswalk)

    def record(self, task, verdict="pass", name=None, resolves=None):
        packet = next(p for p in self.build()["packages"] if p["task"] == task)
        record = {"id": name or "R-" + task, "package_id": packet["id"], "input_digest": packet["input_digest"],
                  "task": task, "reviewer_id": "fixture-reviewer", "reviewer_kind": "human", "verdict": verdict,
                  "created_at": "2026-09-08", "rationale": "Fixture rationale", "evidence_locators": ["p1"],
                  "limitations": [], "resolves": resolves or []}
        self.save("verification/reviews/" + record["id"] + ".json", record)
        return record

    def test_missing_reviews_are_not_green(self):
        result = self.build()
        self.assertEqual(result["counts"]["planned_reviews"], 4)
        self.assertEqual(len(result["blockers"]), 4)

    def test_current_context_and_four_reviews_can_satisfy_composition_gates(self):
        for task in compiler.TASKS:
            self.record(task)
        self.assertEqual(self.build()["blockers"], [])

    def test_duplicate_contribution_fails(self):
        self.save("research/contributions/collision/sources.json", {"schema_version": 1, "sources": [self.source]})
        with self.assertRaisesRegex(ValueError, "Duplicate ID"):
            self.build()

    def test_unknown_claim_and_dependency_cycle_fail(self):
        self.write("paper.md", "[C-MISSING]")
        with self.assertRaisesRegex(ValueError, "Unknown claim"):
            self.build()
        self.write("paper.md", "[C-TEST-001]")
        self.artifacts[0]["depends_on"] = ["A-TEST"]
        self.save("verification/artifacts.json", {"schema_version": 1, "artifacts": self.artifacts})
        with self.assertRaisesRegex(ValueError, "cycle"):
            self.build()

    def test_source_hash_mismatch_fails(self):
        self.write("out/sources/original.txt", "Changed source")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.build()

    def test_missing_original_context_blocks(self):
        self.source["regions"][0]["context_status"] = "short_excerpt_only"
        self.save("research/sources.json", {"schema_version": 1, "sources": [self.source]})
        self.assertTrue(any("context missing" in b for b in self.build()["blockers"]))

    def test_assurance_case_nodes_are_linked_to_claim_reviews(self):
        self.set_assurance_case()
        result = self.build()
        self.assertEqual(result["counts"]["system_releases"], 1)
        self.assertEqual(result["counts"]["obligations"], 1)
        package = next(p for p in result["packages"] if p["id"] == "P-C-TEST-001-source_support")
        self.assertEqual(package["assurance_case_links"], [
            {"node_id": "EA-TEST-001", "role": "evidence_artifact"},
            {"node_id": "O-TEST-001", "role": "obligation"},
        ])
        for task in compiler.TASKS:
            self.record(task)
        self.assertEqual(self.build()["assurance_case_blockers"], [])

    def test_risk_context_preserves_metric_limits_and_invalidates_reviews(self):
        self.set_assurance_case()
        self.case["risk_contexts"] = [{
            "id": "RC-TEST-001", "title": "Fixture risk context",
            "release_id": "REL-TEST-001", "hazard_id": "H-TEST-001", "status": "supported",
            "assumption_ids": ["AS-TEST-001"], "evidence_artifact_ids": ["EA-TEST-001"],
            "claim_ids": ["C-TEST-001"], "risk_statement": "A bounded fixture risk statement.",
            "metric_limit": "A fixture metric is not a safety score."
        }]
        self.save("assurance/assurance_case.json", self.case)
        package = next(p for p in self.build()["packages"] if p["id"] == "P-C-TEST-001-source_support")
        self.assertIn({"node_id": "RC-TEST-001", "role": "risk_context"}, package["assurance_case_links"])
        for task in compiler.TASKS:
            self.record(task)
        before = self.build()["snapshot"]
        self.case["risk_contexts"][0]["metric_limit"] = "Changed bounded metric limit."
        self.save("assurance/assurance_case.json", self.case)
        after = self.build(baseline=before)
        self.assertIn("RC-TEST-001", after["changes"]["changed"])
        self.assertIn("R-source_support", after["stale_review_ids"])

    def test_assurance_case_rejects_unknown_reference_and_invalidates_reviews(self):
        self.set_assurance_case()
        self.case["hazards"][0]["release_id"] = "REL-MISSING"
        self.save("assurance/assurance_case.json", self.case)
        with self.assertRaisesRegex(ValueError, "Unknown release"):
            self.build()

        self.set_assurance_case()
        for task in compiler.TASKS:
            self.record(task)
        before = self.build()["snapshot"]
        self.case["obligations"][0]["title"] = "Changed fixture obligation"
        self.save("assurance/assurance_case.json", self.case)
        after = self.build(baseline=before)
        self.assertIn("R-source_support", after["stale_review_ids"])
        self.assertIn("O-TEST-001", after["changes"]["changed"])
        self.assertIn("P-C-TEST-001-source_support", after["changes"]["affected"])

    def test_method_crosswalk_is_validated_and_invalidates_linked_reviews(self):
        self.set_method_crosswalk()
        package = next(p for p in self.build()["packages"] if p["id"] == "P-C-TEST-001-source_support")
        self.assertEqual(package["method_crosswalk_links"], [
            {"node_id": "M-TEST-001", "role": "external_method"},
            {"node_id": "MAP-TEST-001-TEST-001", "role": "method_mapping"},
        ])
        for task in compiler.TASKS:
            self.record(task)
        before = self.build()["snapshot"]
        self.crosswalk["methods"][0]["mappings"][0]["note"] = "Changed fixture mapping"
        self.save("assurance/method_crosswalk.json", self.crosswalk)
        after = self.build(baseline=before)
        self.assertIn("R-source_support", after["stale_review_ids"])
        self.assertIn("MAP-TEST-001-TEST-001", after["changes"]["changed"])

        self.crosswalk["methods"][0]["mappings"][0]["obligation_id"] = "O-MISSING"
        self.save("assurance/method_crosswalk.json", self.crosswalk)
        with self.assertRaisesRegex(ValueError, "Unknown obligation"):
            self.build()

    def test_dependency_change_invalidates_review_and_propagates(self):
        self.write("dependency.md", "Original independent background")
        self.artifacts[0]["depends_on"] = ["A-DEP"]
        self.artifacts.append({"id": "A-DEP", "path": "dependency.md", "kind": "background", "depends_on": []})
        self.save("verification/artifacts.json", {"schema_version": 1, "artifacts": self.artifacts})
        old_record = self.record("cross_artifact")
        before = self.build()["snapshot"]
        self.write("dependency.md", "Changed independent background")
        after = self.build(baseline=before)
        self.assertIn(old_record["id"], after["stale_review_ids"])
        self.assertIn("A-TEST", after["changes"]["affected"])
        self.assertIn("P-C-TEST-001-cross_artifact", after["changes"]["affected"])

    def test_historical_failure_survives_revision_until_human_resolution(self):
        self.record("challenge", "fail", "R-objection")
        self.write("paper.md", "Revised scoped claim. [C-TEST-001]")
        self.assertTrue(any("unresolved fail" in b for b in self.build()["blockers"]))
        for task in compiler.TASKS[:-1]:
            self.record(task, name="R-new-" + task)
        self.record("human_disposition", resolves=["R-objection"])
        self.assertEqual(self.build()["blockers"], [])

    def test_human_review_invalidates_when_other_review_results_change(self):
        for task in compiler.TASKS:
            self.record(task)
        self.record("challenge", name="R-another-review")
        self.assertIn("R-human_disposition", self.build()["stale_review_ids"])

    def test_empty_project_and_untagged_content_cannot_pass(self):
        self.write("paper.md", "An untagged factual statement.")
        self.assertTrue(any("no explicit claim tags" in b for b in self.build()["blockers"]))
        self.save("verification/claims.json", {"schema_version": 1, "claims": []})
        with self.assertRaisesRegex(ValueError, "nonempty"):
            self.build()

    def test_input_mutation_is_detected(self):
        original = compiler.read_json
        def mutate(path, tracked=None):
            value = original(path, tracked)
            if path.name == "sources.json":
                path.write_text(path.read_text() + " ")
            return value
        with patch.object(compiler, "read_json", mutate):
            with self.assertRaisesRegex(ValueError, "Input changed"):
                self.build()

    def test_model_cannot_sign_human_disposition(self):
        record = self.record("human_disposition")
        record["reviewer_kind"] = "model"
        with self.assertRaisesRegex(ValueError, "requires a human"):
            compiler.check_review(record)

    def test_path_escape_fails(self):
        self.artifacts[0]["path"] = "../outside.md"
        self.save("verification/artifacts.json", {"schema_version": 1, "artifacts": self.artifacts})
        with self.assertRaisesRegex(ValueError, "escapes project"):
            self.build()

    def test_invalid_import_does_not_poison_review_store(self):
        record = self.record("human_disposition")
        (self.root / "verification/reviews/R-human_disposition.json").unlink()
        record["resolves"] = ["R-NONEXISTENT"]
        incoming = self.root / "incoming.json"
        incoming.write_text(json.dumps(record))
        with patch.object(compiler.sys, "argv", ["compile.py", "--root", str(self.root), "--import-review", str(incoming)]):
            with patch.object(compiler.sys, "stderr", io.StringIO()):
                self.assertEqual(compiler.main(), 1)
        self.assertEqual(list((self.root / "verification/reviews").glob("*.json")), [])
        self.assertEqual(self.build()["counts"]["review_records"], 0)

    def test_review_cannot_resolve_another_claim_or_later_objection(self):
        objection = self.record("challenge", "fail", "R-objection")
        disposition = self.record("human_disposition", resolves=["R-objection"])
        for package, created_at, expected in (
            ("P-C-OTHER-challenge", "2026-09-08", "another claim"),
            (objection["package_id"], "2026-09-09", "predates"),
        ):
            altered = dict(objection, package_id=package, created_at=created_at)
            with self.assertRaisesRegex(ValueError, expected):
                compiler.validate_reviews({altered["id"]: altered, disposition["id"]: disposition})


if __name__ == "__main__":
    unittest.main()
