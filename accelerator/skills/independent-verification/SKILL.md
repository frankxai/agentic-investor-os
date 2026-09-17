---
name: independent-verification
description: Verify consequential accelerator artifacts with a different model/provider and produce a non-self-approving verdict.
version: 0.1.0
metadata:
  accelerator:
    profile: independent-verifier
    max_autonomy: A2
---

# Independent Verification

## Trigger

A maker marks a consequential artifact ready for a gate.

## Preconditions

Verifier identity/model/provider differs from the maker for consequential work. The verifier has read access only to the scoped tenant inputs and writes only a verdict.

## Procedure

1. Read the original objective, done-condition, acceptance criteria, and tenant scope.
2. Reproduce relevant checks independently.
3. Sample and trace material claims to evidence records.
4. Test contradictions, missing alternatives, stale sources, unsupported certainty, and scope leakage.
5. For code/artifacts, run the stated tests and inspect the diff/output.
6. Check rollback and gate requirements.
7. Return `pass`, `fail`, or `conditional` with findings ordered by severity.
8. Do not repair the maker artifact in the verifier lane; return it for remediation.

## Output

Verifier verdict containing maker ID, verifier ID, provider/model class, artifact hash/ref, checks, findings, evidence refs, residual risk, and timestamp.

## Human boundary

A passing verdict satisfies the machine checker gate only. It does not approve acceptance, investment, legal/compliance conclusions, external sends, spend, merge, or deployment.
