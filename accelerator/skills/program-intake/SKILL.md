---
name: program-intake
description: Convert a consented accelerator application into a tenant-scoped normalized intake without inventing missing facts.
version: 0.1.0
metadata:
  accelerator:
    profile: evidence-lab
    max_autonomy: A2
---

# Program Intake

## Trigger

`application.consented`

## Inputs

- Consent reference and data classification.
- Raw application.
- Program thesis/schema.
- Tenant IDs.

## Procedure

1. Verify consent and tenant IDs before reading private fields.
2. Normalize founder-supplied facts, source context, stage, geography, customer, business model, traction assertions, goals, and requested support.
3. Label each field `supplied`, `publicly_observed`, `inferred`, or `unknown`.
4. Do not convert founder assertions into verified evidence.
5. Identify sensitive fields and restrict them to the application tenant.
6. Produce missing-information questions ranked by decision relevance.
7. Create an intake evidence record and route to Thesis Fit Analyst.

## Output

- Normalized intake.
- Missing-information list.
- Data-classification summary.
- Evidence references.

## Gates

Private data-room, financial, health, identity, employment, customer, security, or repo access requires explicit scope. Outreach is not allowed.

## Verification

No required field is silently guessed. Every non-supplied observation has a source. No raw application content enters shared memory or public Git.
