# Genre-specific mixing/mastering practice: hip hop

Source caveat: the named-engineer material comes from Sound On Sound "Inside Track" columns by Paul Tingen (Derek Ali, Noah "40" Shebib, Maddmix) and one Mix Online Q&A (Brian "Big Bass" Gardner). It gives chains and principles but very few dB or Hz figures. Most numbers come from staff-written vendor guides (iZotope Learn) and small blogs, labelled as such. DR values come from user-submitted dr.loudness-war.info logs; vinyl and lossy rips are flagged because they do not represent the CD master. Items marked "search summary" were read in search results, not on a fetched page. Snare, hat and sample-bed specifics are thin.

## 1. Low end: kick vs 808/sub

### Takeaway
In modern hip hop the 808 and kick are set first and use up most of the mix-bus headroom. The 808 reaches small speakers through added harmonics around 100 Hz, from saturation or a distorted parallel copy. Kick-vs-808 conflict is usually handled by ducking only the kick's fundamental band in the 808, not the whole 808.

### Cited Findings
- Maddmix (named engineer, 21 Savage) says the 808 usually causes mix-bus overload, so he sets 808 and kick levels first and mixes the drums around them. Sound On Sound Inside Track: 21 Savage, [link](https://www.soundonsound.com/techniques/inside-track-21-savage)
- Maddmix duplicates the 808, smashes the copy with compression and/or distortion to add harmonics around 100 Hz, and blends it under the original so it translates to small speakers. Same source.
- Maddmix's gain staging: the "All Drums" group runs nearly to red, while "All Music" and "All Vocals" sit about halfway up the meter. Producer files often arrive peaking at 0 dB and get clip-gained down. Same source.
- Noah "40" Shebib (Drake, "Headlines"): on a sawbass he cut some bottom with EQ, used Renaissance Bass to supply content under 100 Hz, and added distortion with Avid Lo-Fi. On another bass line he cut around 95 Hz, pulled the Lo-Fi sample rate down to 4400 Hz and used light compression. Heavy bottom from the SSL pass was reduced to favour top-end "pop". Sound On Sound, [link](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)
- 40: the reduced bass gave the track headroom to be pushed louder for radio, since the track is snare-driven. Same source.
- iZotope Learn (vendor guide, Kevin McHugh): the original TR-808 kick is about a 50 Hz sine; the example kick's fundamental is 62 Hz. A dynamic EQ band at 62 Hz on the 808, sidechained to the kick, ducks only that band while the rest of the 808's harmonics decay freely. Sidechain settings are qualitative only ("very low" threshold, "medium" ratio, "relatively short" release). About 30% wet tube saturation; suggested headroom about 6 dB; on K-20 metering, mix peaks average +4 to +5 and the 808 sits at -3 to 0. [link](https://www.izotope.com/en/learn/how-to-mix-808s.html)
- iZotope Learn (vendor, Nick Messitte): high-pass the original bass at roughly 60 to 90 Hz and let a pure sine copy carry the lowest frequencies. [link](https://www.izotope.com/en/learn/8-tips-for-mixing-rap-and-hip-hop.html)
- Search summary only, not fetched: an iZotope kick/bass article puts most kick and bass energy between 20 and 160 Hz ([link](https://www.izotope.com/community/blog/how-to-mix-kick-and-bass)); a Major Mixing blog suggests multiband sidechain below about 100 Hz ([link](https://majormixing.com/10-tips-for-mixing-808)); another guide puts 808 energy at 30 to 60 Hz ([link](https://dj-master-web.vercel.app/en/blog/hiphop-rnb-mastering-en)).

### Inferences
- On finished masters, kick and 808 both land in the Demucs drums or bass stems. Stem gains of ±2 dB and small EQ moves cannot undo sidechain decisions. The safe moves are probably a small bass-stem shelf or bell in 40 to 60 Hz and a small 80 to 120 Hz bell for small-speaker audibility, within ±3 dB.
- The low end consumes most of the headroom, so a bass-stem boost will drive the limiter hardest. Check limiter gain reduction after any bass-stem increase.

### Gaps
- No sourced numeric sidechain attack, release or depth, and no named-engineer mono-below-X Hz figure.
- No sourced 200 to 500 Hz "mud" numbers for hip hop specifically.

## 2. Vocals

### Takeaway
Rap vocals are kept loud and forward, processed as one consistent chain and mixed last, onto a beat whose mids are left sparse. Named-engineer sources describe chains, not dB values. The numbers come from vendor or blog guides: high-pass at 80 to 100 Hz and presence around 5 kHz.

### Cited Findings
- 40 kept Drake's vocal loud and forward, processed all vocals as one piece for a consistent performance, and sent vocals to a separate bus from drums and music. Lead chain: Q8 EQ, De-esser, Renaissance EQ, RVox, a Pultec EQP-1A emulation and Smack!; vocal bus: RCompressor, SSL EQ and Q8. No dB figures. [link](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)
- Derek Ali (Kendrick Lamar, *To Pimp A Butterfly*) used a Renaissance Compressor with the threshold "all the way down to -18" (no ratio). Most vocal EQ, including high- and low-pass, was on the SSL console. S1 Imager for width, a Distressor for grit and top-end presence, a dbx 902 de-esser. Guest vocals got Fairchild 670 parallel compression. [link](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)
- Maddmix mixes vocals last. Sparse mids in the beat leave room for them, and he aims for roughly the same vocal levels in every mix (no dB given). [link](https://www.soundonsound.com/techniques/inside-track-21-savage)
- iZotope Learn (vendor): doubles panned to the same spot read as slapback or stutter if more than about 20 ms apart. Parallel compression on vocals is blended in, no ratios given. [link](https://www.izotope.com/en/learn/8-tips-for-mixing-rap-and-hip-hop.html)
- Search summary only, blog guides, figures not mapped to a specific URL: high-pass at about 100 Hz, or 80 to 100 Hz for male rap vocals; a gentle high shelf around 5 kHz, or presence at 5 to 8 kHz; de-ess after brightening EQ, though Audiofanzine argues for de-essing before EQ. Candidates: [musicguymixing](https://www.musicguymixing.com/how-to-eq-rap-vocals/), [Audiofanzine](https://en.audiofanzine.com/recording-mixing/editorial/articles/mixing-rap-vocals-part-2-eq.html), [Violet Recording](https://violetrecording.com/how-to-mix-rap-vocals/).

### Inferences
- Because rap vocals sit loud by convention, a vocal-stem raise of +0.5 to +1.5 dB is in-genre. Raising it further risks exposing Demucs bleed (hats and snare transients in the vocal stem).
- A presence bell on the vocal stem around 3 to 5 kHz needs a sibilance check, since sources agree brightening worsens sibilance.

### Gaps
- No sourced vocal-to-beat dB offset, compression ratios or gain-reduction figures, named-engineer de-ess band, or ad-lib placement numbers.

## 3. Drums, hats, snare

### Takeaway
Only fragments were found. Named engineers shape snare with EQ and transient tools, and they tolerate top-end "harshness" for pop.

### Cited Findings
- Derek Ali: API 550 on the snare, cutting around 1 kHz and adding high end. Neve 2254 for parallel drum compression and an SPL Transient Designer for thump. Little plug-in processing on drums. [link](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)
- 40: a Transient Designer made the kick "snappier and pointier". A Renaissance Axe on the drum master was barely working at a threshold of -1. He favoured top-end "pop and harshness" over heavy bottom. [link](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)

### Inferences
- In boom-bap the snare is often the loudest transient; in trap the 808 dominates. A drums-stem move therefore changes perceived punch more on boom-bap and limiter load more on trap. Not sourced.

### Gaps
- No sourced snare body or crack frequencies, no hi-hat harshness band, no measured boom-bap vs trap differences.

## 4. Samples and the beat bed ("other")

### Takeaway
Producers and engineers commonly degrade or filter musical parts (lo-fi, sample-rate reduction, rolled-off top) and keep the mids sparse so the vocal sits on top.

### Cited Findings
- 40 used Avid Lo-Fi heavily on the bass and on three of five extra keyboard parts, mostly sample-rate reduction and distortion. He recalls Drake asking him to lo-fi entire songs, and that he first resisted taking the top end out. [link](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)
- Maddmix: the sparse mid-range in the beat leaves room for vocals. [link](https://www.soundonsound.com/techniques/inside-track-21-savage)

### Inferences
- A dark or filtered "other" stem is often intentional in hip hop. Brightening it to fix "dullness" may undo the aesthetic. A small 1 to 4 kHz dip on "other" (about -1 to -2 dB, Q ≤ 1.5) to clear room for the vocal fits the practice described; the depth is not sourced.
- Consistent with the project's existing rule: do not gate or expand "other" (project rule, not a source).

### Gaps
- No sourced numbers for a carving dip, low-mid cleanup or vinyl-sample treatment. Ringer and Reverb pieces on Bob Power and *The Low End Theory* came up in searches but were not fetched.

## 5. Mastering and loudness

### Takeaway
DR database logs show golden-age hip hop CDs near DR 11 to 12. Around 2010 to 2013, Kanye releases dropped to DR 4 to 5. Blog guides put modern competitive hip hop at roughly -10 to -7 LUFS integrated. Spotify normalises to -14 LUFS and asks for a true peak below -2 dBTP on masters louder than that. Named mastering engineers object to crunch and distortion, not to loudness itself.

### Cited Findings (DR database; higher DR means more dynamic)
- Nas, *Illmatic* (1994, 16/44.1 FLAC): album DR 11, tracks 9 to 13. [link](https://dr.loudness-war.info/album/view/53950); a second log agrees: [link](https://dr.loudness-war.info/album/view/9796). *Illmatic XX* (2014) at DR 7 is confirmed in [remasters.md](remasters.md).
- A Tribe Called Quest, *The Low End Theory* (1991; CD source, analysed as 256 kbps lossy): album DR 12, tracks 9 to 14. [link](https://dr.loudness-war.info/album/view/68793)
- Dr. Dre, *The Chronic*: 2017 European vinyl at DR 14 (vinyl, not comparable with CD). [link](https://dr.loudness-war.info/album/view/167449). The 1992 CD entries are in [remasters.md](remasters.md).
- Kanye West, *My Beautiful Dark Twisted Fantasy* (2010 CD, lossless): album DR 5, tracks 2 to 11. [link](https://dr.loudness-war.info/album/view/162078)
- Kanye West, *Yeezus* (2013; CD source, 256 kbps m4a): album DR 4, tracks 2 to 6. [link](https://dr.loudness-war.info/album/view/71700)
- Kendrick Lamar, *good kid, m.A.A.d city* (2012): album DR 11, tracks 10 to 12 (search summary, not fetched; vinyl source). [link](https://dr.loudness-war.info/album/view/91906)
- Travis Scott, *Birds in the Trap Sing McKnight* (2016; vinyl source, 320 kbps MP3 log): album DR 11. Vinyl caveat applies. [link](https://dr.loudness-war.info/album/view/156235)
- Not found: any Drake album, a CD or digital *Astroworld*.

### Cited Findings (engineers and docs)
- Derek Ali's stereo bus: an SSL bus compressor most of the time and a GML 8200 EQ for light tuning, skipped when the mix is already very loud. Mixes went to half-inch tape; Mike Bozzi mastered *TPAB* from the reels at Bernie Grundman. [link](https://www.soundonsound.com/techniques/inside-track-kendrick-lamars-pimp-butterfly)
- 40 used an L2 on the master bus for reference mixes only and removed it before mastering. He said he avoided loudness-war techniques on the album. [link](https://www.soundonsound.com/techniques/noah-40-shebib-recording-drakes-headlines)
- Brian "Big Bass" Gardner (mastering engineer): does not object to loud masters, only to distortion ("I just object to it crapping out"). Says pop and hip hop are the main culprits for over-compressed mixes and asks for pulled-back mixes; processing a crunched mix accentuates the crunch. No numbers. Mix Online, [link](https://www.mixonline.com/recording/brian-big-bass-gardner-qa-366242)
- Chris Gehringer (Sterling Sound): a search snippet, not fetched, has him saying he cut his teeth on hip hop and favours "big dynamic music". [link](https://top40-charts.com/news.php?nid=105981)
- Spotify (official docs): normalises to -14 LUFS (ITU 1770); Loud setting -11 LUFS with a limiter at -1 dB sample, 5 ms attack, 100 ms decay. Recommends ≤ -1 dBTP, and below -2 dBTP for masters louder than -14 LUFS. [link](https://support.spotify.com/us/artists/article/loudness-normalization/)
- Blog and vendor LUFS ranges, search summary, not mapped to individual URLs: competitive hip hop at -8 to -10 LUFS integrated, some guides -10 to -7 or -10 to -6, trap sometimes louder. Candidates: [Sage Audio](https://www.sageaudio.com/articles/what-is-loudness-for-mastering), [Violet Recording](https://violetrecording.com/how-to-master-hip-hop/), [RoEx](https://www.roexaudio.com/blog/what-lufs-should-i-master-at). Low authority.

### Inferences
- For golden-age CDs (DR 11 to 12), a gentle remaster to about -11 to -10 LUFS keeps the genre's punch. 2010s masters at DR 4 to 5 are already past what the tool should push; the useful move there is tonal, not louder. DR is not LUFS, and the mapping is not measured here.
- Masters above -14 LUFS get a -2 dBTP ceiling for lossy copies, consistent with Spotify's guidance and the project's MP3 rule.

### Gaps
- No named-engineer LUFS figures for hip hop. No sourced 808 clipping practice at mastering (Maddmix's limiting section is on page 2 of the SOS article, not retrieved).
- Not covered: Dave Kutch, Mike Bozzi, Young Guru, Manny Marroquin, Pensado, Ken Lewis.
