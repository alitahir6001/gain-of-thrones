# Handoff — live state snapshot

## Last updated
2026-11-10, session 3 of `.ai/`: closed the five gaps the first real remaster session found. Merged to `main` as PR #2 (nine commits, merge commit `90175db`).

## Current state
`main` is at `90175db`, with session 3's work merged (PR #2), and this checkout is on `main`. The repo has no CI; `uv run pytest` passes 30 locally. `got export` now takes render files or folders and a required `--format` (mp3, aac, flac, alac, wav). It prints a `carried:` line per file, and the skill asks the person which formats they want. `got analyze` adds `--blocks` and, with `--stems`, a snare line. `dsp.crack_lift` is an opt-in drum stage (ADR 0016), and heavy-guitar's default output stays byte-identical. The Cattle Mutilation remaster is final: `work/Freaks [EP]/presets/v9.py` at -10 LUFS; `~/Music/Rigor Mortis/Freaks [EP] (remaster)/` holds its FLAC and MP3 (rips moved to `~/Music/Rigor Mortis/Freaks [EP]/` on 2026-11-12).

## Active task
None. Session 3 closed the five gaps from the first remaster session: export formats, single-track export, "?-bit", snare and solo rows, and `crack_lift`. What changed and the measurements are in `.ai/history.md` and PR #2. The next task is the user's pick from the open threads below.

## Open threads
- AAC's decoded true peak doesn't fall in step with its gain. On v9, -1.07 dB gave -1.90 dBTP and -1.22 dB gave -1.85. The loop took 4 encodes and landed at -2.32 dBTP, 0.32 dB under the ceiling (-11.5 LUFS vs the MP3's -11.1). That is within the rule; a search for the highest passing gain would recover it. Not built.
- Not run: the CLAUDE.md maintainer regression on 03 The Haunted (no stems here; about 19 min to split). heavy-guitar's default was verified byte-identical on Cattle Mutilation's stems instead.
- Housekeeping from session 2: `~/Desktop/projects/gain-of-thrones.old` can be deleted once the user is satisfied. The two test sessions and VS Code still point at the old `/private/tmp` path. Local branch `docs/adr-backfill` is merged.
- ADRs 0009, 0010, 0014 and 0015 say "(alternatives not recorded)"; fill them only if the user remembers real alternatives.
- From the build: drop the `torchaudio<2.9` pin? demucs 4.1.0 needs torchaudio only for training. Harness repo: the `write-adr` change is uncommitted; the user commits there.

## Next recommended step
Ask the user which open thread to take next. On their OK, delete the merged branches `docs/adr-backfill` and `feat/session-1-gaps`, local and remote.

## Out of scope
The other five Freaks EP tracks (1367 s of audio, about 1.4 hours to split), unless the user asks. Opus export (the user chose WAV, ALAC and AAC). Merging TRACKTOTAL into MP4's track field: it is reported as not carried instead.
