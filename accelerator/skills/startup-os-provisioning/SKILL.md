---
name: startup-os-provisioning
description: Provision a minimal private Day-0 Company OS after a valid human acceptance receipt and tenant authorization.
version: 0.1.0
metadata:
  accelerator:
    profiles: [program-director, venture-builder]
    max_autonomy: A3
---

# Startup OS Provisioning

## Trigger

`company.accepted.with_receipt`

## Preconditions

- Valid, scoped, unexpired human acceptance receipt.
- Institution/program/company tenant IDs.
- Authorized workspace owner, retention policy, and data classes.
- Rollback owner.

## Procedure

1. Validate the receipt reference; never create it from the agent run.
2. Create or select one private company workspace/repo.
3. Write a tenant manifest with allowed users, tools, data classes, memory namespace, and retention.
4. Select the smallest modules needed from Business OS, Creator OS, Investor OS, or relevant vertical systems.
5. Establish one source of truth for goals, tasks, evidence, decisions, costs, and approvals.
6. Create a 30-day backlog around the company's highest-evidence constraint.
7. Define product, GTM, operations, founder, and proof lanes only if needed.
8. Configure task envelopes and maker/checker rules.
9. Request human approval for invitations, permissions, imports, paid tools, external sends, or deployment.
10. Run isolation, validation, and rollback checks before requesting activation.

## Output

Tenant manifest, Company OS manifest, onboarding checklist, 30-day backlog, rollback plan, activation request.

## Verification

No other tenant data is reachable. No secrets are written. Every module has an owner and first-win workflow. Activation remains gated.
