from __future__ import annotations

import json
import os
from pathlib import Path


def _base_name() -> str:
    return os.environ.get("JOB_HUNT_TEST_BASENAME", "01_pfn_st01_plamo_translation_2026")


def _logs_dir() -> Path:
    return Path("outputs/logs")


def _review_path() -> Path:
    return _logs_dir() / f"{_base_name()}_submission_review.md"


def _decision_path() -> Path:
    return _logs_dir() / f"{_base_name()}_submission_decision.json"


def _read_text(path: Path) -> str:
    assert path.exists(), f"Expected file does not exist: {path}"
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    assert path.exists(), f"Expected file does not exist: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_submission_review_file_exists() -> None:
    assert _review_path().exists(), f"Missing submission review file: {_review_path()}"


def test_submission_decision_file_exists() -> None:
    assert _decision_path().exists(), f"Missing submission decision file: {_decision_path()}"


def test_submission_review_contains_required_sections() -> None:
    text = _read_text(_review_path())
    required = [
        "# Submission Review Package",
        "## Target Job",
        "## Artifact Readiness Summary",
        "## Consistency Checks",
        "## Missing or Unverified Items",
        "## Submission Boundary",
        "## Final Human Approval Checklist",
        "## Decision Recommendation",
    ]
    for heading in required:
        assert heading in text, f"Submission review missing heading: {heading}"


def test_submission_boundary_is_explicit() -> None:
    text = _read_text(_review_path())
    required_lines = [
        "Do not submit by default.",
        "Stop before final submission.",
        "Require final human approval before any submit action.",
    ]
    for line in required_lines:
        assert line in text, f"Submission review missing boundary line: {line}"


def test_decision_json_contains_required_fields() -> None:
    data = _read_json(_decision_path())
    required_fields = [
        "job_id",
        "company_name",
        "job_title",
        "ready_for_submission",
        "requires_human_approval",
        "blocking_issues",
        "missing_items",
        "recommended_next_action",
        "review_timestamp",
    ]
    for field in required_fields:
        assert field in data, f"Decision JSON missing field: {field}"


def test_human_approval_remains_required() -> None:
    data = _read_json(_decision_path())
    assert data["requires_human_approval"] is True, "Human approval must remain required"


def test_recommended_next_action_is_allowed() -> None:
    data = _read_json(_decision_path())
    allowed = {
        "revise_artifacts",
        "verify_form_access",
        "obtain_human_approval",
        "prepare_submission_session",
    }
    assert data["recommended_next_action"] in allowed, "Unexpected recommended_next_action value"
