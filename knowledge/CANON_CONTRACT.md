# Investor Canon Contract

Status: `v0.1` — public-safe Golden Pack  
HITL: every card ships as `pending_human_review` until Frank accepts it  
Not a securities recommendation. Not a trading system.

## Ground truth

1. Human primary sources only: shareholder letters, filings, whitepapers, lecture notes, dated memos.
2. LLMs may tag and chunk. They may not originate canon.
3. A concept card is an original mechanism + attribution + failure modes. It is not a book dump.
4. No row in `RIGHTS.jsonl` → no card.
5. Public git gets short quotes (≤90 words) plus original agent directives. Full PDFs stay out of git.
6. Vector search is non-authoritative. The card file + hash wins.
7. Compliance Sentinel (see `AGENTS.md`) still gates any live use.

## What this pack is

Educational research substrate for Investor OS agents: how to *think* about evidence, ownership, and protocol mechanics.

## What this pack is not

- A model portfolio
- A buy/sell signal
- A substitute for 10-K reading
- A dump of Graham/Munger/Taleb copyrighted books (those stay private-cold if purchased)

## Card rules

- YAML frontmatter must validate against `schema/concept-card.schema.json`
- `source.quote` is optional; if present, ≤90 words, verbatim, with URL + SHA-256 of the retrieved artifact
- `agent_directive` must name a fail-closed behavior
- Forbidden in this repo: machine paths, “guaranteed” outcome language, personalized conclusions

## Storage

| Layer | Here |
|---|---|
| Rights | `knowledge/RIGHTS.jsonl` |
| Semantic hub | `knowledge/cards/` |
| Evals | `knowledge/evals/` |
| Cold originals | not in git (`knowledge/_raw/` ignored) |
| Runtime | cite `id` from memos; no citation → fail eval |

## Validation

```bash
python scripts/validate_canon.py
python scripts/dcf_educational.py --self-test
npm run validate
```
