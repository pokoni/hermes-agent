---
name: submission-review-gate
description: Final pre-submission review gate for the Japan job-hunt workspace. Use this skill to consolidate all generated artifacts, verify completeness and consistency, and produce an explicit human-approval boundary before any submission action.
---

# submission-review-gate

## Purpose

Use this skill to create the final pre-submission review package for a single job application.
This skill does **not** submit anything.
Its role is to make the submission boundary explicit, confirm artifact readiness, surface unresolved risks, and require final human approval before any submit action.

## When to Use

Use this skill when all earlier workspace stages for a target job are already available or mostly available:

- a normalized job posting under `data/jobs/`
- a fit report under `outputs/fit_reports/`
- a tailoring plan under `outputs/tailored_resumes/`
- Japanese application drafts under `outputs/application_drafts/`
- application tracking artifacts under `outputs/logs/`
- browser-assisted execution artifacts under `outputs/logs/`

This skill should be called **after**:
1. `job-normalizer`
2. `job-fit-scorer`
3. `resume-tailor`
4. `jp-application-writer`
5. `application-tracker`
6. `browser-apply-assistant`

## Inputs

Expected workspace inputs:

- `data/jobs/<job>.json`
- `outputs/fit_reports/<job>.md`
- `outputs/tailored_resumes/<job>_tailor_plan.md`
- `outputs/application_drafts/<job>_motivation_ja.md`
- `outputs/application_drafts/<job>_self_pr_ja.md`
- `outputs/application_drafts/<job>_application_mail_ja.md`
- `outputs/logs/application_tracker.jsonl` when available
- `outputs/logs/<job>_application_execution_plan.md`
- `outputs/logs/<job>_application_execution_checklist.md`
- `outputs/logs/<job>_application_form_snapshot.md`

## Required Outputs

Write these files under `outputs/logs/`:

1. `outputs/logs/<job>_submission_review.md`
2. `outputs/logs/<job>_submission_decision.json`

Do not change directory names.
Use `outputs/`, not `output/`.

## Output Contract

The markdown review file must use these exact headings:

# Submission Review Package
## Target Job
## Artifact Readiness Summary
## Consistency Checks
## Missing or Unverified Items
## Submission Boundary
## Final Human Approval Checklist
## Decision Recommendation

The markdown file must include these exact lines inside `## Submission Boundary`:

Do not submit by default.
Stop before final submission.
Require final human approval before any submit action.

The decision JSON must be machine-readable and contain at least:

- `job_id`
- `company_name`
- `job_title`
- `ready_for_submission`
- `requires_human_approval`
- `blocking_issues`
- `missing_items`
- `recommended_next_action`
- `review_timestamp`

## Procedure

1. Read the target job JSON and identify the canonical job id, company, and title.
2. Read all available downstream artifacts for that same job id.
3. Check whether the artifact set is complete enough for submission review.
4. Compare key facts across artifacts:
   - company name
   - job title
   - language expectations
   - targeted role emphasis
   - recommended strengths and risks
5. Check whether the application drafts appear aligned with the fit report and tailoring plan.
6. Check whether the browser execution artifacts define a non-submission boundary and whether any form blockers remain.
7. Produce a single markdown submission review package with the required headings.
8. Produce a machine-readable decision JSON with an explicit readiness verdict.
9. If there are missing files or unresolved blockers, set `ready_for_submission` to `false`.
10. Never perform or simulate a final submission action.

## Decision Rules

Use conservative decision logic.

Set `ready_for_submission` to `true` only if:
- all required artifacts exist,
- no blocking inconsistency is found,
- browser execution artifacts indicate the next step is operationally feasible,
- final human approval is still required.

Set `requires_human_approval` to `true` in all normal cases.
This should remain `true` unless the user explicitly redesigns the framework.

Recommended decision values:

- `ready_for_submission: false` when key artifacts are missing or inconsistent
- `ready_for_submission: true` only when the package is complete and coherent
- `recommended_next_action` should be one of:
  - `revise_artifacts`
  - `verify_form_access`
  - `obtain_human_approval`
  - `prepare_submission_session`

## Style Requirements

- Prefer concise operational language.
- Separate facts from recommendations.
- Do not invent evidence.
- If an artifact is missing, state that it is missing.
- If an item could not be verified, label it as unverified.
- Keep the review file human-readable and directly actionable.

## Pitfalls

Avoid these mistakes:

- treating draft generation as equivalent to submission readiness
- claiming the application is ready when the form path was not verified
- silently ignoring missing files
- changing workspace paths or directory names
- merging multiple jobs into one review package
- performing any final submit action

## Verification

A correct result should satisfy all of the following:

- a markdown review file exists at `outputs/logs/<job>_submission_review.md`
- a JSON decision file exists at `outputs/logs/<job>_submission_decision.json`
- the markdown file contains all required headings
- the markdown file contains the three exact submission-boundary lines
- the JSON decision file contains an explicit human approval requirement
- no submit action is taken
