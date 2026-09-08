# AutonomousNegotiationProtocol

ANP is a GenLayer primitive for consensus-driven agreement formation between autonomous agents. It records an append-only proposal chain and finalizes only when identity, constraints, preference alignment, fairness, improvement, commitment, and freshness pass.

Deterministic logic enforces participant authority, exact term commitments, policy bounds, deadlines, round limits, and proposal continuity. Leader and validators independently assess alignment, fairness, and improvement, comparing decisions and bounded score buckets.

Finalized terms produce an immutable proof-root certificate. Execution is bound to the certified terms hash and protected against replay. Commit and finalize are accepted only in pre-terminal review states; `FINALIZED`, `EXECUTED`, and `INVALID` are terminal. A certificate is write-once and execution marks it consumed without allowing replacement or reset.

## Consensus boundary

- Clients own UI, private preferences, and non-authoritative previews.
- ANP owns proposal history, policy enforcement, semantic consensus, certification, and replay protection.
- Private documents remain offchain; the contract stores hashes and concise evidence.

## Lifecycle

`POLICY → OPEN → PROPOSALS → COMMITMENTS → FINAL_REVIEW → FINALIZED → EXECUTED`

## Live deployment

- [Corrected StudioNet contract](https://explorer-studio.genlayer.com/address/0x781382906eEd4C193B39386183eeC85440dF97a1)
- [Onchain lifecycle proofs](LIVE_PROOFS.md)

## Validate

```bash
genvm-lint check contracts/AutonomousNegotiationProtocol.py
```
