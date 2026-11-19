Run /get-session-context, then read `docs/adding-a-genre.md` and `docs/research/heavy-metal-punk.md` (the model for a genre report).

Two things this session, in this order:

1. Hip hop research and preset (main task). Follow `docs/adding-a-genre.md` step by step:
   - Plan first (it touches 3+ files): what the report will cover and which sources, and ask me before any paid API or LLM call, with the expected cost.
   - Write `docs/research/hip-hop.md` plus source notes in `docs/research/hip-hop/`, in the same shape as the heavy-metal-punk report: how hip hop is usually mixed and mastered (sourced numbers: loudness, low end, vocal level), remasters that were praised or panned and why, how well Demucs separates it (808s and sub bass, sampled loops that land in "other", vocal ad-libs), and a complaint-to-frequency/move table. Mark inferences as inferences.
   - Draft `src/gain_of_thrones/presets/hip_hop.py` inside the separation envelope, register it, and run `uv run pytest`.
   - Then stop and ask me for a track to measure and blind A/B. It doesn't ship unless I pick it.

2. If time remains, the open threads in `.ai/handoff.md`, my pick:
   - 05 Worms of the Earth: blind A/B at a lower target (it costs 5.5 dB of limiting, 77% of the time, at -9.3 LUFS).
   - The `got abtest` gotcha (killed at turn end when run from Bash in the background) and the -21.7 dB regression residual: propose the wording, I decide whether it goes into the skill or CLAUDE.md.
   - Leftover files (prototype v4 renders, Trash): list them with sizes; I'll decide.

Don't start a second task before the first is done or I say so.
