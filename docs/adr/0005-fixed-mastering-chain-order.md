---
status: accepted
date: 2026-11-05
---
# One fixed mastering chain; presets fill in only the per-stem stages

## Context and Problem Statement
The research combined sourced ordering rules (compressor before limiter, true-peak control last among the processors, dither once at the end) with inferred placement for the separation steps (`docs/research/heavy-metal-punk.md:67`). Presets needed one fixed order to plug into.

## Considered Options
* The research's full chain, including an optional repair stage and a broad bus EQ (`docs/research/heavy-metal-punk.md:69-82`)
* Multiband bus compression, which the research's sources advise against (`docs/research/heavy-metal-punk.md:59`, `:80`)
* A fixed engine order, with presets filling in only the per-stem stages: stems, preset chains, explicit balance, plus the residual, then bus compressor, true-peak limiter and dither (`src/gain_of_thrones/master.py:1`)

## Decision Outcome
Chosen option: "A fixed engine order", because it keeps the sourced order and puts every tonal move in the per-stem chains, where the envelope applies (inferred: `src/gain_of_thrones/master.py:1` has no bus EQ, and ADR-0004 drops repair). The settings sit inside the research's ranges: a 2:1 bus compressor with 35 ms attack and 120 ms release (`src/gain_of_thrones/presets/heavy_guitar.py:49`; `docs/research/heavy-metal-punk.md:80`), a -1.2 dBTP ceiling (`src/gain_of_thrones/presets/heavy_guitar.py:51`; `docs/research/heavy-metal-punk.md:81`), and flat TPDF dither to 24-bit (`src/gain_of_thrones/master.py:69`; `docs/research/heavy-metal-punk.md:82`).

### Consequences
* Good, because every stage's job is sourced, or labelled as inference, in one table (`docs/research/heavy-metal-punk.md:69-82`).
* Good, because the bus compressor's threshold is searched per track to take a set amount of loudness off (about 1.5 dB), so it works about as hard on any source (`src/gain_of_thrones/master.py:23-24`).
* Bad, because there is no bus EQ stage, so a whole-mix tilt has to be built from per-stem moves (inferred).

## More Information
Evidence: `docs/research/heavy-metal-punk.md:59`, `:65-82`; `src/gain_of_thrones/master.py:1`, `:23-24`, `:56`, `:63`, `:69` (commit 69e71cd); `src/gain_of_thrones/presets/heavy_guitar.py:49`, `:51` (commit 3dcab1d). The date is when the research notes were compiled (`docs/research/heavy-metal-punk/general_mastering.md:3`). Related: ADR-0003, ADR-0004, ADR-0006.
