# Fit Scoring Prompt Asset

Use this prompt asset when comparing `data/candidate_profile.json` with one normalized job posting in `data/jobs/`.

## Goal

Produce an explainable fit analysis that helps decide whether to apply and how to tailor the resume.

## Instructions

1. Read the candidate profile first.
2. Read the normalized job JSON second.
3. Evaluate required skills, preferred skills, domain alignment, language alignment, experience alignment, and evidence strength.
4. Use conservative scoring.
5. Distinguish between `not evidenced` and `clear gap`.
6. Recommend 2-4 experiences to emphasize.
7. Produce a final recommendation band:
   - high priority apply
   - apply with tailoring
   - borderline / selective apply
   - not recommended now

## Do Not

- Do not score based on vague AI similarity alone.
- Do not ignore Japanese language expectations.
- Do not claim candidate skills that are not supported by profile evidence.
- Do not generate a total score without rationale.
