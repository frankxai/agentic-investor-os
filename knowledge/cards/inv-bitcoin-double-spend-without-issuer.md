---
id: inv-bitcoin-double-spend-without-issuer
type: protocol
domain: investor
license: source-permitted-commentary
public_ok: true
hitl_status: pending_human_review
source:
  title: "Bitcoin: A Peer-to-Peer Electronic Cash System"
  url: https://bitcoin.org/bitcoin.pdf
  retrieved: "2026-08-21"
  sha256: "db8f2e180a8e681e4f5c4a13dbd51180cd608cadb5f757a59fdda01665e7eb9a"
  quote: >-
    Digital signatures provide part of the solution, but the main benefits
    are lost if a trusted third party is still required to prevent
    double-spending. We propose a solution to the double-spending problem
    using a peer-to-peer network. The network timestamps transactions by
    hashing them into an ongoing chain of hash-based proof-of-work.
failure_modes:
  - Confusing “no issuer” with “no risk”
  - Treating price as the protocol
  - Ignoring the majority-hash-power attack model named in the paper
agent_directive: >-
  Crypto diligence must separate (1) protocol claim, (2) implementation,
  (3) market price. If an intake only has (3), fail it.
---

# Bitcoin’s actual problem statement

The paper is not a valuation. It is a design for electronic cash that
does not require a trusted party to stop double-spends, using a
timestamped proof-of-work chain.

**Agent use:** when a token is described as “like Bitcoin,” require the
double-spend / consensus story in one paragraph. Marketing adjectives
are not a protocol.

**Not implied:** that proof-of-work is the only valid design, or that
BTC is an asset to buy.
