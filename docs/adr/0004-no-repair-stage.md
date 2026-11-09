---
status: accepted
date: 2026-11-05
---
# No repair stage: don't de-clip, de-limit or denoise the source

## Context and Problem Statement
Hot reissue CDs arrive limited, sometimes with clipping printed in (`docs/research/heavy-metal-punk.md:9-15`). The research surveyed repair tools and left repair as an optional stage, to be A/B'd against no repair (`docs/research/heavy-metal-punk.md:73`). Should the tool repair the source before separating it?

## Considered Options
* De-clip where flat-tops appear (iZotope RX De-clip)
* De-limit at a low Amount (the open-source De-limiter, or Ozone 12's Unlimiter)
* Broadband noise reduction
* No repair: measure clipping and only avoid making it worse

All four are from `docs/research/heavy-metal-punk.md:15` and `:73`.

## Decision Outcome
Chosen option: "No repair" (inferred: `src/` has no repair stage and `README.md:28` says printed clipping stays), because the research found each repair tool risky on this material: RX De-clip is "not intended for brickwall-limited audio", the ML de-limiters were trained on modern plug-in limiting and are untested on 1980s analog limiting, a de-clipper can mistake guitar distortion for clipping, and noise reduction would smear cymbals and guitar fizz first (`docs/research/heavy-metal-punk.md:15`).

### Consequences
* Good, because no repair artifacts are added to distorted guitars or cymbals (`docs/research/heavy-metal-punk.md:15`).
* Bad, because clipping already printed on the CD stays; every render counts flat-top runs so the tool never adds more (`README.md:28`; `docs/agent-tools.md:69`).
* Bad, because the CD's limiting isn't undone, so extra loudness comes out of peak headroom the source already spent (`docs/research/heavy-metal-punk.md:88`).

## More Information
Evidence: `docs/research/heavy-metal-punk.md:9-15`, `:73`, `:88`; `README.md:28`. No source states this choice outright; it is inferred from the research and from what the code leaves out. The date is when the research notes were compiled (`docs/research/heavy-metal-punk/general_mastering.md:3`). Related: ADR-0005.
