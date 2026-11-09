---
status: accepted
date: 2026-11-08
---
# Carry one loudness shift across the whole album

## Context and Problem Statement
A single-track A/B picks a winning loudness for one song. Applying it to an album means setting targets for tracks whose original loudness differs.

## Considered Options
* One shift for every track, so the loudest lands at the target (`src/gain_of_thrones/album.py:1-2`)
* A separate loudness target per track (inferred from `src/gain_of_thrones/album.py:1-2`, which aims to keep "the CD's song-to-song levels")

## Decision Outcome
Chosen option: "One shift for every track", because the CD's song-to-song levels survive and the album keeps its flow (`src/gain_of_thrones/album.py:1-2`; `README.md:13`; `docs/listen-and-measure.md:15`).

### Consequences
* Good, because a single-track winner carries over by arithmetic: the shift is the winner's LUFS minus that track's original, and the target is the loudest original plus the shift (`docs/agent-tools.md:83`).
* Good, because the shift is tested: the loudest track lands on the target, and the differences between tracks survive (`tests/test_album.py:6`, `:14`).
* Bad, because quieter tracks end up quieter than a per-track target would make them (inferred).

## More Information
Evidence: `src/gain_of_thrones/album.py:1-2`, `:15-19` (commit 0364057); `tests/test_album.py:6`, `:14`; `README.md:13`; `docs/listen-and-measure.md:15`; `docs/agent-tools.md:81-83`. The date is the first commit; earlier history is not in git. Related: ADR-0012.
