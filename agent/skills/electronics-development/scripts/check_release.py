#!/usr/bin/env python3
"""Read-only evidence gate. Exit 0 ready, 1 blocked, 2 invalid configuration/records."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path

STAGES = {
    'prototype': ('operating-envelope', 'component-review', 'design-checks', 'protection-review',
                  'thermal-analysis', 'layout-review', 'manufacturing-review', 'bringup-plan'),
    'bench': ('assembly-inspection', 'unpowered-checks', 'logic-bringup', 'bench-test-setup'),
    'qualified': ('functionality', 'thermal-measurements', 'transient-measurements', 'fault-measurements'),
}
MEASURED = set(STAGES['qualified']) | {'assembly-inspection', 'unpowered-checks', 'logic-bringup'}
KINDS = {'review', 'calculation', 'simulation', 'measurement'}


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


def assess(config_path, stage):
    config_path = Path(config_path).resolve()
    config = read(config_path)
    require(config.get('schema_version') == 1, 'Unsupported config schema_version')
    require(stage in STAGES, 'Unknown release stage')
    require(nonempty(config.get('board')) and nonempty(config.get('revision')), 'Board/revision required')
    require(nonempty(config.get('project_root')), 'project_root required')
    root = (config_path.parent / config['project_root']).resolve()
    require(root.is_dir(), 'project_root does not exist')
    inputs = config.get('design_inputs')
    require(isinstance(inputs, list) and bool(inputs) and len(set(inputs)) == len(inputs), 'Nonempty unique design_inputs required')
    evidence_path = local(root, config.get('evidence_file'))
    required = []
    for name, ids in STAGES.items():
        required.extend(ids)
        if name == stage:
            break
    blockers, results = [], []
    hashes = {}
    for name in inputs:
        path = local(root, name)
        if path.is_file():
            hashes[name] = sha(path)
        else:
            blockers.append(f'Missing design input: {name}')
    evidence = read(evidence_path) if evidence_path.is_file() else None
    if evidence is None:
        blockers.append('Missing evidence file')
    else:
        require(evidence.get('schema_version') == 1 and isinstance(evidence.get('checks'), dict), 'Invalid evidence schema')
        require(evidence.get('board') == config['board'] and evidence.get('revision') == config['revision'], 'Evidence board/revision mismatch')
    for check_id in required:
        issues = []
        record = evidence['checks'].get(check_id) if evidence else None
        if record is None:
            issues.append('Missing required check')
        else:
            require(isinstance(record, dict), f'Invalid record: {check_id}')
            status = record.get('status')
            require(status in {'passed', 'failed', 'blocked', 'skipped'}, f'Invalid status: {check_id}')
            if status != 'passed':
                issues.append(f"{status}: {record.get('summary', 'No finding recorded')}")
            else:
                require(record.get('kind') in KINDS, f'Invalid evidence kind: {check_id}')
                if check_id in MEASURED and record['kind'] != 'measurement':
                    issues.append('Physical inspection/measurement required; simulation or review cannot substitute')
                for field in ['acceptance', 'summary', 'performed_by', 'performed_at']:
                    if not nonempty(record.get(field)):
                        issues.append(f'Missing {field}')
                if nonempty(record.get('performed_at')):
                    stamp = datetime.fromisoformat(record['performed_at'].replace('Z', '+00:00'))
                    require(stamp.tzinfo is not None, f'Timestamp must include timezone: {check_id}')
                    if stamp > datetime.now(timezone.utc) + timedelta(minutes=5):
                        issues.append('Evidence timestamp is in the future')
                if record.get('design_inputs_sha256') != hashes or len(hashes) != len(inputs):
                    issues.append('Stale or incomplete design input hashes')
                artifacts = record.get('artifacts')
                require(isinstance(artifacts, list), f'Artifacts must be a list: {check_id}')
                if not artifacts:
                    issues.append('No supporting artifact')
                for item in artifacts:
                    require(isinstance(item, dict) and nonempty(item.get('sha256')), f'Invalid artifact: {check_id}')
                    path = local(root, item.get('path'))
                    if not path.is_file() or sha(path) != item['sha256']:
                        issues.append(f"Missing or changed artifact: {item['path']}")
                if record.get('kind') == 'measurement':
                    for field in ['board_serial', 'conditions', 'instruments']:
                        if not nonempty(record.get(field)):
                            issues.append(f'Missing measurement metadata: {field}')
        results.append({'id': check_id, 'status': 'blocked' if issues else 'passed', 'findings': issues})
    return {'schema_version': 1, 'policy_version': 1, 'board': config['board'], 'revision': config['revision'],
            'stage': stage, 'status': 'BLOCKED' if blockers or any(r['findings'] for r in results) else 'READY',
            'checked_at': datetime.now(timezone.utc).isoformat(), 'config_sha256': sha(config_path),
            'evidence_sha256': sha(evidence_path) if evidence else None, 'design_inputs_sha256': hashes,
            'blockers': blockers, 'checks': results,
            'scope': 'Record completeness and freshness only; engineering judgement and physical evidence remain necessary.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('board_config', type=Path)
    parser.add_argument('--stage', required=True, choices=STAGES)
    parser.add_argument('--output', type=Path, help='Optional report; default writes only stdout')
    args = parser.parse_args()
    try:
        result = assess(args.board_config, args.stage)
        code = 0 if result['status'] == 'READY' else 1
    except (ValueError, OSError, TypeError, KeyError) as error:
        result = {'schema_version': 1, 'status': 'INVALID', 'error': str(error)}
        code = 2
    payload = json.dumps(result, indent=2) + '\n'
    if args.output and code != 2:
        # Never let report output overwrite design inputs, evidence or configuration.
        target = args.output.resolve()
        protected = {args.board_config.resolve()}
        if 'design_inputs_sha256' in result:
            cfg = read(args.board_config)
            root = (args.board_config.resolve().parent / cfg['project_root']).resolve()
            protected |= {local(root, p) for p in cfg['design_inputs']}
            protected.add(local(root, cfg['evidence_file']))
        records = read(local(root, cfg['evidence_file'])) if 'design_inputs_sha256' in result and local(root, cfg['evidence_file']).is_file() else {}
        for record in records.get('checks', {}).values():
            artifacts = record.get('artifacts', [])
            if isinstance(artifacts, list):
                for artifact in artifacts:
                    if isinstance(artifact, dict) and isinstance(artifact.get('path'), str):
                        protected.add(local(root, artifact['path']))
        if target in protected or target.suffix.lower() != '.json':
            parser.error('Output must not overwrite inputs or a non-JSON file')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload)
    print(payload, end='')
    return code


if __name__ == '__main__':
    raise SystemExit(main())
