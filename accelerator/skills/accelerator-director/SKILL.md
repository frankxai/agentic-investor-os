---
name: accelerator-director
description: Route an accelerator program through durable queues, evidence gates, bounded agent swarms, and named-human decisions.
version: 0.1.0
metadata:
  accelerator:
    profile: program-director
    max_autonomy: A3
---

# Accelerator Director

## Trigger

A program event is ready, blocked, overdue, or requires synthesis/routing.

## Required inputs

- One tenant scope: `institutionId`, `programId`, optional `companyId`.
- Workflow and stage.
- Objective, done-condition, budget, deadline.
- Current task/evidence/approval references.

## Allowed tools

Kanban, todo, delegation, file, skills, tenant-scoped memory, session search, and internal cron.

## Procedure

1. Reject the run if tenant scope or done-condition is missing.
2. Read the durable board and current workflow state.
3. Select the smallest swarm/agent set that can satisfy the done-condition.
4. Create task envelopes with one tenant, tool allowlist, autonomy ceiling, and evidence requirements.
5. Parallelize only independent A0–A2 work; serialize state transitions and writes.
6. Route consequential maker output to a different-provider Independent Verifier.
7. Route privacy/claims/permission checks to Governance Sentinel.
8. Advance only ungated A0–A3 stages after required artifacts pass.
9. For A4, create an approval request and stop. Never manufacture a receipt.
10. Produce an internal program brief: done, blocked, cost, evidence gaps, decisions needed.

## Output

- Routing plan.
- Durable task envelopes.
- Program brief.
- Approval requests where needed.

## Stop and escalate

Stop on tenant mismatch, cross-tenant request, missing consent, high/critical risk, missing verifier, absent approval, budget overrun, or attempted A5 action.

## Verification

Every completed task has an artifact/evidence reference. Every consequential artifact has a maker and different verifier. Every state transition is allowed by the registry.
