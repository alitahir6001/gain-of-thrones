# Handoff — live state snapshot

## Last updated
2026-11-14, session 4 of `.ai/`: housekeeping, ADR alternatives, torchaudio dropped, lossy gain bisection, maintainer regression, music library tidy, and the whole Freaks EP remastered with v9. A parallel session added `got plot` and README polish.

## Current state
`main` is pushed and clean; `uv run pytest` passes 40 (no CI). The Freaks EP is done: all six tracks in `work/Freaks [EP]/renders/album/` (v9, +1.07 LU, except 02 at its approved -10.0), exported as MP3 (one gain -1.16 dB, all <= -2.05 dBTP, 14/14 tags, cover kept) and copied to `~/Music/Rigor Mortis/Freaks [EP] (remaster)/`, which also holds 02's v9 FLAC. The full log is `work/Freaks [EP]/notes.md` (session 4 section).

## Active task
None. Session 4's list is finished:
1. [x] Merged branches deleted; `gain-of-thrones.old` and three Music-app duplicate MP3s moved to the Trash; two stale test sessions archived (user)
2. [x] ADR 0009/0010/0014/0015 alternatives filled; 0010 and 0015 marked as reconstructed on 2026-11-10 (agent)
3. [x] torchaudio removed: demucs 4.1.0 needs it only for training; a full split still works (agent)
4. [x] `export.next_gain` bisects the lossy gain back up: v9 AAC -2.32 -> -2.06 dBTP (+0.17 dB), MP3 +0.08 dB, at up to 9 encodes (agent)
5. [x] Maintainer regression on 03 with a fresh split: every master number matches the prototype; residual -21.7 vs -21.2 (stems differ) (agent)
6. [x] `~/Music` organized as Artist/Album; rips now at `~/Music/Rigor Mortis/Freaks [EP]/` (agent, user OK'd)
7. [x] EP remaster: 03 blind A/B picked -10.6 over -9.6; album at +1.0; 02 blind A/B picked -10.0 over the album's -11.0; MP3 only (user picked) (both)

## Open threads
- 05 Worms of the Earth costs the most: limiter GR max 5.5 dB, active 77% at -9.3 LUFS (04: 4.1/28%, 06: 4.4/50%). Only 02 and 03 were A/B'd; offer a blind A/B of 05 at a lower target.
- Leftovers on disk: the prototype's v4 renders and MP3 set (584 MB) in `~/Library/Application Support/Claude/scratch-workspaces/.../scratch-2026-11-05-f68799/output/`; the Trash still holds `gain-of-thrones.old`. The user's call to delete. Only 02 has a FLAC in the remaster folder.
- `got abtest` started from Bash in the background was killed at turn end twice (exit 144). Run it in the Terminal panel (`run_in_terminal`); worth a line in the skill or CLAUDE.md if the user agrees.
- CLAUDE.md's maintainer regression quotes residual -21.2 dB; a fresh split gives -21.7 (Demucs `--shifts` is random). Worth noting there, on the user's OK.
- Next genre: hip hop. Follow `docs/adding-a-genre.md` (research report + notes, draft preset, register, measure, blind A/B).

## Next recommended step
Ask the user: hip hop research first, or the 05 Worms of the Earth A/B.

## Out of scope
Opus export; TRACKTOTAL merged into MP4's track field; re-splitting for byte-identity with the prototype (its stems are gone).
