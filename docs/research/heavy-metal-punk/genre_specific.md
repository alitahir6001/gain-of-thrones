# Genre-specific mixing/mastering practice: punk, hardcore, thrash, metal (heavy distorted guitars)

Context for the report writer: remaster of a 1980s punk/thrash-adjacent EP from its CD (already ~-10 to -12 LUFS), worked on Demucs stems (drums, bass, vocals, other=guitars). Client: original cloudy/muffled; liked crisper version; guitars still small/cloudy; vocals reverby ("singing in a barn") and slightly buried; cymbals drowned at high headphone volume.

Source caveat up front: the most numerically dense source found is Mark Mynett's two-part SOS guide (Dec 2009). Mynett is a metal producer/lecturer (University of Huddersfield). Nail The Mix's cheat sheet is staff-written (2025), not a named engineer. Mike Senior's SOS Mix Rescue (Apr 2007) is hard rock, not punk/metal. Several engineer interviews named in the brief (Boatright, Douches, Jack Control, Carl Saff) exist only as podcasts or paywalled pieces; I could not extract numeric statements from them. Kerrang's mastering-metal-and-hardcore feature and Reverb's "clarity in metal and punk mixes" article both returned HTTP 403.

## 1. Distorted guitar EQ: mud, fizz, bite, filters, size/width without masking vocals

### Takeaway
The sources agree on the usual moves: HPF roughly 65-120 Hz, broad cuts in 200-500 Hz (and resonances near 120-250 Hz), presence/bite 1-5 kHz with a deliberate dip where the vocal lives (~2.4-3.8 kHz), brightness 5-8 kHz, fizz notches 6-10 kHz, LPF ~10-12.4 kHz. The main tool for getting vocals out of the guitars is "mirrored" EQ: cut the guitars in the band where the vocal gets boosted.

### Cited Findings
- Mynett (SOS, Dec 2009): rhythm guitar HPF "anywhere between 65 and 105Hz" depending on tuning. Don't boost 65-80 Hz; boost slightly higher (~85-120 Hz) for tighter low end. — [Sound On Sound, Mixing Metal pt 2](https://www.soundonsound.com/techniques/mixing-metal)
- Mynett example guitar chain: HPF 85 Hz; boost 89 Hz; tight-Q cuts at 123 Hz and 186 Hz; wide-Q boost 1.82 kHz; wider-Q cut 2.39 kHz; brightness boost 6.86 kHz; LPF 12.4 kHz. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mynett: cut boomy resonances around 250 Hz and "pillowy" frequencies around 1.5-2.5 kHz; optionally add a slight wide-Q boost at 1-2.5 kHz. Brightness usually sits at 5-8 kHz. Rhythm guitars rarely need compression; if used, "a low ratio and slow attack." — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mynett mirrored EQ: boost the vocal around 3.79 kHz and cut the same region on the rhythm guitars. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- SOS's 2009 Mixing Metal audio-examples page: 225-350 Hz in guitars tends to mask the bass guitar. — [SOS audio examples](https://www.soundonsound.com/techniques/mixing-metal-audio-examples)
- Mike Senior (SOS Mix Rescue, Apr 2007, NY hard rock): rhythm guitars cut ~350 Hz and ~2.5 kHz (~2 dB at 2.5 kHz) to clear the vocal's presence region; lead guitar HPF ~250 Hz. — [SOS Mix Rescue: Generals & Majors](https://www.soundonsound.com/techniques/mix-rescue-generals-majors)
- Nail The Mix staff (June 27, 2025): rhythm guitar HPF 80-120 Hz (raise until thin, back off); broad cut 200-500 Hz; small deliberate boosts 2-5 kHz for presence/pick attack; narrow-Q notches 6-10 kHz for fizz; LPF ~10-12 kHz. No dB values given. — [Nail The Mix EQ cheat sheet](https://nailthemix.com/eq-cheat-sheet)
- Nail The Mix pocket idea: if guitars are cut at ~400 Hz, give the bass energy there. — [Nail The Mix](https://nailthemix.com/eq-cheat-sheet)
- Secondary guides: mud usually lives in ~200-500 Hz and builds up as tracks stack; LPF ~6-10 kHz to tame fizz, applied post-distortion. — [Mastering The Mix](https://www.masteringthemix.com/blogs/learn/how-to-mix-distorted-guitar); [Nail The Mix low-pass article](https://nailthemix.com/low-pass-filter)

### Inferences
- For the "small/cloudy" guitars on the "other" stem: the likely combination is a broad 2-4 dB cut in ~200-400 Hz (plus narrow resonance cuts near 120-250 Hz), a wide 1-2 dB lift around 1.5-2 kHz, and brightness at ~5-7 kHz. Then carve a 1.5-3 dB dip at ~2.5-3.8 kHz so the vocal can sit there. Starting values come from Mynett and Senior; the amounts are my estimate.
- Don't LPF the guitar stem hard (below ~10 kHz) on this material. Demucs "other" may hold cymbal bleed, and an aggressive LPF would make the client's cymbal complaint worse. Inference, not measured.
- Width: no source gave numbers for stereo width on finished double-tracked guitars. On a stem, mid/side EQ (a little extra side-channel presence/brightness, low end kept mono) is a common way to make guitars feel bigger without a level jump in the center where the vocal sits. This is general practice I could not source to a named engineer here.

### Gaps
- Kurt Ballou, Andy Sneap, Jens Bogren: no extractable numeric statements found. Ballou material exists only as paid course listings (Nail The Mix Converge session; CreativeLive "Dynamic EQ and Ambient Mic Treatments"). — [CreativeLive listing](https://site.creativelive.com/class/gear-gods-presents-studio-pass-kurt-ballou/lessons/dynamic-eq-and-ambient-mic-treatments)
- No source gave numeric stereo-width or M/S guidance for heavy guitars.

## 2. Cymbals vs guitar masking; harshness; high listening levels

### Takeaway
Cymbal brightness/air sits at ~8-12+ kHz and harshness at ~3-6 kHz. Distorted guitars are typically low-passed around 10-12.4 kHz, which leaves the 10 kHz+ band to the cymbals. Mixers keep cymbals audible by giving them the top octave (shelf boost 8-12 kHz) and dipping the guitars and cymbals where they collide in the 2-6 kHz harshness zone. Dynamic EQ or multiband handles crash-only harshness.

### Cited Findings
- Mynett: overheads/hats HPF "as high as 550Hz," ride ~400 Hz; slight brightness boost 10-12 kHz; harshness "often located in the 3-6kHz region"; prefers uncompressed overheads. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Nail The Mix staff: overheads HPF ~400-500 Hz; surgical cuts 500 Hz-1 kHz for clanky hats/chinas; gentle wide dip 2-5 kHz for harshness; smooth high shelf 12 kHz+ for sheen. — [Nail The Mix](https://nailthemix.com/eq-cheat-sheet)
- Mike Senior (SOS, 2007): shelf boost of a few dB above 8 kHz on both overheads; narrow dips at 14 kHz (5 dB front mic, 2.5 dB rear) for hi-hat harshness. — [SOS Mix Rescue](https://www.soundonsound.com/techniques/mix-rescue-generals-majors)
- Dynamic EQ is recommended for harshness that appears only on loud hits (crashes); multiband/de-esser-style processing over static carving for drums. Secondary sources found via search, not named engineers. — [Nail The Mix, At The Gates/Russ Russell soothe session](https://nailthemix.com/atg-drum-mix-russ-russell-eq-soothe); [Harmony Central, taming overbearing cymbals](https://www.harmonycentral.com/articles/taming-overbearing-cymbals)
- Angry Metal Guy's remaster critique cites cymbal/guitar balance as a mix-level problem remastering can't fully fix: Megadeth *Countdown to Extinction* original had "guitars too far back and cymbals too far forward." — [Angry Metal Fi, Mar 27, 2015](https://www.angrymetalguy.com/angry-metal-fi-re-mastering-remasters/)

### Inferences
- The client's "cymbals drowned at high headphone volume" fits two mechanisms: (a) guitar energy at ~2-6 kHz masks cymbal wash, and ear sensitivity peaks near 3-4 kHz, so this band gets more prominent as you turn up; (b) a limiter driven by a full-band guitar wall pumps the cymbal decay down. The equal-loudness point is general psychoacoustics (ISO 226), not sourced here; another researcher covers it. Likely fix on stems: lift drum-stem air with a high shelf of +1.5-3 dB from ~8-10 kHz, dynamic-cut guitar stem 2.5-5 kHz only when it peaks, and avoid LPF on guitars below ~11-12 kHz. Starting values are taken from the sources above; the combination is my inference.
- Don't add broad 3-5 kHz boosts to the guitars or the full mix to get "crisp." That band reads harsh at high levels. Get crispness from 6-12 kHz instead (Mynett's 6.86 kHz guitar brightness, 10-12 kHz cymbal air).

### Gaps
- No named-engineer statement found on the Fletcher-Munson effect on headphones specifically for heavy music.
- No mastering-engineer source found for multiband settings (crossovers, ratios) specific to cymbals vs guitars.

## 3. Vocal clarity in dense punk/metal mixes

### Takeaway
Vocal presence goes at ~3.3-4.5 kHz (with a matching guitar cut) and air at 10-12 kHz, with the HPF set high (~100-170 Hz). De-ess at 5-8 kHz before brightening. Compression is fast attack, medium release. No source in scope covered de-reverbing a vocal.

### Cited Findings
- Mynett: vocal HPF often ~160 Hz (content "very rarely" below 85 Hz); brightness ~4.5 kHz plus air 10-12 kHz; de-ess first; compression "very fast attack and medium release"; delay usually a simple eighth-note repeat; mirrored boost at 3.79 kHz with a guitar cut there. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mike Senior: lead vocal HPF ~170 Hz; presence boost a few dB at 3.3 kHz; multiband compression crossover at 750 Hz; ~1 dB high-shelf cut at 12 kHz; backing vocals HPF 150 Hz. — [SOS Mix Rescue](https://www.soundonsound.com/techniques/mix-rescue-generals-majors)
- Nail The Mix staff: HPF ~100-120 Hz; broad 2-5 kHz boost for intelligibility; de-esser/dynamic EQ 5-8 kHz; 12 kHz+ air for modern metalcore. — [Nail The Mix](https://nailthemix.com/eq-cheat-sheet)

### Inferences
- "Singing in a barn" on a Demucs vocal stem: the reverb tail and room are baked into the stem (and Demucs also bleeds some ambience into it). Likely approaches: a de-reverb tool on the vocal stem, gentle downward expansion/gating so the tail drops between phrases, and cutting low-mid "room" (~200-500 Hz) plus a higher HPF (~150-170 Hz). Mynett's and Senior's HPF values support the last one. The de-reverb tool choice belongs to whoever covers restoration/separation.
- Level: raise the vocal stem ~1-2 dB relative to guitars after the mirrored EQ, rather than boosting presence harder. Over-boosted 3-5 kHz becomes harsh at the client's high listening level (see section 2). This is an inference.

### Gaps
- No named punk/metal engineer statement found on de-reverbing vocals or on target vocal-to-guitar level ratios.

## 4. Drum punch in punk/thrash

### Takeaway
Kick weight is 60-110 Hz (don't boost below ~75 Hz), with a cut at 250-450 Hz and click at ~4 kHz or ~7-10 kHz for fast double-kick. Snare body is 150-250 Hz, box 175-500 Hz cut, crack 3-8 kHz, wires 10-12 kHz. Kick compression uses slow attack (>20 ms) to keep transients. Drum bus: 3:1, 10 ms attack, 100-200 ms release, ~4-5 dB GR.

### Cited Findings
- Mynett kick: HPF 60-80 Hz; weight 60-110 Hz, "avoid amplifying any frequencies lower than 75Hz"; cut 250-450 Hz; click ~4 kHz or ~8 kHz for fast double-kick. Example: HPF 65 Hz, medium-Q boost 82 Hz, cut 341 Hz, gentle boost 3.62 kHz, larger boost 7.22 kHz (or 9-10 kHz). Compression attack "relatively slow (above 20 milliseconds)," fast-medium release, high ratio. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mynett snare: HPF 110-170 Hz; body 200-450 Hz; boxiness cut 175-500 Hz; attack 4-8 kHz; wires 10-12 kHz; compression attack/release "within a few milliseconds"; short plate 500-800 ms decay, 7-11 ms pre-delay. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mynett master bus (if used): ratio no more than 2:1, 3-4 dB GR; keep ≥6 dB headroom on channels/buses. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mike Senior: kick compressor attack ~20 ms with a 7 dB boost at 1.6 kHz; drum bus 3:1, attack 10 ms, release 150 ms (100-200 ms usable), ~4-5 dB GR on peaks; snare notches 300-600 Hz. — [SOS Mix Rescue](https://www.soundonsound.com/techniques/mix-rescue-generals-majors)
- Nail The Mix staff: kick 50-80 Hz weight, 200-500 Hz wide cut, 2-5 kHz beater (optionally dynamic EQ so it boosts only on hits), 8 kHz+ air; snare 150-250 Hz body, 400-800 Hz ring cut, 3-6 kHz crack, 10 kHz+ wires. — [Nail The Mix](https://nailthemix.com/eq-cheat-sheet)
- Alan Douches (Tape Op #31, Sep 2002): values mixes that arrive with headroom, "sometimes as much as 5 to 7 dB," because "they're not killing their transients"; criticizes using 0 dBFS "as a limiter." — [Tape Op](https://tapeop.com/interviews/31/alan-douches)

### Inferences
- With a drum stem from a CD that is already hot (~-10 to -12 LUFS), the original transients are already clipped or limited. Use a transient shaper or upward expansion on the drum stem (attack +, sustain neutral) before re-limiting, and leave the final limiter more headroom than the source had. That restores perceived punch better than EQ. Inference; separation artifacts may limit how far this can go.
- Parallel compression: not covered numerically by any in-scope source (Mynett explicitly doesn't discuss it).

### Gaps
- No named punk/thrash engineer numbers for parallel drum compression or transient shaping.

## 5. Bass in punk/thrash

### Takeaway
Keep bass HPF around 60 Hz. Separate it from the kick by not cutting the same bands (kick weight 60-110 Hz, cut at 250-450 Hz). Growl/definition is at 2-3.5 kHz and grit in a 250-400 Hz to 2-5 kHz band. Corrective cuts go at 200-450 Hz with wide Q. Heavy compression (8:1-10:1) is normal for metal bass.

### Cited Findings
- Mynett: bass HPF usually 60 Hz; distortion channel band-limited by HPF ~250-400 Hz and LPF ~2-5 kHz; attack/definition boost 2-3.5 kHz; corrective EQ 200-450 Hz wide Q, avoiding heavy cuts in the same range as the kick; two compressors in series (fast-attack peak catcher, then slow-attack body control), ratios 8:1-10:1 may be needed. — [SOS](https://www.soundonsound.com/techniques/mixing-metal)
- Mike Senior: bass high-shelf cut 3 dB at 150 Hz; dip ~350 Hz shared with kick and guitars. — [SOS Mix Rescue](https://www.soundonsound.com/techniques/mix-rescue-generals-majors)
- Nail The Mix staff: split bass into sub (LPF ~150 Hz) and grit (HPF) tracks; give bass the pocket where guitars are cut (~400 Hz). — [Nail The Mix](https://nailthemix.com/eq-cheat-sheet)
- SOS: guitar 225-350 Hz masks bass. — [SOS audio examples](https://www.soundonsound.com/techniques/mixing-metal-audio-examples)

### Inferences
- On stems you can emulate the sub/grit split by duplicating the bass stem, LPF ~150 Hz on one copy and band-limiting the other to ~400 Hz-3 kHz. That helps the bass read on small speakers once the guitars' 200-400 Hz cut opens a pocket. Inference.

### Gaps
- No punk-specific bass-mix interviews found.

## 6. Loudness norms: classic 80s punk/thrash CDs vs remasters; engineers' views

### Takeaway
DR Database entries show 1980s original CDs of this genre were quite dynamic (Slayer *Reign in Blood* 1986 CD DR14; Black Flag *Slip It In* 1984 SST CD DR13; Metallica *Master of Puppets* original ~DR12). 1990s-2000s remasters typically lost 4+ DR points (Puppets 1995 DR8; Dead Kennedys *Fresh Fruit* 2005 DR7). Some later reissues came back up (Metallica 2016 vinyl DR11). The client's CD at ~-10 to -12 LUFS is already roughly in DR8-10 territory. That is a rough inference: DR and LUFS are different metrics.

### Cited Findings
- Slayer *Reign in Blood*, original Def Jam CD (9 24131-2, 1986): album DR14, tracks 13-15. — [DR Database](https://dr.loudness-war.info/album/view/114866) (URL from search results; the DR figure is from the search summary of DR database entries; verify the exact entry ID before citing)
- Black Flag *Slip It In* (1984, SST-CD-029): album DR13; *In My Head* (1990, SST): DR12. — [DR Database](https://dr.loudness-war.info/album/view/17829)
- Minor Threat *Out of Step* (Dischord, listed 2016 lossless download; comment says remastered at Silver Sonya 2003): DR9, tracks 8-10. The entry's dates are inconsistent. *20 Years of Dischord* compilation tracks are mostly DR8-10. — [DR Database search results](https://dr.loudness-war.info/album/view/88381)
- Dead Kennedys *Fresh Fruit for Rotting Vegetables* 25th Anniversary (2005; John Cuniberti, The Plant, with East Bay Ray): DR7 (tracks 6-7). Another entry (listed 2002, release unclear): DR8. The 2022 Chris Lord-Alge remix was made from the multitracks (Manifesto, Sep 30, 2022); Jello Biafra objected to Lord-Alge as remixer. — [DR Database](https://dr.loudness-war.info/album/view/206375); [DR Database alt](https://dr.loudness-war.info/album/view/175810); [Rolling Stone](https://www.rollingstone.com/music/music-news/dead-kennedys-fresh-fruit-for-rotting-vegetables-reissue-1378541/)
- Metallica *Master of Puppets*: 1995 George Marino remaster DR8, which the writer says cut "four points of DR" from the 1986 original (so ~DR12); Steve Hoffman's 1999 DCC version used the 1995 tapes. — [Angry Metal Fi, Mar 2015](https://www.angrymetalguy.com/angry-metal-fi-re-mastering-remasters/)
- Metallica 2016 *Kill 'Em All* and *Ride the Lightning* remasters (Howie Weinberg; Chris Bellman cut lacquers for KEA): 180g vinyl rips DR11 (tracks 10-12). An MP3-sourced RTL entry reads DR7, and a commenter says it is about as loud as the 1995 remaster "but more punch." Lossy/vinyl DR readings aren't comparable to CD. — [DR Database RTL](https://www.dr.loudness-war.info/album/view/107935); [DR Database KEA](https://dr.loudness-war.info/album/view/145730)
- Megadeth *Killing Is My Business* c.2002 remaster: DR6; Mustaine's 2004 remix/remasters vs older albums at DR10+. — [Angry Metal Fi](https://www.angrymetalguy.com/angry-metal-fi-re-mastering-remasters/)
- Alan Douches (Tape Op, Sep 2002): wants mix headroom (5-7 dB); "Every time you add a process, you risk degrading the signal"; works by "accumulating subtleties." — [Tape Op #31](https://tapeop.com/interviews/31/alan-douches)
- Douches has a URM podcast episode (May 2015/2016) on mastering for streaming normalization and the loudness war, but no transcript was available to quote. — [URM EP10](https://urm.academy/ep10-interview-master-feat-alan-douches)
- Brad Boatright (Audiosiege): podcasts (URM EP318, Master Your Mix EP198) cover vinyl, client feedback, and mastering as creative work; no loudness figures were extractable. — [URM EP318](https://urm.academy/urmpc318-brad-boatright/); [Master Your Mix EP198](https://masteryourmix.com/?p=9104)
- Jack Control (Enormous Door, Austin): specializes in metal/punk/hardcore. Reviews describe his remasters (Severed Head of State) as heavier and more forceful. No loudness numbers found. — [SoundBetter profile](https://www.soundbetter.com/profiles/669913-jack-control); [CVLT Nation](https://cvltnation.com/severed-head-state-remastered-lps-now-streaming/)
- Carl Saff: quoted saying the best mastered discs are ones where you're not thinking about the mastering; no punk-reissue loudness statements found. — [Central Track](https://www.centraltrack.com/?p=113092)

### Inferences
- The client's source CD at ~-10 to -12 LUFS is louder than the genre's 1980s CD originals (DR12-14) but similar to or quieter than the 2000s remasters (DR6-8). There is little reason to push integrated loudness higher. Aim for the same or ~1 dB louder at most, and spend the effort on tonal balance and transient restoration. Streaming normalization (-14 LUFS on Spotify/YouTube) would turn down anything louder anyway; that is general knowledge covered by other researchers.
- Fan reception (Angry Metal Guy, DR DB comments) consistently rewards reissues that restore dynamics and punishes "louder" remasters. That supports a conservative-loudness choice.

### Gaps
- No DR values found for Bad Brains (Org Music/Dave Gardner reissues), Black Flag *Damaged*, Misfits, Descendents, or the Slayer 2024 reissue.
- No direct loudness statements from Ted Jensen, Howie Weinberg, Maor Appelbaum, Jens Bogren, or Andy Sneap on punk/thrash reissues were found in this pass.
- Kerrang "inside the hidden art of mastering metal and hardcore" (quotes Douches) returned 403. — [Kerrang](https://kerrang.com/inside-the-hidden-art-of-mastering-metal-and-hardcore)

## 7. Remastering classic punk/hardcore/thrash catalog: what changed, reception

### Takeaway
Respected punk reissue engineers stress getting the source right and doing no harm before chasing improvements. Fan and critic reception of thrash remasters is mostly framed in DR terms: louder 1990s/2000s remasters are criticized, and Weinberg's 2016 Metallica remasters were received as more dynamic.

### Cited Findings
- Dave Gardner (Infrasonic; Bad Brains reissues on Org Music's Bad Brains Records, *The Pitch*, June 10, 2021): tapes restored and baked by Dan Johnson (Audio Archiving Services), then captured to a "super high resolution digital archive." Gardner masters from the archive, not the tapes. He compared band-supplied assets against original LPs, a bootleg 7", a first pressing of "Pay to Cum," and the ROIR cassette to choose correct versions. "Before you can even make it better, you have to really make sure you're not making it worse." Results described as better "crispness and clarity"; no loudness/EQ specifics given. — [The Pitch](https://www.thepitchkc.com/engineer-dave-gardner-on-making-bad-brains-sound-better-than-ever-before/); [Stereophile](https://stereophile.com/content/orgs-dave-gardner-rescues-bad-brains-album)
- Dischord: Minor Threat *Complete Discography* remastered 2003 (mastering engineer not confirmed). *First Demo Tape* (2003) was mixed by Ian MacKaye and Don Zientara at Inner Ear (Dec 2001) and mastered by Chad Clark at Silver Sonya. — [Dischord](https://dischord.com/release/40); [Punky Gibbon](https://punkygibbon.co.uk/bands/m/minorthreat_firstdemo.html)
- Metallica 1995 remasters (George Marino) seen as a loudness downgrade; 2016 Weinberg remasters measured more dynamic on vinyl. *...And Justice for All* is seen as unfixable by remastering alone (mix-level problem). — [Angry Metal Fi](https://www.angrymetalguy.com/angry-metal-fi-re-mastering-remasters/); [DR Database](https://www.dr.loudness-war.info/album/view/107935)
- Noel Summerville's Earache "FDR" (Full Dynamic Range) reissues were judged generally better than brickwalled originals, though "some retouches are questionable." — [Angry Metal Fi](https://www.angrymetalguy.com/angry-metal-fi-re-mastering-remasters/)
- Dead Kennedys 2022 full remix by Chris Lord-Alge was contested by Jello Biafra. A remix changes the record's identity more than a remaster does. — [Rolling Stone](https://www.rollingstone.com/music/music-news/dead-kennedys-fresh-fruit-for-rotting-vegetables-reissue-1378541/)

### Inferences
- Working from Demucs stems is effectively a light remix, not a pure remaster. The Biafra/Lord-Alge reaction and the Mustaine 2004 complaints (re-recorded parts, clipping) suggest keeping stem rebalancing modest (roughly ±1-3 dB per stem) so the result still sounds like the original record. Inference.
- Gardner's "don't make it worse" principle is relevant here because separation artifacts (phasey cymbals, smeared vocal tails) can become audible once stems are pushed. A/B every stem move against the original CD at matched loudness.

### Gaps
- No primary statements found from SST/Greg Ginn on Black Flag reissues, or from Dischord on how the 2003 Minor Threat remaster differs from earlier CDs.
- No fan-reception data (forum consensus) found for Bad Brains Org Music reissues.
