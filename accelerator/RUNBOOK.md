# Accelerator OS Runbook

## 1. Roles in a real installation

- **Program owner:** owns thesis, policy, capacity, acceptance, and external relationships.
- **Program director profile:** routes work and prepares decision/support packets.
- **Evidence lab profile:** conducts public and explicitly authorized research.
- **Venture builder profile:** works inside one accepted company's private repo.
- **Portfolio operator profile:** compiles scorecards, support, costs, and program learning.
- **Independent verifier profile:** checks consequential output using a different model/provider.
- **Governance sentinel:** may block; it never grants legal/compliance approval.

## 2. Session and task contract

Every run begins with a task envelope containing:

- institution, program, and optional company tenant IDs;
- workflow and stage;
- assigned agent/profile;
- objective and done-condition;
- allowed tools and write scopes;
- input and evidence references;
- autonomy ceiling;
- budget and deadline;
- required verifier and approval gates.

No envelope means no autonomous work.

## 3. Daily program cycle

1. The Program Director reads the durable board, not chat history.
2. It validates tenant scope and reclaims stale tasks.
3. It routes ready tasks to event-eligible agents.
4. Agents write artifacts and evidence records to their assigned tenant.
5. Consequential artifacts move to Independent Verifier.
6. Governance Sentinel checks privacy, claims, permissions, and gates.
7. Passed internal work advances automatically only through A0–A3 stages.
8. Gated actions remain pending with a human-readable approval request.
9. Program Director publishes an internal daily brief: completed, blocked, cost, evidence gaps, and decisions needed.

Recommended schedules:

- every 15 minutes: queue health and stale-claim recovery (script-only where possible);
- daily: application intake normalization and evidence freshness scan;
- weekly: company scorecard/support review;
- monthly: portfolio review, cost attribution, retention review, anonymized learning candidates;
- never scheduled without human gate: outreach, public posts, acceptance, investment, production, spend.

## 4. Application and selection workflow

### Intake

- Require consent and a data-classification label before analysis.
- Normalize only supplied/public information.
- Record missing information rather than infer it.
- Create a separate tenant space immediately.

### Screening

- Apply explicit thesis criteria and disqualifiers.
- Produce fit dimensions, not a magical composite score.
- A low fit score routes to a stop recommendation; it does not auto-reject.

### Diligence

- Build a question graph across market, product, technical, team, GTM, economics, legal/compliance, and impact as relevant.
- Each claim carries evidence state: observed, sourced, founder-asserted, inferred, contradicted, stale, or unknown.
- Research agents may use public sources autonomously. Private demos, repos, data rooms, paid sources, references, or security tests require scoped authorization.
- Stop when the predeclared evidence bar is met or the budget/timebox is exhausted.

### IC packet

- Memo Editor synthesizes thesis fit, evidence, contradictions, risks, missing information, and possible support plan.
- Independent Verifier tests source coverage and reasoning.
- Governance Sentinel confirms that the packet is decision support, not an autonomous recommendation.
- The named human records accepted, rejected, or hold.

## 5. Day-0 Company OS

After acceptance:

1. create a private company repo or isolated workspace;
2. issue the tenant manifest and retention policy;
3. provision only approved memory and tools;
4. map company goals to the smallest relevant Agentic Business OS/Creator OS modules;
5. create a 30-day backlog with owners and evidence of done;
6. create product, GTM, operations, founder, and proof lanes only when needed;
7. send no invitations/imports until approved;
8. activate after an onboarding verifier confirms isolation and rollback.

Default first 30 days:

- Week 1: truth baseline, customer/problem evidence, operating dashboard.
- Week 2: one product or offer experiment.
- Week 3: one distribution/customer-discovery loop.
- Week 4: proof review, support plan, cost/value assessment.

## 6. Weekly company loop

```text
capture facts -> compare with milestones -> identify blocker
-> route one support lane -> execute bounded work
-> verify -> founder review -> learning record
```

The system should prefer one resolved constraint over ten generic recommendations.

Company scorecard fields:

- declared milestone;
- observed evidence;
- customer/product/GTM/operations state;
- top constraint;
- support action and owner;
- risk delta;
- agent/tool cost;
- next proof event;
- founder confirmation or correction.

## 7. Portfolio loop

- Each company is processed independently first.
- Portfolio Operator receives approved scorecard summaries, not raw company workspaces.
- Cross-company learning is a candidate until anonymization and human approval pass.
- Benchmarks include cohort definition, sample size, time window, metric definition, and uncertainty.
- No fund-level model learns from private company material by default.

## 8. Tool policy

### Hermes

- Kanban: durable work queue and dependencies.
- Delegation: bounded research/review only; children inherit tenant scope.
- Cron: internal scans and packet generation; never human-gated side effects.
- Profiles: five permission/model boundaries, not organizational decoration.
- Skills: versioned procedures loaded by task.
- Gateway: notify humans; chat does not replace task state.

### SIS

- Search only the tenant vault mounted for the task.
- Append evidence, decisions, and lessons with idempotency keys.
- Use public/shared vaults only for approved non-confidential material.
- Treat current SIS MCP fragmentation as an integration constraint: use the supported operational `sis_*` facade and route writes through the canonical gateway as it consolidates.

### GitHub and coding agents

- One company repo/worktree per writing lane.
- Draft PR first; tests and verifier verdict required.
- No automatic merge, deployment, migration, secret handling, or billing action.
- Company repos remain private unless separately approved.

### Research tools

- Preserve URL, timestamp, extracted claim, evidence state, and confidence.
- Prefer primary sources.
- Never contact founders, customers, competitors, or references without approval.

## 9. Failure and escalation

Immediately pause a task on:

- tenant mismatch or missing tenant ID;
- attempted access outside allowed scope;
- secret/PII leakage;
- unsupported consequential claim;
- tool/budget overrun;
- contradictory source evidence;
- failed verifier verdict;
- action requiring an absent approval;
- high or critical safety, legal, privacy, or reputational risk.

Recovery requires an incident record, containment, verifier verdict, and named human resume receipt for high/critical events.

## 10. Minimal pilot

Use synthetic/public-safe data first. Then run with one partner and a maximum of five consented companies. Scope the first pilot to either selection support or Day-0 OS installation; do not promise the entire platform at once.

Track:

- time from application to IC-ready;
- evidence completeness and stale-source rate;
- human overrides and reasons;
- founder activation within seven days;
- support task completion;
- model/tool cost per company;
- verifier failure rate;
- privacy/gate incidents;
- partner and founder satisfaction.

## 11. Promotion rule

The accelerator is ready for a paid partner pilot only when:

- synthetic end-to-end run passes;
- tenancy negative tests pass;
- gated state transitions fail closed;
- evidence and approval schemas validate;
- maker/checker separation is demonstrated;
- one Day-0 OS can be provisioned and rolled back;
- cost attribution works;
- public copy describes capabilities without outcome promises.

### Receipt and verifier invariants

- A company-scoped gate never accepts a null or different `companyId`.
- A receipt ID is consumed once; replay fails closed.
- `expiresAt` must contain an explicit timezone and be in the future.
- `ic_ready` requires a stored evidence record and a passing verifier verdict.
- Maker and verifier agent IDs and providers must differ.
