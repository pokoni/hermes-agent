# Live Submission Adapter Prompt

You are preparing a controlled live submission dry-run package for the Hermes Japan job-hunting workspace.

Use the fixed project structure:

- Candidate data: `data/candidate_profile.json`
- Experience data: `data/master_experiences.json`
- Normalized jobs: `data/jobs/`
- Generated artifacts: `outputs/`
- Logs and execution artifacts: `outputs/logs/`

Do not use `output/`.
Do not create new top-level directories.

## Current Frozen Workflow

The current workflow ends with:

- `submission-review-gate`
- `live-submission-adapter`

There is no `submission-session-orchestrator` in this project.
Do not require it.
Do not mention it.
Do not block on it.

## Primary Goal

Create a safe, reviewable dry-run package for one job application.
The package must help the user understand exactly what would happen during a supervised application attempt.

The default state is not submission.
The default state is dry-run preparation.

## Mandatory Boundary

Every live submission package must include these statements:

- Do not submit by default.
- Stop before final submission.
- Require explicit human approval before any submit action.
- This skill prepares a controlled dry run unless the user explicitly authorizes a live submission step.

## Required Upstream Artifacts

Check for these real upstream artifacts:

- `outputs/fit_reports/<job_basename>.md`
- `outputs/tailored_resumes/<job_basename>_tailor_plan.md`
- `outputs/application_drafts/<job_basename>_motivation_ja.md`
- `outputs/application_drafts/<job_basename>_self_pr_ja.md`
- `outputs/application_drafts/<job_basename>_application_mail_ja.md`
- `outputs/logs/<job_basename>_application_execution_plan.md`
- `outputs/logs/<job_basename>_application_execution_checklist.md`
- `outputs/logs/<job_basename>_application_form_snapshot.md`
- `outputs/logs/<job_basename>_submission_review.md`
- `outputs/logs/<job_basename>_submission_decision.json`

If any required artifact is missing, do not fail silently.
Produce a blocked package and list the missing artifacts.

If the submission decision indicates blocking issues, keep the package blocked.

## Output 1: Dry Run Plan

Create:

`outputs/logs/<job_basename>_live_submission_dry_run_plan.md`

It must contain exactly these section headings:

# Live Submission Dry Run Plan

## Target Job

## Application URL

## Required Prior Artifacts

## Dry Run Browser Steps

## Stop Conditions

## Human Approval Boundary

## Expected Outputs

## Output 2: Field Mapping

Create:

`outputs/logs/<job_basename>_live_submission_field_mapping.md`

It must contain exactly these section headings:

# Live Submission Field Mapping

## Candidate Identity Fields

## Contact Fields

## Education Fields

## Experience Fields

## Motivation and Self-PR Fields

## Upload Fields

## Fields Requiring Human Input

## Mapping Risks

## Output 3: Authorization Request

Create:

`outputs/logs/<job_basename>_live_submission_authorization_request.md`

It must contain exactly these section headings:

# Live Submission Authorization Request

## Submission Status

## Materials to Review

## Blocking Issues

## Human Approval Boundary

## Approval Checklist

## Authorization Phrase

## Output 4: Result Stub JSON

Create:

`outputs/logs/<job_basename>_live_submission_result_stub.json`

Use this structure:

```json
{
  "job_basename": "<job_basename>",
  "status": "dry_run_prepared",
  "live_submission_performed": false,
  "human_approval_required": true,
  "final_submit_clicked": false,
  "missing_artifacts": [],
  "blocking_sources": [],
  "notes": []
}
```

If blocked, set `status` to `blocked` and list missing artifacts and blocking sources.

## Writing Rules

- Do not invent candidate facts.
- Do not invent unavailable form fields.
- Use `requires human input` for unknown fields.
- Prefer explicit checklists over vague prose.
- Keep the human approval boundary visible and repeated.
- Do not mention nonexistent intermediate workflow stages.
