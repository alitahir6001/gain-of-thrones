# Handoff — live state snapshot

## Last updated
2026-11-10, session 3 of `.ai/`: closed the five gaps the first real remaster session found. Nine commits on `feat/session-1-gaps` (the five gaps, the CLAUDE.md lessons, README's step-3 line, the history and this file), open as PR #2, not merged.

## Current state
`main` is still at `a6b4d9f`. This session's work is nine commits on `feat/session-1-gaps`, open as PR #2 against `main` and ready for review (the repo has no CI). `uv run pytest` passes 30 (20 at the start). `got export` now takes render files or folders and a required `--format` (mp3, aac, flac, alac, wav). It prints a `carried:` line per file, and the skill asks the person which formats they want. `got analyze` adds `--blocks` and, with `--stems`, a snare line. `dsp.crack_lift` is an opt-in drum stage (ADR 0016), and heavy-guitar's default output stays byte-identical. The Cattle Mutilation remaster is final: `work/Freaks [EP]/presets/v9.py` at -10 LUFS; `~/Music/Freaks [EP] (remaster)/` holds its FLAC and MP3.

## Active task
Close the session-1 gaps, one commit per gap, in the order 3, 2, 1, 5, 4 (plan approved by the user). Why: that session hand-made `renders/final/`, exported MP3 and FLAC without asking, printed "?-bit", and wrote its own snare and solo scripts.
1. [x] Gap 3: no bit depth for lossy files: `measure.py`, `tests/test_measure.py` (agent)
2. [x] Gap 2: `got export RENDER...` (files or folders), `export.default_out`: `export.py`, `cli.py`, `tests/test_export.py`, agent-tools, SKILL step 7 paragraph, README step 5 "or only the tracks you pick" (agent)
3. [x] Gap 1: WAV, ALAC, AAC; `--format` required; `carried:` line: `export.py`, `cli.py`, `tests/test_export.py`, agent-tools table, SKILL step 7 table and description, README step 5 (agent; user picked the formats)
4. [x] Gap 5: `dsp.transient_lift` and `dsp.crack_lift`, `tests/test_dsp.py`, ADR 0016 and its index line, agent-tools paragraph (agent; user chose a generic stage over a preset)
5. [x] Gap 4: `got analyze --blocks` and the snare line: `measure.py`, `cli.py`, `tests/test_measure.py`, agent-tools, two SKILL table rows (agent; user said build both)
6. [x] Committed on `feat/session-1-gaps` (branched off `main`), one commit per gap, each built from that gap's snapshot and tested on its exact staged tree. A sixth commit holds the CLAUDE.md lessons (dither RNG, `aac_at`). Pushed 2026-11-10. Then, at the user's request, three more commits: README's step-3 line, `.ai/history.md` and this file (agent; the user said commit and push)

## Open threads
- AAC's decoded true peak doesn't fall in step with its gain. On v9, -1.07 dB gave -1.90 dBTP and -1.22 dB gave -1.85. The loop took 4 encodes and landed at -2.32 dBTP, 0.32 dB under the ceiling (-11.5 LUFS vs the MP3's -11.1). That is within the rule; a search for the highest passing gain would recover it. Not built.
- Not run: the CLAUDE.md maintainer regression on 03 The Haunted (no stems here; about 19 min to split). heavy-guitar's default was verified byte-identical on Cattle Mutilation's stems instead.
- Housekeeping from session 2: `~/Desktop/projects/gain-of-thrones.old` can be deleted once the user is satisfied. The two test sessions and VS Code still point at the old `/private/tmp` path. Local branch `docs/adr-backfill` is merged.
- ADRs 0009, 0010, 0014 and 0015 say "(alternatives not recorded)"; fill them only if the user remembers real alternatives.
- From the build: drop the `torchaudio<2.9` pin? demucs 4.1.0 needs torchaudio only for training. Harness repo: the `write-adr` change is uncommitted; the user commits there.

## Next recommended step
The user reviews and merges PR #2. After the merge, delete the local and remote `docs/adr-backfill` and `feat/session-1-gaps` branches if the user agrees.

## Out of scope
The other five Freaks EP tracks (1367 s of audio, about 1.4 hours to split), unless the user asks. Opus export (the user chose WAV, ALAC and AAC). Merging TRACKTOTAL into MP4's track field: it is reported as not carried instead.
