#!/usr/bin/env python3
"""Read-only cross-discipline evidence gate. Exit codes: 0 READY, 1 BLOCKED, 2 INVALID."""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

PHASES = ("design", "prototype", "bench", "qualified")
POLICIES = {
    "mechanical": {
        "design": {"cad-integrity": "inspection", "interface-review": "review",
                   "tolerance-review": "review", "load-review": "analysis"},
        "prototype": {"manufacturing-review": "review", "independent-review": "independent"},
        "bench": {"as-built-inspection": "measurement", "dimensional-measurement": "measurement"},
        "qualified": {"functional-measurement": "measurement"},
    },
    "simulation": {
        "design": {"model-provenance": "review", "analytical-baseline": "calculation"},
        "prototype": {"convergence": "simulation", "corner-cases": "simulation",
                      "result-assessment": "simulation", "independent-review": "independent"},
    },
}
KINDS = {"review", "inspection", "calculation", "simulation", "measurement"}
OPS = {"eq", "lt", "lte", "gt", "gte"}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(root, value):
    require(isinstance(value, str) and bool(value.strip()), 'Expected a nonempty relative path')
    path = (root / value).resolve()
    require(not Path(value).is_absolute() and path.is_relative_to(root), 'Paths must stay within project_root')
    return path


def read(path):
    obj = json.loads(path.read_text())
    require(isinstance(obj, dict), f'Expected JSON object: {path}')
    return obj


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())



def digest(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"),
                                      allow_nan=False).encode()).hexdigest()


def required_checks(domains, stage):
    checks = {}
    for domain in domains:
        if domain == "electrical":
            continue
        for phase in PHASES[:PHASES.index(stage) + 1]:
            for name, kind in POLICIES[domain].get(phase, {}).items():
                checks[f"{domain}.{name}"] = kind
    if len(domains) > 1 and stage != "design":
        checks["integration.interface-review"] = "independent"
    return checks


def test_metrics(rules, metrics):
    require(isinstance(rules, list) and isinstance(metrics, dict), "Invalid criteria/metrics")
    findings = []
    for rule in rules:
        require(isinstance(rule, dict), "Invalid criterion")
        name, op, expected = rule.get("metric"), rule.get("op"), rule.get("value")
        require(nonempty(name) and op in OPS and type(expected) in (bool, int, float),
                "Criterion requires metric, operator, numeric/boolean value")
        require(type(expected) is not float or math.isfinite(expected), "Nonfinite threshold")
        unit = rule.get("unit")
        require(unit is None or nonempty(unit), "Invalid unit")
        actual = metrics.get(name)
        if not isinstance(actual, dict) or "value" not in actual:
            findings.append(f"Missing metric {name}")
            continue
        value = actual["value"]
        if (type(value) is bool) != (type(expected) is bool) or type(value) not in (bool, int, float):
            findings.append(f"Wrong metric type: {name}")
            continue
        if type(value) is float and not math.isfinite(value):
            findings.append(f"Nonfinite metric: {name}")
            continue
        if actual.get("unit") != unit:
            findings.append(f"Wrong unit: {name}")
            continue
        matched = {"eq": value == expected, "lt": value < expected, "lte": value <= expected,
                   "gt": value > expected, "gte": value >= expected}[op]
        if not matched:
            findings.append(f"Acceptance failed: {name}: {value} {op} {expected} {unit or ''}")
    return findings


def validate_dependencies(definitions):
    require(isinstance(definitions, dict), "check_definitions must be an object")
    for key, value in definitions.items():
        require(isinstance(value, dict), f"Invalid check definition: {key}")
        deps = value.get("depends_on", [])
        require(isinstance(deps, list) and all(isinstance(x, str) for x in deps)
                and len(deps) == len(set(deps)), f"Invalid dependencies: {key}")
        require(all(x != key and x in definitions for x in deps), f"Unknown/self dependency: {key}")
    visiting, done = set(), set()

    def visit(name):
        if name in done:
            return
        require(name not in visiting, f"Dependency cycle: {name}")
        visiting.add(name)
        for dep in definitions[name].get("depends_on", []):
            visit(dep)
        visiting.remove(name)
        done.add(name)
    for name in definitions:
        visit(name)


def assess(config_path, stage):
    require(stage in PHASES, "Unknown stage")
    config_path = Path(config_path).resolve()
    cfg = read(config_path)
    require(cfg.get("schema_version") == 1, "Unsupported schema_version")
    for field in ("project", "revision", "author", "project_root", "evidence_file"):
        require(nonempty(cfg.get(field)), f"Missing {field}")
    root = (config_path.parent / cfg["project_root"]).resolve()
    require(root.is_dir(), "project_root not found")
    domains = cfg.get("domains")
    require(isinstance(domains, list) and bool(domains)
            and all(isinstance(x, str) for x in domains)
            and len(domains) == len(set(domains)), "domains must be a unique nonempty list")
    require(all(x in (*POLICIES, "electrical") for x in domains), "Unknown domain")
    inputs = cfg.get("design_inputs")
    require(isinstance(inputs, list) and bool(inputs)
            and all(isinstance(x, str) for x in inputs)
            and len(inputs) == len(set(inputs)), "design_inputs must be unique and nonempty")
    hashes, blockers = {}, []
    for name in inputs:
        path = local(root, name)
        if path.is_file():
            hashes[name] = sha(path)
        else:
            blockers.append(f"Missing design input: {name}")
    definitions = cfg.get("check_definitions", {})
    validate_dependencies(definitions)
    evidence_path = local(root, cfg["evidence_file"])
    evidence = read(evidence_path) if evidence_path.is_file() else None
    if evidence is None and any(d != "electrical" for d in domains):
        blockers.append("Missing evidence file")
    if evidence is not None:
        require(evidence.get("schema_version") == 1 and isinstance(evidence.get("checks"), dict),
                "Invalid evidence schema")
        require(evidence.get("project") == cfg["project"] and evidence.get("revision") == cfg["revision"],
                "Evidence identity/revision mismatch")
    records = evidence["checks"] if evidence else {}
    required = required_checks(domains, stage)
    results = []
    for check, category in required.items():
        problems = []
        record = records.get(check)
        definition = definitions.get(check, {})
        if not isinstance(record, dict):
            problems.append("Missing required evidence")
        else:
            require(record.get("status") in ("passed", "failed", "blocked", "skipped"),
                    f"Unknown evidence status: {check}")
            if record["status"] != "passed":
                problems.append(f"{record['status']}: {record.get('summary', 'No summary')}")
            else:
                kind = record.get("kind")
                require(kind in KINDS, f"Unknown kind for {check}")
                allowed = ({"review", "calculation", "simulation"} if category == "analysis" else
                           {"review"} if category == "independent" else {category})
                if kind not in allowed:
                    problems.append(f"Wrong evidence kind: expected {category}, got {kind}")
                for field in ("acceptance", "summary", "performed_by", "performed_at"):
                    if not nonempty(record.get(field)):
                        problems.append(f"Missing {field}")
                if nonempty(record.get("performed_at")):
                    try:
                        timestamp = datetime.fromisoformat(record["performed_at"].replace("Z", "+00:00"))
                        require(timestamp.tzinfo is not None, "Evidence timestamps require timezone")
                        if timestamp > datetime.now(timezone.utc) + timedelta(minutes=5):
                            problems.append("Future evidence timestamp")
                    except ValueError:
                        problems.append("Invalid evidence timestamp")
                if record.get("design_inputs_sha256") != hashes or len(hashes) != len(inputs):
                    problems.append("Missing or stale design input hashes")
                artifacts = record.get("artifacts")
                require(isinstance(artifacts, list), f"Invalid artifacts for {check}")
                if not artifacts:
                    problems.append("Supporting artifacts missing")
                for item in artifacts:
                    require(isinstance(item, dict) and nonempty(item.get("sha256")), "Invalid artifact")
                    target = local(root, item.get("path"))
                    if not target.is_file() or sha(target) != item["sha256"]:
                        problems.append(f"Missing/stale artifact: {item['path']}")
                if category == "independent":
                    if (record.get("independent") is not True or not nonempty(record.get("reviewer"))
                            or record.get("reviewer") in (cfg["author"], None)
                            or record.get("reviewer") != record.get("performed_by")):
                        problems.append("Missing independent reviewer declaration or identity")
                if kind == "measurement":
                    for field in ("specimen_id", "conditions", "instruments"):
                        if not nonempty(record.get(field)):
                            problems.append(f"Missing measurement metadata: {field}")
                if kind == "simulation":
                    solver = record.get("solver")
                    if (not isinstance(solver, dict)
                            or not all(nonempty(solver.get(k)) for k in ("name", "version"))
                            or not nonempty(record.get("model_limits"))):
                        problems.append("Solver/version and model limits required")
                    if record.get("converged") is not True:
                        problems.append("Convergence not established")
                rules = definition.get("criteria", [])
                require(isinstance(rules, list), f"Invalid criteria: {check}")
                rules = list(rules)
                if check == "mechanical.cad-integrity":
                    rules += [{"metric": "valid_geometry", "op": "eq", "value": True},
                              {"metric": "recompute_ok", "op": "eq", "value": True}]
                if check == "simulation.corner-cases":
                    rules += [{"metric": "cases_run", "op": "gte", "value": 2}]
                if check in ("simulation.result-assessment", "mechanical.functional-measurement") and not definition.get("criteria"):
                    problems.append("Project-specific numerical acceptance criteria required")
                problems += test_metrics(rules, record.get("metrics", {}))
                for dep in definition.get("depends_on", []):
                    if dep not in required:
                        problems.append(f"Dependency not evaluated: {dep}")
                    if (not isinstance(record.get("upstream_sha256"), dict)
                            or record["upstream_sha256"].get(dep) !=
                            (digest(records[dep]) if isinstance(records.get(dep), dict) else None)):
                        problems.append(f"Stale/missing upstream evidence fingerprint: {dep}")
        results.append({"id": check, "status": "BLOCKED" if problems else "PASS", "findings": problems})
    # Transitively block downstream checks even if the upstream check is listed later.
    status_map = {r["id"]: r["status"] for r in results}
    for _ in results:
        updated = False
        for result in results:
            if result["status"] == "BLOCKED":
                continue
            for dep in definitions.get(result["id"], {}).get("depends_on", []):
                if status_map.get(dep) != "PASS":
                    result["findings"].append(f"Dependency blocked: {dep}")
                    result["status"] = "BLOCKED"
                    status_map[result["id"]] = "BLOCKED"
                    updated = True
                    break
        if not updated:
            break
    electrical = None
    if "electrical" in domains:
        if stage == "design":
            blockers.append("Electrical adapter has no design gate; prototype or later required")
        else:
            config = cfg.get("electrical_config")
            require(nonempty(config), "electrical_config is required")
            target = local(root, config)
            if not target.is_file():
                blockers.append("Missing electrical release config")
            else:
                checker = Path(__file__).resolve().parents[2] / "electronics-development/scripts/check_release.py"
                require(checker.is_file(), "Original electronics release checker missing")
                try:
                    run = subprocess.run([sys.executable, str(checker), str(target),
                                          "--stage", stage], capture_output=True,
                                         text=True, timeout=30, check=False)
                    electrical = json.loads(run.stdout)
                    require(isinstance(electrical, dict), "Invalid electrical checker response")
                    if run.returncode or electrical.get("status") != "READY":
                        blockers.append(f"Electrical release: {electrical.get('status', 'INVALID')}")
                except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
                    blockers.append(f"Electrical checker unavailable/invalid: {exc}")
    ready = not blockers and all(r["status"] == "PASS" for r in results)
    return {"schema_version": 1, "project": cfg["project"], "revision": cfg["revision"],
            "stage": stage, "status": "READY" if ready else "BLOCKED",
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "config_sha256": sha(config_path),
            "evidence_sha256": sha(evidence_path) if evidence else None,
            "design_inputs_sha256": hashes, "blockers": blockers, "checks": results,
            "electrical": electrical,
            "scope": "Evidence and numerical-criterion checks only; not proof of physics, certification, or permission to manufacture."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--stage", choices=PHASES, required=True)
    parser.add_argument("--output", type=Path, help="Write a NEW .json report only")
    args = parser.parse_args()
    try:
        result = assess(args.config, args.stage)
        code = 0 if result["status"] == "READY" else 1
        if args.output:
            out = args.output.absolute()
            require(out.suffix.lower() == ".json" and not out.exists() and not out.is_symlink(),
                    "Report must be a new .json file")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (ValueError, TypeError, KeyError, OverflowError, AttributeError, RecursionError) as exc:
        result, code = {"schema_version": 1, "status": "INVALID", "error": str(exc)}, 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
