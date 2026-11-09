---
status: accepted
date: 2026-11-08
---
# Measure the MP3 gain after encoding, with one gain for the album

## Context and Problem Statement
Renders sit at a -1.2 dBTP ceiling (`src/gain_of_thrones/presets/heavy_guitar.py:51`), which is fine for lossless playback, but lossy copies should peak at -2 dBTP or lower (`docs/research/heavy-metal-punk.md:61`, `:81`). MP3 encoders overshoot the peaks of their input.

## Considered Options
* Predict the MP3 gain from the WAV peaks
* Encode, decode, measure the true peak, and lower the gain until every MP3 is at or under -2 dBTP (`src/gain_of_thrones/export.py:54-67`)

## Decision Outcome
Chosen option: "Encode, decode, measure", because the prediction failed: on the Freaks EP the predicted -0.8 dB left MP3s at up to -1.7 dBTP, and the measured answer was -1.16 dB (`docs/listen-and-measure.md:30`; `CLAUDE.md:20`). The gain is one value for the whole album, so the song-to-song levels survive (`src/gain_of_thrones/export.py:2`; ADR-0011).

### Consequences
* Good, because every MP3 is checked after encoding (`tests/test_export.py:27`).
* Good, because the FLAC export keeps the rendered samples unchanged at 24-bit (`src/gain_of_thrones/export.py:1`, `:42`; `docs/agent-tools.md:90`; `tests/test_export.py:39`).
* Good, because ReplayGain tags measured on the original are dropped, so players won't apply values that no longer match the levels (`src/gain_of_thrones/export.py:1-2`, `:33`).
* Bad, because the MP3s play about 1 dB quieter than the FLACs (inferred from the -1.16 dB gain in `docs/listen-and-measure.md:30`).

## More Information
Evidence: `src/gain_of_thrones/export.py:1-3`, `:11`, `:33`, `:40-42`, `:54-67` (commit ded1abf); `tests/test_export.py:27`, `:39`; `docs/agent-tools.md:89-90`; `CLAUDE.md:20`; `docs/research/heavy-metal-punk.md:61`, `:81`. The date is the first commit; earlier history is not in git. Related: ADR-0006, ADR-0011.
