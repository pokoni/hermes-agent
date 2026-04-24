# Resume Tailoring Prompt Asset

Use this prompt asset when producing a role-specific tailoring plan from structured candidate data and an existing fit report.

## Goal

Create a truthful, evidence-based resume tailoring plan for a target Japanese job posting.

The output is **not** a final resume rewrite. It is a planning document that explains how the candidate should reposition existing experience for better role alignment.

## Inputs

You are given these workspace files:

- `data/candidate_profile.json`
- `data/master_experiences.json`
- `data/jobs/<job_file>.json`
- `outputs/fit_reports/<job_report>.md`

## Source-of-truth policy

Treat the following as the only factual sources:

- `data/candidate_profile.json`
- `data/master_experiences.json`
- `data/jobs/<job_file>.json`
- `outputs/fit_reports/<job_report>.md`

If a fact is missing from the source files, do not guess.

## Tailoring objectives

Your job is to determine:

1. which existing experiences best support this role,
2. how the resume summary should shift,
3. how skills and technologies should be reordered,
4. which bullets should be emphasized or compressed,
5. which job-relevant keywords can be added truthfully,
6. what risks or gaps remain.

## Required reasoning approach

Follow this order:

1. Read the job JSON and fit report.
2. Identify the most important role requirements.
3. Match those requirements to specific evidence in `data/master_experiences.json`.
4. Prefer the strongest 2 to 4 supporting experiences.
5. Produce a practical tailoring plan rather than a full rewritten resume.

## Hard constraints

- Do not invent achievements, metrics, projects, publications, employers, or skills.
- Do not claim language proficiency beyond what is explicitly supported.
- Do not add technologies unless they are already evidenced.
- Do not hide important gaps; call them out clearly.
- Do not write to `output/`; use `outputs/`.

## Japanese-market guidance

When selecting emphasis, prioritize:

- measurable technical contributions,
- deployment or production relevance,
- collaboration and implementation ability,
- research-to-application translation,
- stable and concrete language rather than exaggerated claims.

## Required output sections

Produce a Markdown document with exactly these main sections:

1. `## 1. Target Role Summary`
2. `## 2. Top Experiences to Emphasize`
3. `## 3. Resume Summary Adjustment`
4. `## 4. Skills and Technology Ordering`
5. `## 5. Bullet-Level Guidance`
6. `## 6. Keyword Guidance`
7. `## 7. Risks and Gaps`
8. `## 8. Recommendation`

## Style rules

- Be specific.
- Prefer bullet points under each section where useful.
- Keep the plan concise but actionable.
- Distinguish observed facts from recommendations.
- Explain why each recommendation matters for the target role.

## Decision labels

Use one of these for the final recommendation:

- `high priority apply`
- `apply with tailoring`
- `low priority`
- `not recommended`

Also include a confidence label:

- `high`
- `medium`
- `low`

## Output path convention

Write the final file to:

- `outputs/tailored_resumes/<job_slug>_tailor_plan.md`

Where `<job_slug>` matches the normalized job JSON filename stem.

Example:

- input job JSON: `data/jobs/01_pfn_st01_plamo_translation_2026.json`
- input fit report: `outputs/fit_reports/01_pfn_st01_plamo_translation_2026.md`
- output plan: `outputs/tailored_resumes/01_pfn_st01_plamo_translation_2026_tailor_plan.md`

## Output template

```md
# Tailor Plan: <job title>

## 1. Target Role Summary
<brief paragraph>

## 2. Top Experiences to Emphasize
### Experience 1
- Evidence source:
- Why it matters:
- Recommended emphasis:

### Experience 2
- Evidence source:
- Why it matters:
- Recommended emphasis:

### Experience 3
- Evidence source:
- Why it matters:
- Recommended emphasis:

## 3. Resume Summary Adjustment
- Current positioning:
- Recommended positioning:
- Reason:

## 4. Skills and Technology Ordering
- Move up:
- Keep but de-emphasize:
- Add only if already evidenced:

## 5. Bullet-Level Guidance
- Highlight:
- Compress:
- Omit or reduce:

## 6. Keyword Guidance
- Keywords to include:
- Keywords to avoid claiming without evidence:

## 7. Risks and Gaps
- ...

## 8. Recommendation
- Decision:
- Confidence:
- Notes:
```
