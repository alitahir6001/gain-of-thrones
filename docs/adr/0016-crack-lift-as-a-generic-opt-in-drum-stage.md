---
status: accepted
date: 2026-11-09
---
# Offer crack_lift as a generic opt-in drum stage, not a preset default

## Context and Problem Statement
In the first real remaster session, the person kept hearing the CD's snare as better: it had more crack and snap, and less wash around it. A lift of the drum stem's 3-8 kHz attacks (`crack_lift`, at most +2 dB) then won a blind, level-matched A/B. That was one track's evidence, and the code lived only in the session's preset copy in the gitignored work folder (`.ai/handoff.md:19` at a6b4d9f). The research names both halves of the move: a transient shaper on the drum stem with attack up and sustain neutral (inference), and 3-8 kHz as the snare's crack band (sourced) (`docs/research/heavy-metal-punk.md:48`, `:50`). The question was where it should live, given that `heavy-guitar`'s default output must stay byte-identical for the maintainer regression (`CLAUDE.md`).

## Considered Options
* Add crack_lift to heavy-guitar's default drum chain
* A new preset with crack_lift
* Define crack_lift in `heavy_guitar.py` but leave it out of its chains
* Leave it in the session's preset copy
* A generic drum stage in `dsp.py` that any preset can add

## Decision Outcome
Chosen option: "A generic drum stage in `dsp.py` that any preset can add", for three reasons. The move belongs to the drum stem, not to one genre: the maintainer turned down a "heavy-guitar-snare" preset because "Guitar is a guitar, and snare is drums" (2026-11-09). One track's evidence is too little to change a default. And the stock preset file stays untouched.

`dsp.transient_lift` is the band-limited lift: the 1 ms envelope minus the 30 ms one, times `amount`, clipped to 0..`max_db`, smoothed over 2 ms. `dsp.crack_lift` is the ready stage with the values that won (3-8 kHz, x0.5, max +2 dB) (`src/gain_of_thrones/dsp.py:30-45`). A preset copy turns it on with one import and one entry at the end of its `"drums"` chain (`docs/agent-tools.md`, `got master`).

### Consequences
* Good, because heavy-guitar's default output is unchanged. `heavy_guitar.py` is not touched, and re-rendering the stock preset on the same stems was byte-identical before and after the change (2026-11-09).
* Good, because the stage reproduces the winning render: the session's preset, re-rendered with `dsp.crack_lift` in place of its own copy, was byte-identical to the render that won.
* Good, because synthetic tests pin its behaviour: attacks are lifted up to the cap, held notes and releases are left alone, and a kick-like low attack is untouched (`tests/test_dsp.py`).
* Bad, because the evidence is one track, and it was tested blind only with the drum-stem compressor already off. With the compressor on, it is untested.
* Bad, because it costs limiter work: on that track the limiter's maximum gain reduction rose from 2.8 to 3.1 dB.

## More Information
Evidence: the session's remaster log (`notes.md` in the gitignored work folder, "Session 2", round 8). It records the snap (5-8 kHz) local crest at drum-stem hits going from 6.54 to 7.70 dB (the CD: 7.65), the lift active 35% of the time with a mean of 0.7 dB, and limiter GR max 2.8 to 3.1 dB. The crest is a proxy that agreed with the ear in rounds 5 and 8 and disagreed in round 7. `.ai/handoff.md:19` at a6b4d9f records that an ADR for this was skipped until the repo held evidence. Related: ADR-0002 (a lift of at most 2 dB stays inside the separation envelope), ADR-0005 (presets fill in the per-stem stages), ADR-0010 (presets are Python modules, so a copy can import the stage).
