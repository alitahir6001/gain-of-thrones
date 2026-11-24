---
status: superseded by ADR-0019
date: 2026-11-21
---
# Record the blind A/B pick on the server, final before Reveal

## Context and Problem Statement
Until 2026-11-21 the A/B page (ADR-0008) only revealed the files in the browser. The person then told the agent "which slot won and what it was" (`docs/agent-tools.md:87` at 6074825), so the result of every round reached the session as retyped words. The page also carried every file name in its own data and shuffled the slots on each load (`src/gain_of_thrones/abtest/__init__.py:35-39`, `ab_blind_template.html:188` at 6074825). A retyped file name was ambiguous once, and the agent had to ask again which file had won (the person's request for this change, 2026-11-21; not in the repo). The person also wanted to choose which renders go into a round themselves. The question was how the winner and the set of renders should reach the server without weakening the blind test.

## Considered Options
* The person reveals the files and tells the agent which slot won (as before)
* The server records the pick: one per round, refused after Reveal, printed and logged; the server holds the file names until Reveal

## Decision Outcome
Chosen option: "The server records the pick: one per round, refused after Reveal, printed and logged; the server holds the file names until Reveal", because the agent then reads the winner's full path instead of interpreting a retyped name, and the logged pick is the blind one.

"Pick this one" POSTs the slot. The server refuses a second pick, a pick after Reveal and an unknown slot (`src/gain_of_thrones/abtest/__init__.py:119-130`). It prints `pick: slot B = <path>` and appends a row to `<work>/abtest-picks.tsv` with the time, the reference, the winner and every slot's play gain and path (`:132-138`; `docs/agent-tools.md`, `got abtest`). The server shuffles the slots once per round and sends a file name to the page only after Reveal (`:90`, `:146-159`). With no VERSION on the command line, the page first lists the reference track's renders in the work folder and the person ticks up to six (`:53`, `:99-107`). The slots are still shuffled, and level matching is unchanged (ADR-0008).

### Consequences
* Good, because the winner is a full path from the server, not a retyped name. Tests pin that the logged file is the blind slot's file and that the pick is final (`tests/test_abtest.py:104`, `:127`, `:136`).
* Good, because the page can no longer show a file name early: it doesn't receive one until Reveal (`tests/test_abtest.py:94`).
* Good, because every pick has a record in the work folder, with the gains each slot played at.
* Bad, because a misclicked pick can't be undone. In a round whose files were given on the command line, there is also no reset (`src/gain_of_thrones/abtest/__init__.py:109-112`), so a new round means restarting `got abtest` (inferred from that code).
* Bad, because `got abtest` now writes a file into the work folder. Before, it wrote nothing (at 6074825 the module only read audio files and wrote HTTP replies).

## More Information
Evidence: commit fafcb20, merged as d38e142 (PR 3); `src/gain_of_thrones/abtest/__init__.py:1-4`; `tests/test_abtest.py:86-162`; `docs/agent-tools.md` (`got abtest`); `.claude/skills/remaster-session/SKILL.md`. PR 3 first wrote this decision as an amendment paragraph at the end of ADR-0008; that paragraph now points here. Related: ADR-0008 (blind level-matched A/B, which this extends), ADR-0009 (the person decides, the agent measures).

Superseded by [ADR-0019](0019-picks-after-reveal-and-undo-marked-blind-or-not.md): a pick after Reveal is now allowed and logged as not blind, and a pick can be undone.
