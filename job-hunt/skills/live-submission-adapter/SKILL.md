# live-submission-adapter

## Purpose

Use this skill to prepare a controlled, human-approved live submission dry-run package for the Hermes Japan job-hunting workspace.

This skill is the final adapter layer in the current frozen framework. It does not introduce new workflow stages and it must not depend on any component that does not exist in the workspace.

Its job is to:

- read the approved upstream artifacts for one job,
- determine whether the job is ready to enter a supervised live submission attempt,
- generate a dry-run execution package,
- stop before final submission unless the user explicitly authorizes a live action in the current session.

## Fixed Workflow Position

This skill comes after:

1. `job-normalizer`
2. `job-fit-scorer`
3. `resume-tailor`
4. `jp-application-writer`
5. `application-tracker`
6. `browser-apply-assistant`
7. `submission-review-gate`

There is no `submission-session-orchestrator` in the current project framework.
Do not mention, require, or invent that component.

## Workspace Scope

Operate only inside the fixed `job-hunt/` workspace structure.

### Inputs

- `data/candidate_profile.json`
- `data/master_experiences.json`
- `data/jobs/<job_basename>.json`

### Required upstream artifacts

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

### Outputs

- `outputs/logs/<job_basename>_live_submission_dry_run_plan.md`
- `outputs/logs/<job_basename>_live_submission_field_mapping.md`
- `outputs/logs/<job_basename>_live_submission_authorization_request.md`
- `outputs/logs/<job_basename>_live_submission_result_stub.json`

Do not create new top-level directories.
Do not rename `outputs/` to `output/`.

## When to Use

Use this skill when:

- the job already has a normalized JSON file,
- upstream materials have already been generated,
- the browser assistance stage has already produced execution artifacts,
- the submission review gate has already produced a decision,
- the user wants a final dry-run package before any live submission attempt.

If required upstream artifacts are missing, or if the submission decision indicates blocking issues, still produce the live submission dry-run package but mark it as blocked and list every blocking item clearly.

## Hard Safety Boundary

The following exact statements must appear in the live submission dry-run plan and authorization request:

- Do not submit by default.
- Stop before final submission.
- Require explicit human approval before any submit action.
- This skill prepares a controlled dry run unless the user explicitly authorizes a live submission step.

Never click a final submit button unless the user explicitly requests it in the current session.

If the user asks for full autonomous submission without review, refuse that part and continue with dry-run preparation only.

## Procedure

1. Identify the job basename from the requested job JSON path.
2. Read the normalized job JSON.
3. Read the available upstream artifacts under `outputs/`.
4. Check whether the submission review artifacts exist.
5. Check whether the submission decision contains unresolved blockers.
6. Generate the dry-run plan.
7. Generate the field mapping document.
8. Generate the authorization request.
9. Generate the result stub JSON.
10. Do not perform final submission by default.

## Required Output: Dry Run Plan

Write to:

`outputs/logs/<job_basename>_live_submission_dry_run_plan.md`

The markdown document must contain these exact headings:

```markdown
# Live Submission Dry Run Plan

## Target Job

## Application URL

## Required Prior Artifacts

## Dry Run Browser Steps

## Stop Conditions

## Human Approval Boundary

## Expected Outputs
```

The `## Required Prior Artifacts` section must refer only to real upstream artifacts in the current framework.
Do not mention nonexistent session-orchestrator files.

The `## Human Approval Boundary` section must include these exact lines:

```markdown
Do not submit by default.
Stop before final submission.
Require explicit human approval before any submit action.
This skill prepares a controlled dry run unless the user explicitly authorizes a live submission step.
```

## Required Output: Field Mapping

Write to:

`outputs/logs/<job_basename>_live_submission_field_mapping.md`

The markdown document must contain these exact headings:

```markdown
# Live Submission Field Mapping

## Candidate Identity Fields

## Contact Fields

## Education Fields

## Experience Fields

## Motivation and Self-PR Fields

## Upload Fields

## Fields Requiring Human Input

## Mapping Risks
```

Use `unknown`, `not available`, or `requires human input` instead of guessing.

## Required Output: Authorization Request

Write to:

`outputs/logs/<job_basename>_live_submission_authorization_request.md`

The markdown document must contain these exact headings:

```markdown
# Live Submission Authorization Request

## Submission Status

## Materials to Review

## Blocking Issues

## Human Approval Boundary

## Approval Checklist

## Authorization Phrase
```

The `## Human Approval Boundary` section must include these exact lines:

```markdown
Do not submit by default.
Stop before final submission.
Require explicit human approval before any submit action.
This skill prepares a controlled dry run unless the user explicitly authorizes a live submission step.
```

The `## Authorization Phrase` section must state that live submission requires a fresh, explicit user instruction in the current session.

## Required Output: Result Stub JSON

Write to:

`outputs/logs/<job_basename>_live_submission_result_stub.json`

The JSON must contain:

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

If required artifacts are missing or the submission decision is blocked, use `"status": "blocked"` and record the relevant missing artifacts and blocking sources.

## Verification

Before finishing, verify that all four output files exist and contain the required headings.

If browser access fails or the application page is closed, still write the dry-run package and explain the limitation under stop conditions and mapping risks.

## Pitfalls

- Do not rename `outputs/`.
- Do not write output files outside `outputs/logs/`.
- Do not fabricate form fields if the page is inaccessible.
- Do not mark the package as ready if the submission review gate still reports blocking issues.
- Do not refer to nonexistent session artifacts.
- Do not click final submission by default.
