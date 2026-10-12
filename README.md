# SOVRINT™ Research Validation Layer

**Author:** Katrina Pietroniro™  
**Project:** Ontological Computation™ — Integrity-Based Computational Correction  
**DOI reference:** 10.5281/zenodo.20278720 (owner-recorded; landing page not independently verified in this audit).  
**Status:** Active validation and observability research infrastructure

## Purpose

The SOVRINT™ Research Validation Layer is a structured, evidence-bearing environment for runtime integrity modeling, correction-engine benchmarking, telemetry replay, ontology validation, governance-state verification, and reproducibility.

This repository now separates two different classes of material:

1. **Canonical recovery registries**, which preserve authored equations, symbols, variables, theorems, and source lineage without alteration or inferred promotion.
2. **Non-canonical operational validation artifacts**, which provide synthetic fixtures, provisional models, deterministic validators, tests, reports, and replay workflows.

The operational layer may test procedures around evidence, provenance, consent, transition legality, correction boundaries, and authorization. It may not reinterpret or modify the canonical layer.

## Canonical layer

The current canonical registry preserves eight locked equations in:

```text
registry/EQ_BIBLE_OMEGA.md
```

The theorem book remains intentionally unpopulated until original authored theorem statements, premises, domains, source references, and an explicit canonical lock are recovered.

Canonical files include:

```text
CANONICAL_REGISTRY_INDEX.md
registry/EQ_BIBLE_OMEGA.md
registry/THEOREM_BOOK_OMEGA.md
registry/VARIABLE_DICTIONARY_OMEGA.md
registry/SYMBOL_ONTOLOGY_OMEGA.md
provenance/SOURCE_REGISTER.md
schemas/equation-record.schema.json
```

## Validation runtime v1

The first operational suite, `SOVRINT-RVL-SUITE-001`, provides:

- a provisional, explicitly non-canonical governance-state model;
- eight synthetic positive and negative control cases;
- deterministic transition validation;
- evidence and provenance checks;
- consent-gate validation;
- bounded-correction and authorization checks;
- exact-presence tests for the eight locked equation transcriptions;
- a synthetic runtime trace dataset;
- a reproducibility notebook;
- a baseline protocol report;
- GitHub Actions validation and report artifacts.

A suite passes when every observed outcome matches its declared expected outcome. Negative controls remain visibly invalid and must return the exact expected finding code.

## Repository structure

```text
/datasets/synthetic
/manifests
/models
/notebooks
/provenance
/registry
/replay
/reports
/schemas
/tests
/validation
/.github/workflows
```

Key operational files:

```text
models/governance-state-model.json
validation/cases/runtime_integrity_cases.json
validation/engine.py
replay/run_replay.py
tests/test_validation_engine.py
datasets/synthetic/runtime_trace_v1.csv
manifests/validation-suite-v1.json
reports/BASELINE_VALIDATION_PROTOCOL.md
notebooks/reproducibility_walkthrough.ipynb
```

## Run the validation suite

Python 3.11 or newer is recommended. The runtime uses only the Python standard library.

```bash
python replay/run_replay.py
python -m unittest discover -s tests -v
```

The replay command writes:

```text
reports/latest_validation_results.json
```

GitHub Actions also uploads the generated report as a workflow artifact.

## Validation dimensions

The current runtime tests:

- explicit synthetic/non-canonical classification;
- legal progression through declared runtime states;
- evidence presence;
- provenance completeness;
- consent before governed decision or execution;
- bounded correction targets;
- explicit correction authorization;
- deterministic agreement with expected results;
- preservation of the exact locked equation transcriptions.

## Boundary statement

This repository is not:

- a medical diagnostic platform;
- a coercive surveillance system;
- an autonomous decision authority;
- a universal scientific theory;
- proof that a conceptual model is empirically valid outside the supplied tests;
- permission to infer missing variable, symbol, operator, or theorem definitions.

It is:

- a systems-architecture validation environment;
- a reproducibility scaffold;
- a runtime observability research layer;
- a governed boundary between recovered canon and synthetic testing.

## Governing constraints

1. Never alter a locked equation.
2. Never reinterpret a symbol without explicit authorization.
3. Preserve timestamps, authorship, source lineage, and attribution.
4. Preserve original naming.
5. Separate exact recovery from inference.
6. Never promote generated explanation into canon.
7. Every canonical entry must resolve to a provenance record.
8. Every operational model must declare whether it is canonical or provisional.
9. Synthetic fixtures must remain visibly synthetic.
10. Correction tests must preserve consent, authorization, and bounded intervention rules.

## Publication infrastructure

The repository is structured for GitHub, Zenodo, OpenAIRE, DOI synchronization, reproducibility workflows, institutional indexing, and publication evidence packaging.

## Citation

Katrina Pietroniro™. *SOVRINT™ Research Validation Layer: Runtime Integrity, Correction Benchmarks, and Synthetic Telemetry Evidence Package.* DOI: 10.5281/zenodo.20278720 (owner-recorded; landing page not independently verified in this audit).

© 2026 Katrina Pietroniro™. All Rights Reserved.
