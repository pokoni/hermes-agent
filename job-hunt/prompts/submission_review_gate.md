# submission_review_gate prompt asset

Use this prompt asset when generating the final pre-submission review package for a single job application inside the fixed `job-hunt/` workspace.

## Goal

Create a final review package that answers one operational question:

**Is this application package ready to move into a human-approved submission session, without actually submitting anything?**

## Workspace rules

- Keep all paths inside the existing `job-hunt/` workspace.
- Use `outputs/`, not `output/`.
- Do not rename directories or component names.
- Do not perform a final submit action.
- Do not claim submission happened.
- Require explicit final human approval before any submit action.

## Inputs to inspect

Read the following when available:

- `data/jobs/<job>.json`
- `outputs/fit_reports/<job>.md`
- `outputs/tailored_resumes/<job>_tailor_plan.md`
- `outputs/application_drafts/<job>_motivation_ja.md`
- `outputs/application_drafts/<job>_self_pr_ja.md`
- `outputs/application_drafts/<job>_application_mail_ja.md`
- `outputs/logs/application_tracker.jsonl`
- `outputs/logs/<job>_application_execution_plan.md`
- `outputs/logs/<job>_application_execution_checklist.md`
- `outputs/logs/<job>_application_form_snapshot.md`

## Required markdown headings

The markdown output must use these exact headings:

# Submission Review Package
## Target Job
## Artifact Readiness Summary
## Consistency Checks
## Missing or Unverified Items
## Submission Boundary
## Final Human Approval Checklist
## Decision Recommendation

Inside `## Submission Boundary`, include these exact lines:

Do not submit by default.
Stop before final submission.
Require final human approval before any submit action.

## Required JSON fields

The decision JSON must contain:

- `job_id`
- `company_name`
- `job_title`
- `ready_for_submission`
- `requires_human_approval`
- `blocking_issues`
- `missing_items`
- `recommended_next_action`
- `review_timestamp`

## Review logic

Use a conservative gate.

The package is **not** ready if:
- required artifacts are missing,
- key facts conflict across files,
- generated drafts are not aligned with the target role,
- browser execution artifacts still show unresolved blocking issues,
- the actual application path is unclear or unverified.

The package may be treated as operationally ready only if:
- all major artifacts exist,
- no blocking inconsistency is found,
- the next manual execution step is clear,
- final human approval remains required.

## Preferred language style

- concise
- operational
- explicit
- audit-friendly

## Recommended decision phrases

Use one of these for `recommended_next_action`:
- `revise_artifacts`
- `verify_form_access`
- `obtain_human_approval`
- `prepare_submission_session`

## Never do these

- never submit
- never fabricate readiness
- never hide missing artifacts
- never omit the human approval boundary
