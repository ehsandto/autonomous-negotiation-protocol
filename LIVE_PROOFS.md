# Live StudioNet proofs

Contract: [`0x781382906eEd4C193B39386183eeC85440dF97a1`](https://explorer-studio.genlayer.com/address/0x781382906eEd4C193B39386183eeC85440dF97a1)

The source correction is committed in [`150e4fe`](https://github.com/ehsandto/autonomous-negotiation-protocol/commit/150e4fe): terminal sessions reject further proposals/commitments, finalize is pre-terminal only, and certificates cannot be overwritten after consumption.

| Proof | Transaction | Result |
|---|---|---|
| Corrected deployment | [`0x94fdf5...df0665`](https://explorer-studio.genlayer.com/tx/0x94fdf5893ff3a57b43ee76fc8cf88d3bb25b23ce62b1a6f727a13e3b82df0665) | Finalized, majority agreement |
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
