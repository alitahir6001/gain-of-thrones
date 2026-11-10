# Gain of Thrones

A remastering tool for a person and their agent: the person listens and decides, the agent measures, renders and explains the numbers.

- For any remaster request, follow the session skill: `.claude/skills/remaster-session/SKILL.md`.
- Tools: `uv run got <command>`, documented in `docs/agent-tools.md`. Every command prints measured numbers; read them before telling the person anything.
- Research: `docs/research/README.md` (one report per genre; each names its preset). New genre: `docs/adding-a-genre.md`.
- Tests: `uv run pytest` (synthetic signals only). Never commit audio: `.gitignore` excludes it and `tests/test_no_audio.py` fails if git tracks any.
- Ask before any paid API or LLM call and state the expected cost.

## Lessons (measured, not guessed)

- pedalboard's `Limiter` is not a ceiling: it adds make-up gain (a -6 dB threshold put a test tone at 0 dBFS; driven to loudness it left 1529 flat-top runs on one track). Use `limiter.tp_limit`.
- Never gate or expand the "other" stem; it exposes separation errors. The vocal gate in `heavy-guitar` was approved by ear.
- Add the stem residual back at unity. A residual around -21 dB means the stems sum back, not that they are clean.
- htdemucs_ft crashes on MPS ("Output channels > 65536 not supported"): CPU on Apple Silicon, about 3.8 s per audio second at `--shifts 2`.
- ffmpeg `ebur128` prints per-frame short-term loudness only with `-loglevel verbose`.
- Subprocesses get `stdin=DEVNULL` (`io.run`): ffprobe and friends otherwise swallow a caller's piped input.
- Folder names like `Freaks [EP]` break glob; `io.audio_files` uses `pathlib` iteration.
- MP3 gain must be measured after encoding: predicting it from the WAV peaks left MP3s at -1.7 dBTP instead of -2.
- Demucs `--shifts` is random, so re-splitting changes stems slightly. Mastering the same stems is bit-identical, given the same `--target` list: the dither comes from one RNG per call, so the -10 render of `--target -11 --target -10` differs by 1 LSB from a lone `--target -10`.
- ffmpeg's Apple AAC encoder (`aac_at`) added 820 samples to a 3 s file (ffmpeg 9.0.2). Export uses the built-in `aac`, which decodes to the exact length.
- A/B switching changes gain only; seeking to re-sync caused audible thumps.

## Maintainer regression (local only, needs the Freaks EP)

`got master` on a Freaks track's stems must reproduce `freaks_ep_v4_verify.txt` from the prototype (kept outside the repo). 03 The Haunted at -10.8 LUFS: residual -21.2 dB, null 0.00e+00, -10.82 LUFS, -1.30 dBTP, limiter GR max 3.4 dB. With the prototype's own stems, the render is byte-identical to the prototype's.
