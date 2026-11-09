# Handoff — live state snapshot

## Last updated
2026-11-08, session 1 of `.ai/` (the remaster log in `work/Freaks [EP]/notes.md` calls the same work "session 2").

## Current state
Gain of Thrones is public at github.com/alitahir6001/gain-of-thrones: 19 commits on `main`, pushed from this checkout, with `.ai/` and `docs/adr/` (ADRs 0001-0015 plus index, backfilled today and checked against MADR 4.0.0) still uncommitted. The Cattle Mutilation remaster is final: `work/Freaks [EP]/presets/v9.py` at -10 LUFS, exported (FLAC bit-identical to the render, MP3 at -2.20 dBTP) and copied to `~/Music/Freaks [EP] (remaster)/`. The global `write-adr` skill now checks MADR's latest release before writing (tested with a fresh haiku session; uncommitted in the user's harness repo).

## Active task
Make today's work durable. Why: everything after the first push is uncommitted, and this checkout sits in a temp folder (see Open threads).
1. [x] git init, 19 commits code-first, push to `origin/main` (agent)
2. [x] Scaffold `.ai/`; backfill ADRs 0001-0015 and `docs/adr/README.md` (agent)
3. [ ] Review `docs/adr/` and commit it (user decides; the agent commits only when asked)
4. [ ] Decide whether `.ai/` belongs in the public repo; it names local work folders (user)
5. [ ] Push (agent, on request)

## Open threads
- This checkout lives under `/private/tmp` (a session scratchpad macOS can clear). `work/` is gitignored and exists only here: stems, renders, presets v2-v10, `analysis/` scripts and the remaster log. Re-splitting costs about 3.8 s per audio second, and Demucs shifts are random, so new stems would differ (`CLAUDE.md:16`, `:21`).
- The snare fix that won blind (`crack_lift`: a drum-stem 3-8 kHz transient lift, max +2 dB) lives only in `work/Freaks [EP]/presets/v9.py`, not in the stock `heavy-guitar` preset. One track's evidence; the measurements are in `notes.md` ("Session 2"). It was ADR candidate #16 (proposed), skipped because the repo holds no evidence for it yet.
- README doesn't say users can ask for more loudness (the person's feedback; not done).
- ADRs 0009, 0010, 0014 and 0015 list "(alternatives not recorded)"; fill them only if the user remembers real alternatives.
- Harness repo (`~/Desktop/projects/harness`): the `write-adr` change and its `.ai/history.md` line are uncommitted; the user makes their own commits there.

## Next recommended step
Commit `docs/adr/` (and `.ai/` if the user wants it public), push, then move the checkout out of `/private/tmp`.

## Out of scope
The other five Freaks EP tracks (about 2.5 hours to split) and porting `crack_lift` into the stock preset, unless the user asks.
