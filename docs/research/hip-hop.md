# Hip Hop

> Preset: `hip-hop` (`src/gain_of_thrones/presets/hip_hop.py`), draft, not yet picked in a blind A/B. Research notes: [hip-hop/](hip-hop/). Genre-neutral mastering, remastering and perception findings are in [heavy-metal-punk/](heavy-metal-punk/) and are linked, not repeated.

## Protect the low end and the vocal, and leave the beat's character alone

Hip hop puts two things first: the kick/808 low end, which uses up most of the mix-bus headroom, and a loud, forward vocal sitting on a beat whose mids are kept sparse ([SOS Inside Track: 21 Savage](https://www.soundonsound.com/techniques/inside-track-21-savage); [SOS, Noah "40" Shebib](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)). On a finished master both are mix decisions already made, so stem work can only nudge them. The separation evidence sets the same small envelope as for heavy music, with one twist: the genre's lo-fi, filtered samples are often deliberate, so the "other" stem should be cleared for the vocal rather than brightened. Loudness is where a remaster can do the most harm. Every classic hip hop CD remaster that could be paired with its original in the DR database measures 1 to 4 DR less dynamic, and the 2023 *Chronic* CD logs DR 7 against DR 11 to 14 for the 1992 CDs ([remasters.md](hip-hop/remasters.md)). *Inference:* treat golden-age CDs (DR 9 to 12) as having modest room for a gentle remaster, and treat 2000s+ masters (DR 4 to 8) as tonal-only jobs. Do not make them louder.

## Reissues changed content and loudness more than tone

The best-documented change in a hip hop reissue is legal, not sonic. After a 2006 jury verdict over an Ohio Players sample, *Ready to Die* lost samples on later pressings, and the "U.S. Amended Version" is now the default streaming edition ([SPIN](https://www.spinmagazine.com/2006/03/judge-orders-big-album-shelves/); [Qobuz](https://www.qobuz.com/us-en/album/ready-to-die-the-remaster-us-amended-version-94568-the-notorious-big/0075679456861)). De La Soul's catalog reached streaming in 2023 only after samples were cleared again for that format ([Complex](https://www.complex.com/music/de-la-soul-streaming-platforms-reservoir-interview)). *Inference:* a hip hop "remaster" can differ from the original in what it contains, which no processing repairs, so the person's choice of rip matters more than for most genres.

The loudness pattern is consistent across the DR database pairs ([dr.loudness-war.info](https://dr.loudness-war.info/album/list?artist=Notorious); details in [remasters.md](hip-hop/remasters.md)):

| Album | Original CD | Later CD/digital | Vinyl |
|---|---|---|---|
| *Illmatic* | DR 11 (1994) | DR 7 (*Illmatic XX*, 2014, incl. bonus tracks) | |
| *Ready to Die* | DR 9 (1994) | DR 8 (2004 remaster) | DR 13 (1995) |
| *Life After Death* | DR 10 / 9 (1997) | DR 6 (2014, lossy log) | |
| *The Chronic* | DR 11 and DR 14 (1992, two logs disagree) | DR 9 (2005), DR 7 (2023) | DR 13 to 15 |
| *Enter the Wu-Tang* | DR 11 (1993/94) | DR 8 (2007 Japan K2) | |
| *Doggystyle* | DR 11 (1993) | DR 10 / 8 (2001), DR 8 (2005 DVD-A) | |

For contrast, Kanye West's *My Beautiful Dark Twisted Fantasy* (2010 CD) logs DR 5 and *Yeezus* DR 4 ([DR DB](https://dr.loudness-war.info/album/view/162078); [DR DB](https://dr.loudness-war.info/album/view/71700)), and *The Low End Theory* DR 12 ([DR DB](https://dr.loudness-war.info/album/view/68793)). Vinyl DR is not comparable to CD DR (inference: surface noise and clicks inflate the peaks). Complaints found were about squashed remasters, removed samples and pressing faults, all anecdotal ([DVD Talk on *The Chronic*](https://forum.dvdtalk.com/sitemap/t-558775.html); [Head-Fi on *Ready to Die*](https://www.head-fi.org/threads/notorious-b-i-g-ready-to-die-remaster-vs-original.245242/)). The one mastering engineer quoted on loudness, Brian "Big Bass" Gardner, does not object to loud masters, only to distortion, and names pop and hip hop as the main sources of over-compressed mixes ([Mix](https://www.mixonline.com/recording/brian-big-bass-gardner-qa-366242)). No sourced statement was found from an engineer about remastering hip hop catalog or keeping its sampled lo-fi character. That is the biggest gap in this report.

## Demucs was barely tested on rap, so measure every track

No published work breaks Demucs scores out by genre. MUSDB18, the benchmark behind htdemucs_ft's 9.0 dB SDR, has 8 rap tracks out of 150 ([tracklist](https://raw.githubusercontent.com/sigsep/website/master/content/datasets/assets/tracklist.csv); [Demucs README](https://cdn.jsdelivr.net/gh/facebookresearch/demucs@main/README.md)). On MoisesDB, pooled over all genres, HT-Demucs scores **vocals 10.05, bass 11.64, drums 10.94, other 7.00 dB SDR**, so "other" is again the weakest stem ([MoisesDB, ISMIR 2023](https://archives.ismir.net/ismir2023/paper/000073.pdf)). The heavy-music report's remixing evidence still applies: a 6 dB vocal boost via separation gave "small but perceptible" degradation ([Wierstorf et al.](https://aes2.org/publications/elibrary-page/?id=19277)). The same envelope therefore holds: stem gain within ±2 dB, EQ within ±3 dB at Q ≤ 1.5.

Loud masters are the measured risk. On musdb-XL (6 to 7 dB of limiting), Demucs v3's **drum SDR fell 2.5 dB while bass and other barely moved**, and loudness-normalizing the input cut that drop to 0.4 dB ([Jeon and Lee, arXiv 2208.14355](https://ar5iv.labs.arxiv.org/html/2208.14355)). *Inference:* if that carries over to htdemucs_ft, a loud rap master puts drum content into "other" and the residual, which the pipeline adds back at unity. Lowering the input before separation is a cheap test, but its effect on v4 is unmeasured.

The genre-specific failure modes are documented only by anecdote ([separation.md](hip-hop/separation.md)):
- **808s:** vendor guides file 808s under "bass" and warn that 808 kick and sub split unpredictably ([drumsplit](https://drumsplit.pages.dev/guides/drum-separation-for-hip-hop)). *Inference:* the click goes to "drums" and the sustained tail to "bass". Processing the two stems differently pulls an 808's attack and tail apart, so bass-stem moves should stay small, and any keyed ducking between the two stems is suspect.
- **Samples:** boom-bap samples leave traces in the drum stem ([drumsplit](https://drumsplit.pages.dev/guides/drum-separation-for-hip-hop)). *Inference:* a soul sample gets split by role, with its singer in "vocals" and its drums in "drums", so a vocal-stem lift also lifts the sampled singer.
- **Ad-libs, doubles, throws:** stacked ad-libs stay with the lead; backing vocals and doubles are where models disagree ([deton24 UVR guide](https://docs.google.com/document/u/0/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c/mobilebasic), about Roformer models, not Demucs). *Inference:* reverb and delay throws split between "vocals", "other" and the residual, so a vocal-stem gain move does not move them by the same amount. No gate on the vocal stem: dense ad-libs and throws are exactly what a gate would chop.
- **Scratches and crackle** have no target stem and most likely land in "other" or the residual (inference). This is another reason not to gate or expand "other".

## Each complaint maps to a stem move

Named engineers here describe chains more than numbers. Frequencies marked "sourced" come from the cited mix references, and amounts are this report's estimates for stem work unless marked otherwise.

| Complaint / stem | Move | Numbers | Basis |
|---|---|---|---|
| 808 inaudible on small speakers (bass) | Bell on the 808's harmonics, no saturation | +1 to +2 dB at ~100 Hz, Q 1 | Frequency sourced: Maddmix adds harmonics "around 100 Hz" ([SOS](https://www.soundonsound.com/techniques/inside-track-21-savage)); amount inference |
| Sub too heavy, limiter working hard (bass) | Low shelf down | -1 to -2 dB below ~50 Hz | 40 cut bottom to free headroom for loudness ([SOS](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)); 808 fundamental ~50 to 62 Hz ([iZotope](https://www.izotope.com/en/learn/how-to-mix-808s.html)); amount inference |
| Low end muddy (bass, other) | Broad low-mid cut | -1.5 to -2.5 dB at 250-350 Hz, Q ≤ 1 | Mud range sourced for rock/metal only ([heavy-metal-punk.md](heavy-metal-punk.md)); hip hop figure is a gap |
| Kick lost under the 808 (bass) | Keyed dip on the bass stem's kick band, keyed from raw drums | 40-100 Hz, max -2 dB | Dynamic band ducking sourced ([iZotope](https://www.izotope.com/en/learn/how-to-mix-808s.html)). On stems it is inference and risky (split 808), so it is opt-in, not in the preset |
| Vocal buried (vocals, other) | Vocal level, then a keyed pocket in "other" while the vocal is loud | Vocal +1 to +1.5 dB; other 1.5-4 kHz, max -2 dB | Sparse mids for the vocal sourced (Maddmix); amounts inference |
| Vocal muddy (vocals) | High-pass, low-mid cut | HPF 80-100 Hz; -1.5 to -2 dB at ~250 Hz | HPF from blog guides (search summary, [genre_specific.md](hip-hop/genre_specific.md)); cut inference |
| Vocal sibilant (vocals) | De-ess before brightening | 5-8 kHz | Blog guides; Derek Ali used a dbx 902 ([SOS](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)); band sourced for metal ([heavy-metal-punk.md](heavy-metal-punk.md)) |
| Vocal dull (vocals) | Presence and air | +1 to +2 dB at 3-5 kHz; +1 dB shelf from 10 kHz | Presence "around 5 kHz" from blog guides; amounts inference |
| Sample dull or lo-fi ("other") | Leave it, or at most a +1 dB shelf above 8 kHz | | 40 lo-fi'd keys and whole songs on purpose ([SOS](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)); restraint is inference |
| Snare lacks crack (drums) | Boxy-mid dip and top; or the opt-in `crack_lift` stage | -1 dB near 1 kHz; +1 dB shelf above 8 kHz | Derek Ali cut ~1 kHz and added top on the snare ([SOS](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)); `crack_lift` from ADR 0016 |
| Hats harsh (drums) | Gentle dip | -1 to -1.5 dB at 3-6 kHz | Harshness band sourced for metal cymbals only ([heavy-metal-punk.md](heavy-metal-punk.md)); hip hop figure is a gap |
| Already squashed (DR 4-8 source) | No added loudness; target at or below the source's integrated LUFS | | DR pattern above; Gardner on crunch ([Mix](https://www.mixonline.com/recording/brian-big-bass-gardner-qa-366242)); inference |

Two warnings apply to this table. First, all of these are mix-stage ideas aimed at stems carved out of a finished master, so the heavy-music report's caveat holds: a move on a summed stem hits its bleed too. Second, the low end consumes most of the headroom. *Inference:* any bass-stem lift shows up first as limiter gain reduction, so read `GR max` and flat-tops after every low-end move.

## Loudness: match the source's era, ceiling as before

Spotify normalizes to -14 LUFS, and its Loud setting to -11 LUFS. It asks for true peaks below -2 dBTP on masters louder than -14 LUFS ([Spotify for Artists](https://support.spotify.com/us/artists/article/loudness-normalization/)). Blog and vendor guides put "competitive" modern hip hop at -10 to -7 LUFS integrated. These are low-authority figures read from search summaries ([genre_specific.md](hip-hop/genre_specific.md)). Ian Shepherd's -10 LUFS short-term guideline and the loudness-matched perception studies carry over unchanged ([heavy-metal-punk.md](heavy-metal-punk.md#the-clients--95-lufs-costs-about-3-db-of-peak-headroom)). Two named mixers who state a loudness view both avoided master-bus limiting in their own mixes: 40 used an L2 for reference mixes only, and Derek Ali sent mixes to tape for Mike Bozzi to master ([SOS](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines); [SOS](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)). *Position (inference):* for a DR 9 to 12 CD, a target of about -11 to -10 LUFS is in-genre and leaves the limiter in Katz's 1 to 3 dB range. For a DR 4 to 8 master, keep the target at the source's own loudness and spend the session on tone. Bus compression should use a slower release than for rock (inference: fast release on a bus dominated by an 808 modulates the waveform and reads as distortion). The -1.2 dBTP ceiling stays for lossless; lossy export already measures to -2 dBTP.

## The draft preset

`hip-hop` applies the table's middle values and nothing that the evidence flags as risky:
- drums: 25 Hz HPF, -1 dB at 1 kHz, +1 dB shelf from 8 kHz, no compressor (the drum stem is the one limiting damages most).
- bass: 25 Hz HPF (keeps the 808 fundamental), -1.5 dB at 300 Hz, +1.5 dB at 100 Hz, light 2:1 compression with slow release.
- vocals: 90 Hz HPF, -1.5 dB at 250 Hz, de-ess 5-8 kHz, then +1.5 dB at 4 kHz, +1 dB shelf from 10 kHz, 2:1 compression. No gate.
- other: 40 Hz HPF, -1.5 dB at 300 Hz, and a vocal pocket at 1.5-4 kHz keyed from the raw vocal stem (max -2 dB). No brightening, gating or expansion.
- Balance: vocals +1.0 LU, the rest 0. Bus: 2:1, 30 ms attack, 200 ms release, about 1 dB of integrated drop. Ceiling -1.2 dBTP.

Left out on purpose: the kick/808 keyed dip (split 808 risk), any saturation, any low shelf boost, and any change to the sample's top end.

## Open questions

No study measures htdemucs_ft on rap, 808s, samples or limited hip hop masters. The 808 split question is measurable per track: compare each stem's energy below 60 Hz and its alignment with kick onsets. No engineer source covers remastering hip hop catalog. The low-mid mud and hat-harshness bands are borrowed from rock and metal sources. The blind A/B is the test of all of it.
