# Engineering design review report contract

Produce an inspectable review in the owning project's `docs/` or `evidence/`, linked from the relevant change/task. Example structure:

```markdown
# Design review: <project / subsystem / revision>
- Review ID / date:
- Requested gate and declared scope:
- Author / reviewer / independence: INDEPENDENT | SELF_REVIEW | UNKNOWN
- Baseline: revision or hashes, source paths, requirements, interface versions
- Artifacts inspected:
- Checks actually rerun (commands, versions, results):
- Evidence inspected (type, conditions, hashes and limitations):
- Unreviewed areas and reasons:

## Findings
| ID | Severity | Requirement / artifact | Observation and evidence | Consequence | Action | Disposition |
| ... |

## Gate decision
- Status: PASS | BLOCKED | NEEDS_REVIEW
- Blocking findings / unavailable required checks:
- Residual risks and exact scope of pass:
- Next actions and required human approval:
```

Severity definitions:
- **BLOCKER:** observed safety/functional failure, invalid baseline or mandatory evidence absent; must prevent claimed gate.
- **MAJOR:** significant performance, manufacturability, testability or cross-discipline risk requiring resolution before gate, unless a documented, authorized scope exclusion applies.
- **MINOR:** improvement or localized nonblocking defect, tracked to closure.
- **NOTE:** observation or question, not evidence of a failure.

For each finding, identify an exact artifact/feature/line and what supports the conclusion. An unresolved high-risk unknown is not a pass. A recorded `PASS` is not regulatory certification. Never claim independent review if the reviewer designed the change.
