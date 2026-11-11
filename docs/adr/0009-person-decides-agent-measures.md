---
status: accepted
date: 2026-11-08
---
# The person decides by ear; the agent measures and explains

## Context and Problem Statement
The tool is built for a person and their agent working together (`CLAUDE.md:3`). Meters can say what changed and what it cost, but not which version sounds better, and only the person listens. Who decides what ships, and how?

## Considered Options
* The person listens and decides; the agent measures and explains
* Match a loudness target or a reference track automatically

## Decision Outcome
Chosen option: "The person listens and decides; the agent runs the tools, measures every render before the person hears it, and explains the numbers, but never says which version sounds better", because the project is built on the principle that "their ears decide", with numbers reporting what a choice costs (`.claude/skills/remaster-session/SKILL.md:14`; `README.md:3`). Each round changes one thing, "so both of you know what made the difference" (`.claude/skills/remaster-session/SKILL.md:15`).

### Consequences
* Good, because every shipped preset value has a blind listening win behind it (`src/gain_of_thrones/presets/heavy_guitar.py:3-4`).
* Good, because a render is checked before anyone spends listening time on it (`.claude/skills/remaster-session/SKILL.md:12`; `docs/listen-and-measure.md:12`).
* Bad, because progress is limited by the person's listening time, one change per round (inferred from `docs/listen-and-measure.md:14`).
* Bad, because the agent's metrics and the person's ears can disagree, and the ears win (inferred from `.claude/skills/remaster-session/SKILL.md:14`).

## More Information
Evidence: `CLAUDE.md:3`, `:6`; `README.md:3`; `.claude/skills/remaster-session/SKILL.md:12-15` (commit 3f30294); `docs/listen-and-measure.md:5`, `:12-14`. The date is the first commit; earlier history is not in git. Related: ADR-0008.
