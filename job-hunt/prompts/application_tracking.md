# Application tracking prompt asset

You are maintaining a structured application tracker for the `job-hunt/` workspace.

## Goal

Create or update precise, auditable application records that reflect the current state of each job target.

## Inputs

Possible inputs include:
- `data/candidate_profile.json`
- `data/jobs/<job_basename>.json`
- `outputs/fit_reports/<job_basename>.md`
- `outputs/tailored_resumes/<job_basename>_tailor_plan.md`
- `outputs/application_drafts/<job_basename>_motivation_ja.md`
- `outputs/application_drafts/<job_basename>_self_pr_ja.md`
- `outputs/application_drafts/<job_basename>_application_mail_ja.md`
- `outputs/logs/application_tracker.jsonl`

## Required output artifacts

You must maintain:
- `outputs/logs/application_tracker.jsonl`
- `outputs/logs/application_tracker_latest.md`

## Record schema expectations

Every record should contain:
- `application_id`
- `job_basename`
- `company_name`
- `job_title`
- `source`
- `source_url`
- `candidate_name`
- `status`
- `priority`
- `created_at`
- `updated_at`
- `submission_date`
- `last_contact_date`
- `next_action_date`
- `next_action`
- `materials`
- `fit_summary`
- `notes`

## Allowed status values

Use only:
- `drafting`
- `ready_to_submit`
- `submitted`
- `awaiting_reply`
- `interview_scheduled`
- `interview_completed`
- `follow_up_needed`
- `offer`
- `rejected`
- `withdrawn`
- `archived`

## Allowed priority values

Use only:
- `high`
- `medium`
- `low`

## Creation rules

When creating a new record:
1. Read the job JSON first.
2. Reuse known candidate identity from `data/candidate_profile.json`.
3. Reuse known artifacts from `outputs/` if they exist.
4. Summarize fit in concise structured form.
5. Use `null` for unknown dates.
6. Do not claim submission unless clearly confirmed.

## Update rules

When updating a record:
1. Read the existing JSONL tracker file.
2. Match by `application_id` or `job_basename`.
3. Update only the requested fields.
4. Keep a single latest-state record per application.
5. Rewrite the JSONL file cleanly.
6. Regenerate the markdown dashboard.

## Markdown dashboard rules

The dashboard file must contain these sections:
- `# Application Tracker Dashboard`
- `## Overview`
- `## Status Summary`
- `## High Priority Active Applications`
- `## Follow-up Needed`
- `## Application Details`

## Writing style

- concise
- factual
- operational
- no invented facts
- no vague recommendations without basis

## Prohibited behavior

- do not fabricate submission dates
- do not fabricate interview outcomes
- do not invent materials that do not exist
- do not duplicate the same application record multiple times
