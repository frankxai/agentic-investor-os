---
id: inv-damodaran-cost-of-capital-is-a-dataset
type: definition
domain: investor
license: source-permitted-commentary
public_ok: true
hitl_status: pending_human_review
source:
  title: Damodaran Cost of Capital dataset page
  url: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/wacc.html
  retrieved: "2026-08-21"
  quote: ""
failure_modes:
  - Freezing last year's industry WACC as a law of nature
  - Applying a US industry mean to a single private company without adjustment
  - Using WACC as a buy trigger
agent_directive: >-
  If a memo cites WACC, require the Damodaran (or filing) vintage date,
  geography, and that it is an input to an educational model, not a verdict.
---

# Cost of capital is dated data

Damodaran’s NYU page is a teaching dataset titled “Cost of Capital.”
Industry costs of capital are **empirical snapshots**, updated, not
eternal constants.

This card carries no numeric table on purpose. Numbers go stale; the
method does not: name the date, the industry mapping, and the gap
between a mean and the company under study.

Pair with `scripts/dcf_educational.py` for formula self-tests only.
