# Agentic Investor OS

**An agentic operating system for thesis, deal flow, diligence, memos, portfolio support, and investor communications.**

[![Validate](https://github.com/frankxai/agentic-investor-os/actions/workflows/validate.yml/badge.svg)](https://github.com/frankxai/agentic-investor-os/actions/workflows/validate.yml)
[![Standard](https://img.shields.io/badge/standard-agentic%20operating%20system-111827)](https://github.com/frankxai/agentic-operating-system-standard)
[![Status](https://img.shields.io/badge/status-public%20starter-0f766e)](./docs/MODULE_CHARTER.md)

Agentic Investor OS helps investors, founders, angels, accelerators, and portfolio operators turn scattered opportunities into structured diligence, memos, risk registers, and support loops.

It is a workflow and research-organization system. Investment, legal, tax, accounting, and regulated decisions require qualified human review.

## First-Win Workflow

```text
thesis -> opportunity intake -> diligence queue -> memo -> risk register -> decision gate -> portfolio support loop
```

## What It Produces

| Artifact | Purpose |
|---|---|
| Thesis brief | Defines mandate, market lens, exclusions, and evidence needs. |
| Opportunity intake | Captures startup, asset, fund, market, or partnership context. |
| Diligence memo | Summarizes evidence, questions, risks, and decision criteria. |
| Risk register | Tracks business, market, technical, legal, financial, and execution risks. |
| Portfolio support plan | Turns post-decision help into concrete 30-day support. |
| Investor update brief | Converts portfolio state into clear stakeholder communication. |

## Agent Swarm

| Agent | Output |
|---|---|
| Thesis Architect | Thesis, mandate, exclusions, and evidence bar. |
| Deal Intake Analyst | Opportunity summary and missing information list. |
| Diligence Lead | Evidence queue, source needs, and open questions. |
| Market Analyst | Market map and competition questions. |
| Product Analyst | Product, user, workflow, and differentiation notes. |
| Technical Analyst | Architecture, implementation, and technical-risk notes. |
| Memo Editor | Investor memo or founder-facing packet. |
| Portfolio Support Lead | 30-day support plan and operating cadence. |
| Compliance Sentinel | Blocks regulated claims and routes expert review. |

## Core Files

| File | Purpose |
|---|---|
| [AGENTS.md](./AGENTS.md) | Agent roles and repo rules. |
| [SKILLS.md](./SKILLS.md) | Skill inventory and activation model. |
| [WORKFLOWS.md](./WORKFLOWS.md) | Canonical investor workflows. |
| [LOOPS.md](./LOOPS.md) | Operating loops for thesis, diligence, portfolio, and communication. |
| [registry/investor-os.json](./registry/investor-os.json) | Machine-readable module registry. |
| [templates](./templates) | Diligence memo, risk register, and support-plan templates. |
| [examples](./examples) | Public-safe example intake. |

## Standard Alignment

This repo implements the [Agentic Operating System Standard](https://github.com/frankxai/agentic-operating-system-standard) as an Investor OS module.

Compliance target: `L3-agent-os` moving toward `L4-standard-module`.

## Use It

Validate:

```bash
npm run validate
```

Start a memo:

```bash
cp templates/diligence-memo.md docs/work-in-progress-memo.md
```

Start a risk register:

```bash
cp templates/risk-register.md docs/work-in-progress-risk-register.md
```

## Safety

- No autonomous investment decisions.
- No legal, tax, accounting, securities, or compliance conclusions.
- No confidential company data in public examples.
- No public claims without evidence.
- No outreach or publication without human approval.

## Commercial Path

The public repo is the starter. Paid offers can include diligence sprints, portfolio support systems, investor update systems, data-room organization, and private pro plugins.
