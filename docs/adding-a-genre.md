# Adding a genre

For music that doesn't match any report in [research/README.md](research/README.md). The agent researches and drafts the preset; the person decides by ear whether it ships.

1. **Research pass.** Write `docs/research/<genre>.md`, with source notes in `docs/research/<genre>/`. Cover how the genre is usually mixed and mastered (sourced numbers), which remasters of it were praised or panned and why, how well Demucs separates its instruments, and a table mapping typical complaints to frequency ranges and moves, like the one in [heavy-metal-punk.md](research/heavy-metal-punk.md). Mark inferences as inferences. Ask before any paid API or LLM call, and state the expected cost.
2. **Draft a preset.** Copy `src/gain_of_thrones/presets/heavy_guitar.py` to `src/gain_of_thrones/presets/<name>.py` and set `CHAINS`, `BALANCE`, `BUS_COMP` and `CEILING` from the research. Stay inside the envelope: EQ within 3 dB at Q 1.5 or lower, stem gain within 2 dB, no gating or expansion on stems that mix several instruments. The docstring names the genre, the report, and the envelope.
3. **Register it.** Add it to `PRESETS` in `src/gain_of_thrones/presets/__init__.py`, to the report's header line, and to the table in `docs/research/README.md`. `uv run pytest` then renders it through the smoke test (noise stems, loudness within 0.03 LU, true peak under the ceiling, exact bypass null).
4. **Measure one track.** Render it with the new preset and check the residual, the null test, limiter gain reduction, flat-tops, and the band changes against the original.
5. **Blind A/B before keeping it.** Compare against the original, and against `heavy-guitar` or another close preset if one exists. If the person doesn't pick it, it doesn't ship.
