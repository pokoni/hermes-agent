---
name: job-fit-scorer
title: Japan Job Fit Scorer
description: Compare data/candidate_profile.json against a normalized job posting in data/jobs/ and produce an explainable fit analysis for Japanese job applications.
version: 1.0.0
author: OpenAI
metadata:
  tags:
    - japan-jobs
    - resume-matching
    - fit-scoring
    - explainability
  requires_toolsets:
    - files
---

# Japan Job Fit Scorer

Evaluate how well the candidate profile matches a normalized job posting and produce a clear, evidence-based fit report.

## When To Use

Use this skill when:
- a job posting has already been normalized into `data/jobs/*.json`
- the user asks whether a role is worth applying to
- the user wants to know which experiences should be emphasized
- the user wants an explainable score before resume tailoring

Do **not** use this skill before job normalization is complete.
Do **not** use this skill to draft the final Japanese application materials.

## Stable Workspace Assumptions

This skill assumes the current working directory is `job-hunt/` and uses the fixed project structure:

- `data/candidate_profile.json` -> canonical candidate profile
- `data/master_experiences.json` -> detailed evidence inventory
- `data/jobs/*.json` -> normalized job postings
- `output/fit_reports/` -> fit analysis output location

Do not move files or invent alternate directories.

## Core Principle

Scoring must be **explainable**.
Never output a score without showing:
- strongest matches
- weakest matches
- which experiences should be emphasized
- which risks or gaps matter most
- whether the role is worth pursuing now

## Inputs

Required:
- `data/candidate_profile.json`
- one normalized job file from `data/jobs/`

Recommended:
- `data/master_experiences.json`

## Output Contract

Write a human-readable report to `output/fit_reports/`.

Preferred filename pattern:
- `output/fit_reports/<job_id>.md`

The report should include:
- job summary
- fit score breakdown
- matching evidence
- key gaps
- resume emphasis suggestions
- final recommendation

## Scoring Framework

Use the following sub-scores, each on a 0-5 scale:

1. **Required skill match**
   - How many required skills are clearly supported by the profile?
2. **Preferred skill match**
   - How many bonus skills are present?
3. **Domain alignment**
   - Does the candidate's background align with the role domain?
4. **Language alignment**
   - Is the candidate's Japanese/English profile compatible with the role?
5. **Experience alignment**
   - Are the candidate's strongest projects relevant to the role's actual work?
6. **Evidence strength**
   - Are there measurable outcomes, shipped systems, publications, or strong proof points?

Then compute a final recommendation band:
- 24-30: **high priority apply**
- 18-23: **apply with tailoring**
- 12-17: **borderline / selective apply**
- 0-11: **not recommended now**

If the data is incomplete, say so explicitly and lower confidence.

## Matching Rules

### 1. Match by meaning, not only by exact wording
Japanese job postings may express the same idea using different terms.
Examples:
- edge AI / 組み込みAI / on-device inference
- 画像処理 / computer vision / visual inspection
- 高速化 / 推論最適化 / latency reduction

Use semantic matching, but do not over-claim.

### 2. Prioritize evidence-backed experience
Prefer evidence such as:
- deployment on edge devices
- measurable latency or model-size improvement
- publications
- shipped products
- internships with concrete technical responsibilities

### 3. Distinguish mismatch from unknown
If the candidate profile does not mention a skill:
- do not assume absence if the evidence base is incomplete
- mark it as `not evidenced` rather than definitively missing when appropriate

### 4. Japanese-market considerations
Include special attention to:
- language requirements
- internship vs full-time eligibility
- location constraints
- research vs product orientation
- whether the role appears to expect strong business Japanese

## Procedure

### Step 1: Read candidate data
Inspect:
- `data/candidate_profile.json`
- `data/master_experiences.json` if available

Identify:
- strongest skills
- strongest experience domains
- language profile
- publications or shipped systems
- constraints such as graduation timeline or location

### Step 2: Read one normalized job JSON
Inspect the selected file from `data/jobs/`.
Extract:
- role summary
- required skills
- preferred skills
- domain
- language expectations
- work style and location

### Step 3: Build evidence mapping
For each important job requirement, map one of these outcomes:
- `supported`
- `partially supported`
- `not evidenced`
- `clear gap`

Cite which candidate experience supports each matched area.

### Step 4: Score each subcomponent
Assign 0-5 for each sub-score.
Be conservative.
If a skill is only weakly implied, do not score it as a strong match.

### Step 5: Write recommendations
Write concrete guidance on:
- which 2-4 experiences to foreground
- which keywords to add to resume bullets if truthful
- which gaps to acknowledge or de-emphasize
- whether this role should be prioritized

### Step 6: Save the report
Write the report to `output/fit_reports/<job_id>.md`.

## Recommended Report Structure

```md
# Fit Report: <job title>

## Overall Recommendation
- Recommendation: Apply with tailoring
- Total Score: 21/30
- Confidence: Medium

## Score Breakdown
- Required skill match: 4/5
- Preferred skill match: 3/5
- Domain alignment: 4/5
- Language alignment: 3/5
- Experience alignment: 4/5
- Evidence strength: 3/5

## Strongest Matches
- ...

## Weakest Areas / Gaps
- ...

## Experiences To Emphasize
- ...

## Resume Tailoring Suggestions
- ...

## Risks
- ...
```

## Decision Heuristics

Prefer **high priority apply** when:
- the role directly matches edge AI, computer vision, deployment, optimization, or related work
- the candidate has 2 or more strong evidence-backed matches
- the language requirement is not clearly beyond the candidate's current profile

Prefer **apply with tailoring** when:
- domain fit is strong but some tools or language expectations are weaker

Prefer **not recommended now** when:
- the role depends heavily on missing fundamentals
- there is a major language or eligibility mismatch
- the candidate profile offers very little evidence for the actual job responsibilities

## Pitfalls

Avoid these mistakes:
- giving a high score based only on broad AI similarity
- ignoring Japanese language or business communication requirements
- treating unpublished assumptions as evidence
- writing generic recommendations that do not map back to candidate data
- using raw job files instead of normalized JSON

## Verification

The task is complete only if:
- the selected job file came from `data/jobs/`
- candidate data came from `data/candidate_profile.json`
- the report is written to `output/fit_reports/`
- the score is broken down into subcomponents
- each major recommendation is traceable to concrete evidence or explicitly marked as a gap
