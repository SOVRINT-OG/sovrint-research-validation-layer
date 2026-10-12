# SOVRINT™ Research Validation Layer

## Baseline Validation Protocol — RVL-001

**Author:** Katrina Pietroniro™  
**DOI lineage:** 10.5281/zenodo.20278720  
**Classification:** Publication-safe reproducibility scaffold  
**Canonical status:** Non-canonical operational validation layer

## Objective

RVL-001 tests whether a runtime record remains inside explicitly declared governance boundaries. It evaluates procedural integrity only. It does not prove, calculate, expand, normalize, reinterpret, or promote any equation, theorem, variable, symbol, ontology, or universal scientific claim.

## Validation dimensions

1. Every fixture must be labelled `NON_CANONICAL_SYNTHETIC_FIXTURE`.
2. Runtime state transitions must follow the provisional state model.
3. Evidence must be present before inference or intervention is accepted.
4. Provenance must identify source type, source reference, and capture time.
5. Required consent must exist before governed decision or execution states.
6. Requested correction must be bounded.
7. Requested correction must be explicitly authorized.
8. The observed outcome must match the fixture's declared expected outcome.
9. The eight locked equation transcriptions must remain present exactly once in `EQ_BIBLE_OMEGA.md`.

## Baseline case matrix

| Case | Purpose | Expected result | Expected code |
|---|---|---:|---|
| VAL-001 | Complete governed path with consent | Valid | — |
| VAL-002 | Inference stage skipped | Invalid | `ILLEGAL_TRANSITION` |
| VAL-003 | Execution without required consent | Invalid | `CONSENT_GATE_FAILED` |
| VAL-004 | Observation-only record | Valid | — |
| VAL-005 | Unbounded correction | Invalid | `CORRECTION_UNBOUNDED` |
| VAL-006 | Unauthorized correction | Invalid | `CORRECTION_UNAUTHORIZED` |
| VAL-007 | Missing evidence packet | Invalid | `EVIDENCE_REQUIRED` |
| VAL-008 | Authorized bounded correction | Valid | — |

A successful suite run does **not** require every case to be valid. It requires every observed result and finding code to match the declared expected result. This permits negative controls to remain visible and reproducible.

## Reproduction

From the repository root:

```bash
python replay/run_replay.py
python -m unittest discover -s tests -v
```

The replay command writes a machine-readable report to:

```text
reports/latest_validation_results.json
```

## Interpretation boundary

A passing RVL-001 run demonstrates that the supplied software and fixtures behave deterministically under this protocol. It does not establish empirical validity outside the test environment, scientific universality, medical applicability, legal authority, surveillance legitimacy, or autonomous decision authority.
