---
id: inv-uniswap-v2-constant-product
type: protocol
domain: investor
license: source-permitted-commentary
public_ok: true
hitl_status: pending_human_review
source:
  title: Uniswap v2 Core
  url: https://uniswap.org/whitepaper.pdf
  retrieved: "2026-08-21"
  sha256: "967d8a7665376f51ccc2bc66a9b5ebe4d514f10d4dee7ec6706b45933bdb4896"
  quote: >-
    Each Uniswap v1 pair stores pooled reserves of two assets, and provides
    liquidity for those two assets, maintaining the invariant that the
    product of the reserves cannot decrease. Traders pay a 30-basis-point
    fee on trades, which goes to liquidity providers.
failure_modes:
  - Treating LP fees as “yield” without inventory risk / impermanent loss
  - Applying v2 invariant to v3 concentrated positions
  - Ignoring that contracts are non-upgradeable (named in the paper)
agent_directive: >-
  AMM notes must state the invariant, fee recipient, and what happens to
  LPs when the price moves. “APY” without inventory risk fails the card.
---

# Constant-product AMM (v1/v2)

Uniswap v2 keeps the v1 invariant: reserve product does not decrease
(fees aside). The 30 bp fee accrues to LPs. This is a **mechanical**
description.

Educational simulation of `x * y = k` belongs in code tests, not in a
memo as a return forecast.

**Limit:** v3/v4 are different designs. Do not cite this card for
concentrated liquidity.
