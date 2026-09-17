---
name: thesis-fit
description: Evaluate program fit against explicit criteria while keeping scoring separate from human acceptance or investment decisions.
version: 0.1.0
metadata:
  accelerator:
    profile: evidence-lab
    max_autonomy: A2
---

# Thesis Fit

## Trigger

`application.normalized`

## Inputs

Normalized intake, program thesis, exclusions, evidence bar, and tenant scope.

## Procedure

1. Extract each explicit criterion and disqualifier from the current program thesis.
2. Map application evidence to each criterion.
3. Rate dimensions independently: aligned, partly aligned, not aligned, or unknown.
4. Show evidence and uncertainty beside every rating.
5. Record disqualifiers exactly; do not invent new policy during a review.
6. Produce open questions and the cheapest next evidence action.
7. Return `proceed-to-screening`, `clarify`, or `stop-recommendation` as routing advice only.

## Output

Fit matrix, disqualifiers, open questions, evidence gaps, routing advice.

## Human boundary

No score accepts, rejects, invests, or determines eligibility. A human owns those decisions and may override with a recorded rationale.

## Verification

Every criterion traces to the thesis version. Every rating traces to supplied or observed evidence. Unknown remains unknown.
