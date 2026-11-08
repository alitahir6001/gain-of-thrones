# General Professional Mastering Best Practice

Research notes, compiled 2026-11-05. Source-quality key: [P] = primary (engineer's own words / platform documentation), [S] = secondary (vendor blog, trade-press teaser, aggregator). Several high-value primary sources could not be retrieved: Sound On Sound's Ian Shepherd "Mastering Essentials" series (2020) is paywalled (only standfirsts were readable), AES TD1004 returned HTTP 403, iZotope's signal-chain article and FabFilter's mastering-EQ page returned 404. These are flagged under Gaps.

Context for the writer: the target file is a 16-bit/44.1 kHz CD rip at about -11 LUFS integrated with true peaks at +0.2 dBTP, for personal headphone listening. Where a finding bears directly on that file, it is noted under Inferences.

## Signal chain order (EQ vs compression, M/S, saturation, limiting, dither last)

### Takeaway
The only ordering rules the retrieved sources state firmly are at the end of the chain: the limiter sits after any compression, and dither is applied once, as the very last step, only when reducing word length. EQ/compression order is a judgment call, and no primary source retrieved this session prescribes it.

### Cited Findings
- A mastering engineer interviewed by MusicRadar: "As a rule of thumb, the compressor should be the final device prior to the limiter." [S] — [MusicRadar, "Master bus compression explained... by a mastering engineer"](https://musicradar.com/news/tech/master-bus-compression-explained-by-a-mastering-engineer-629292)
- Dither must be the final process: apply it "once, as the final step before export"; any later gain change or sample-rate conversion undermines it. Do not dither in the DAW and again in a plug-in. [S, vendor] — [iZotope, "What Is Dithering in Audio?" (Jan 11, 2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- iZotope's Ozone workflow for CD: master and bounce at high resolution with DAW dither off, then convert to 44.1 kHz while staying at 32-bit, then enable dither in Ozone and set the output to 16-bit. In other words, sample-rate conversion comes before dither. [S] — [iZotope (2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- Sage Audio advises loading the whole chain at once with subtle settings, rather than adding plug-ins one at a time, because settings interact. It also advises re-checking tonal balance after compression. [S] — [Sage Audio, "Mastering Compression Settings"](https://www.sageaudio.com/articles/mastering-compression-settings)
- FabFilter: fast limiting or hard clipping creates inter-sample peaks, and "the same happens during operations like MP3 conversion". So true-peak control belongs at the very end of the processing chain, after any clipper. [P, manufacturer manual] — [FabFilter Pro-L 2 help, True Peak Limiting](https://www.fabfilter.com/help/pro-l/using/truepeaklimiting)

### Inferences
- A defensible order consistent with the sources: corrective/subtractive EQ, then (optional) gentle compression, then tonal/M/S EQ and saturation if used, then a clipper if used, then a true-peak limiter, then SRC (none needed here, since the file stays at 44.1 kHz), then dither to the final word length. Only the "compressor before limiter" and "dither last" parts are sourced; the rest is inference.
- For this project, if the output is 24-bit or 32-bit float FLAC for personal use, the "dither last" rule only matters when writing a 16-bit file.

### Gaps
- No primary source retrieved this session on EQ-before-vs-after-compression rationale, or on where M/S and saturation stages go. The iZotope signal-chain article (izotope.com/en/learn/mastering-signal-chain.html) returned 404. Katz's book *Mastering Audio* covers this but was not accessible online.

## EQ philosophy (subtractive vs additive, move sizes, Q, M/S, linear vs minimum phase, high-pass)

### Takeaway
Mastering EQ moves are broad and small: the commonly cited rule of thumb is within about ±3 dB with wide Q. Needing more than that suggests the mix needs fixing. Ian Shepherd's framing is "balance, don't match": EQ toward a good overall tonal balance rather than copying a reference curve.

### Cited Findings
- Shepherd calls EQ "the single most important factor in mastering, once you've decided the loudness". His SOS EQ article is titled "Balance, Don't Match". [P, standfirst only] — [Sound On Sound, Ian Shepherd, Nov 2020](https://www.soundonsound.com/techniques/mastering-essentials-eq-balance-dont-match)
- Rule of thumb: keep boosts and cuts within about 3 dB, since larger moves suggest the mix needs rework. Use wide Q rather than narrow. The vendor's own "Master Mode" caps moves at 4 dB and Q 1.5. [S, vendor, 2017] — [Mastering The Mix, "How To EQ During Mastering"](https://www.masteringthemix.com/blogs/learn/how-to-eq-during-mastering)
- Typical frequency moves from the same source:
  - Gentle wide-bell cut at 20 or 40 Hz to gain headroom and tighten the bass.
  - Small cut at 160 or 320 Hz for boxiness, or a boost at 320 Hz for body (risk: mud).
  - Wide boost around 80 Hz for warmth (costs headroom).
  - 3–7 kHz for presence on vocals, snare and guitars.
  - High shelf above 10 kHz for "sparkle".
  - Mid-channel boost at 1–5 kHz to bring a centred lead vocal forward (M/S use).
  
  [S] — [Mastering The Mix](https://www.masteringthemix.com/blogs/learn/how-to-eq-during-mastering)
- Mastering EQ "uses broad, gentle curves to adjust the overall tonal balance", unlike surgical mix EQ. A/B bypass checks are recommended. [S, search-result summary of an aggregator] — [Sound On Sound series listing](https://www.soundonsound.com/series/audio-mastering-essentials-how-achieve-great-sounding-results)

### Inferences
- For a punk/thrash CD rip, the "within ±3 dB, wide Q" rule is a sensible ceiling. Larger corrections on a finished 1980s master are a sign the problem may not be EQ-fixable.
- Bob Katz's general position (see the Compression section) is to judge by ear rather than by fixed numbers. The same logic applies to EQ move sizes.

### Gaps
- Linear vs minimum phase: no retrieved source gave a substantive comparison (pre-ringing on linear-phase low-frequency moves, phase shift on minimum-phase). The FabFilter mastering-EQ learn page returned 404. Mastering The Mix only notes that a linear-phase mode "preserves phase".
- Side-channel high-pass frequencies (commonly quoted elsewhere as roughly 100–150 Hz) and master high-pass values: no source retrieved this session gives a number.
- No primary engineer interview (Ludwig, Calbi, Weinberg) with EQ numbers was retrieved.

## Bus compression in mastering (ratios, gain reduction, attack/release, multiband)

### Takeaway
Mastering compression is gentle: ratios around 1.5:1–2:1 and roughly 1–3 dB of gain reduction are the recurring figures. Bob Katz insists there is no universal safe amount: it depends on the unit, the attack/release relative to tempo, and the material. He is skeptical of multiband compression.

### Cited Findings
- Katz on how much gain reduction is acceptable: "6dB gain reduction on a vocal solo with a nicely-designed tube opto compressor may be barely noticeable" but "1 dB on an entire mix with the wrong unit can be severely degrading!" His advice is "Use your ears". [P] — [Bob Katz, Digido FAQ "Compression – How much gain reduction to use? Pumping…", Mar 30, 2017](https://www.digido.com/?p=1509)
- Katz on pumping: pumping depends on attack/release relative to the music's tempo and frequency content, not on a 10–12 dB threshold. "Only a couple or 3 dB of compression will cause audible pumping or breathing effects" with the wrong settings. Less audible noise means "you can get away with more compression". [P] — [Katz, Digido (2017)](https://www.digido.com/?p=1509)
- Katz on multiband compression: "I'm not a fan of multiband compression as it can produce a very unnatural sound." [P] — [Katz, Digido (2017)](https://www.digido.com/?p=1509)
- Katz: compression is "a powerful esthetic tool" and should not be used merely as a loudness tool. "A hotter record means lower sound quality." [P] — [Bob Katz, "Level Practices (Part 2)", digido.com](https://www.digido.com/portfolio-item/level-practices-part-2/)
- Katz (via a Gearspace user paraphrasing his book): discussion of upward/parallel compression at 2:1–2.5:1. [S, forum paraphrase, unverified against the book] — summarised in search results; book not accessed
- Katz-derived MIT course note: it is "probably better to remove all the labels on the knob (except slow and fast) and just listen". [S, course notes quoting Katz's essay] — [MIT 21M.380 lecture 10 notes](https://dspace.mit.edu/bitstream/handle/1721.1/122035/21m-380-spring-2012/contents/lecture-notes/MIT21M_380S12_lec10.pdf)
- Typical mastering compressor settings: ratio 1.5:1–2:1, moderately slow attack, fast or auto release, gain reduction kept under about 3 dB. [S, vendor] — [Mastering The Mix](https://www.masteringthemix.com/blogs/learn/how-to-eq-during-mastering)
- Starting point: about 40 ms attack, about 150 ms release, soft knee, lookahead off. [S, one vendor's starting point] — [Sage Audio](https://www.sageaudio.com/articles/mastering-compression-settings)
- Bobby Owsinski: set the mastering compressor to 1.5:1 or 2:1, and "think gentle here instead of aggressive". [S, author/educator] — [Bobby Owsinski blog, self-mastering tips](https://bobbyowsinskiblog.com/self-mastering-tips/)
- Shepherd's SOS compression article (Dec 2020) states that "compression in mastering is different — both the goals and the methods". It describes "three different mastering compression techniques" and argues "the goal is to be invisible". [P, standfirst only; body paywalled] — [Sound On Sound, "Mastering Essentials: Compression & Limiting"](https://www.soundonsound.com/techniques/mastering-essentials-compression-limiting)

### Inferences
- The source material for this project is already a CD-era master at about -11 LUFS. Little or no further compression is likely warranted, consistent with Katz's warning that hotter means lower quality. This is inference; it depends on listening.
- Fast release on dense, distorted guitars risks audible pumping, per Katz's tempo/frequency point. Slower attack lets transients through.

### Gaps
- The three techniques in Shepherd's SOS article could not be read (paywall).
- No retrieved interview gives Ludwig, Calbi or Weinberg compression settings. A Gearspace "Q&A with Howie Weinberg" thread surfaced in search but was not fetched.

## Limiting (acceptable gain reduction, true-peak ceilings, oversampling, inter-sample peaks, clipping vs limiting)

### Takeaway
Katz describes 1–3 dB of peak limiting as potentially "very invisible", though invisible is not the same as natural. Ceilings should be set as true peak: -1 dBTP is the common streaming recommendation, and Spotify asks for -2 dBTP on masters louder than -14 LUFS. Oversampled/true-peak limiting (for example 4x) holds inter-sample overs to about 0.1 dB.

### Cited Findings
- Katz: "1 to 3 dB or so gain reduction can be very invisible", "but invisible is not the same as 'natural.'" For loudness without changing the sound, use peak limiting; for a deliberate musical change, "some sort of compression rather than limiting may be the key". [P] — [Katz, Digido (2017)](https://www.digido.com/?p=1509)
- Katz: starting a limiter at a fixed threshold such as -6 dBFS is "bad advice"; gain reduction is "not an indication of loudness". [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)
- A MusicRadar mastering engineer advises aiming for about 2 dB of gain reduction into the limiter. A homerecording.com poster says most MEs use about 2–3 dB through a limiter. [S; forum claim anecdotal] — [MusicRadar](https://musicradar.com/news/tech/master-bus-compression-explained-by-a-mastering-engineer-629292)
- Spotify: keep true peak below -1 dBTP for lossy formats (Ogg/Vorbis, AAC). If the master is louder than -14 LUFS integrated, keep true peak below -2 dBTP "to avoid extra distortion". [P, platform doc, current page] — [Spotify for Artists, "Loudness normalization"](https://support.spotify.com/us/artists/article/loudness-normalization/)
- Shepherd: master with true peaks no higher than -1 (dBTP). [P] — [Production Advice, "How loud?" (orig. Sept 26, 2017)](https://productionadvice.co.uk/how-loud/)
- FabFilter, on inter-sample peaks: fast limiting or hard clipping produces inter-sample (true) peaks. The reconstructed analogue waveform can exceed the sample values, so a DAC may clip even when the samples do not, and lossy (MP3) conversion does the same. [P, manufacturer] — [FabFilter Pro-L 2 help](https://www.fabfilter.com/help/pro-l/using/truepeaklimiting)
- FabFilter on oversampling: oversampling is "the best way" to minimise inter-sample peaks and distortion. With 4x oversampling and 0.1 ms minimum lookahead, inter-sample peaks stay within about 0.1 dB. True-peak mode works in two stages, reducing existing true peaks and then smoothing its own overshoot, and adds about 5 ms latency. [P] — [FabFilter Pro-L 2 help](https://www.fabfilter.com/help/pro-l/using/truepeaklimiting)
- Katz's K-System article bases its peak guidance on sample peaks, not inter-sample peaks. It is an older text and predates widespread true-peak metering. [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)

### Inferences
- The source file's +0.2 dBTP true peak means it already has inter-sample overs: playback DACs or lossy encoders may clip it. Any remaster should end with a true-peak limiter (oversampled) set to about -1 dBTP. That ceiling is safe for headphone playback through any decoder.
- Because the user is not streaming the result, Spotify's -2 dBTP rule for loud masters applies only if the file is later encoded lossy. For lossless personal playback, -1 dBTP gives margin.

### Gaps
- Clipping vs limiting: no primary source retrieved this session compared soft-clipping before the limiter with limiting alone, beyond FabFilter's note that hard clipping creates inter-sample peaks.
- AES TD1004 (2015) true-peak and loudness recommendations could not be fetched (HTTP 403). From prior knowledge, not verified this session: TD1004 recommends -16 to -20 LUFS for streaming and -1 dBTP max (-2 dBTP for low-bit-rate codecs). The writer should treat this as unverified.

## Loudness (LUFS targets, streaming normalization values, PLR/PSR, loudness war, Dynamic Range Day, loudness penalty)

### Takeaway
Most services normalize music to about -14 LUFS, and Apple Music to -16 LUFS. Shepherd's practical guideline is to keep the loudest sections no louder than about -10 LUFS short-term with true peaks at or below -1 dBTP, which typically lands -11 to -14 LUFS integrated. Louder masters are simply turned down, so extra loudness buys nothing on normalized playback.

### Cited Findings
- **Spotify (current doc):**
  - Target "-14 dB LUFS" per ITU 1770. Premium users can pick Loud "-11dB LUFS", Normal "-14dB LUFS" or Quiet "-19dB LUFS".
  - The Loud setting applies a limiter "set to engage at -1 dB (sample values), with a 5 ms attack time and a 100 ms decay time".
  - Positive gain for quiet masters is capped so that 1 dB of headroom remains.
  - Album mode normalizes the whole album as one, preserving track-to-track level relationships. Track mode is used for shuffle and playlists.
  
  [P] — [Spotify for Artists, "Loudness normalization"](https://support.spotify.com/us/artists/article/loudness-normalization/)
- **Apple Music:** Sound Check moved to LUFS measurement and is enabled by default on new iOS devices and Macs. It follows AES TD1008 and normalizes to -16 LUFS. The Apple Music web player did not normalize at the time (Mar 2022). [P-ish: Ian Shepherd writing on MeterPlugs; no Apple doc found] — [MeterPlugs, Ian Shepherd, "Apple Switches to LUFS, Enables Sound Check by Default", Mar 23, 2022](https://www.meterplugs.com/blog/2022/03/23/apple-switch-to-lufs.html)
- Conflict: Mastering The Mix claims Apple streams at an average of -14 LUFS with Sound Check on. This conflicts with Shepherd's -16 figure and I could not verify it. [S] — [Mastering The Mix, "producing music for Apple Music"](https://www.masteringthemix.com/blogs/learn/producing-music-for-apple-music)
- **YouTube:** changed its loudness reference to -14 LUFS in 2019. YouTube and TIDAL do not turn quieter music up, only down. [P-ish] — [MeterPlugs, YouTube changes loudness reference to -14 LUFS (Sept 18, 2019)](https://www.meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html); [Production Advice, "How loud?"](https://productionadvice.co.uk/how-loud/)
- **YouTube measurement:** the "content loudness" value in Stats for Nerds shows how much YouTube turned a video down. One source says this figure can deviate up to about 3 dB from expected. [S, forum/aggregator] — [Production Advice, YouTube Music](https://productionadvice.co.uk/youtube-music/)
- **TIDAL and Amazon:** about -14 LUFS (Shepherd, 2022). [P-ish] — [MeterPlugs (2022)](https://www.meterplugs.com/blog/2022/03/23/apple-switch-to-lufs.html). Secondary sources conflict on TIDAL: some say it normalizes HiFi/Max tiers, some that it doesn't, and some that album normalization is always on. [S] — [Elysia, "Mastering for Spotify, YouTube, Tidal…"](https://www.elysia.com/mastering-for-spotify-youtube-tidal-amazon-music-apple-music-and-other-streaming-services/)
- **Deezer:** commonly cited at -15 LUFS. **SoundCloud:** reportedly no normalization. [S, unverified] — [Elysia](https://www.elysia.com/mastering-for-spotify-youtube-tidal-amazon-music-apple-music-and-other-streaming-services/)
- **Shepherd's guideline:**
  - Master no louder than -10 LUFS short-term at the loudest moments, with true peaks no higher than -1. He calls this his "simplest and best guideline".
  - Don't chase a specific integrated number. Following the short-term rule, popular genres usually land about -11 to -14 LUFS integrated.
  - A YouTube loudness penalty of about -3 dB is acceptable for the loudest material; beyond that, louder is a "losing battle".
  - One master is enough; there's no need for per-platform versions.
  - The free Loudness Penalty site (with MeterPlugs) previews per-platform turn-down.
  
  [P] — [Production Advice, "How loud?" (orig. Sept 26, 2017, updated since)](https://productionadvice.co.uk/how-loud/)
- **Dynamic Range Day (first held March 20, 2010):**
  - The loudness war pushes average level against the CD's full-scale ceiling, causing "distortion, lost punch, and a flat, lifeless sound" plus listener fatigue.
  - Metallica's *Death Magnetic* is the emblem: 20,000+ fans petitioned for a remaster, and much of the album has about 2 dB dynamic range.
  - Until recently, even the loudest CDs kept at least 8 dB "even at their loudest points".
  
  [P] — [Production Advice, "Dynamic Range Day" (Feb 24, 2010)](https://productionadvice.co.uk/dynamic-range-day/)
- **Katz on crest factor:** a low crest factor "can only be obtained using dynamic-range compression". Material with crest factor well below 14 dB should not be peaked to full scale because it will "sound too loud". [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)
- **Katz K-System:**
  - Calibrate monitors so meter 0 dB = 83 dB SPL per channel (C-weighted, slow) using pink noise at -20 dBFS RMS.
  - K-20 suits wide-range material, K-14 most pop/rock home-listening material, K-12 broadcast. "Use K-20 while mixing and save K-14 for the calibrated mastering suite."
  - In practice, K-14 implies average level about 14 dB below full scale, i.e. a peak-to-average ratio of about 14 dB.
  
  [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)

### Inferences
- The source file at about -11 LUFS integrated already sits at the loud end of Shepherd's -11 to -14 window. On Spotify Normal it would be turned down about 3 dB; on Apple about 5 dB. For personal headphone listening there is no loudness benefit to pushing it louder. A remaster that ends up somewhat quieter (e.g. -12 to -14 LUFS) after true-peak-safe limiting loses nothing in normalized playback.
- PLR (peak-to-loudness ratio) = true peak minus integrated loudness. For the source file that is +0.2 - (-11) = 11.2 dB. This is arithmetic on the user-supplied numbers, not a measurement.

### Gaps
- PLR/PSR target values: neither retrieved Shepherd page gave numeric PLR/PSR targets. His meter (MeterPlugs Dynameter) and other writings discuss PSR, but no figure was retrieved.
- EBU R128 (-23 LUFS broadcast target, -1 dBTP max) and ITU-R BS.1770 (K-weighting, gating at -70 LUFS absolute and -10 LU relative) were not fetched this session. These are prior-knowledge values; treat them as unverified.
- No current (2025-2026) official Apple, YouTube, TIDAL or Amazon documentation was found. Values above rely on Ian Shepherd/MeterPlugs (2019, 2022) plus vendor blogs. The Spotify page is the only current platform primary source.

## Dither and word length

### Takeaway
Dither only when reducing bit depth, exactly once, as the final step. For 16-bit output, noise-shaped dither is worthwhile; for 24-bit, flat TPDF is enough; 32-bit float output needs none.

### Cited Findings
- "Dithering should always be off unless you're bouncing audio to lower bit depths." [S, vendor] — [iZotope (Jan 11, 2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- When exporting 24-bit or lower, dither, even from a 32-bit float session. When exporting 32-bit float, dither isn't needed. [S] — [iZotope (2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- For 16-bit, noise shaping (which EQs dither noise away from sensitive frequencies) "can make a noticeable difference". For 24-bit, dither noise is inaudible even without shaping, so flat TPDF is sufficient. [S] — [iZotope (2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- Don't assume a plug-in self-dithers, and don't double-dither between DAW and plug-in. [S] — [iZotope (2023)](https://www.izotope.com/en/learn/what-is-dithering-in-audio.html)
- Katz: 24-bit has a "theoretically 48 dB better signal-to-dither-ratio than 16-bit", and hitting 0 dBFS is unnecessary for good SNR at 20–24 bits. [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)

### Inferences
- For this project, the source is 16-bit, but processing (any gain change, EQ, limiting) yields higher-resolution output. Exporting 24-bit FLAC with TPDF dither (or 32-bit float with no dither, if the player supports it) avoids a second 16-bit truncation and keeps headroom. Exporting back to 16-bit needs dither, ideally noise-shaped.

### Gaps
- No primary source (e.g. Katz's book chapter, Weiss/POW-r docs) on specific noise-shaping curve choices was retrieved.

## Loudness-matched A/B, reference tracks, monitoring and translation, ear fatigue

### Takeaway
Loudness-match every comparison, because louder reliably sounds "better". Use a calibrated, consistent monitoring level (Katz: 83 dB SPL reference). Check against references for tonal balance, but balance rather than imitate (Shepherd). Detailed sourced guidance on headphone-vs-speaker translation, mono checks and fatigue was not retrievable this session.

### Cited Findings
- Katz: calibrated monitoring at a fixed gain (meter 0 = 83 dB SPL) means "0 dB always represents the same calibrated SPL". Constant use of the 88–90+ dB "red zone" means the monitor is miscalibrated or the mix is overcompressed. Severe processing distortion often appears when monitor gain has to be turned below -6 dB. [P] — [Katz, "Level Practices (Part 2)"](https://www.digido.com/portfolio-item/level-practices-part-2/)
- Shepherd: "balance, don't match". References inform tonal balance but should not be copied by curve-matching. [P, title/standfirst only] — [SOS, Nov 2020](https://www.soundonsound.com/techniques/mastering-essentials-eq-balance-dont-match)
- Shepherd: heavily compressed CDs cause listener fatigue ("tiredness and headaches"). [P] — [Production Advice, Dynamic Range Day (2010)](https://productionadvice.co.uk/dynamic-range-day/)
- A/B bypass checks are recommended for mastering EQ. [S] — [SOS series listing via search summary](https://www.soundonsound.com/series/audio-mastering-essentials-how-achieve-great-sounding-results)
- Shepherd's Loudness Penalty tool previews how each platform will turn a track down, effectively giving a loudness-matched comparison. [P] — [Production Advice, "How loud?"](https://productionadvice.co.uk/how-loud/)

### Inferences
- For a headphone-only remaster, a practical analogue of Katz's fixed-gain monitoring is to fix the headphone volume, loudness-match the original and remaster (by integrated LUFS), and A/B blind. Otherwise the louder version wins by default.
- A mono check is still useful on headphones, because headphones hide phase/width problems that collapse on speakers. This is inference; no source was retrieved.

### Gaps
- SOS "Three Ms of Mastering" (Oct 2020) body was paywalled, so its content on monitoring and referencing couldn't be read.
- No retrieved source on ear-fatigue break intervals, monitoring level recommendations specific to headphones, or mono-compatibility checks in mastering.
- Bob Ludwig, Greg Calbi and Howie Weinberg interviews were not retrieved. No direct quotes from them are included.
