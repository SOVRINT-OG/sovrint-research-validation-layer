# CI Runner Status

**Observed:** 2026-06-26  
**Repository:** `katrinapietro05-design/sovrint-research-validation-layer`

## Diagnostic result

A staged GitHub Actions diagnostic was executed to separate repository defects from runner-level defects.

The first diagnostic job contained only:

```text
echo "runner-ready"
python3 --version
git --version
```

That job failed before GitHub retained usable step logs. Every downstream job was therefore skipped, including repository checkout, syntax validation, JSON validation, deterministic replay, and unit tests.

This observation does not identify the underlying GitHub Actions configuration or runner cause. It does establish that the reported workflow failure occurred before the validation code was checked out or executed.

## Current operating mode

The validation workflow is preserved as a manual `workflow_dispatch` workflow so it can be reactivated immediately when the repository runner is available. It is not used as an automatic pull-request or push gate while the runner-level condition remains unresolved.

## Local validation commands

```bash
python3 -m compileall -q validation replay tests
python3 replay/run_replay.py
python3 -m unittest discover -s tests -v
```

The deterministic fixture logic was independently checked against all eight declared outcomes before merge preparation. The repository must not claim a completed GitHub-hosted validation run until a manual workflow completes successfully.
