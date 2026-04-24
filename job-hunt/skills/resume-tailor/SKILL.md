---
name: resume-tailor
description: Generate a truthful, evidence-based resume tailoring plan for a specific Japanese job posting using the candidate profile, master experience inventory, and an existing fit report. Use this skill when the user wants to customize resume emphasis for a target role, especially after a fit analysis has already been completed.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# resume-tailor

## Purpose

Use this skill to create a **tailoring plan** for a target job before generating any final resume or application document.

This skill does **not** directly rewrite the candidate's canonical source data. It produces an intermediate planning artifact that explains:

- which experiences should be emphasized,
- how the summary should be adjusted,
- how the technology stack should be reordered,
- which bullets should be weakened or omitted,
- which keywords should be incorporated.

The goal is to improve relevance for a target role in the Japanese market **without fabricating or exaggerating any facts**.

## When to use

Use this skill when all or most of the following are true:

- `data/candidate_profile.json` exists,
- `data/master_experiences.json` exists (optional; if missing, fall back to candidate_profile.json's work_experience and projects),
- a normalized target job JSON already exists under `data/jobs/`,
- a fit analysis report already exists under `outputs/fit_reports/`,
- the user wants guidance on how to adapt their resume for that job.

Use this skill **before**:

- generating a tailored resume draft,
- generating Japanese motivation statements,
- generating self-PR text,
- preparing application email copy.

## When not to use

Do **not** use this skill when:

- the target job has not yet been normalized,
- the fit report has not yet been created,
- the user wants to change factual profile data,
- the task is to submit an application automatically,
- the request is only to score fit rather than propose resume emphasis changes.

If the fit report does not exist yet, first use the job-fit stage.

## Required inputs

This skill expects the following workspace structure inside `job-hunt/`:

- `data/candidate_profile.json` (required)
- `data/master_experiences.json` (optional; if missing, fall back to work_experience and projects from candidate_profile.json)
- `data/jobs/<job_file>.json` (required)
- `outputs/fit_reports/<job_report>.md` (required)

## Output location

Write the result to:

- `outputs/tailored_resumes/<job_slug>_tailor_plan.md`

Create `outputs/tailored_resumes/` if it does not already exist.

## Core rules

1. **Never invent facts.**
   - Do not fabricate projects, metrics, degrees, employers, publications, or language levels.
2. **Preserve canonical truth.**
   - Use `data/candidate_profile.json` as the primary source of truth; if `data/master_experiences.json` exists, use it for richer evidence mapping.
3. **Prefer reordering over rewriting.**
   - Move emphasis toward the most relevant evidence before trying to rephrase aggressively.
4. **Every recommendation must be evidence-based.**
   - Each suggested emphasis change must be traceable to an actual experience entry.
5. **Be explicit about gaps.**
   - If the job asks for something the candidate does not clearly have, say so.
6. **Separate facts from recommendations.**
   - State what the candidate has versus what should be emphasized.
7. **Optimize for Japanese-market relevance.**
   - Favor concrete outcomes, deployed work, collaboration, measurable results, and role fit.

## Procedure

### Step 1: Read required inputs

Read these files:

- `data/candidate_profile.json` (required)
- `data/master_experiences.json` (optional; if missing, use work_experience and projects from candidate_profile.json)
- the target file under `data/jobs/` (required)
- the corresponding fit report under `outputs/fit_reports/` (required)

If one of these is missing, stop and report the missing dependency clearly.

### Step 2: Identify the target role requirements

Extract the most important job-side signals from the normalized job JSON and fit report, including:

- role objective,
- required skills,
- preferred skills,
- domain or product context,
- language expectations,
- location or work style constraints,
- strongest reasons the role fits,
- biggest gaps or risks.

### Step 3: Map the role to candidate evidence

Search `data/master_experiences.json` for the best supporting evidence.

For each recommendation, identify:

- experience title,
- organization,
- relevant technologies,
- measurable outcomes,
- evidence keywords,
- why that experience supports the target role.

Prefer the strongest 2 to 4 evidence units rather than listing everything.

### Step 4: Build the tailoring strategy

Generate a plan covering these sections:

1. **Target role summary**
   - one short paragraph describing what the job is seeking.
2. **Top experiences to emphasize**
   - 3 items maximum.
3. **Resume summary adjustment**
   - how to reposition the opening summary.
4. **Skills / technology ordering adjustment**
   - what should move up, down, or be grouped differently.
5. **Bullet-level emphasis guidance**
   - which bullets should be highlighted, compressed, or omitted.
6. **Keyword insertion guidance**
   - exact role-relevant keywords already supported by real evidence.
7. **Risk and gap notes**
   - what remains missing or weaker.
8. **Suggested application decision**
   - one of: `high priority apply`, `apply with tailoring`, `low priority`, `not recommended`.

### Step 5: Write the output file

Write a Markdown file to:

- `outputs/tailored_resumes/<job_slug>_tailor_plan.md`

The output must be human-readable and concise, but specific.

## Required output format

Use this structure:

```md
# Tailor Plan: <job title>

## 1. Target Role Summary
...

## 2. Top Experiences to Emphasize
### Experience 1
- Evidence source:
- Why it matters:
- Recommended emphasis:

### Experience 2
...

### Experience 3
...

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

## Naming guidance

Use the normalized job filename stem as `<job_slug>`.

Examples:

- job JSON: `data/jobs/01_pfn_st01_plamo_translation_2026.json`
- fit report: `outputs/fit_reports/01_pfn_st01_plamo_translation_2026.md`
- tailor plan output: `outputs/tailored_resumes/01_pfn_st01_plamo_translation_2026_tailor_plan.md`

## Verification checklist

Before finishing, verify all of the following:

- the output path is under `outputs/tailored_resumes/`,
- no invented experiences were introduced,
- each recommended emphasis can be traced to real candidate evidence,
- the guidance is specific to the target role,
- the recommendation section includes rationale,
- the plan distinguishes strong matches from weak or missing areas.

### Automated verification (recommended)

After writing the plan, run an automated check via `execute_code` to catch issues a manual review might miss:

```python
from hermes_tools import read_file

result = read_file('outputs/tailored_resumes/<job_slug>_tailor_plan.md')
content = result['content']

# 1. Check all required headings are present
sections = [
    '## 1. Target Role Summary',
    '## 2. Top Experiences to Emphasize',
    '## 3. Resume Summary Adjustment',
    '## 4. Skills and Technology Ordering',
    '## 5. Bullet-Level Guidance',
    '## 6. Keyword Guidance',
    '## 7. Risks and Gaps',
    '## 8. Recommendation',
]
missing = [s for s in sections if s not in content]
if missing:
    print(f'MISSING SECTIONS: {missing}')
else:
    print('All 8 required sections present.')

# 2. Scan for fabricated-claim warning signs
fabrication_triggers = ['fabricate', 'invent', 'speculative', 'make up']
for phrase in fabrication_triggers:
    if phrase in content.lower():
        print(f'WARNING: Possible fabricated claim detected: "{phrase}"')

# 3. Check evidence traceability
has_evidence = 'Evidence source:' in content
print(f'Evidence traceable to source: {has_evidence}')

# 4. Check role specificity (customize these check strings per job)
has_role_specific = '<company_name>' in content or '<job_title>' in content
print(f'Guidance specific to target role: {has_role_specific}')

# 5. Check recommendation section has decision + confidence
has_decision = 'Decision:' in content
has_confidence = 'Confidence:' in content
print(f'Recommendation has decision: {has_decision}, confidence: {has_confidence}')

# 6. Check strong vs weak areas are distinguished
has_risks = '## 7. Risks and Gaps' in content
has_highlight = 'Highlight' in content
has_compress = 'Compress' in content or 'Omit' in content or 'reduce' in content
print(f'Strong vs weak areas distinguished: {has_risks and has_highlight and has_compress}')
```

Replace `<company_name>` and `<job_title>` with actual expected text fragments from the target job before running. Run this script and confirm zero failures before declaring the task complete.

## Common pitfalls

Avoid these mistakes:

- rewriting the entire resume instead of producing a plan,
- copying the fit report without adding evidence mapping,
- suggesting unsupported keywords,
- recommending claims that cannot be proven from candidate data,
- using vague advice such as “make it more relevant” without concrete actions,
- writing to `output/` instead of `outputs/`.

## Example invocation

If Hermes is started from the `job-hunt/` directory, use relative workspace paths like these:

- `data/candidate_profile.json`
- `data/master_experiences.json`
- `data/jobs/01_pfn_st01_plamo_translation_2026.json`
- `outputs/fit_reports/01_pfn_st01_plamo_translation_2026.md`

Example task:

> Create a tailoring plan using `data/candidate_profile.json`, `data/master_experiences.json`, `data/jobs/01_pfn_st01_plamo_translation_2026.json`, and `outputs/fit_reports/01_pfn_st01_plamo_translation_2026.md`, then write the result to `outputs/tailored_resumes/01_pfn_st01_plamo_translation_2026_tailor_plan.md`.
