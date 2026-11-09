---
status: accepted
date: 2026-11-08
---
# A new genre ships only with a research report and a blind A/B win

## Context and Problem Statement
Presets encode a genre's mixing knowledge: heavy-guitar's values come from the heavy metal and punk research and won a blind A/B on a thrash/punk EP (`src/gain_of_thrones/presets/heavy_guitar.py:1-4`). Other music needs other moves. How does a new genre get a preset?

## Considered Options
* Run an existing preset on any music (ruled out: `.claude/skills/remaster-session/SKILL.md:41`, "Don't run a heavy-guitar preset on, say, classical music")
* Research the genre, draft a preset from the research inside the envelope, and keep it only if the person picks it in a blind A/B (`docs/adding-a-genre.md:5-9`)

## Decision Outcome
Chosen option: "Research the genre, draft a preset from the research inside the envelope, and keep it only if the person picks it in a blind A/B", because a preset carries genre-specific numbers, and "if the person doesn't pick it, it doesn't ship" (`docs/adding-a-genre.md:9`).

### Consequences
* Good, because each report names its presets, and each preset's docstring names its report (`docs/research/README.md:3`).
* Good, because every registered preset runs through the same smoke test: noise stems, loudness within 0.03 LU, true peak under the ceiling, and an exact null (`docs/adding-a-genre.md:7`; `tests/test_master.py:13`).
* Bad, because a new genre costs a research pass before its first render, and any paid API or LLM call in it needs the person's OK first (`docs/adding-a-genre.md:5`; `CLAUDE.md:9`).

## More Information
Evidence: `docs/adding-a-genre.md:5-9` (commit a8e294a); `docs/research/README.md:3`; `.claude/skills/remaster-session/SKILL.md:39-41`; `src/gain_of_thrones/presets/heavy_guitar.py:1-4`; `CLAUDE.md:7`. The date is the first commit; earlier history is not in git. Related: ADR-0002, ADR-0010.
