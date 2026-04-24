# Stable templates for browser-apply-assistant

## Execution plan template

```md
# Application Execution Plan

## Target Job
- Company: ...
- Job Title: ...
- Job ID / Basename: ...

## Application URL
- Primary URL: ...
- Fallback / Notes: ...

## Available Workspace Artifacts
- data/jobs/...json
- outputs/fit_reports/...
- outputs/tailored_resumes/...
- outputs/application_drafts/...

## Planned Browser Actions
1. Open the application page.
2. Confirm page reachability and login requirements.
3. Detect visible form fields.
4. Map ready workspace artifacts to form fields.
5. Prepare draft-only fill steps.

## Submission Boundary
Do not submit by default.
Stop before final submission.
Require final human review before any submit action.

## Open Questions
- ...
```

## Execution checklist template

```md
# Application Execution Checklist

## Required Form Fields
- Name
- Email
- ...

## Required Uploads
- Resume
- Additional documents
- ...

## Draft Answers Ready
- Motivation draft: ready / missing
- Self PR draft: ready / missing

## Missing Information
- ...

## Final Human Review Items
- Confirm target role and company
- Confirm uploaded files
- Confirm all draft answers
```

## Form snapshot template

```md
# Application Form Snapshot

## Page Access Result
- Reachable / not reachable
- Login required / unknown
- Notes

## Detected Form Elements
- Text inputs
- Textareas
- Select boxes
- Checkboxes

## Upload Slots
- Resume upload
- Cover letter upload
- Other attachments

## Blocking Issues
- Missing URL
- Login wall
- Deadline closed

## Recommended Next Step
- Draft-only fill
- Wait for user review
- Verify live page later
```
