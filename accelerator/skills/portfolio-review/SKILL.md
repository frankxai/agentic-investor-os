---
name: portfolio-review
description: Produce tenant-safe company health briefs, support routes, cost attribution, and approved portfolio learning candidates.
version: 0.1.0
metadata:
  accelerator:
    profile: portfolio-operator
    max_autonomy: A3
---

# Portfolio Review

## Trigger

Weekly company review or monthly portfolio review is due.

## Procedure

1. Process each company independently inside its tenant.
2. Compare declared milestone with observed evidence.
3. Identify the single highest-leverage current constraint.
4. Produce a company health brief: progress, evidence, risk delta, cost, support need, next proof event.
5. Route support through the approved support catalog and create bounded task envelopes.
6. Attribute model, tool, contractor, and operator cost to the company where data exists.
7. Create cross-company learning only as a candidate with raw details removed.
8. Require anonymization and human approval before adding any aggregate to shared benchmarks.
9. State cohort, sample size, time window, definitions, and uncertainty for every benchmark.

## Output

Company health briefs, support queue, cost report, risk escalations, anonymized learning candidates.

## Gates

External introductions, resource allocation, contractor/spend, benchmark publication, raw cross-company sharing, or public claims.

## Verification

Portfolio artifacts contain only approved summaries. Every support task has an owner/done-condition. Costs remain attributable, not estimated as fact without labeling.
