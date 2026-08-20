---
id: inv-extraction-queue
type: queue
domain: investor
license: pending-extraction
public_ok: true
hitl_status: pending_human_review
source:
  title: Extraction queue (no quotes)
  url: https://www.oaktreecapital.com/insights
  retrieved: "2026-08-21"
failure_modes:
  - Writing a Marks or Dalio card from memory
agent_directive: >-
  Do not emit Howard Marks or Dalio quotes until RIGHTS.jsonl shows a
  sha256 on a retrieved text artifact.
---

# Do not fake the rest

Queued, **not extracted this pass**:

- Howard Marks, “The Illusion of Knowledge” (Oaktree page was JS-gated)
- Dalio, *Principles for Navigating Big Debt Crises* (free PDF, author site)
- SEC EDGAR 10-K parser as a tool, not a card
- FRED series catalog

Until those hashes exist, agents may **link** the URL and stop.
