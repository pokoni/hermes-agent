# live-submission-adapter framework fix

This note freezes the correct dependency boundary for the current terminal stage.

## Correct dependency chain

`submission-review-gate` -> `live-submission-adapter`

## Incorrect dependency chain that must not be used

`submission-review-gate` -> `submission-session-orchestrator` -> `live-submission-adapter`

There is no `submission-session-orchestrator` component in the current project structure.
Therefore:

- do not require session artifacts,
- do not mention session artifacts in output files,
- do not block live submission dry-run preparation on nonexistent session artifacts.

## Required upstream artifacts for live-submission-adapter

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

## Stable output expectation

The live submission adapter still produces these four files:

- `<job_basename>_live_submission_dry_run_plan.md`
- `<job_basename>_live_submission_field_mapping.md`
- `<job_basename>_live_submission_authorization_request.md`
- `<job_basename>_live_submission_result_stub.json`

## Safety boundary

The stage remains non-default submission only.
It must stop before final submission unless the user explicitly authorizes a live action in the current session.
