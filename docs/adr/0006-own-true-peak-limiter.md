---
status: accepted
date: 2026-11-08
---
# Use a look-ahead true-peak limiter, not pedalboard's Limiter

## Context and Problem Statement
The chain ends in a true-peak limiter at the ceiling (ADR-0005). pedalboard's `Limiter` is not a ceiling: it adds make-up gain. A -6 dB threshold put a test tone at 0 dBFS, and driven to loudness it left 1529 clipped flat-top runs on one track (`CLAUDE.md:13`; `docs/listen-and-measure.md:25`).

## Considered Options
* pedalboard's `Limiter`
* A look-ahead limiter that keeps the 4x-oversampled (true) peak under the ceiling (`src/gain_of_thrones/limiter.py:13-14`)

## Decision Outcome
Chosen option: "A look-ahead limiter that keeps the 4x-oversampled (true) peak under the ceiling", because at the same loudness it left 0 flat-top runs where pedalboard's left 1529 (`docs/listen-and-measure.md:25`), and 4x-oversampled true-peak limiting is what the research names for holding inter-sample peaks (`docs/research/heavy-metal-punk.md:59`, `:81`).

### Consequences
* Good, because renders don't clip: tests cover bursts and a spike, an inter-sample peak, hard driving, and leaving the signal alone away from peaks (`tests/test_limiter.py:10`, `:20`, `:29`, `:39`).
* Good, because rendering and export use the same true-peak meter (`src/gain_of_thrones/limiter.py:8`; `src/gain_of_thrones/export.py:9`).
* Bad, because the project maintains its own limiter DSP rather than using a library's (inferred).

## More Information
Evidence: `CLAUDE.md:13`; `src/gain_of_thrones/limiter.py:1-2`, `:13-14` (commit f73587b); `tests/test_limiter.py`; `docs/listen-and-measure.md:25`. The date is the first commit; earlier history is not in git. Related: ADR-0005, ADR-0012.
