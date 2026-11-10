---
name: remaster-session
description: Run a remastering session with the person for music they own (CD rips, lossless files). Measure the rips, match the genre's research and preset, turn what they want to hear different into measured moves, render, run blind level-matched A/B tests, then do the whole album and export it in the formats they pick (MP3, AAC, FLAC, ALAC, WAV). Use whenever someone asks to remaster, master, fix, clean up, rebalance, or make louder or clearer an album or a track.
---

# Remaster session

You and the person are the audio engineer together. **They are the ears and they decide. You are the hands and the meters:** you run the tools, measure every result, and explain the numbers in plain words. The tools are `uv run got <command>`, run from the repo root (reference: `docs/agent-tools.md`).

## Rules

1. **Measure every render before the person hears it.** Read what `master` prints: null test `0.00e+00`, loudness within 0.03 LU of target, true peak at the ceiling, flat-top runs 0, and how hard the limiter worked. If something is off, fix it before playing anything.
2. **Every listening comparison is blind and level-matched** (`got abtest`). Never treat a comparison at different loudness as evidence: louder always sounds better.
3. **Their ears decide.** Report numbers and what a choice costs (for example "louder means the limiter takes 4.7 dB off the peaks"), but never tell them which version sounds better.
4. **One change per round,** so both of you know what made the difference.
5. **Stay inside the separation envelope:** EQ within 3 dB at Q 1.5 or lower, stem gain within 2 dB, no gate or expander on "other". Bigger moves expose separation artifacts.
6. **No audio in git.** Work files go in `work/` (gitignored) or a folder the person picks.
7. **Ask before any paid API or LLM call** and state the expected cost.
8. **Long jobs run in the background** with a time estimate given up front: splitting takes about 3.8 s per second of audio on an Apple Silicon CPU (12 minutes for a 3-minute song, hours for an album).

## 1. Check setup

Run `ffmpeg -version`, `uv --version`, then `uv sync` and `uv run got --help`. If something is missing, give the exact install step and wait: ffmpeg via `brew install ffmpeg` (macOS), `winget install ffmpeg` (Windows) or `sudo apt install ffmpeg` (Debian/Ubuntu); uv from https://docs.astral.sh/uv/.

## 2. Measure the rips and explain them

Ask where the album is; don't search their disk. Then run `uv run got analyze "<album folder>"/*.flac` (any audio format works; quote the folder).

Tell them in plain words what it shows, for example:

- **Loudness (I, LUFS):** early-80s CDs often sit at -14 to -18; loudness-war masters at -6 to -9.
- **Peaks (TP):** above 0 dBTP means the CD itself can clip in players and MP3 encoders.
- **Punch (PLR, DR):** peak headroom above the average. DR8 or lower means heavily limited; DR12 and up is roomy.
- **Clipping (flat-top runs):** clipping printed into the CD. It can't be undone here, only not made worse.
- **Balance (bands):** use it to compare renders against the original, not as a score.

Start a short log at `work/<album>/notes.md`: the original numbers now, then every render's settings, measurements and A/B result. Later sessions can't see this conversation, but they can read the log.

## 3. Genre: research and preset

Ask what the music is. Find its report in `docs/research/README.md`, read it (above all the complaint table, the chain, and the loudness section), and use its preset (`heavy-guitar` for heavy metal and punk). If no report fits, say so and offer the add-a-genre path (`docs/adding-a-genre.md`): research, a draft preset, a blind A/B before it ships. Don't run a heavy-guitar preset on, say, classical music.

## 4. What do they want to hear different?

Ask in their words, one question at a time, then map each complaint to a measurement and a move. For `heavy-guitar` (the values live in `src/gain_of_thrones/presets/heavy_guitar.py`):

| They say | Look at | Move, one per round |
|---|---|---|
| Guitars cloudy, muddy | low-mid band vs original | "other" `PeakFilter(300, -3, 0.7)` is at the limit; deepen "other" `PeakFilter(150, -1.5, 1.5)` toward -3, or the bass stem's 300 Hz cut |
| Guitars small, thin | mid and upper-mid bands | "other" `PeakFilter(1800, ...)` toward +2.5; `BALANCE["other"]` toward 0 |
| Vocal buried | vocal balance line, upper-mid | `BALANCE["vocals"]` up 0.5 LU at a time (2 max); "other" `PeakFilter(3200, -2, 1.2)` toward -3 |
| Vocal reverby, far away | by ear (no meter for reverb) | vocal high-pass 160 toward 170 Hz, vocal 300 Hz cut; expect artifacts first here |
| Harsh S's | presence band, de-esser activity | de-esser `pct` 90 down to 85, or `max_cut` up |
| Cymbals lost when loud | >6k crest, limiter GR, highs | lower `--target` first (less limiting); drum `HighShelfFilter(8000, ...)` toward +3; the drum-keyed `guitar_dip`: `pct` 70 toward 60 so it acts more often (`max_cut` is already at the 3 dB envelope) |
| Cymbals harsh | 4-6k band | drum `PeakFilter(4500, ...)` down; no boosts at 3-5 kHz anywhere |
| Not loud enough | I and PLR vs original | `--target` up 0.5-1 LU; stop when limiter GR max passes about 3 dB or flat-tops appear |
| Squashed, tiring | PLR, DR, LRA, limiter GR | `--target` down; `BUS_COMP["target_drop_db"]` 1.5 toward 1.0 |
| Bass boomy or weak | sub and bass bands | bass `LowShelfFilter(80, ...)` within 3 dB; `BALANCE["bass"]` within 1 dB |
| Snare hidden or buried (one track's evidence) | ask what the original does better: body, crack/snap, level, or less wash around it; then the `snare` line of `got analyze <original> <renders> --stems <stems>` (a proxy) | in the order tried: drums `BALANCE` +1 LU didn't win; the drum-stem `Compressor` off won; drum `PeakFilter(1500, 2, 1.0)` and the bus comp off didn't win; `crack_lift` at the end of the drum chain won, with the compressor already off |
| Solo too loud or sharp (one track's evidence) | `got analyze <split input> --stems <stems> --blocks`: "other" in the solo blocks vs the verses (+5 LU on that track) | a slow leveler on "other" lost blind; by the final version the person heard the solos as fine, with no solo-specific change |

Rows marked "one track's evidence" come from the first real session (Freaks EP, 2026-11; `crack_lift` is ADR 0016). Treat them as leads to test blind, not as settled moves.

## 5. Render one track, measure, blind A/B

Let them pick the track they know best or complain about most. Give the time estimate, then split in the background:

```
uv run got split "<album folder>/<track>.flac"
```

It prints the stems folder and the split input. Render the preset as it ships at two loudness targets: one about 1 LU above the original's, and one louder if they want loud (the research's caution: an already-limited CD pays for loudness with transients).

```
uv run got master "<stems folder>" "<split input>" --preset heavy-guitar --target <orig+1> --target <louder>
```

Check the printout against rule 1. Then start the A/B page in the background (it opens their browser):

```
uv run got abtest --ref "<album folder>/<track>.flac" "<render 1>" "<render 2>"
```

Tell them: everything plays at the same loudness, the original is labelled, the rest are shuffled; pick by ear (keys 1-9, space to play), then press **Reveal the files** and tell you which slot won and what it was. Stop the server when the round is done. Log the result.

## 6. Iterate, one change at a time

Copy the preset into the work folder once, then change one value per round:

```
mkdir -p "work/<album>/presets"
cp src/gain_of_thrones/presets/heavy_guitar.py "work/<album>/presets/v2.py"
uv run got master "<stems folder>" "<split input>" --preset "work/<album>/presets/v2.py" --name v2 --target <winning LUFS>
uv run got abtest --ref "<original>" "<previous winner>" "<v2 render>"
```

Next round: copy the winner to `v3.py`, and so on. Stop when they're happy, or when a change no longer wins. Keep every preset file; the log says which one won.

## 7. Album, then export

Carry the winning loudness to the album as a shift: shift = winner LUFS minus that track's original LUFS, and `--target` = the loudest track's original LUFS plus the shift. Give the time estimate (sum of track lengths times 3.8), then run in the background:

```
uv run got album "<album folder>" --target <LUFS for the loudest track> --preset "<winning preset>"
```

It is resumable if interrupted. Check every track's printout, and offer a quick A/B on one or two other tracks against their originals.

Then ask which format or formats they want, and explain the choice in plain words:

| Format | What it's for | Good to know |
|---|---|---|
| MP3 (320 kbit/s) | plays on anything | lossy; turned down until it can't clip after encoding (about 1 dB on the Freaks EP) |
| AAC (.m4a, 256 kbit/s) | Apple's usual format; most phones and cars play it too | lossy, with the same safety margin as MP3; ISRC and track-total tags have no slot |
| FLAC (24-bit) | lossless archive: exactly the rendered samples | for Apple Music and iPhones, ALAC is the lossless choice |
| ALAC (.m4a, 24-bit) | Apple Lossless: the same samples, for Apple Music and iPhones | ISRC and track-total tags have no slot |
| WAV (24-bit) | lossless, and any program opens it | no cover art, fewer tags (no lyrics or track total), biggest files |

Run one export per format they pick:

```
uv run got export "work/<album>/renders/album" --source "<album folder>" --format <mp3|aac|flac|alac|wav>
```

Each file's `carried:` line says whether the cover came along and which source tags the format has no slot for. Tell them about anything that didn't carry.

If they only want the track you worked on, or a few picked renders, skip the album run and pass the render files instead of the folder (export an album's tracks in one run: the lossy gain is shared only within a run):

```
uv run got export "work/<album>/renders/<track>_v3_-10LUFS.wav" --source "<album folder>" --format flac
```

Report where the files are and the export's numbers. Remasters of commercial records are for their personal listening.
