# Listen, then measure

The method behind Gain of Thrones, written for people. The agent follows the same loop, step by step, in `.claude/skills/remaster-session/SKILL.md`.

The roles: you are the client and the ears, the agent is the engineer's hands and meters. Every listening request maps to a measurement, and every render is checked by measuring the file itself before anyone listens to it.

## The loop

1. **Measure the original.** Loudness (LUFS), peak headroom (PLR), dynamics (DR), clipping (flat-top runs), tonal balance (bands). This is the baseline every render is compared against.
2. **Say what you want to hear different,** in your own words: "the guitars are cloudy", "the vocal sounds far away", "the cymbals vanish when it gets loud".
3. **Turn each complaint into a measurement and a move.** The genre's research report has the table. For heavy guitars: cloudy guitars are energy at 200-400 Hz, a buried vocal is guitar/vocal masking at 2.4-3.8 kHz, lost cymbals are guitar/cymbal masking at 3-6 kHz plus limiting.
4. **Change one thing, render, measure.** Before listening, check the render: loudness on target, true peak under the ceiling, no flat-tops, and a limiter that isn't working too hard.
5. **Blind, level-matched A/B** against the original and the previous best. A louder version sounds better even when it isn't, so the A/B page turns every version down to the quietest one and hides which is which.
6. **Keep what wins and repeat.** One change per round, so you know what made the difference.
7. **Do the album with one loudness shift for every track,** so the album's song-to-song flow survives, then export.

## Rules of thumb

- **Small moves.** Separated stems are not clean: the guitar stem holds vocal and cymbal bleed. Keep EQ within 3 dB at gentle (wide) Q and stem levels within 2 dB, and judge every move in the full mix, never solo.
- **Loudness costs something.** Every extra dB of loudness on an already-limited CD comes out of the peaks, which is where snare crack and cymbal decay live. Try a version close to the original's loudness next to a louder one, level-matched, and let your ears decide.
- **Keep a fixed listening volume** during a session, and if you can, check the winner on a second system.

## Lessons (measured, not guessed)

- **pedalboard's Limiter is not a ceiling.** It adds make-up gain: with a -6 dB threshold it put a test tone at 0 dBFS, and driven to loudness it left 1529 clipped flat-top runs on one track (DR7). The look-ahead true-peak limiter here left 0 at the same loudness.
- **Don't gate the "other" stem** (the guitars). A gate there also gates the separation errors and makes them audible. A gate on the vocal stem was fine and approved by ear.
- **Add the residual back.** Demucs stems sum to the input minus about 1% of its energy (a residual around -21 dB). That residual carries transients and cymbal top end, so dropping it loses them. A small residual means the stems sum back, not that they're clean.
- **Lower the input before splitting.** The CD peaked above 0 dBTP; lowering it 1.5 dB in float keeps the stems from clipping.
- **MPS crashes** on Apple Silicon with htdemucs_ft ("Output channels > 65536 not supported"). Splitting runs on the CPU: about 3.8 s per second of audio on an M1 Max.
- **MP3 encoding overshoots.** Predicting the MP3 gain from the WAV peaks (-0.8 dB) left the Freaks EP MP3s at up to -1.7 dBTP. Measuring after encoding needed -1.16 dB to get every file under -2 dBTP.
- **Demucs is random** when using shifts: splitting the same track twice gives slightly different stems. Mastering the same stems twice gives a bit-identical file.
- **Switch A/B versions by gain only.** An older A/B page re-synced by seeking every 250 ms and caused a periodic thump.
