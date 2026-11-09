---
status: accepted
date: 2026-11-08
---
# Never commit audio; tests use synthetic signals

## Context and Problem Statement
The tool works on records people own, usually commercial CDs (`README.md:5`, `:41`), and its work folders hold stems, renders and exports, about 5 GB per 45-minute album (`README.md:26`). The repository is public.

## Considered Options
* (alternatives not recorded)

## Decision Outcome
Chosen option: "No audio in git: `.gitignore` excludes audio formats and the work folders, a test fails if git tracks any audio file, and tests use synthetic signals only" (`CLAUDE.md:8`; `.gitignore:1-16`), because remasters of commercial records are for personal listening (`README.md:41`), and the work files are large (`README.md:26`).

### Consequences
* Good, because `tests/test_no_audio.py:11-16` fails as soon as git tracks a file with an audio extension (`src/gain_of_thrones/io.py:10`).
* Good, because the session rules repeat it: work files go in `work/` or a folder the person picks (`.claude/skills/remaster-session/SKILL.md:17`).
* Bad, because tests can't use real recordings, and the full-track regression check needs the Freaks EP, so it runs only on a maintainer's machine (`CLAUDE.md:24-26`).

## More Information
Evidence: `.gitignore:1-16`, `tests/test_no_audio.py:11-16` (commit 05e0de9); `CLAUDE.md:8`, `:24-26`; `.claude/skills/remaster-session/SKILL.md:17`; `README.md:26`, `:41`; `src/gain_of_thrones/io.py:10`. The date is the first commit; earlier history is not in git.
