# Agent tools: the `got` command

The person never types these. The agent runs them from the repo root as `uv run got <command>` and reads back the numbers each one prints. Quote paths: album folders often contain spaces and brackets.

Work folder (default `./work/<album folder name>/`, gitignored; `--work` puts it anywhere):

```
work/<album>/
  input/<track>.wav                        source lowered 1.5 dB, 32-bit float (the "split input")
  stems/htdemucs_ft/<track>/{drums,bass,vocals,other}.wav, stems/<track>.log
  renders/<track>_<name>_<LUFS>LUFS.wav    got master
  renders/album/                           got album
  export/<format>/                         got export
  targets.tsv                              got album
```

Disk: about 1.8 MB per second of audio for stems plus input (roughly 5 GB for a 45-minute album).

## got analyze

`got analyze <files...> [--stems DIR] [--blocks]`: measures any file ffmpeg can read. About 5 s per 5-minute track.

```
03 The Haunted.flac: I -11.6 LUFS | LRA 2.9 | max S -9.6 LUFS | TP +0.2 dBTP | PLR 11.8 dB | DR10 (10.2) | flat-top runs(>=3) 2
  format: flac 44100 Hz 2 ch 16-bit 296.667 s
  bands:  sub -12.0 | bass -2.0 | low-mid -9.6 | mid -9.9 | upper-mid -12.0 | presence -16.5 | air -23.7 | >16k -38.2 dB re total
  highs:  2-4k -12.0 | 4-6k -17.7 | 6-10k -21.2 | 10-16k -26.5 dB re total | >6k crest 20.4 dB
```

| Field | Meaning |
|---|---|
| I | integrated loudness, EBU R128 (ffmpeg) |
| LRA | loudness range, LU: small means the level hardly changes |
| max S | loudest 3-second stretch (short-term LUFS) |
| TP | true peak, 4x oversampled. Above 0 dBTP can clip in players and encoders |
| PLR | TP minus I: peak headroom above the average. Lower means more limiting |
| DR | TT DR meter (the DR database method). DR8 or lower is heavily limited. n/a under 6 s |
| flat-top runs | runs of 3+ samples at the file's maximum: clipping printed into the file |
| bands | energy per band in dB relative to the file's total. Compare files; the absolute values mean little |
| highs | finer 2-16 kHz split. >6k crest: cymbal transient sharpness, higher is less squashed |

`--stems DIR` adds each Demucs stem's share of the 2-16 kHz bands, e.g. how much of 4-6 kHz is guitars ("other") versus cymbals ("drums"). It also adds a `snare` line under each file of the stems' track: the original rip, the split input and its renders qualify (same rate and length as the drum stem), and other files say skipped.

```
  snare (proxy; local crest at 500 drum-stem hits): body 150-300 14.06 | attack 1-2k 6.96 | snap 5-8k 7.70 dB
```

Hits are the drum stem's 150-300 Hz peaks (top 10%, at least 100 ms apart). Each band's number is how far the snare rises above the sound around it: the band's envelope peak at the hit minus its 20th percentile within +-200 ms, median over the hits. Overall level doesn't change it. It is a proxy from one track. It agreed with the ear in two rounds (the drum compressor off; `crack_lift`), and it pointed the wrong way in one: it favored taking the bus comp off, which lost. Compare versions with it, and let the blind A/B decide.

`--blocks` adds a table of loudness per 5 s block, one column per file and, with `--stems`, one per stem (silent blocks read -inf). A section that jumps shows up here. On the Freaks EP, "other" went from -20 to -21 LUFS in the verses to -14.4 to -16 in the solos (stems of the split input), while the mix rose only about 0.5 LU.

## got split

`got split <track> [--work DIR] [--shifts N] [--device D]`: lowers the track 1.5 dB in float (CD rips can peak above 0 dBTP and would clip the stems), then runs Demucs `htdemucs_ft` with float32 output. Prints the stems folder and the split input: `master` needs both.

- Time: 3.8 s per second of audio on an M1 Max CPU at `--shifts 2` (12 minutes for a 3-minute song). Run it in the background and tell the person how long.
- Device: `cuda` if available, else `cpu`. Never `mps`: htdemucs_ft crashes on it.
- The first run downloads about 340 MB of model weights (four 84 MB models) from Hugging Face.
- Skips anything that exists, so an interrupted split resumes. Demucs's shifts are random, so re-splitting gives slightly different stems (residual -21.2 vs -21.3 dB on the same track).

## got master

`got master <stems_dir> <split_input> --target LUFS [--target LUFS ...] [--preset NAME|PATH] [--ceiling dBTP] [--name LABEL] [--out DIR]`

Chain: per-stem preset chains, then each stem set to its original loudness plus the preset's `BALANCE`, then the residual (input minus the stem sum) added back at unity, bus compressor, look-ahead true-peak limiter at the ceiling minus 0.1 dB, flat TPDF dither, 24-bit WAV. Writes `<out>/<track>_<name>_<target>LUFS.wav` (default out: `renders/` beside the input folder). About 45 s per 5-minute track.

What it prints and what to check:

| Line | Normal | Act when |
|---|---|---|
| residual | -20 to -22 dB re input | much higher: stems and input don't belong together |
| null test (bypass) | `0.00e+00` | anything else: stems or input mismatch; stop |
| de-esser / guitar dip | active a few % / about a third of the time | active most of the time: threshold too low for this track |
| stem lines | original -> after chain -> balanced | balanced must equal original + `BALANCE` |
| bus comp | about 1.5 dB loudness drop | |
| per target | LUFS within 0.03 of target, dBTP at the ceiling | limiter GR max over 3 dB or active over 30%: the loudness costs transients |
| analyze of the written file | flat-top runs 0 | any flat-tops: something clips; stop |

`--preset` takes a registered name (`heavy-guitar`) or a path to a preset `.py` file. To iterate, copy the preset into the work folder, change one value, and render with `--preset work/<album>/presets/v2.py --name v2`. `--name` labels the file; it defaults to the preset name.

Opt-in stage for any preset copy: `crack_lift` lifts the drum stem's 3-8 kHz attacks (snare crack and snap) by at most 2 dB and leaves the cymbal wash alone. Add `from gain_of_thrones.dsp import crack_lift` and append `crack_lift` to the copy's `"drums"` chain. It prints how often it acted. It won one blind round, on one track, with the drum compressor already off (ADR 0016).

## got abtest

`got abtest --ref ORIGINAL VERSION... [--port N] [--no-browser]`: measures each file's loudness, turns every file down to the quietest one (never up), and serves a blind A/B page on `127.0.0.1` (random free port unless `--port`). Opens the person's default browser unless `--no-browser`. It blocks until stopped, so run it in the background and stop it when the round is done.

The person sees the song name (the reference's title tag, else its file name), "Original (reference)" plus shuffled blind slots A, B, C. They pick by ear, then press **Reveal the files** and tell you which slot won and what it was. The page decodes every file into browser memory (about 110 MB per 5-minute track), so keep a round to six versions or fewer.

## got album

`got album <src_dir> --target LUFS [--preset NAME|PATH] [--work DIR] [--shifts N] [--device D]`: measures every track's original loudness and applies one shift to all of them, so the loudest track lands at `--target` and the CD's song-to-song levels survive (targets rounded to 0.1 LU). Writes `targets.tsv`, then splits and masters each track into `renders/album/`. Resumable: existing stems and renders are skipped. Hours for an album: run it in the background.

To carry a single-track A/B winner to the album: shift = winner LUFS minus that track's original LUFS; `--target` = loudest original + shift.

## got export

`got export RENDER... --source <src_dir> --format mp3|aac|flac|alac|wav [--out DIR]`: each RENDER is a render `.wav`, or a folder with one render per track such as `renders/album/`. Pairs each render with the source file whose name starts the render's name, and copies the source's tags and embedded cover. ReplayGain tags are dropped (the levels changed). Default out: `<work>/export/<format>/`.

To export one track, or a hand-picked set, pass the render files themselves; there's no need to copy them into a folder:

```
uv run got export "work/<album>/renders/<track>_v9_-10LUFS.wav" --source "<album folder>" --format flac
```

Two renders of the same track in one run is an error that lists them. The lossy gain is shared by the files of one run, so export an album's tracks in one run; a track exported on its own gets its own gain. After the first passing gain, it bisects back up toward the last failing one (within 0.05 dB, at most 9 encodes in all), because a decoded true peak doesn't fall in step with the gain.

`--format` is required: the person picks (the skill explains the choices in plain words). One format per run.

| `--format` | File | Audio | Cover | Tags with no slot (of the Freaks rip's 14) |
|---|---|---|---|---|
| `mp3` | .mp3, 320 kbit/s, ID3v2.3 | lossy: one gain, <= -2 dBTP | kept | none |
| `aac` | .m4a, 256 kbit/s, ffmpeg's built-in encoder | lossy: one gain, <= -2 dBTP | kept | isrc, tracktotal, organization, involvedpeople, net radio owner |
| `flac` | .flac, 24-bit | the rendered samples unchanged | kept | none |
| `alac` | .m4a, 24-bit | the rendered samples unchanged | kept | as `aac` |
| `wav` | .wav, 24-bit | the rendered samples unchanged | none: WAV can't hold it | lyrics, tracktotal, organization, involvedpeople, net radio owner |

- Lossy gain: lowered until every decoded file of the run measures at or under -2 dBTP (ADR 0012). It is measured after encoding because encoders overshoot: on the Freaks EP the predicted -0.8 dB left MP3s at -1.7 dBTP, and the measured answer was -1.16 dB.
- AAC uses ffmpeg's built-in `aac` encoder: Apple's `aac_at` added 820 samples to a 3 s test file (ffmpeg 9.0.2), and the built-in one decoded to the exact length.
- Lossless files keep the render's -1.2 dBTP ceiling.

It prints the analyze line of every exported file, then `carried:` (cover kept or not, and which source tags the format has no slot for). The tag column above was measured with synthetic audio carrying the Freaks rip's tag names; other rips can differ.
