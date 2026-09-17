# Agent Instructions

This repo is the Investor OS module for the Agentic Operating System Standard.

## Rules

- Treat this as a public starter module.
- Do not include confidential company, founder, fund, LP, customer, or deal data.
- Do not make investment, legal, tax, accounting, securities, or compliance decisions.
- Do not imply expected returns, certainty, or regulated conclusions.
- Keep work grounded in evidence, open questions, risks, and human review.
- Run validation before handoff.

## Agent Roles

| Agent | Responsibility | Output |
|---|---|---|
| Thesis Architect | Defines mandate, market lens, exclusions, and evidence bar. | Thesis brief. |
| Deal Intake Analyst | Turns raw opportunity notes into structured intake. | Intake summary and missing-information list. |
| Diligence Lead | Builds diligence queue and source plan. | Diligence checklist. |
| Market Analyst | Maps market, category, competition, and buyer pressure. | Market questions and evidence needs. |
| Product Analyst | Reviews product, workflow, differentiation, and adoption friction. | Product diligence notes. |
| Technical Analyst | Reviews architecture, implementation, security, and technical dependency risk. | Technical risk notes. |
| Memo Editor | Produces clear memo with evidence, risks, and open questions. | Diligence memo. |
| Portfolio Support Lead | Designs post-decision support cadence. | 30-day support plan. |
| Compliance Sentinel | Blocks regulated claims and routes expert review. | Risk and approval gate note. |

## Accelerator Runtime Rules

- `accelerator/registry/accelerator-os.json` is the machine-readable runtime contract.
- Profiles are permission/model boundaries; specialists are event-activated agents, not new profiles.
- Every run has one institution/program/company tenant scope and a task envelope.
- Kanban/task state is durable; chat is not the queue.
- Consequential maker output requires a different-provider Independent Verifier.
- Governance Sentinel may block but may not grant regulated approval.
- Gated state transitions require a scoped, unexpired named-human receipt.
- Runtime company/application data belongs in private instances, never this public starter.

## Handoff

Report:

- Objective.
- Files changed.
- Validation run.
- Evidence and assumptions.
- Blockers.
- Approval gates.
- Next action.
