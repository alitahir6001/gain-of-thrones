---
status: accepted
date: 2026-11-05
---
# Keep per-stem moves inside the separation envelope

## Context and Problem Statement
Demucs stems carry each other's bleed: the guitar stem holds vocal and cymbal bleed (`docs/listen-and-measure.md:19`). Remixing studies found that separation-based vocal boosts of up to 6 dB came with "small but perceptible" degradation (`docs/research/heavy-metal-punk.md:23`). How far can a preset move a stem before separation artifacts show?

## Considered Options
* Small moves only: EQ within ±3 dB at Q 1.5 or lower, stem gain within ±2 dB, no gate or expander on "other"
* Larger stem boosts, up to the 6 dB tested in the remixing literature (`docs/research/heavy-metal-punk.md:23`)
* Gating or expanding the "other" stem (`CLAUDE.md:14`)

## Decision Outcome
Chosen option: "Small moves only", because the research put the ceiling at about ±2 dB of stem gain and ±3 dB of wide EQ (`docs/research/heavy-metal-punk.md:7`, `:75`, `:77`), and a gate on "other" also gates the separation errors and makes them audible (`docs/listen-and-measure.md:26`). The gate ban covers stems that mix several instruments; a gate on the vocal stem was approved by ear (`CLAUDE.md:14`; `docs/adding-a-genre.md:6`).

### Consequences
* Good, because every preset and every session works to one shared limit (`.claude/skills/remaster-session/SKILL.md:16`; `docs/adding-a-genre.md:6`; `src/gain_of_thrones/presets/heavy_guitar.py:7-8`).
* Good, because the heavy-guitar values won a blind, level-matched A/B while inside it (`src/gain_of_thrones/presets/heavy_guitar.py:3-4`).
* Bad, because masking that would need more than 3 dB of cut or boost stays partly unresolved (inferred from the limits themselves).

## More Information
Evidence: `docs/research/heavy-metal-punk.md:7`, `:17-23`, `:75`, `:77`; `src/gain_of_thrones/presets/heavy_guitar.py:7-8` (commit 3dcab1d); `.claude/skills/remaster-session/SKILL.md:16`; `README.md:28`; `CLAUDE.md:14`; `docs/listen-and-measure.md:19`, `:26`. The date is when the research notes were compiled (`docs/research/heavy-metal-punk/general_mastering.md:3`). Related: ADR-0001, ADR-0013.
