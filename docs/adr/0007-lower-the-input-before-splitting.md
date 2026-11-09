---
status: accepted
date: 2026-11-08
---
# Lower the input 1.5 dB in float before splitting

## Context and Problem Statement
CD rips can peak above 0 dBTP (the example analysis shows +0.2 dBTP: `docs/agent-tools.md:24`), and stems separated from such a file would clip (`src/gain_of_thrones/separate.py:1-2`). The research offered two remedies: lower the input 1 to 2 dB in float before separation, or make sure the stems are written in float (`docs/research/heavy-metal-punk.md:25`, `:72`).

## Considered Options
* Split the rip as it is
* Lower the input 1 to 2 dB in float before separation
* Write the stems in float

## Decision Outcome
Chosen option: "Lower the input 1 to 2 dB in float before separation", set at 1.5 dB and combined with float32 stems, because the research rates the gain-down as zero risk (`docs/research/heavy-metal-punk.md:72`), and float32 stems keep the bypass null exactly 0 (`src/gain_of_thrones/separate.py:44`; `src/gain_of_thrones/master.py:38`).

### Consequences
* Good, because no stem clips (`docs/listen-and-measure.md:28`).
* Good, because the split input and the stems belong together, so the null test can catch a mismatch (`docs/agent-tools.md:64`).
* Bad, because the split input sits 1.5 dB under the CD, so numbers measured on it read 1.5 dB low against the original (inferred from `docs/agent-tools.md:9`).

## More Information
Evidence: `src/gain_of_thrones/separate.py:1-3`, `:23`, `:31`, `:44` (commit fe58d44); `docs/agent-tools.md:9`, `:46`; `docs/listen-and-measure.md:28`; `docs/research/heavy-metal-punk.md:25`, `:72`. The date is the first commit; earlier history is not in git. Related: ADR-0001, ADR-0003.
