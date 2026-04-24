---
name: application-tracker
description: Track job applications, material versions, status changes, and follow-up actions for the Hermes Japan job-hunt workspace.
allowed-tools: Read, Write, Edit, MultiEdit, LS, Glob, Grep
---

# Application Tracker

## Purpose

Use this skill to create and update structured application tracking records inside the `job-hunt/` workspace.

This skill is responsible for keeping a persistent record of:
- which job was targeted,
- which materials were used,
- the current application status,
- important dates,
- next actions,
- concise notes.

This skill does **not** submit applications. It only records and maintains the application state.

## When to use

Use this skill when the user wants to:
- log a newly prepared application,
- record that a job was submitted,
- update an existing application status,
- store which generated documents were used,
- track interview progress,
- track follow-up actions,
- summarize current application pipeline state.

Do **not** use this skill for:
- job normalization,
- fit scoring,
- resume tailoring,
- Japanese motivation/self-PR drafting,
- browser automation.

## Workspace assumptions

All paths below are relative to the `job-hunt/` workspace root.

Canonical input files:
- `data/candidate_profile.json`
- `data/jobs/<job_basename>.json`
- `outputs/fit_reports/<job_basename>.md`
- `outputs/tailored_resumes/<job_basename>_tailor_plan.md`
- `outputs/application_drafts/<job_basename>_motivation_ja.md`
- `outputs/application_drafts/<job_basename>_self_pr_ja.md`
- `outputs/application_drafts/<job_basename>_application_mail_ja.md`

Canonical tracker artifacts:
- `outputs/logs/application_tracker.jsonl`
- `outputs/logs/application_tracker_latest.md`

Schema reference:
- `schemas/application_record.schema.json`

## Required tracking model

Each application record must represent exactly one job target.

The canonical record format is JSON with these fields:
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

### Status vocabulary

Use only these status values unless the user explicitly defines an extension:
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

### Priority vocabulary

Use only:
- `high`
- `medium`
- `low`

## File conventions

### application_tracker.jsonl

Store one JSON object per line in:
- `outputs/logs/application_tracker.jsonl`

Rules:
- append a new line when creating a new application record,
- when updating a record, rewrite the file so the latest state is reflected exactly once per application,
- keep the file valid JSONL,
- keep keys stable and readable,
- prefer explicit `null` over invented values.

### application_tracker_latest.md

Maintain a human-readable summary at:
- `outputs/logs/application_tracker_latest.md`

This summary should include:
- total application count,
- counts by status,
- highest-priority active applications,
- follow-up-needed items,
- concise per-application rows or bullets.

## Procedure

### A. Create a new application record

1. Read the target job JSON from `data/jobs/`.
2. Read `data/candidate_profile.json` if needed for candidate identity.
3. If available, read related fit/tailoring/application draft outputs.
4. Construct a single application record.
5. Validate it against `schemas/application_record.schema.json` conceptually.
6. Write or update `outputs/logs/application_tracker.jsonl`.
7. Regenerate `outputs/logs/application_tracker_latest.md`.
8. Briefly report what was added.

### B. Update an existing application record

1. Read `outputs/logs/application_tracker.jsonl`.
2. Find the record matching `application_id` or `job_basename`.
3. Update only the fields supported by the request.
4. Keep untouched facts unchanged.
5. Rewrite `outputs/logs/application_tracker.jsonl` with exactly one latest record per application.
6. Regenerate `outputs/logs/application_tracker_latest.md`.
7. Briefly report the updated status and next action.

### C. Summarize the pipeline

1. Read `outputs/logs/application_tracker.jsonl`.
2. Group by status.
3. Identify high-priority active applications.
4. Identify items needing follow-up.
5. Update `outputs/logs/application_tracker_latest.md`.
6. Return a concise summary.

## Record construction rules

### application_id

Build `application_id` deterministically from:
- `<job_basename>__<status-or-created-date-suffix>` is acceptable for first draft,
- prefer stable IDs such as `<job_basename>__001` when possible.

Do not generate random IDs unless explicitly requested.

### materials

`materials` should be an object containing paths when available, for example:
- `fit_report`
- `tailor_plan`
- `motivation_ja`
- `self_pr_ja`
- `application_mail_ja`
- `resume_version`
- `other`

If a file does not exist, set that field to `null` rather than inventing a path.

### fit_summary

`fit_summary` should contain concise machine-readable fields:
- `overall_fit`
- `confidence`
- `key_strengths`
- `key_gaps`
- `recommendation`

Do not paraphrase wildly. Stay consistent with the fit report.

### notes

`notes` should be short and operational.
Prefer bullets or a short list of strings, not long essays.

## Output style for the markdown dashboard

The `application_tracker_latest.md` file should use this structure:

```md
# Application Tracker Dashboard

## Overview
- Total applications: X
- Active applications: Y
- Follow-up needed: Z

## Status Summary
- drafting: ...
- ready_to_submit: ...
- submitted: ...
...

## High Priority Active Applications
- <job_basename> | <company> | <status> | next action: ...

## Follow-up Needed
- <job_basename> | next action date: ... | note: ...

## Application Details
### <job_basename>
- Company: ...
- Job title: ...
- Status: ...
- Priority: ...
- Submission date: ...
- Next action: ...
- Materials: ...
```

## Constraints

- Never invent submission dates, contact dates, interview dates, or recruiter communications.
- Never say a job was submitted unless the user or a source file clearly indicates it.
- Never fabricate which document version was used.
- Prefer `null` for unknown dates.
- Keep tracking data operational and auditable.
- Do not mix multiple jobs into one record.

## Verification checklist

Before finishing, verify:
- file paths use `data/`, `schemas/`, and `outputs/` correctly,
- `outputs/logs/application_tracker.jsonl` exists and is valid JSONL,
- each application appears only once in latest-state form,
- `status` is from the allowed vocabulary,
- `priority` is from the allowed vocabulary,
- `application_tracker_latest.md` was regenerated.

## Typical commands / requests

- "Create a tracker entry for the PFN application using the existing fit report and tailoring plan."
- "Mark the PFN application as ready_to_submit and set next action date to 2026-04-25."
- "Record that the application was submitted today."
- "Summarize all current applications and tell me which ones need follow-up."
