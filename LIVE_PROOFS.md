# Live StudioNet proofs

Contract: [`0x781382906eEd4C193B39386183eeC85440dF97a1`](https://explorer-studio.genlayer.com/address/0x781382906eEd4C193B39386183eeC85440dF97a1)

The source correction is committed in [`150e4fe`](https://github.com/ehsandto/autonomous-negotiation-protocol/commit/150e4fe): terminal sessions reject further proposals/commitments, finalize is pre-terminal only, and certificates cannot be overwritten after consumption.

| Proof | Transaction | Result |
|---|---|---|
| Corrected deployment | [`0x94fdf5...df0665`](https://explorer-studio.genlayer.com/tx/0x94fdf5893ff3a57b43ee76fc8cf88d3bb25b23ce62b1a6f727a13e3b82df0665) | Finalized, majority agreement |
| Session open (session-2) | [`0xc574f0...5d113`](https://explorer-studio.genlayer.com/tx/0xc574f04e5e2857182bd1685f292733f06d100dbeab6d6f7ff3c30a9105f5d113) | Accepted, 5-validator agreement |
| Proposal (prop-2) | [`0xc9a5df...70167`](https://explorer-studio.genlayer.com/tx/0xc9a5df86df56900112063746f33b4a47ff530041f75c04d68c3a725389270167) | Submitted onchain |
| Counterparty commitment | [`0x9b1b99...ea768`](https://explorer-studio.genlayer.com/tx/0x9b1b997efacae6091620c287150fd4b9b1c0744fc9ec8a81436cbf67070ea768) | Accepted, signed by counterparty |
| Owner commitment | [`0x2e2870...9e4f6`](https://explorer-studio.genlayer.com/tx/0x2e28708de00a56b21aee2a37cf43e7e9a8b77d0cd2f079a89ede24a3b999e4f6) | Accepted, signed by owner |
| Semantic finalization attempt | [`0xc5fa20...9045b`](https://explorer-studio.genlayer.com/tx/0xc5fa20959f4b8d42c0ff25691d54cf2332dc7afe273a84b52fcb77d07ed9045b) | Accepted consensus transaction; validator semantic disagreement means no certified execution claim |
| Deployment | [`0xec7b11...8973a0`](https://explorer-studio.genlayer.com/tx/0xec7b11f2c2ef2de9ef9be2054d7bf5256c8df778320c9b8559eed933efe8973a0) | Accepted, 5/5 validator agreement |
| Bounded policy | [`0x5c5076...81edfe`](https://explorer-studio.genlayer.com/tx/0x5c50767246ebf869fceb6baa519d2ba4273d436037b6708d2107984c0481edfe) | Accepted |
| Negotiation session | [`0x8fa920...95cf22`](https://explorer-studio.genlayer.com/tx/0x8fa9209dba6b5f350a28a2f7f9619eb12794354a33b4f1da719d7c26b295cf22) | Accepted |
| Terms proposal | [`0xb3dfda...d204fe`](https://explorer-studio.genlayer.com/tx/0xb3dfda7be62a8deee6ff461794b44682bfe79350576fc1c9ef30d6483fd204fe) | Constraints passed |
| Party B commitment | [`0xce2cc9...82844e`](https://explorer-studio.genlayer.com/tx/0xce2cc92f5e07aaa4a20053c0f77ed12a0bc26a922f6c257204fad3501982844e) | Exact terms committed |
| Semantic finalization | [`0x3b695c...07811c`](https://explorer-studio.genlayer.com/tx/0x3b695c399c357d106c71d2178017326df895fc148f3fe8be8453299ead07811c) | Accepted, consensus proof approved |
| Certificate execution | [`0x94e811...b4a74a`](https://explorer-studio.genlayer.com/tx/0x94e811a70bbc3891a56edefa36050c885430dc54e8029a72eefe64f7abb4a74a) | Executed, 5/5 validator agreement |

## Verified consensus output

- State: `EXECUTED`
- Fairness score: `88`
- Alignment score: `84`
- Proof root: `4135ac379d47adf35efc3964983c31336d03a6c4e06784458bd8435cc5e035a8`
- Certificate: `b7c33ff1b97b39b60f32b7977dbf5a5ad87356be84b124e1a3a8dd71b3d80d2e`

```json
{"identity":true,"constraints":true,"alignment":true,"fairness":true,"improvement":true,"commitment":true,"freshness":true}
```
