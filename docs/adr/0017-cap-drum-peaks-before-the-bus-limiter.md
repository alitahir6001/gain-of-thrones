---
status: accepted
date: 2026-11-21
---
# Cap the drum stem's peaks in heavy-guitar so the bus limiter stops ducking the mix

## Context and Problem Statement
After listening in the car to an album mastered with the stock `heavy-guitar` preset, the person heard "the volume adjusting itself" for a fraction of a second, again and again. Measured, the cause was the final true-peak limiter (40 ms look-ahead, about 120 ms recovery; `src/gain_of_thrones/limiter.py`): on every drum hit it turned the whole mix down 3-6 dB for 60-80 ms. At those moments the drum stem alone peaked within 1-2 dB of the mix peak, with the other stems 18 dB or more below it. So the guitars and vocal ducked with every hit. The question was how to stop that without losing loudness or the snare, and whether the fix belongs in the shipped preset or stays opt-in like `crack_lift` (ADR-0016).

## Considered Options
* Lower `--target` until the dips go away
* Cap the drum stem at its own true peak minus 3 dB
* Cap the drum stem at its own true peak minus 5 dB
* Cap the drum stem at the lower of its true peak minus 5 dB and the raw stems' loudness plus 10.77 dB, as a generic opt-in stage
* The same cap, in the shipped `heavy-guitar` drum chain

## Decision Outcome
Chosen option: "The same cap, in the shipped `heavy-guitar` drum chain", because it won three blind, level-matched A/Bs on three tracks and two albums. One of those albums needed it and one hardly did. The person chose to ship it rather than keep it opt-in (2026-11-21).

`dsp.drum_cap_db(drum_tp, mix_lufs)` is the rule: `min(drum_tp - 5, mix_lufs + 10.77)`. `dsp.drum_peaks` measures both from the processed drum stem and the raw stems' sum, then runs `tp_limit` with a 5 ms look-ahead at that ceiling (`src/gain_of_thrones/dsp.py`). It is the last stage of the drum chain (`src/gain_of_thrones/presets/heavy_guitar.py`). The 10.77 dB is where "peak minus 5" landed on the first track it won. It stops looser caps on tracks whose drums peak higher above the mix.

### Consequences
* Good, because the dips drop several times over. On the first album, dips over 3 / 4 dB per minute went from 38.9 / 21.2 to 9.2 / 1.3 on the track that won first, and from 91.8 / 70.6 to 31.2 / 4.6 on the densest one. The bus limiter's GR max fell on all 12 tracks (for example 8.2 to 5.1 dB).
* Good, because loudness, the ceiling and clipping are unchanged: every render stays within 0.03 LU of its target and at -1.30 dBTP with no flat-tops. On the second album, dips over 3 dB per minute on the track that won went from 21.3 to 9.8.
* Good, because the snare proxy barely moves. Body / attack / snap changed by -0.06 / -0.06 / -0.13 dB on the second album's test track, and by at most 0.02 dB on the track where `crack_lift` had won.
* Good, because the shipped preset reproduces the winning session render byte for byte (re-rendered 2026-11-21).
* Bad, because on tracks with no dips the cap still takes up to 5 dB off the drum peaks. On the second album, "peak minus 5" was the lower limit on all six tracks (5.5-6.6 dB over the stems' loudness), so the 10.77 dB limit never acted there.
* Bad, because the maintainer regression numbers in `CLAUDE.md` change: on its track at -10.8 LUFS, limiter GR max goes from 3.4 to 2.8 dB and the time active from 20% to 15%.

## More Information
Evidence: the session logs (`notes.md` in each gitignored work folder; first album "Session 2 (2026-11-21): car-test dips", second album's dip measurements of 2026-11-21). A dip is a run of 10 ms frames whose maximum bus-limiter GR exceeds 3 or 4 dB. Blind A/B outcomes: "peak minus 5" beat stock and "peak minus 3" ("I could hear the dips in the other two"); the min rule beat stock and "peak minus 5" on the densest track ("I heard the dips in heavy guitar version"); on the second album it beat the approved session preset without the cap. Lowering `--target` was the session-1 answer to the same complaint ("dip at random times"), at a cost in loudness the person didn't want. Related: ADR-0006 (the bus limiter), ADR-0008 (blind level-matched A/B), ADR-0016 (crack_lift stayed opt-in on one track's evidence).

Later evidence (2026-11-22; the decision above is unchanged): on a second-album track that barely dips (1.9 dips over 3 dB per minute without the cap, 1.0 with it; cap active 2%; snare proxy within 0.02 dB), the person picked the version **without** the cap in a blind round (`abtest-picks.tsv` in that work folder). That makes the blind record 3 wins and 1 loss, and the loss is on the kind of track the "Bad, because" above describes. Two more rounds on tracks with no dips favored the cap, but only after Reveal, so they don't count as blind.
