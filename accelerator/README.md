# Accelerator OS

A governed operating system for running an accelerator, venture studio, or portfolio-support program with agent swarms.

This pack is the executable bridge between Agentic Investor OS and a real program. It defines runtime profiles, agents, skills, workflows, tenant boundaries, evidence records, approvals, and a local control-plane CLI.

It does **not** let agents invest, accept companies, send external messages, move money, make regulated conclusions, or cross tenant boundaries.

## The operating model

```text
public application
  -> consent + tenant assignment
  -> intake swarm
  -> selection swarm
  -> evidence room + IC packet
  -> named human decision
  -> Day-0 company OS
  -> venture-builder swarm
  -> weekly company loop
  -> portfolio intelligence loop
  -> graduation / continuing support
```

The accelerator is one coherent system with five runtime profiles and event-activated role agents. Profiles are security boundaries. Agents are roles. Skills are procedures. Workflows are state machines. Kanban is the durable queue. SIS is the memory layer. Git and evidence records hold provenance. Chat is only a cockpit.

## Four planes

| Plane | Owns | Canonical substrate |
|---|---|---|
| Program control | program thesis, applications, stages, approvals, support queues | Accelerator OS registry + Hermes Kanban |
| Evidence and memory | sources, observations, contradictions, decision history, lessons | evidence records + SIS MCP/private vault |
| Company execution | Day-0 OS, product/GTM sprints, draft PRs, scorecards | private company repo + Agentic Business OS |
| Human governance | acceptance, investment, legal, spend, external sends, production | named approval receipts |

## Runtime profiles: five, not fifty

Do not create one Hermes profile per specialist or startup. Use profiles only where isolation, model policy, and tool permissions materially differ.

| Profile | Purpose | Max autonomy | Principal tools |
|---|---|---:|---|
| `program-director` | route work, maintain queues, synthesize operating state | A3 | Kanban, todo, delegation, file, SIS memory, cron |
| `evidence-lab` | public research and diligence artifacts | A2 | web, browser, X search, vision, code execution, file |
| `venture-builder` | bounded work inside an accepted company's private repo | A3 | terminal, file, code execution, browser, GitHub via CLI |
| `portfolio-operator` | support routing, scorecards, program learning | A3 | Kanban, file, memory, web, code execution, cron |
| `independent-verifier` | maker-not-checker validation and gate verdicts | A2 | read-oriented web, browser, file, terminal, vision |

An institution receives its own deployment or isolated `HERMES_HOME`. A company is a tenant namespace and private repo inside that institution, not another global profile. A verifier uses a provider/model different from the maker for consequential work.

## Autonomy ladder

| Level | Meaning | Examples |
|---|---|---|
| A0 | observe | read a permitted record, report state |
| A1 | analyze | research, compare, identify missing evidence |
| A2 | draft | create internal memos, plans, issues, scorecards |
| A3 | bounded execute | create reversible internal artifacts, draft PRs, run tests, enqueue tasks |
| A4 | human approval required | accept/reject, external send, invite, merge/deploy, spend, sensitive access |
| A5 | never autonomous | invest/move money, sign, make legal or compliance decisions, bypass tenancy |

Agents may autonomously run A0–A3 only within their allowlisted tenant, tools, budget, workflow stage, and done-condition. A4 actions wait for a scoped, unexpired named-human receipt. A5 actions have no agent path.

## Swarms

### Selection swarm

Triggered when a consented application enters the program.

- Intake Analyst normalizes the application.
- Thesis Fit Analyst scores fit against explicit criteria.
- Market, Product, and Technical Analysts gather source-backed observations.
- Diligence Lead owns the question/evidence graph.
- Memo Editor creates the IC packet.
- Governance Sentinel blocks unsupported claims or missing approvals.
- Independent Verifier checks source coverage and reasoning.

Output: an **IC-ready packet**, never an investment or acceptance decision.

### Company-launch swarm

Triggered only after a human acceptance receipt.

- Onboarding Operator obtains authorized workspace and data boundaries.
- Startup OS Architect selects modules and creates the company manifest.
- Product Builder creates a bounded 30-day delivery backlog.
- GTM Operator creates customer-discovery and channel experiments.
- Governance Sentinel reviews claims, permissions, and external actions.

Output: a private Day-0 Company OS, 30-day plan, and queued tasks.

### Portfolio-compounding swarm

Runs weekly/monthly for active companies.

- Portfolio Health Analyst compiles evidence-backed state.
- Support Router matches blockers to approved help lanes.
- FinOps Analyst attributes model/tool cost per company.
- Program Director allocates internal support capacity.
- Portfolio Operator creates the review packet and learning candidates.

Output: company scorecards, support queue, risks, and anonymization candidates. No cross-company raw-data sharing.

### Assurance swarm

Runs at each consequential gate and may block any other swarm.

- Governance Sentinel checks privacy, claims, conflict, regulatory, and approval requirements.
- Independent Verifier checks evidence/provenance with a different model/provider.
- A named human resolves gated decisions.

## Agent activation

Agents are not ambient personas. They activate from workflow events:

```text
application.created          -> Intake Analyst
application.normalized       -> Thesis Fit Analyst
screening.requested          -> Market + Product + Technical Analysts
diligence.questions_ready    -> Diligence Lead
diligence.evidence_ready     -> Memo Editor + Independent Verifier
ic.packet_ready              -> Governance Sentinel -> HUMAN
company.accepted             -> Company-launch swarm
company.week_started         -> Venture-builder lanes
portfolio.review_due         -> Portfolio-compounding swarm
risk.high_or_critical        -> Assurance swarm + pause
```

The machine-readable source is [`registry/accelerator-os.json`](./registry/accelerator-os.json).

## Skill contract

Every accelerator skill must declare:

1. trigger;
2. allowed profile and tools;
3. tenant and data classification requirements;
4. inputs and evidence minimum;
5. deterministic procedure;
6. output artifact;
7. approval gates;
8. stop/escalation conditions;
9. verification.

The initial skill pack is under [`skills/`](./skills/).

## Tooling

| Capability | Default | Rule |
|---|---|---|
| Orchestration | Hermes profiles + Kanban + delegation | durable task is a Kanban/task envelope, not chat |
| Scheduling | Hermes cron/webhook | only bounded internal scans; external sends remain gated |
| Memory | SIS operational MCP (`sis_*`) behind private tenant vaults | append evidence/decisions; no fund or company mixing |
| Public research | web/browser/X search | store source URL, observed time, quotation/claim, confidence |
| Code/product | GitHub + coding agents through private company repos | draft PR, tests, verifier; no automatic merge/deploy |
| Public intake | FrankX/Vercel application route | minimal data, consent, private ingestion |
| Communication | Telegram/Slack/email gateway | cockpit/notification only; approval before external send |
| Observability | event ledger + task/agent cost records | every run has tenant, agent, workflow, cost, result, evidence refs |

Start with Git/JSON/SQLite and private vaults. Introduce Postgres, object storage, queues, or a hosted control plane only when the pilot proves concurrency and tenancy needs. Do not start with a complex always-on platform.

## Data boundaries

```text
institution/<institution-id>/
  program/<program-id>/            # thesis, cohort, approvals
  companies/<company-id>/          # private company memory and artifacts
  shared/benchmarks/               # approved anonymized aggregates only
  audit/                            # immutable event and approval references
```

Required invariants:

- every task, artifact, evidence record, memory write, and cost record carries `institutionId`, `programId`, and where relevant `companyId`;
- an agent receives one tenant scope per run;
- raw company data never enters shared benchmarks;
- public Git contains only templates and synthetic examples;
- no private application or diligence data is written into this starter repo;
- deletion/export requests follow the institution's retention policy and remain human-controlled.

## Workflow state machine

```text
applied
 -> consented
 -> normalized
 -> screened
 -> diligence
 -> ic_ready
 -> HUMAN: accepted | rejected | hold
 -> onboarding
 -> active
 -> graduated | archived
```

The CLI blocks agent progression through the human decision boundary without an approval receipt reference.

## Local control-plane CLI

The CLI is intentionally stdlib-only and stores no secrets:

```bash
python scripts/accelerator_os.py validate
python scripts/accelerator_os.py init-program \
  --program-id synthetic-pilot \
  --name "Synthetic Pilot" \
  --output ./tmp/synthetic-pilot
python scripts/accelerator_os.py intake \
  --program ./tmp/synthetic-pilot \
  --application-id app-001 \
  --company-id company-synthetic-studio \
  --company "Synthetic Studio" \
  --source public-safe-demo \
  --consent-ref consent://synthetic/demo-only
python scripts/accelerator_os.py record-evidence \
  --program ./tmp/synthetic-pilot \
  --application-id app-001 \
  --evidence-id app-001/intake-v1 \
  --claim "Synthetic intake was normalized" \
  --state observed \
  --source-type experiment \
  --source fixture://app-001/intake \
  --title "Synthetic intake fixture" \
  --created-by intake-analyst \
  --confidence 0.8 \
  --data-class company-private
python scripts/accelerator_os.py advance \
  --program ./tmp/synthetic-pilot \
  --application-id app-001 \
  --stage normalized \
  --evidence evidence://app-001/intake-v1
python scripts/accelerator_os.py status --program ./tmp/synthetic-pilot
```

Ungated transitions resolve every `evidence://` reference to a typed record inside the same tenant. Transition to `ic_ready` additionally requires a passing verdict from the `independent-verifier` profile using a provider different from the maker.

`accepted`, `rejected`, `hold`, `onboarding`, and `active` are gated. Approval receipts must be company-bound, timezone-aware, unexpired, and single-use. The CLI verifies and consumes a receipt; it never authorizes or manufactures the decision. The human approval system remains outside the agent process.

## Pilot design

Run one program with five synthetic or fully consented companies:

1. intake and screening only for all five;
2. human-selected two proceed to a diligence sprint;
3. one accepted company receives a Day-0 OS and one 30-day support lane;
4. measure cycle time, evidence completeness, founder activation, support load, model/tool cost, false-positive gates, and human overrides;
5. do not deploy capital in the pilot.

## Success criteria

- 100% of consequential claims link to evidence records.
- 100% of cross-stage gated transitions have named approval receipts.
- 0 cross-tenant raw-data reads/writes.
- 100% of consequential maker output has an independent verifier verdict.
- support and model/tool costs are attributable per company.
- the system can reconstruct why a task ran, what it changed, and who approved the next gate.

## Install path

This public pack is the reference module. A real institution should deploy:

1. one private program instance;
2. isolated tenant data and SIS vault namespaces;
3. the five runtime profiles with minimum toolsets;
4. the skill pack;
5. Kanban workflows and event triggers;
6. private company repos for accepted companies;
7. a human approval service or signed receipt process.

See [`RUNBOOK.md`](./RUNBOOK.md) for the daily/weekly operating cadence.
