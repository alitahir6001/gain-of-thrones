---
status: accepted
date: 2026-11-22
---
# Allow A/B picks after Reveal and undo, in an append-only log that marks each pick blind or not

## Context and Problem Statement
ADR-0018 made the pick final for the round and refused it after Reveal (`src/gain_of_thrones/abtest/__init__.py:119-130` at 976deca). On 2026-11-22 the person compared three Freaks EP songs. In two rounds they revealed before picking, so those rounds recorded nothing. They said subtle differences are easier to hear once they know which file is which. A misclicked pick also couldn't be undone (ADR-0018, Consequences). This request is not in the repo; the person's choices were relayed in the brief for this change. The question was how to take a late or changed pick without losing track of which picks were blind.

## Considered Options
* Keep the pick final for the round and refuse it after Reveal (ADR-0018)
* Allow picks after Reveal and an undo, logged append-only with a `blind` yes/no column

## Decision Outcome
Chosen option: "Allow picks after Reveal and an undo, logged append-only with a `blind` yes/no column", because the person still gets a recorded result after revealing first, and the log keeps the blind picks apart from the informed ones.

A round has one current pick. A second pick is refused until **Undo the pick** clears the first (`src/gain_of_thrones/abtest/__init__.py:182-202`). Every pick and every undo appends a row to `<work>/abtest-picks.tsv` with `event` (`pick`/`undo`), `song`, `round` and `blind` (`yes` before Reveal, `no` after) (`:23`, `:204-212`). Rows are never rewritten. The current result of a round is its last row for that song and round (`docs/agent-tools.md`, `got abtest`). The server still holds file names until Reveal (ADR-0018), and stdout says `(blind)` or `(after reveal)`. A log with the ADR-0018 header is moved to `abtest-picks.v1.tsv` on the first write, so one file never mixes two schemas (`:52-69`).

### Consequences
* Good, because a round where the person revealed first still records a result. Tests pin that a late pick is logged `blind no` (`tests/test_abtest.py:132`).
* Good, because a misclick can be undone, and the log still shows every pick and undo in order (`tests/test_abtest.py:143`).
* Bad, because a winner is no longer always a blind result: the agent has to read the `blind` column and say so (`docs/agent-tools.md`; `.claude/skills/remaster-session/SKILL.md`, step 5).
* Bad, because reading a round's result takes one more step: the last row per song and round, not simply the last row.

## More Information
Evidence: commit b3fedc9 (late picks, undo, log columns); `src/gain_of_thrones/abtest/__init__.py`; `src/gain_of_thrones/abtest/ab_blind_template.html:256`, `:309`; `tests/test_abtest.py:110-168`. The same change set added one server for every song of an album (`got abtest --source`, commit 657a0fb), which is why each row names its song. Supersedes ADR-0018's "final before Reveal" rule; its server-held file names and logging stand. Related: ADR-0008 (blind level-matched A/B), ADR-0009 (the person decides, the agent measures).
