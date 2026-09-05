# AutonomousNegotiationProtocol

ANP is a GenLayer primitive for consensus-driven agreement formation between autonomous agents. It records an append-only proposal chain and finalizes only when identity, constraints, preference alignment, fairness, improvement, commitment, and freshness pass.

Deterministic logic enforces participant authority, exact term commitments, policy bounds, deadlines, round limits, and proposal continuity. Leader and validators independently assess alignment, fairness, and improvement, comparing decisions and bounded score buckets.

Finalized terms produce an immutable proof-root certificate. Execution is bound to the certified terms hash and protected against replay.

## Consensus boundary

- Clients own UI, private preferences, and non-authoritative previews.
- ANP owns proposal history, policy enforcement, semantic consensus, certification, and replay protection.
- Private documents remain offchain; the contract stores hashes and concise evidence.

## Lifecycle

`POLICY → OPEN → PROPOSALS → COMMITMENTS → FINAL_REVIEW → FINALIZED → EXECUTED`

## Live deployment

- [StudioNet contract](https://explorer-studio.genlayer.com/address/0x708d3056B37cFb4B73f32B0A8050987268AdAf99)
- [Onchain lifecycle proofs](LIVE_PROOFS.md)

## Validate

```bash
genvm-lint check contracts/AutonomousNegotiationProtocol.py
```
