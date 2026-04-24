# Browser-assisted application stage: next steps

This stage adds a safe execution layer on top of the existing workspace pipeline.

## What this stage should do

- inspect the application entry point,
- identify required fields and uploads,
- map existing workspace artifacts to form requirements,
- prepare an execution checklist,
- stop before final submission by default.

## Recommended usage order

1. Ensure these artifacts already exist for the target job:
   - `data/jobs/<job>.json`
   - `outputs/fit_reports/<job>.md`
   - `outputs/tailored_resumes/<job>_tailor_plan.md`
   - `outputs/application_drafts/*`
2. Run `browser-apply-assistant`
3. Review the three generated log artifacts
4. Only then decide whether to proceed with browser filling

## Suggested first run

Use the PFN job first because the workspace already contains aligned inputs for it.

## Suggested future extension

After this stage is stable, the next module should be:

- `submission-review-gate`

Its job would be to perform a final pre-submit validation and require explicit authorization before submission.
