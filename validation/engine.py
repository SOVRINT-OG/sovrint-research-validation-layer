#!/usr/bin/env python3
"""Deterministic validation engine for SOVRINT Research Validation Layer.

This module validates synthetic runtime fixtures against an explicitly
provisional governance-state model. It does not calculate, interpret, alter,
or promote any equation, theorem, variable, or symbol in the canonical
registries.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


REQUIRED_CASE_FIELDS = {
    "case_id",
    "title",
    "classification",
    "status_path",
    "evidence",
    "provenance",
    "consent_required",
    "consent_present",
    "correction",
    "expected_valid",
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    valid: bool
    expected_valid: bool
    expectation_matched: bool
    codes: list[str]
    expected_codes: list[str]
    findings: list[dict[str, str]]


class ValidationInputError(ValueError):
    """Raised when a suite or model cannot be interpreted safely."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationInputError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationInputError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValidationInputError(f"Top-level JSON value must be an object: {path}")
    return payload


def _finding(findings: list[Finding], code: str, message: str) -> None:
    findings.append(Finding(code=code, message=message))


def _validate_transition_path(
    path: Any,
    allowed_transitions: dict[str, list[str]],
    states: set[str],
    findings: list[Finding],
) -> list[str]:
    if not isinstance(path, list) or not path:
        _finding(findings, "STATUS_PATH_REQUIRED", "status_path must be a non-empty list.")
        return []

    normalized: list[str] = []
    for index, state in enumerate(path):
        if not isinstance(state, str) or state not in states:
            _finding(
                findings,
                "UNKNOWN_STATE",
                f"status_path[{index}] is not present in the provisional state model.",
            )
            continue
        normalized.append(state)

    for previous, current in zip(normalized, normalized[1:]):
        if current not in allowed_transitions.get(previous, []):
            _finding(
                findings,
                "ILLEGAL_TRANSITION",
                f"Transition {previous} -> {current} is not permitted by the provisional model.",
            )
    return normalized


def validate_case(case: dict[str, Any], model: dict[str, Any]) -> CaseResult:
    findings: list[Finding] = []
    case_id = str(case.get("case_id", "UNIDENTIFIED"))

    missing = sorted(REQUIRED_CASE_FIELDS - set(case))
    if missing:
        _finding(findings, "REQUIRED_FIELD_MISSING", f"Missing fields: {', '.join(missing)}")

    if case.get("classification") != "NON_CANONICAL_SYNTHETIC_FIXTURE":
        _finding(
            findings,
            "CLASSIFICATION_INVALID",
            "Runtime fixtures must be explicitly classified as non-canonical synthetic fixtures.",
        )

    states = set(model.get("states", []))
    allowed_transitions = model.get("allowed_transitions", {})
    if not states or not isinstance(allowed_transitions, dict):
        raise ValidationInputError("The governance-state model is missing states or transitions.")

    normalized_path = _validate_transition_path(
        case.get("status_path"), allowed_transitions, states, findings
    )

    evidence = case.get("evidence")
    if not isinstance(evidence, list) or not any(
        isinstance(item, str) and item.strip() for item in evidence
    ):
        _finding(findings, "EVIDENCE_REQUIRED", "At least one evidence reference is required.")

    provenance = case.get("provenance")
    if not isinstance(provenance, dict):
        _finding(findings, "PROVENANCE_REQUIRED", "A structured provenance record is required.")
    else:
        for field in ("source_type", "source_reference", "captured_at"):
            if not isinstance(provenance.get(field), str) or not provenance[field].strip():
                _finding(
                    findings,
                    "PROVENANCE_INCOMPLETE",
                    f"Provenance field '{field}' must be present and non-empty.",
                )

    rules = model.get("rules", {})
    consent_gate_states = set(rules.get("consent_gate_states", []))
    reaches_consent_gate = any(state in consent_gate_states for state in normalized_path)
    if case.get("consent_required") and reaches_consent_gate and not case.get("consent_present"):
        _finding(
            findings,
            "CONSENT_GATE_FAILED",
            "The path reaches a governed decision or execution state without required consent.",
        )

    correction = case.get("correction")
    if not isinstance(correction, dict):
        _finding(findings, "CORRECTION_RECORD_REQUIRED", "A correction descriptor is required.")
    elif correction.get("requested"):
        if rules.get("correction_must_be_bounded", True) and not correction.get("bounded"):
            _finding(
                findings,
                "CORRECTION_UNBOUNDED",
                "A requested correction must declare a bounded target and intervention scope.",
            )
        if rules.get("correction_requires_authorization", True) and not correction.get("authorized"):
            _finding(
                findings,
                "CORRECTION_UNAUTHORIZED",
                "A requested correction must carry explicit authorization.",
            )
        if not isinstance(correction.get("target"), str) or not correction["target"].strip():
            _finding(
                findings,
                "CORRECTION_TARGET_REQUIRED",
                "A requested correction must name its bounded target.",
            )

    codes = sorted({item.code for item in findings})
    expected_codes = sorted(set(case.get("expected_codes", [])))
    valid = not findings
    expected_valid = bool(case.get("expected_valid"))
    expectation_matched = valid == expected_valid and codes == expected_codes

    return CaseResult(
        case_id=case_id,
        valid=valid,
        expected_valid=expected_valid,
        expectation_matched=expectation_matched,
        codes=codes,
        expected_codes=expected_codes,
        findings=[asdict(item) for item in findings],
    )


def run_suite(suite: dict[str, Any], model: dict[str, Any]) -> dict[str, Any]:
    if model.get("canonical") is not False or model.get("status") != "PROVISIONAL_TEST_MODEL":
        raise ValidationInputError(
            "The runtime validator only accepts models explicitly marked non-canonical and provisional."
        )

    cases = suite.get("cases")
    if not isinstance(cases, list):
        raise ValidationInputError("Validation suite must contain a 'cases' list.")

    results = [validate_case(case, model) for case in cases if isinstance(case, dict)]
    matched = sum(result.expectation_matched for result in results)
    valid_cases = sum(result.valid for result in results)
    invalid_cases = len(results) - valid_cases

    return {
        "suite_id": suite.get("suite_id", "UNIDENTIFIED-SUITE"),
        "model_id": model.get("model_id", "UNIDENTIFIED-MODEL"),
        "classification": "NON_CANONICAL_VALIDATION_OUTPUT",
        "summary": {
            "total_cases": len(results),
            "valid_cases": valid_cases,
            "invalid_cases": invalid_cases,
            "expectations_matched": matched,
            "expectation_mismatches": len(results) - matched,
            "suite_passed": matched == len(results),
        },
        "results": [asdict(result) for result in results],
    }


def write_report(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the SOVRINT synthetic validation suite.")
    parser.add_argument(
        "--suite",
        type=Path,
        default=Path("validation/cases/runtime_integrity_cases.json"),
        help="Path to the synthetic validation suite.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=Path("models/governance-state-model.json"),
        help="Path to the provisional governance-state model.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/latest_validation_results.json"),
        help="Path for the machine-readable validation report.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = run_suite(load_json(args.suite), load_json(args.model))
        write_report(report, args.output)
    except ValidationInputError as exc:
        print(f"VALIDATION INPUT ERROR: {exc}")
        return 2

    summary = report["summary"]
    print(
        "SOVRINT validation suite: "
        f"{summary['expectations_matched']}/{summary['total_cases']} expectations matched; "
        f"suite_passed={summary['suite_passed']}"
    )
    return 0 if summary["suite_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
