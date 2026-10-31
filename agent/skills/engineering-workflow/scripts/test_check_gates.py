#!/usr/bin/env python3
"""Deterministic gate regression tests; no solver or hardware required."""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_gates as gate


class Gates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "cad.FCStd").write_text("original CAD")
        (self.root / "support.log").write_text("actual check log")
        self.cfg_path = self.root / "gate.json"
        self.ev_path = self.root / "evidence.json"
        self.cfg = {
            "schema_version": 1, "project": "mirror-holder", "revision": "A",
            "project_root": ".", "author": "design-agent", "domains": ["mechanical"],
            "design_inputs": ["cad.FCStd"], "evidence_file": "evidence.json",
            "check_definitions": {"mechanical.functional-measurement": {"criteria": [
                {"metric": "deflection", "op": "lte", "value": 0.05, "unit": "mm"}]}}
        }
        self.records = {}

    def record(self, check, category):
        kind = {"analysis": "calculation", "independent": "review"}.get(category, category)
        is_independent = check.endswith("independent-review") or check == "integration.interface-review"
        r = {
            "status": "passed", "kind": kind, "acceptance": "Declared criterion",
            "summary": "Recorded check", "performed_by": "review-agent" if is_independent else "technician",
            "performed_at": datetime.now(timezone.utc).isoformat(),
            "design_inputs_sha256": {"cad.FCStd": gate.sha(self.root / "cad.FCStd")},
            "artifacts": [{"path": "support.log", "sha256": gate.sha(self.root / "support.log")}],
            "metrics": {},
        }
        if check == "mechanical.cad-integrity":
            r["metrics"] = {"valid_geometry": {"value": True}, "recompute_ok": {"value": True}}
        if check == "mechanical.functional-measurement":
            r["metrics"]["deflection"] = {"value": 0.04, "unit": "mm"}
        if check == "simulation.corner-cases":
            r["metrics"]["cases_run"] = {"value": 3}
        if check == "simulation.result-assessment":
            r["metrics"]["frequency"] = {"value": 560, "unit": "Hz"}
        if kind == "simulation":
            r.update(solver={"name": "CalculiX", "version": "2.22"},
                     model_limits="Rigid base assumed", converged=True)
        if kind == "measurement":
            r.update(specimen_id="part-1", conditions="20C, nominal load", instruments="calibrated caliper")
        if is_independent:
            r.update(reviewer="review-agent", independent=True)
        return r

    def populate(self, stage="prototype"):
        for check, category in gate.required_checks(self.cfg["domains"], stage).items():
            self.records[check] = self.record(check, category)
        if "simulation" in self.cfg["domains"]:
            self.cfg["check_definitions"]["simulation.result-assessment"] = {
                "criteria": [{"metric": "frequency", "op": "gte", "value": 500, "unit": "Hz"}]}
        self.save()

    def save(self):
        self.cfg_path.write_text(json.dumps(self.cfg))
        self.ev_path.write_text(json.dumps({
            "schema_version": 1, "project": self.cfg["project"],
            "revision": self.cfg["revision"], "checks": self.records}))

    def check(self, stage="prototype"):
        return gate.assess(self.cfg_path, stage)

    def test_missing_checks_fail_closed(self):
        self.save()
        result = self.check()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any(r["findings"] for r in result["checks"]))

    def test_mechanical_prototype_pass(self):
        self.populate()
        self.assertEqual(self.check()["status"], "READY")

    def test_invalid_geometry_blocks(self):
        self.populate()
        self.records["mechanical.cad-integrity"]["metrics"]["valid_geometry"]["value"] = False
        self.save()
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_changed_design_stales_all_checks(self):
        self.populate()
        (self.root / "cad.FCStd").write_text("changed CAD")
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_modified_report_blocks(self):
        self.populate()
        (self.root / "support.log").write_text("changed log")
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_self_review_cannot_pass_independent_gate(self):
        self.populate()
        self.records["mechanical.independent-review"]["reviewer"] = "design-agent"
        self.save()
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_bench_requires_physical_evidence(self):
        self.populate("bench")
        self.records["mechanical.dimensional-measurement"]["kind"] = "simulation"
        self.save()
        self.assertEqual(self.check("bench")["status"], "BLOCKED")

    def test_qualified_numeric_threshold(self):
        self.populate("qualified")
        self.assertEqual(self.check("qualified")["status"], "READY")
        self.records["mechanical.functional-measurement"]["metrics"]["deflection"]["value"] = 0.08
        self.save()
        self.assertEqual(self.check("qualified")["status"], "BLOCKED")

    def test_solver_and_corner_criteria(self):
        self.cfg["domains"] = ["simulation"]
        self.populate()
        self.assertEqual(self.check()["status"], "READY")
        self.records["simulation.corner-cases"]["metrics"]["cases_run"]["value"] = 1
        self.save()
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_cross_domain_evidence_fingerprint(self):
        self.cfg["domains"] = ["mechanical", "simulation"]
        self.cfg["check_definitions"]["mechanical.manufacturing-review"] = {
            "depends_on": ["simulation.result-assessment"]}
        self.populate()
        self.records["mechanical.manufacturing-review"]["upstream_sha256"] = {
            "simulation.result-assessment": gate.digest(self.records["simulation.result-assessment"])}
        self.save()
        self.assertEqual(self.check()["status"], "READY")
        self.records["simulation.result-assessment"]["summary"] = "new result"
        self.save()
        self.assertEqual(self.check()["status"], "BLOCKED")

    def test_path_escape_rejected(self):
        self.populate()
        self.cfg["design_inputs"] = ["../escape"]
        self.save()
        with self.assertRaises(ValueError):
            self.check()

    def test_dependency_cycle_rejected(self):
        self.populate()
        self.cfg["check_definitions"]["mechanical.cad-integrity"] = {
            "depends_on": ["mechanical.interface-review"]}
        self.cfg["check_definitions"]["mechanical.interface-review"] = {
            "depends_on": ["mechanical.cad-integrity"]}
        self.save()
        with self.assertRaises(ValueError):
            self.check()

    def test_electrical_requires_existing_config(self):
        self.cfg["domains"] = ["electrical"]
        self.save()
        with self.assertRaises(ValueError):
            self.check()

    def test_future_timestamp_blocks(self):
        self.populate()
        self.records["mechanical.interface-review"]["performed_at"] = "2099-01-01T00:00:00+00:00"
        self.save()
        self.assertEqual(self.check()["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
