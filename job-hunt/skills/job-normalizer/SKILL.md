---
name: job-normalizer
title: Japan Job Posting Normalizer
description: Normalize raw Japanese job descriptions into schema-compliant JSON under job-hunt/data/jobs/ using the stable project structure.
version: 1.0.0
author: OpenAI
metadata:
  tags:
    - japan-jobs
    - normalization
    - schema
    - recruitment
  requires_toolsets:
    - files
---

# Japan Job Posting Normalizer

Convert raw job descriptions in `data/raw_jobs/` into standardized JSON files in `data/jobs/`.

## When To Use

Use this skill when:
- a new job description has been added to `data/raw_jobs/`
- the user wants a hiring page converted into the shared job posting schema
- a previously normalized job JSON is missing fields or needs cleanup
- multiple job postings need consistent field naming and structure

Do **not** use this skill for resume tailoring, application drafting, or fit scoring.

## Stable Workspace Assumptions

This skill assumes the current working directory is `job-hunt/` and the project structure is fixed:

- `data/raw_jobs/` stores raw source material
- `data/jobs/` stores normalized JSON files
- `schemas/job_posting.schema.json` is the canonical schema
- `data/candidate_profile.json` is **not** used by this skill except for optional compatibility checks

Do not invent new directories.

## Inputs

Primary input sources:
- one raw job file under `data/raw_jobs/`
- optionally, a live job page URL supplied by the user
- optionally, an existing normalized JSON in `data/jobs/` that needs revision

Preferred raw file format:
- Markdown with YAML front matter
- source snapshot blocks
- visible requirements and responsibilities separated from missing information

## Output Contract

Write exactly one normalized JSON file per job posting to `data/jobs/`.

Filename convention:
- raw: `data/raw_jobs/01_company_role_year.md`
- normalized: `data/jobs/01_company_role_year.json`

The output must be valid JSON and align with `schemas/job_posting.schema.json`.

## Required Fields To Populate

At minimum, try to populate:
- `job_id`
- `source_platform`
- `source_url`
- `source_title`
- `company_name`
- `job_title`
- `employment_type`
- `location`
- `language`
- `status`
- `responsibilities`
- `required_skills`
- `preferred_skills`
- `application_method`
- `raw_description`
- `normalization_notes`

If a field is not visible from the source, set it to a safe empty value according to the schema and record the uncertainty in `normalization_notes`.

## Normalization Rules

### 1. Preserve facts
- Never infer unavailable salaries, visa support, or hidden requirements.
- Never rewrite a preferred skill into a required skill.
- Never claim that a position is open indefinitely if the posting is date-bounded.

### 2. Separate visible facts from missing information
- Only place directly supported facts in structured fields.
- Put uncertainty, ambiguity, login-gated details, or interpretation into `normalization_notes`.

### 3. Normalize lists cleanly
Use arrays for:
- `required_skills`
- `preferred_skills`
- `responsibilities`
- `language_requirements`
- `keywords`

Prefer short atomic entries rather than paragraph-sized bullets.

### 4. Preserve Japanese-market semantics
Keep distinctions such as:
- 必須 / MUST -> `required_skills`
- 歓迎 / NICE TO HAVE / Better -> `preferred_skills`
- 業務内容 / 仕事内容 -> `responsibilities`
- 勤務地 / リモート / 出社条件 -> `location` and `work_style`

### 5. Keep source traceability
Always keep enough traceability to reconstruct where the JSON came from:
- source URL
- source title
- retrieval date if available in the raw file
- notes for hidden or inferred omissions

## Procedure

### Step 1: Read the raw job file
Open the selected file under `data/raw_jobs/`.
Extract:
- company name
- job title
- source platform
- source URL
- visible role summary
- visible requirements
- visible preferred skills
- visible responsibilities
- visible work conditions
- anything explicitly missing or hidden

### Step 2: Map content into the stable schema
Translate the extracted content into the schema fields in `schemas/job_posting.schema.json`.

Rules:
- Use exact strings from the source when possible
- Normalize obvious synonyms only when it improves consistency
- Keep the original meaning intact

### Step 3: Fill missing fields safely
If the source does not show a field:
- use schema-safe null/empty values
- mention the missing context in `normalization_notes`

### Step 4: Write the normalized JSON
Save the output to the paired filename under `data/jobs/`.

### Step 5: Self-check before finishing
Verify:
- valid JSON syntax
- no fabricated salary or visa claims
- required vs preferred distinction preserved
- output path matches the fixed project structure

## Recommended JSON Shape

Use the project schema, but conceptually the file should look like:

```json
{
  "job_id": "01_pfn_st01_plamo_translation_2026",
  "source_platform": "preferred",
  "source_url": "https://...",
  "source_title": "...",
  "company_name": "...",
  "job_title": "...",
  "employment_type": "internship",
  "location": "Tokyo, Japan",
  "language": "ja",
  "status": "time_bounded",
  "language_requirements": [],
  "responsibilities": [],
  "required_skills": [],
  "preferred_skills": [],
  "application_method": "apply via official form",
  "raw_description": "summary of visible source content",
  "normalization_notes": [
    "Salary not visible on public page.",
    "Some eligibility details are listed on a separate page."
  ]
}
```

## Pitfalls

Common mistakes to avoid:
- merging required and preferred skills into one list
- treating a company profile page as a job description page
- filling hidden compensation fields from memory or unrelated pages
- dropping uncertainty notes when the source is incomplete
- writing outputs outside `data/jobs/`

## Verification

The task is complete only if all of the following are true:
- the raw job has a matching JSON in `data/jobs/`
- the JSON is syntactically valid
- the JSON respects `schemas/job_posting.schema.json`
- every nontrivial claim is traceable to the raw source or explicitly marked in `normalization_notes`
- no new project directories were introduced
