# Handoff — live state snapshot

## Last updated
2026-11-21, session 5 of `.ai/`: the drum-peak cap went into the shipped `heavy-guitar` preset (PR #4). A side session added the in-page A/B pick and render chooser (PR #3). Hip hop research and a draft preset landed earlier the same day, from other sessions.

## Current state
`main` is at ecfeb53 (PR #4 merged) and `uv run pytest` passes 50 (no CI). `heavy-guitar` now ends its drum chain with `dsp.drum_peaks` (cap = min(drum TP - 5, raw stems LUFS + 10.77)), after three blind wins: Rigor Mortis 04 and 10, Freaks 05 (ADR 0017). `got abtest` records the person's pick on the server (`pick: slot X = <path>` on stdout, a row in `<work>/abtest-picks.tsv`); with no VERSION the person ticks which renders go in (ADR 0018).

## Active task
None. Session 5's list is finished:
1. [x] Dip counter checked on Rigor Mortis 04: 38.9 / 21.2 -> 9.2 / 1.3 dips/min, same as its notes (agent)
2. [x] Freaks v9 dips with and without the cap at the approved targets: only 05 has many (21.3 -> 9.8 >3 dB/min); "TP - 5" binds on all six, so 10.77 never acts there (agent)
3. [x] Blind A/B on Freaks 05 (original, v9, v9+cap): v9+cap won (user)
4. [x] Stage in `dsp.py` with rule and stage tests; preset change; ADR 0017; CLAUDE.md lesson; skill "dips" row; agent-tools entry; one commit each (agent)
5. [x] Maintainer regression numbers updated with the user's OK: 03 at -10.8, GR max 3.4 -> 2.8 dB, active 20 -> 15%, on the work-folder stems (the prototype's stems are gone) (agent)
6. [x] ADR 0018 for PR #3; ADR 0008's amendment paragraph now points to it (agent)

## Open threads
- Freaks `notes.md` has no session-5 entry: a worktree hook blocked writes to the main checkout's `work/`. The text is in `~/Library/Application Support/Claude/side-session-notes/local_be3d0cd6-d693-418f-93fd-7a1e18010d77/drum-cap-freaks.md`; paste it in.
- Freaks album renders and MP3s are v9 without the cap. Only 05 was tested blind with it; offer to re-render and export the EP (at least 05) with v9 + `drum_peaks`. Rigor Mortis's album is already v12, which the shipped preset reproduces byte for byte (04 checked).
- Rigor Mortis: Drive and the car still have the old stock MP3s (the user replaces them; see its `notes.md`).
- Hip hop: draft preset registered (commits 6bbe63f, cc5f4ab). Per `docs/adding-a-genre.md` it still needs measuring and a blind A/B on a real track (inferred from the commit titles; check the research notes).
- Leftovers: local branch `backup/serene-cap-pre-split` (old two-commit history, safe to delete); the prototype's v4 renders (584 MB) in a Claude scratch workspace. The user's call.

## Next recommended step
Ask the user: re-render the Freaks EP with the cap, or start the hip hop blind A/B.

## Out of scope
Opus export; TRACKTOTAL merged into MP4's track field; re-splitting for byte-identity with the prototype (its stems are gone).
