# Provenance

This repository is derived from [blader/humanizer](https://github.com/blader/humanizer) (MIT license, copyright 2025 Siqi Chen). Version 4.0.0 is maintained by Shakthivel Manivanan. This file records who contributed what, so that neither side's work is misattributed.

## Upstream (blader/humanizer, through v3.1.0)

- The Humanizer skill itself: the idea of an agent skill that removes signs of AI writing, its pattern catalog (26 patterns), its structure, and most of the text of `SKILL.md`.
- The package files: plugin manifests, `scripts/validate-package.py`, the README's install instructions and pattern tables, and the GitHub workflows.
- The patterns draw on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## This fork (v4.0.0, Shakthivel Manivanan)

These are original to this fork and came from its maintainer:

- **The direction of the fork:** a humanizer whose target is maximum naturalness under strict fidelity to what the writer actually said, rather than detector evasion.
- **The governing fidelity rules:** "sharpen feelings, never invent them", with optional reactions offered separately from the rewrite, and strict preservation of magnitude, certainty, causation, scope, and conclusions.
- **The academic-writing direction:** treating calibrated hedging as human, overclaiming and stock transitions as AI, and using register research (participial clauses, nominalizations, lexical diversity) as evaluation signals.
- **The evaluation design:** blind pairwise comparison against earlier versions in both presentation orders, explicit tests for invented feelings and magnitude distortion, and treating detector output as a signal rather than ground truth.
- **The "personality and soul" voice guidance** the maintainer brought in, adapted here so that it adds no invented content.

## Where each contribution lives

The upstream history is kept in full; the 4.0 work is in the commits below.

| Contribution | Where to see it | Commit |
|---|---|---|
| Strict-fidelity goal | `SKILL.md` "How to work" step 2, README "What 4.0 changes" | [`dccbe14`](https://github.com/SHAKTHI2207/humanizer/commit/dccbe14), [`4bfe3b6`](https://github.com/SHAKTHI2207/humanizer/commit/4bfe3b6) |
| Sharpen feelings, never invent them | `SKILL.md` "Voice" and "What to return" | [`dccbe14`](https://github.com/SHAKTHI2207/humanizer/commit/dccbe14) |
| Magnitude and claim-strength preservation | `SKILL.md` "How to work" step 2; `eval/samples/19`–`23` | [`dccbe14`](https://github.com/SHAKTHI2207/humanizer/commit/dccbe14), [`771bcf7`](https://github.com/SHAKTHI2207/humanizer/commit/771bcf7) |
| Academic-register rules | `SKILL.md` "Voice" (academic bullet), §9, §12, §13 | [`dccbe14`](https://github.com/SHAKTHI2207/humanizer/commit/dccbe14) |
| Blind judging in both presentation orders | `eval/blind_pairs.py`, `eval/judge.py`, `eval/blind/` | [`771bcf7`](https://github.com/SHAKTHI2207/humanizer/commit/771bcf7) |
| Invented-feeling and distortion tests | `eval/test_fidelity.py`, `keep`/`forbid` in `eval/samples/` | [`771bcf7`](https://github.com/SHAKTHI2207/humanizer/commit/771bcf7) |
| Detector evidence and its interpretation | README "Detectors: what is documented and what is not" | [`4bfe3b6`](https://github.com/SHAKTHI2207/humanizer/commit/4bfe3b6) |
| Human evaluation design | `eval/human_eval.py`, `eval/human/` | [`771bcf7`](https://github.com/SHAKTHI2207/humanizer/commit/771bcf7) |

The upstream history (everything up to [`225a6f3`](https://github.com/SHAKTHI2207/humanizer/commit/225a6f3), blader/humanizer 3.1.0) is unchanged in this repository.

## How the v4.0.0 code and text were produced

The fork's changes were implemented with an AI coding assistant (Claude) working under the maintainer's direction. That covers the edits to `SKILL.md`, the evaluation harness in `eval/` (`tells.py`, `test_fidelity.py`, `run.py`, `judge.py`, `blind_pairs.py`), the evaluation samples, and the documentation. The maintainer set the goals, the rules, and the acceptance criteria and made the design decisions; the assistant wrote most of the code and prose. The blind evaluations were run with separate model instances as rewriters and judges.

## Evidence used, not origin

- Turnitin's public "AI writing detection capabilities FAQs" (read in October 2026): used to understand how a widely used detector describes itself. See the README's "Detectors" section for what it does and does not say.
- Reinhart et al. (2025), "Do LLMs write like humans? Variation in grammatical and rhetorical styles", *PNAS*, doi:10.1073/pnas.2422455122.
- Liang et al. (2023), "GPT detectors are biased against non-native English writers", *Patterns*, doi:10.1016/j.patter.2023.100779.

These informed and validated the implementation. They are not the source of the fork's idea.
