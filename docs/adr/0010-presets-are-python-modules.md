---
status: accepted
date: 2026-11-08
---
# Presets are Python modules, loaded by name or by path

## Context and Problem Statement
Each genre needs its own per-stem chains, balance, bus compression and ceiling (`docs/adding-a-genre.md:6`), and sessions iterate on a preset one value at a time (`.claude/skills/remaster-session/SKILL.md:84`). Some stages are custom functions rather than stock effects, such as a de-esser and a guitar dip keyed by the drums (`src/gain_of_thrones/presets/heavy_guitar.py:15`, `:22`).

## Considered Options
* A Python module per preset, loaded by name or path
* A data file per preset (YAML, TOML or JSON) naming stock effects and their values

## Decision Outcome
Chosen option: "A preset is a Python module with `CHAINS`, `BALANCE`, `BUS_COMP` and `CEILING`, registered by name or loaded from a file path" (`src/gain_of_thrones/presets/__init__.py:1`, `:7`, `:10-19`), because a chain stage can be a pedalboard effect or a plain function (`src/gain_of_thrones/presets/heavy_guitar.py:29`), and a session can copy the file and change one value (`docs/agent-tools.md:71`).

### Consequences
* Good, because a custom stage is just a function placed beside the effects (`src/gain_of_thrones/presets/heavy_guitar.py:29-30`).
* Good, because `BALANCE` sets each stem's level against its original loudness, so EQ and compression can't shift it by accident (`src/gain_of_thrones/presets/heavy_guitar.py:45`).
* Bad, because loading a preset from a path runs that file as Python, so only trusted presets should be loaded (inferred from `src/gain_of_thrones/presets/__init__.py:15`).

## More Information
Considered options were reconstructed on 2026-11-10; they were not weighed at the time. Evidence: `src/gain_of_thrones/presets/__init__.py:1`, `:7`, `:10-19`; `src/gain_of_thrones/presets/heavy_guitar.py:15`, `:22`, `:29-30`, `:45-51` (commit 3dcab1d); `docs/agent-tools.md:71`; `.claude/skills/remaster-session/SKILL.md:84`; `docs/adding-a-genre.md:6-7`. The date is the first commit; earlier history is not in git. Related: ADR-0013.
