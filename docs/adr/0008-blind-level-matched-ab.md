---
status: accepted
date: 2026-11-08
---
# Judge versions in a blind A/B that only turns them down

## Context and Problem Statement
A louder version sounds better even when it isn't: in one AES study a level difference outweighed the cues from compression, and trade practice matches levels to within 0.1 dB (`docs/research/heavy-metal-punk.md:63`). The person needed a way to compare renders by ear in which loudness can't decide the result.

## Considered Options
* Comparing renders at their own loudness (ruled out: `.claude/skills/remaster-session/SKILL.md:13`)
* A blind page that turns every version down to the quietest one and switches between them by gain only
* An earlier page that re-synced the versions by seeking every 250 ms (`docs/listen-and-measure.md:32`)

## Decision Outcome
Chosen option: "A blind page that turns every version down to the quietest one and switches between them by gain only", because then level can't decide the test (`src/gain_of_thrones/abtest/__init__.py:1-2`), and seeking to re-sync caused audible thumps (`CLAUDE.md:22`).

### Consequences
* Good, because playback gains are always 0 dB or below, so no version is boosted (`src/gain_of_thrones/abtest/__init__.py:17-20`; `tests/test_abtest.py:14`).
* Good, because the page is served on 127.0.0.1 only and writes nothing to disk (`src/gain_of_thrones/abtest/__init__.py:2`).
* Bad, because the page decodes every file into browser memory, about 110 MB per 5-minute track, so a round stays at six versions or fewer (`docs/agent-tools.md:77`).
* Bad, because integrated-LUFS matching has known low-frequency weighting errors, so a bassier version can still sound louder (`docs/research/heavy-metal-punk.md:84`).

## More Information
Evidence: `src/gain_of_thrones/abtest/__init__.py:1-2`, `:17-20`; `src/gain_of_thrones/abtest/ab_blind_template.html:209`; `tests/test_abtest.py:14` (commit 1be7acc); `.claude/skills/remaster-session/SKILL.md:13`; `docs/agent-tools.md:75-77`; `docs/research/heavy-metal-punk.md:63`, `:84`. The date is the first commit; earlier history is not in git. Related: ADR-0009.
