# job-hunt workspace instructions

This directory is the dedicated workspace for the Hermes-based Japan job-hunting automation project.

## Scope

- Treat `job-hunt/` as an isolated project workspace inside the Hermes repository.
- Prefer creating and modifying files only under `job-hunt/` unless the task explicitly requires framework-level integration with Hermes core.
- Do not modify Hermes core source, built-in tools, or root project configuration unless clearly necessary and the reason is explained in the output.
- When proposing changes outside `job-hunt/`, first explain why the change cannot be contained inside this workspace.

## Primary project goal

The goal of this workspace is to build a semi-automated job-hunting system for the Japanese market that can:

1. collect and normalize job postings,
2. compare them with the candidate profile,
3. suggest resume customization,
4. generate tailored application materials,
5. optionally assist with application execution later.

At the current stage, prioritize:
- job parsing,
- schema validation,
- fit scoring,
- resume tailoring suggestions.

Do **not** prioritize full auto-apply yet.

## Working principles

- Accuracy is more important than automation.
- Structured data is preferred over ad hoc text rewriting.
- Never invent candidate experience, metrics, dates, skills, publications, degrees, employers, or language levels.
- Preserve factual consistency across all generated materials.
- If profile data is missing, mark it as missing instead of guessing.
- Prefer explainable outputs over opaque scores.

## Recommended workflow order

When asked to build or improve this project, follow this order unless the user explicitly requests otherwise:

1. candidate profile structuring,
2. job posting normalization,
3. job fit scoring,
4. resume tailoring suggestions,
5. document generation,
6. browser automation / auto-fill,
7. application submission automation.

If a task conflicts with this sequence, prefer the earlier foundational layer first.

## Workspace layout

Expected directory structure:

- `job-hunt/data/`
  - candidate and job data
- `job-hunt/data/raw_jobs/`
  - raw copied job descriptions, scraped HTML snapshots, or original text
- `job-hunt/data/jobs/`
  - normalized job posting JSON files
- `job-hunt/data/candidate_profile.json`
  - structured candidate master profile
- `job-hunt/data/master_experiences.json`
  - expanded experience inventory for tailoring and evidence mapping
- `job-hunt/schemas/`
  - JSON schemas for validation
- `job-hunt/prompts/`
  - reusable prompt assets
- `job-hunt/skills/`
  - workspace-specific Hermes skills
- `job-hunt/outputs/`
  - generated reports, tailored materials, scoring outputs, drafts
- `job-hunt/docs/`
  - design docs and planning docs
- `job-hunt/tests/`
  - tests for parsing, scoring, and validation logic

## Data rules

### Candidate profile

`job-hunt/data/candidate_profile.json` is the canonical structured profile.

Use it as the primary source for:
- identity and contact fields,
- education,
- work history,
- publications,
- projects,
- skills,
- languages,
- certifications,
- target roles.

Do not overwrite candidate facts based on generated text.
If new facts are introduced, they must be traceable to the user or an approved source document.

### Master experiences

`job-hunt/data/master_experiences.json` should contain richer evidence units than the public-facing resume.

Each experience entry should ideally include:
- title,
- organization,
- date range,
- context,
- responsibilities,
- technologies,
- measurable outcomes,
- keywords,
- evidence links or references,
- reusable bullets.

Use this file as the source pool for tailoring.

### Raw jobs

Store unprocessed source material in `job-hunt/data/raw_jobs/`.

Examples:
- copied JD text,
- website extracts,
- HTML snapshots,
- recruiter messages,
- notes from job boards.

Do not treat raw job files as canonical structured data.

### Normalized jobs

Store standardized job posting JSON in `job-hunt/data/jobs/`.

Each normalized file should map to the shared job posting schema and should contain:
- source,
- source_url,
- company_name,
- job_title,
- location,
- employment_type,
- language_requirements,
- required_skills,
- preferred_skills,
- responsibilities,
- salary_range if available,
- visa_support if available,
- application_method,
- raw_description or source reference,
- normalization_notes if needed.

Prefer one normalized JSON per job posting.

## Schema rules

- Validate candidate and job JSON against schemas in `job-hunt/schemas/`.
- If schema validation fails, report the problem clearly and do not silently continue.
- Prefer fixing the data or schema explicitly rather than working around malformed fields.
- Keep schemas stable and version changes deliberately.

## Output rules

When generating outputs:
- write intermediate analytical results to `job-hunt/outputs/` when appropriate,
- keep human-readable summaries concise,
- keep machine-readable artifacts structured,
- include why a job is a good or poor match,
- separate facts from recommendations.

Useful output examples:
- fit analysis reports,
- missing-skill summaries,
- tailored bullet suggestions,
- job ranking tables,
- application draft materials.

## Fit scoring guidance

When scoring job fit, prefer explainable scoring with subcomponents such as:
- required skill match,
- preferred skill match,
- domain alignment,
- language alignment,
- experience alignment,
- evidence strength.

A fit score should be accompanied by:
- strongest matching points,
- weakest matching points,
- recommended resume emphasis,
- risks or gaps,
- suggested decision such as:
  - high priority apply,
  - apply with tailoring,
  - low priority,
  - not recommended.

Do not output a score without rationale.

## Resume tailoring guidance

Resume tailoring must:
- preserve truthfulness,
- reorder emphasis rather than fabricate,
- select the most relevant evidence from the master experience pool,
- adapt wording to the job description,
- highlight Japanese-market relevance where appropriate.

Tailoring should prefer:
- concrete achievements,
- deployment experience,
- measurable outcomes,
- role-relevant technologies,
- language suitability,
- research-to-product translation when applicable.

Do not claim experience the candidate does not have.

## Skills guidance

Workspace-local skills under `job-hunt/skills/` should focus on:
- job normalization,
- fit scoring,
- resume tailoring,
- document drafting,
- application workflow assistance.

Suggested skill folders:
- `job-hunt/skills/job-normalizer/`
- `job-hunt/skills/job-fit-scorer/`
- `job-hunt/skills/resume-tailor/`
- `job-hunt/skills/jp-application-writer/`

Each skill should do one thing clearly.
Avoid building one giant skill that mixes parsing, scoring, drafting, and automation together.

## Prompt asset guidance

Store reusable prompt text in `job-hunt/prompts/`.

Recommended prompt categories:
- job normalization instructions,
- skill extraction instructions,
- fit scoring rubric,
- resume tailoring rubric,
- Japanese application writing style guidance.

Prefer reusable prompt assets over repeating long instructions inline.

## Automation boundaries

At this stage, browser automation should be limited to:
- collecting job descriptions,
- helping fill forms in draft mode,
- preparing submission steps for review.

Avoid full autonomous submission by default.

Before any application submission workflow is implemented, the system should already be able to answer:
- Why does this job fit the candidate?
- Which experiences should be emphasized?
- What should change in the resume?
- What are the main gaps or risks?

If those questions cannot be answered reliably, do not proceed to auto-apply design.

## Safety and privacy

This workspace may contain personal data.
Therefore:

- minimize unnecessary duplication of personal information,
- avoid exposing private data in logs or generated summaries,
- do not copy sensitive profile data into unrelated files,
- keep outputs focused on job-search use,
- do not send, publish, or export candidate data unless explicitly requested.

## Decision preferences

When multiple implementation choices are possible, prefer:

1. local workspace changes over global repository changes,
2. structured JSON over unstructured prose,
3. deterministic validation over hidden assumptions,
4. explainable scoring over vague judgments,
5. assisted application workflows over fully autonomous submission.

## First milestone definition

The first milestone for this workspace is complete when the system can reliably do the following for at least three real Japanese job postings:

1. ingest raw job text,
2. normalize it into schema-compliant JSON,
3. compare it with `candidate_profile.json`,
4. output a clear fit analysis,
5. suggest concrete resume emphasis changes.

Until this milestone is complete, treat additional automation as secondary.