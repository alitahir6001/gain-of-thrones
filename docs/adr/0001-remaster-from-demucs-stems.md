---
status: accepted
date: 2026-11-05
---
# Remaster from Demucs stems, not the stereo master alone

## Context and Problem Statement
Gain of Thrones starts from a finished, already-limited CD master, not from multitracks (`README.md:28`). The complaints the research mapped (cloudy guitars, a buried vocal, lost cymbals) are masking problems between instruments, which EQ on the whole mix can't pull apart (`docs/research/heavy-metal-punk.md:7`, `:88`). Which signal should the tool work on?

## Considered Options
* Separate with Demucs `htdemucs_ft`, then process and rebalance each stem
* Separate with `htdemucs`, about 4x faster than `htdemucs_ft`, which "might be a bit better" (`docs/research/heavy-metal-punk.md:25`)
* Process the stereo master only (inferred from `docs/research/heavy-metal-punk.md:88`: "stem separation now makes masking-reduction EQ possible on a finished master")

## Decision Outcome
Chosen option: "Separate with Demucs `htdemucs_ft`, then process and rebalance each stem", because stems are what make masking-reduction EQ possible on a finished master (`docs/research/heavy-metal-punk.md:88`), and the research's chain specifies `htdemucs_ft` with several shifts and float stems (`docs/research/heavy-metal-punk.md:74`).

### Consequences
* Good, because each instrument gets its own EQ, dynamics and level before the stems are summed (`src/gain_of_thrones/master.py:1`).
* Bad, because separation is imperfect: the "other" stem, which holds the guitars, scores only 6.32 dB SDR (`docs/research/heavy-metal-punk.md:19`), so moves must stay small (ADR-0002).
* Bad, because splitting is slow: about 3.8 s per second of audio on an Apple Silicon CPU, since this model crashes on MPS (`CLAUDE.md:16`).
* Bad, because `--shifts` is random, so splitting the same track twice gives slightly different stems (`CLAUDE.md:21`).

## More Information
Evidence: `docs/research/heavy-metal-punk.md:7`, `:19`, `:25`, `:74`, `:88`; `README.md:5`, `:28`; `src/gain_of_thrones/separate.py:1-3` (commit fe58d44); `src/gain_of_thrones/master.py:1` (commit 69e71cd). The date is when the research notes were compiled (`docs/research/heavy-metal-punk/general_mastering.md:3`); the code entered git on 2026-11-08. Related: ADR-0002, ADR-0003, ADR-0007.
