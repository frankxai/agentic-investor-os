# Investor OS Playbook

Agentic Investor OS is a public-safe workflow system for organizing opportunity context, diligence questions, evidence, risks, memos, portfolio support, and stakeholder updates.

It does not make regulated decisions. Any investment, legal, tax, accounting, securities, compliance, confidentiality, outreach, or publication decision stays with a qualified human owner.

## Operating Boundary

Use this module to:

- Turn raw opportunity context into structured intake.
- Convert uncertainty into evidence questions.
- Track source quality, freshness, risks, and open issues.
- Draft review packets for human decision owners.
- Prepare portfolio support plans and investor updates.

Do not use this module to:

- Promise outcomes, returns, revenue, exits, or market certainty.
- Conclude that an opportunity should be bought, sold, funded, or rejected.
- Replace legal, tax, accounting, securities, compliance, or qualified domain review.
- Publish confidential company, founder, customer, fund, LP, or deal data.
- Send outreach or stakeholder communications without approval.

## Evidence Standards

Every material claim should be tagged with an evidence state.

| Evidence State | Meaning | Acceptable Use |
|---|---|---|
| Verified | Checked against a named source or artifact. | Can appear in a memo with source reference. |
| Source-linked | A source is identified but not fully reviewed. | Can appear with caveat and next action. |
| Draft | Based on provided notes, not independently checked. | Internal working notes only. |
| Inferred | Reasoned from available context, but not directly evidenced. | Use only as a question or hypothesis. |
| Missing | Evidence is required and not yet available. | Must remain an open diligence item. |

## Core Workflow

```text
thesis boundary -> intake -> evidence queue -> diligence sprint -> memo -> risk register -> approval gate -> portfolio support or archive
```

## 1. Thesis Boundary

Purpose: define what the module is allowed to evaluate and what is out of scope.

Required fields:

- Mandate or category lens.
- Exclusions.
- Minimum evidence bar.
- Approval owner.
- Public/private handling rule.

Output: thesis brief or mandate note.

Safety gate: do not describe the thesis as a promise of performance or certainty.

## 2. Opportunity Intake

Purpose: convert raw notes into a structured record.

Required fields:

- Opportunity name or placeholder.
- Category, stage, geography, and business model if known.
- Source and date received.
- Materials available.
- Missing materials.
- Known confidentiality limits.
- Human decision owner.

Output: intake summary and missing-information list.

Safety gate: use placeholders for public examples and avoid live deal details.

## 3. Evidence Queue

Purpose: turn questions into source requests.

Minimum lanes:

- Market and buyer urgency.
- Product workflow and adoption.
- Technical architecture and dependency risk.
- Team and operating cadence.
- Go-to-market and distribution.
- Financial model inputs, without conclusions.
- Legal, tax, accounting, securities, and compliance review needs.
- Security, privacy, and data handling.

Output: evidence table with owner, freshness, strength, and next action.

Safety gate: mark expert-review items instead of resolving them inside the module.

## 4. Diligence Sprint

Purpose: coordinate a time-boxed review without pretending certainty.

Recommended stages:

1. Scope the decision, audience, and boundaries.
2. Assign agent lanes.
3. Collect sources and mark evidence strength.
4. Draft risk register.
5. Draft memo and open questions.
6. Run confidentiality and regulated-claim review.
7. Hand off to the human decision owner.

Output: diligence sprint plan, source log, memo, risk register, and approval notes.

Safety gate: the sprint ends with a review packet, not an automated decision.

## 5. Memo And Risk Register

Purpose: summarize what is known, what remains uncertain, and what must be reviewed.

Memo sections:

- Opportunity context.
- Thesis fit as a hypothesis.
- Evidence summary.
- Open questions.
- Risks and gates.
- Support opportunities.
- Human review checklist.

Risk register fields:

- Risk.
- Category.
- Evidence needed.
- Owner.
- Status.
- Gate.
- Next action.

Safety gate: keep recommendations framed as decision criteria, review needs, or support options.

## 6. Investor Update

Purpose: prepare stakeholder communications that are clear, sourced, and approved.

Update sections:

- Period covered.
- Audience and confidentiality level.
- Progress highlights.
- Metrics with source and caveat.
- Asks.
- Risks and open issues.
- Next milestones.
- Approval status.

Safety gate: remove unapproved confidential information and claims that imply certainty.

## Agent Handoffs

| Agent | Receives | Produces | Must Escalate |
|---|---|---|---|
| Thesis Architect | Mandate, category lens, exclusions. | Thesis boundary and evidence bar. | Any unclear mandate or restricted category. |
| Deal Intake Analyst | Raw notes and source context. | Structured intake and missing-info list. | Confidential or unapproved deal details. |
| Diligence Lead | Intake and thesis boundary. | Evidence queue and sprint plan. | Missing critical sources or unsupported claims. |
| Market Analyst | Category and buyer context. | Market questions and source needs. | Unsupported market-size or competition claims. |
| Product Analyst | Product notes, demos, workflow artifacts. | Adoption and workflow questions. | Claims about customer outcomes without proof. |
| Technical Analyst | Architecture notes and dependency list. | Technical risk notes. | Security, privacy, or infrastructure concerns. |
| Memo Editor | Evidence queue, risks, open questions. | Memo draft. | Any decision-like conclusion or missing caveat. |
| Portfolio Support Lead | Memo, risk register, support asks. | 30-day support plan. | Sensitive introductions or public commitments. |
| Compliance Sentinel | Draft packet and communication plan. | Approval gate note. | Regulated claims, confidential data, outreach, or publication. |

## Public-Safe Packet Checklist

- Uses fictional placeholders or approved public information only.
- Contains no founder, customer, LP, fund, or live deal secrets.
- Contains no private paths, credentials, internal URLs, or unpublished strategy.
- Separates evidence from assumptions.
- Labels missing evidence.
- Avoids outcome certainty and performance promises.
- Routes legal, tax, accounting, securities, compliance, confidentiality, outreach, and publication to human approval.

## Decision Packet

A reviewer should be able to answer:

- What is the opportunity or workflow being reviewed?
- What thesis or mandate question does it test?
- Which claims are evidenced, weak, inferred, or missing?
- What risks matter most?
- Which expert reviews or approvals are required?
- What support plan or next action is proposed?

What remains unproven should be explicit. A clean packet makes uncertainty easier to see.
