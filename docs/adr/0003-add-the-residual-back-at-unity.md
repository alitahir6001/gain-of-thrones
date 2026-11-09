---
status: accepted
date: 2026-11-05
---
# Add the stem residual back at unity, before bus processing

## Context and Problem Statement
The four Demucs stems sum to the input minus about 1% of its energy, a residual around -21 dB (`docs/listen-and-measure.md:27`). That residual plausibly holds transients, cymbal top end and distortion the model didn't assign to any stem (`docs/research/heavy-metal-punk.md:21`). Should the mix be the sum of the processed stems alone?

## Considered Options
* Sum the processed stems only and drop the residual
* Add the residual back at unity into the mix bus, before bus processing (the residual is the input minus the stem sum)

## Decision Outcome
Chosen option: "Add the residual back at unity", because dropping it loses the transients and cymbal top end it carries (`docs/listen-and-measure.md:27`), and with every stem stage bypassed the mix then nulls exactly against the input, which makes a bypass null test possible (`docs/research/heavy-metal-punk.md:21`, `:78`).

### Consequences
* Good, because every render runs a null test: max |input - (stems + residual)| must be 0 (`src/gain_of_thrones/master.py:38-41`; `tests/test_master.py:29`; `docs/agent-tools.md:64`).
* Good, because content the split missed survives in every render (`docs/listen-and-measure.md:27`).
* Bad, because the residual is not processed: whatever it holds passes through at unity (inferred from `src/gain_of_thrones/master.py:56`).
* Bad, because a small residual is easy to misread as clean stems; it only means the stems sum back (`CLAUDE.md:15`; `docs/research/heavy-metal-punk.md:21`).

## More Information
Evidence: `docs/research/heavy-metal-punk.md:21`, `:78`; `src/gain_of_thrones/master.py:1`, `:39-41`, `:56` (commit 69e71cd); `CLAUDE.md:15`; `docs/listen-and-measure.md:27`. The date is when the research notes were compiled (`docs/research/heavy-metal-punk/general_mastering.md:3`). Related: ADR-0001, ADR-0005.
