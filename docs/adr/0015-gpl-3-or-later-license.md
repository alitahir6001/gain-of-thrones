---
status: accepted
date: 2026-11-08
---
# License the project GPL-3.0-or-later

## Context and Problem Statement
The audio effects come from pedalboard, which is GPL-3.0; Demucs and pyloudnorm are MIT (`README.md:39`; `pyproject.toml:12`, `:14`). The project needed a license compatible with its dependencies.

## Considered Options
* (alternatives not recorded)

## Decision Outcome
Chosen option: "GPL-3.0-or-later", because the project uses pedalboard (GPL-3.0) (`README.md:39`; `pyproject.toml:6-7`).

### Consequences
* Good, because the license matches pedalboard's GPL-3.0 (inferred from `README.md:39`).
* Bad, because anyone who distributes a modified version must license it under the GPL too (inferred from the license terms in `LICENSE`).

## More Information
Evidence: `README.md:37-41`, `LICENSE` (commit dd8a412); `pyproject.toml:6-7`, `:12`, `:14` (commit 058ea59). Outside this decision: the htdemucs model weights are not part of the repository, and their license is unclear (`README.md:41`). The date is the first commit; earlier history is not in git.
