"""Validation tests for live-submission-adapter outputs.

These tests validate stable output contracts only. They do not perform a live
submission and do not require browser access.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASENAME = os.environ.get("JOB_HUNT_TEST_BASENAME", "02_avilen_semiconductor_cv_ai_intern_2026")
LOGS = ROOT / "outputs" / "logs"


def _read_text(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def _dry_run_plan_path() -> Path:
    return LOGS / f"{BASENAME}_live_submission_dry_run_plan.md"


def _field_mapping_path() -> Path:
    return LOGS / f"{BASENAME}_live_submission_field_mapping.md"


def _authorization_request_path() -> Path:
    return LOGS / f"{BASENAME}_live_submission_authorization_request.md"


def _result_stub_path() -> Path:
    return LOGS / f"{BASENAME}_live_submission_result_stub.json"


def test_dry_run_plan_contains_required_sections() -> None:
    text = _read_text(_dry_run_plan_path())
    required = [
        "# Live Submission Dry Run Plan",
        "## Target Job",
        "## Application URL",
        "## Required Prior Artifacts",
        "## Dry Run Browser Steps",
        "## Stop Conditions",
        "## Human Approval Boundary",
        "## Expected Outputs",
    ]
    for heading in required:
        assert heading in text, f"Dry run plan missing heading: {heading}"


def test_field_mapping_contains_required_sections() -> None:
    text = _read_text(_field_mapping_path())
    required = [
        "# Live Submission Field Mapping",
        "## Candidate Identity Fields",
        "## Contact Fields",
        "## Education Fields",
        "## Experience Fields",
        "## Motivation and Self-PR Fields",
        "## Upload Fields",
        "## Fields Requiring Human Input",
        "## Mapping Risks",
    ]
    for heading in required:
        assert heading in text, f"Field mapping missing heading: {heading}"


def test_authorization_request_contains_required_sections() -> None:
    text = _read_text(_authorization_request_path())
    required = [
        "# Live Submission Authorization Request",
        "## Submission Status",
        "## Materials to Review",
        "## Blocking Issues",
        "## Human Approval Boundary",
        "## Approval Checklist",
        "## Authorization Phrase",
    ]
    for heading in required:
        assert heading in text, f"Authorization request missing heading: {heading}"


def test_submission_boundary_is_explicit() -> None:
    combined = "\n".join([
        _read_text(_dry_run_plan_path()).lower(),
        _read_text(_authorization_request_path()).lower(),
    ])
    required_phrases = [
        "do not submit by default",
        "stop before final submission",
        "require explicit human approval before any submit action",
        "this skill prepares a controlled dry run unless the user explicitly authorizes a live submission step",
    ]
    for phrase in required_phrases:
        assert phrase in combined, f"Missing mandatory boundary phrase: {phrase}"


def test_result_stub_is_safe_json() -> None:
    path = _result_stub_path()
    assert path.exists(), f"Missing expected file: {path}"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data.get("job_basename") == BASENAME
    assert data.get("live_submission_performed") is False
    assert data.get("human_approval_required") is True
    assert data.get("final_submit_clicked") is False
    assert data.get("status") in {"dry_run_prepared", "blocked"}
    assert isinstance(data.get("missing_artifacts", []), list)
    assert isinstance(data.get("blocking_sources", []), list)


def test_no_nonexistent_session_orchestrator_reference() -> None:
    combined = "\n".join([
        _read_text(_dry_run_plan_path()).lower(),
        _read_text(_authorization_request_path()).lower(),
        _read_text(_field_mapping_path()).lower(),
    ])
    assert "submission-session-orchestrator" not in combined
    assert "submission_session_plan" not in combined
    assert "submission_session_manifest" not in combined
    assert "submission_session_ready_check" not in combined
