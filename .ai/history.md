# History

Session logs, change log and measurements, newest first. Not read at session start — pull it in when asked about past work.

## 2026-11-09, session 3: closing the session-1 gaps

Changed (one commit per gap on `feat/session-1-gaps`, PR #2):
- `got analyze` shows no bit depth for lossy files. ffprobe gives MP3/AAC `bits_per_raw_sample` None and `bits_per_sample` 0, which used to print "?-bit".
- `got export RENDER...` takes render files or folders, so one track or a hand-picked set exports directly. Two renders of one track in a run is an error.
- New formats `aac` (256k, built-in encoder), `alac` and `wav` (24-bit). `--format` is required. Each file gets a `carried:` line, and the skill asks the person which formats they want.
- `dsp.crack_lift` is a generic opt-in drum stage (ADR 0016). `got analyze --blocks` gives loudness per 5 s block, and `--stems` adds a snare line ported from `work/Freaks [EP]/analysis/snare_punch3.py`.

Measured (ffmpeg 9.0.2):
- Format probe, on synthetic audio with the Freaks rip's 14 tag names and a cover:
  - WAV 24-bit: samples identical; ffmpeg refuses the cover; no slot for 5 tags (involvedpeople, lyrics, net radio owner, organization, tracktotal).
  - ALAC: identical, cover kept; no slot for 5 tags (involvedpeople, isrc, net radio owner, organization, tracktotal).
  - AAC, built-in encoder: exact length, cover kept. `aac_at`: +820 samples.
  - AIFF with `-write_id3v2 1`: cover and all 14 tags kept (not adopted).
  - Opus 160k: all tags carry (as stream tags); the cover only via a hand-built METADATA_BLOCK_PICTURE (round trip verified); resampled to 48 kHz (not adopted).
- Real audio, the Cattle Mutilation v9 render:
  - WAV and ALAC samples identical (7,792,176 x 2).
  - AAC needed 4 encodes (gain -0.70/-1.07/-1.22/-1.42 dB, decoded TP -1.68/-1.90/-1.85/-2.32 dBTP). Final -2.32 dBTP on both got's meter and ffmpeg's, -11.5 LUFS, exact length, cover sha256 matches the source.
  - FLAC from a single-file export is byte-identical to session 2's export.
- Stock heavy-guitar `--target -10` was byte-identical before and after the crack_lift change. Round 1's -11 and -10 renders reproduce byte for byte only with both targets in one call: a lone `--target -10` differed by 1 LSB in 7,043,023 bytes, because the dither RNG is drawn per call in target order.
- v9 with `dsp.crack_lift` is byte-identical to the session's v9 render (lift active 35%, mean 0.7 dB).
- The ported snare line reproduces the log (body | attack | snap, 500 hits): CD 15.25 | 7.55 | 7.65; v6 14.11 | 7.00 | 6.54; v9 14.06 | 6.96 | 7.70; v8 -11 14.86 | 7.14 | 7.50.
- `--blocks` on the split input: "other" -19.9 to -21.2 LUFS in the verses and -14.4 to -15.9 in the solo blocks; the mix -13.0 to -12.5.
- Two new dsp tests were wrong, not the code:
  - A hard amplitude step is a broadband click, and the lift correctly raised it (2.1e-2). A 10 ms raised-cosine low attack changes 6.4e-7 (-113 dB re the tone).
  - The 2 ms smoothing leaves -2.9e-16 instead of exact zeros on releases.
- Tests: 20 -> 30 passed.
