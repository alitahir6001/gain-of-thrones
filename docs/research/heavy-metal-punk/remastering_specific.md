# Remastering Existing Commercial Recordings (vs. mastering a new mix)

Context: the target is a 1980s punk/thrash EP. The only source is a CD rip (16/44.1 FLAC) that is already hot: about -10 to -12 LUFS integrated, LRA 1-3 LU, true peak +0.2 to +0.3 dBTP. Note on research coverage: 18 tool calls were used. Several pages (Loudersound/Revolver, MusicRadar/Ludwig) returned only site navigation and could not be read in full. Findings marked "per search summary" come from search-result summaries, not fetched full text.

## 1. Source selection and its limits

### Takeaway
Professionals insist on the earliest-generation, unprocessed source: the original master tape, or a flat transfer or safety copy with no EQ, compression or limiting. They treat an already-EQ'd production master as a compromised source. With only a mastered CD, you are working on a second-generation, already-processed signal. Limiting and clipping baked into it can be partly reconstructed, but never truly recovered.

### Cited Findings
- Bob Ludwig (MusicTAP interview): "there is no rule" that a remaster sounds better than the original. Results depend on who does the remaster and which tapes were available. He prefers original master tapes and says flat digital transfers sent by labels make the job harder. On one project the label had lost the masters, and he worked from an analog safety copy the artist kept. He warns that remasters should be checked to confirm they come from the original tape and not a second-generation copy. (Per search summary.) [Digital Bits / MusicTAP: Bob Ludwig](https://archive.thedigitalbits.com/articles/musictap/bobludwig.html)
- Steve Hoffman (2025 account) turned down a label's source, calling it an "EQ dub". He wanted the untouched mixdown, not a CD production master already shaped for consumer discs. When the original is digital, his team cuts from the original digital mixes. As an alternative he asks for a 1:1 flat analog safety copy (30 ips, 1/2-inch, no EQ, compression or limiting). — [Headphonesty, Aug 2025](https://www.headphonesty.com/2025/08/mastering-legend-refused-touch-classic-album/)
- Hoffman (Tape Op): tapes labeled "master" were often already EQ'd and compressed, so they were not true originals. — [Tape Op #85: Steve Hoffman](https://tapeop.com/interviews/85/steve-hoffman)
- Hoffman: keep the signal analog until the last possible moment, do mastering moves in real time, and transfer to digital "without tampering". — [Metro Times](https://www.metrotimes.com/music-2/the-mastering-master-2187013/); [Vintage Rock](https://vintagerock.com/?p=3154)
- Even a full remix from multitracks could not remove clipping printed into the source. On the 2013 Rush *Vapor Trails* remix (David Bottrill), a reviewer said the "brickwalling hatchet job" was "fixed somewhat", but some clipping remains and "can likely never be fixed". — [Popdose roundtable](https://popdose.com/popdose-roundtable-rush-vapor-trails-remixed/); see also [Progarchy](https://progarchy.com/2013/09/27/vapor-trails-remixed/)
- Geddy Lee on that remix: Bottrill's work "finally brought some justice and clarity" to the album. (Per search summary.) — [RushIsABand, Aug 2013](https://www.rushisaband.com/blog/2013/08/01/3738/Long-awaited-Vapor-Trails-remix-coming-October-1st-now-available-for-pre-order)
- Abbey Road's De-mix service is pitched for remastering when only the stereo mix exists. It allows "targeted EQ balancing", for example EQ on the bass guitar "without any impact on the vocals or drums". — [Abbey Road De-mix](https://www.abbeyroad.com/de-mix)

### Inferences
- For this EP, the CD is effectively an "EQ dub plus limiter" source in Hoffman's terms. Any remaster is a repair and rebalance of a finished master, not a re-master from tape.
- What CAN be done from the CD: tonal rebalance; partial peak reconstruction (de-clip, Unlimiter); level reduction to stop inter-sample overs; noise/hum cleanup; demix-based rebalancing. What CANNOT be done: recovering information destroyed by clipping or limiting, recovering the original tape's HF or low-level detail beyond 16-bit/44.1 kHz, or undoing analog-stage choices made at the original mastering.
- True peaks of +0.2 to +0.3 dBTP mean inter-sample overs, so the CD likely distorts slightly in some DACs. Simply lowering gain about 1 dB already removes that, at zero risk.
- The CD's master tape or a flat transfer is not available, and no first-pressing vinyl is mentioned. If an early vinyl pressing or the earliest CD issue exists, it may be a less-limited source. Many 1980s CDs were not loud, so a -10 LUFS figure suggests this rip may be from a later reissue. This is unverified and worth checking.

### Gaps
- Could not fetch Ludwig's MusicRadar interview (page returned only site navigation). Exact quotes on flat transfers are from search summaries.
- Did not find Kevin Gray, Bernie Grundman, Ted Jensen, Greg Calbi or Andy Pearce statements on source selection within the call budget.

## 2. Restoring vs. modernizing; engineer philosophies; criticism of loud remasters

### Takeaway
The respected-engineer consensus: preserve the original engineer's and producer's intent, keep processing minimal, and keep EQ flat where possible. The main criticisms of famous remasters and new releases are crushed dynamic range and audible clipping. Death Magnetic was measured at DR3 and Californication at DR5.

### Cited Findings
- Hoffman (Tape Op): he has done limited restoration "without altering the rest of the sound or changing the intent of the original engineer or producer". — [Tape Op #85](https://tapeop.com/interviews/85/steve-hoffman)
- Hoffman argues a flat (un-EQ'd) master lets listeners set their own EQ, while a master with built-in EQ may not sound right on high-end systems. — [Wikipedia: Remaster](https://en.wikipedia.org/wiki/Remaster)
- PS Audio sums up Hoffman's goal as making the artist sound true to life, with the vocal or lead instrument as the priority. — [PS Audio: Steve Hoffman](https://www.psaudio.com/article/steve-hoffman-mastering-legend-and-audio-restoration-magician/)
- Ludwig, asked whether the loudness war means the death of dynamics: "in many cases, yes". He has argued that streaming loudness normalization makes heavy limiting unnecessary. (Per search summary; dates range 1999 to about 2019.) — [Premier Guitar: Ludwig at SXSW](https://www.premierguitar.com/sxsw-metallica-and-the-loudness-wars); [Trichordist interview](https://thetrichordist.com/tag/bob-ludwig/)
- Giles Martin on Revolver (2022): "I'm not adding digitally enhanced frequencies". He framed the work as "just good mixing". (Per search summary.) — [AnalogPlanet / Stereophile-family interview](https://www.analogplanet.com/content/exclusive-producer-giles-martin-talks-about-mixing-and-de-mixing-beatles-revolver-vinyl)
- Death Magnetic (2008): Ian Shepherd compared the CD with the Guitar Hero III version. He found the game version had "a lot less clipping and more dynamic range", and said the CD was compressed about as much as possible, with audible digital clipping. — [Engadget, 17 Sep 2008](https://www.engadget.com/2008-09-17-engineer-metallica-mix-better-in-guitar-hero-than-on-cd.html); [Gizmodo](https://gizmodo.com/audio-engineer-claims-that-metallicas-latest-album-soun-5051435); [Rolling Stone](https://www.rollingstone.com/music/news/fans-complain-after-death-magnetic-sounds-better-on-guitar-hero-than-cd-20080918)
- DR rankings cited in Louder: Death Magnetic DR3, Californication DR5. Death Magnetic "lost significant amounts of sonic detail". (Per search summary.) — [Louder: Metallica win loudness war](https://loudersound.com/news/metallica-win-loudness-war-but-it-doesn-t-matter)
- Californication is widely called "Exhibit A" of the loudness war. A wiki source alleges heavy HF clipping (low-reliability source). — [20k podcast: Loudness Wars](https://www.20k.org/episodes/loudnesswars); [TV Tropes (low reliability)](https://tvtropes.org/pmwiki/pmwiki.php/LoudnessWar/TheWorstOffenders)
- A Death Magnetic BBC Radio 4 report covered the controversy. — [Blabbermouth](https://blabbermouth.net/news/metallica-death-magnetic-sound-quality-controversy-focus-of-bbc-radio-4-report)
- Fans petitioned for a Californication remix or remaster. I could not confirm an official remaster in these searches. — [search summary; no confirmed primary source]
- Barry Diament's early Atlantic CD masters (Led Zeppelin, Bob Marley) are described in forums as flat, with little or no compression. DR Database logs show a Diament-mastered *Rastaman Vibration* at about DR14-17. This is forum-level evidence. — [Pink Fish Media thread](https://pinkfishmedia.net/forum/threads/led-zeppelin-cd-pressings.257529/); [DR Database entry](https://dr.loudness-war.info/album/view/207452); [AudioStream Q&A via hifivision](https://www.hifivision.com/threads/good-read-q-a-with-barry-diament-of-soundkeeper-recordings.27077)

### Inferences
- For a personal remaster of punk/thrash, "restore" means making it less hot and less distorted while keeping the original balance and aggression. "Modernize" means a brighter, wider, louder result. The engineers above all lean toward restore.
- An EP at LRA 1-3 LU is within the range of criticized loud masters. Its DR is unmeasured here, but such material commonly reads about DR5-7. Running the TT DR offline meter on the rip would give a real number.

### Gaps
- No primary statements found within budget from Kevin Gray, Bernie Grundman, Ted Jensen (who mastered Death Magnetic and publicly distanced himself, but I did not fetch a source), Greg Calbi or Andy Pearce on restore vs. modernize.
- Did not find whether the Vapor Trails remix used original multitracks or the mastered files (it is generally understood to be a remix from multitracks, but unverified here).

## 3. Repairing a hot or clipped CD master: de-clip, de-limit, expansion

### Takeaway
De-clipping (iZotope RX De-clip) interpolates over flat-topped samples above a threshold, and needs headroom because restored peaks exceed 0 dBFS. iZotope states De-clip is "not intended for brickwall-limited audio". For limiting, the tool is ML-based de-limiting: Ozone 12 Unlimiter (Sept 2025), based on Jeon & Lee's 2023 "sample-wise gain inversion" research. Its results are plausible reconstructions, not recovered originals.

### Cited Findings
- RX De-clip "repairs digital and analog clipping by interpolating over peaks that exceed a set threshold, making the waveform rounder". Threshold should be set "just below" where the clipping occurs. The histogram shows clipping as samples bunched at the top and bottom edges. Quality modes are Low, Medium and High: Low is fast and often enough, High is slower and can be better. Makeup gain is applied after processing. The post-limiter is a true-peak limiter that keeps output at or below 0 dBFS. — [iZotope RX De-clip docs](https://help.izotope.com/docs/rx-plug-in-pack/De-clip.html)
- Docs warn that De-clip can push peaks back above 0 dBFS. Restored overs survive only in 32-bit float, and still clip at the DAC unless gain is lowered. — [iZotope RX De-clip docs](https://help.izotope.com/docs/rx-plug-in-pack/De-clip.html)
- RX 8 adds a threshold link toggle so positive and negative thresholds can be set separately (for asymmetric clipping). Suggest auto-detects the threshold. — [iZotope RX docs (RX 6/7/8 versions)](https://s3.amazonaws.com/izotopedownloads/docs/rx700/en/de-clip/index.html)
- iZotope's distortion-repair guide:
  - Workflow: Suggest threshold, preview at Low, compare modes, process, check true peak.
  - The author lowered gain by 10 dB after de-clipping (sounded fine but "noticeably quieter"), or used De-clip's limiter at -1. He found the limiter more aggressive.
  - For leftover burr, use Learn and run De-clip again, use Deconstruct for noise artifacts, or use Spectral Repair.
  - De-clip is "not intended for brickwall-limited audio", because limiting does not produce squared-off waveforms or clipping's noisy harmonics. The guide points to Ozone 12 Unlimiter for that case.
  - [iZotope: Repairing a distorted audio track](https://www.izotope.com/en/learn/repairing-a-distorted-audio-track)
- Ozone 12 Unlimiter (iZotope blog, 2 Sep 2025, Alexey Lukin and Johannes Imort):
  - An "undo button" for overly compressed audio, using ML sample-wise gain inversion inspired by Jeon & Lee.
  - The network predicts the inverse of the limiter's gain curve, finds where limiting occurred and how much expansion is plausible, and leaves unlimited sections untouched.
  - Controls: Threshold and Amount. Runs real-time on the CPU.
  - Intended for heavily processed material and "remastering older recordings".
  - Limitation: "severely brick-walled or distorted sources were not a focus", so edge cases exist.
  - [iZotope: Inside Ozone 12](https://www.izotope.com/en/learn/inside-ozone-12)
- Retail and tutorial descriptions mention a "Learn Threshold" button. A French tutorial notes results are a reconstruction, not the original mix. — [Elephorm tutorial](https://www.elephorm.com/formation/maitriser-ozone-12-les-fondamentaux/restaurer-la-dynamique-dun-morceau-compresse-avec-le-module-unlimiter); [Gearnews review](https://www.gearnews.com/izotope-ozone-12-studio/)
- Jeon & Lee, "Music De-limiter Networks via Sample-wise Gain Inversion" (IEEE WASPAA 2023):
  - The network estimates per-sample gains that reverse limiting, rather than generating the waveform.
  - Training set: musdb-XL-train, 300k segments made by limiting music with a commercial limiter plug-in.
  - Reported reconstruction SI-SDR is about 23.8-24.0 dB on musdb-HQ.
  - Code and weights are public (GitHub jeonchangbin49/De-limiter).
  - [arXiv 2308.01187](https://arxiv.org/abs/2308.01187)

### Inferences
- Order for this EP: (1) lower gain first, in 32-bit float, to create headroom (the source sits above 0 dBTP). (2) De-clip only where real flat-topping shows in the histogram. (3) Unlimiter or expansion gently for limiter damage. (4) Re-check true peak. These steps are not a sourced chain; they are built from the docs above.
- The training data is synthetic modern limiting, so how the Unlimiter performs on 1980s analog-era limiting, tape saturation or intentional guitar distortion is unknown. Distorted guitars may be mistaken for clipping, so audition the de-clip threshold with care on thrash material.
- Upward expansion or de-limiting raises peaks and LRA. Expect a quieter result at equal peak level, which is the point.

### Gaps
- No primary source found for Waves or other de-clippers (e.g. Waves X-Clip, Acon Digital DeClip, CEDAR declip) within budget.
- No independent, measured evaluation of Ozone 12 Unlimiter artifacts. Sources are iZotope or reviewers.
- Did not cover classic upward expansion or transient-designer settings with numbers.

## 4. Noise, hiss, hum, de-essing, HF restoration, avoiding over-processing

### Takeaway
The professional restoration chain is ordered: impulsive noise (clicks) first, then crackle, then broadband noise reduction from a noise profile. Respected remastering engineers apply it sparingly, and audiophile-favored masters often use none.

### Cited Findings
- CEDAR workflow as described in coverage: de-clicking first (clicks, pops, impulsive noise), then decrackling, then noise reduction. The noise reduction samples about 1/40 s of "noise minus signal" from a pause or lead-in. — [Audio magazine, Mar 1992, on CEDAR](https://gammaelectronics.xyz/audio_03-1992_cedar.html)
- Andy Pearce won a CEDAR award (2000) for a 1951 Crosby/Armstrong acetate, using the CEDAR Series 2 DC-1 De-Clicker and CR-1 De-Crackler. — [CEDAR 2000 awards](https://cedaraudio.com/news/2000awards)
- Abbey Road's Andy Walter says he uses CEDAR Retouch "all day every day" in normal mastering. — [Abbey Road: The CEDAR story](https://abbeyroad.com/news/the-cedar-story-with-andy-walter-and-simon-gibson-3361)
- CEDAR's own remastering applications page covers this use case. — [CEDAR: Remastering](https://cedaraudio.com/applications/remastering)
- Hoffman: limited restoration done without changing the rest of the sound or the original intent. — [Tape Op #85](https://tapeop.com/interviews/85/steve-hoffman)

### Inferences
- A digitally sourced 1980s CD should have no vinyl clicks. Tape hiss from a 1980s punk recording would sit under loud, dense music, and broadband NR would likely smear cymbals and guitar fizz before any hiss became a problem. Default to no NR, except a targeted hum notch if hum is measurable in gaps or fades.
- HF "restoration" from a 44.1 kHz CD cannot recover content above about 20 kHz. Brightening is EQ or excitation, not recovery. Martin's "not adding digitally enhanced frequencies" stance argues against exciters.

### Gaps
- No sourced numbers found for de-essing settings, hum notch depth, or NR reduction amounts in remastering.
- No Andy Pearce interview on his NR philosophy found.

## 5. Stereo width (M/S) and mono compatibility in remasters

### Takeaway
I found no primary engineer statements within the call budget on M/S width changes in remastering specifically. The closest is the Revolver team using demixing to re-pan for "a modern ear", which is a remix move, not mastering M/S.

### Cited Findings
- Sam Okell (Giles Martin's engineer, Revolver 2022): once they could separate sources "without any artifacts or real detriment to the sound of the record", they could focus on panning for a modern ear. (Per search summary; exact article not fetched.) — [MusicTech](https://musictech.com/news/gear/the-beatles-revolver-stereo-giles-martin-remixing)

### Inferences
- Widening a CD master with M/S raises side content, including side-channel distortion and noise. Mono fold-down should be checked after any width change. This is a general principle, not sourced here.

### Gaps
- No sourced numbers for typical M/S adjustments, side-channel EQ, or mono-compatibility thresholds (e.g. correlation-meter targets) in remastering.

## 6. Loudness targets of acclaimed vs. criticized remasters (DR, LUFS)

### Takeaway
DR values (TT Dynamic Range meter) are the community's yardstick. Heavily compressed releases read DR6 or lower (Death Magnetic DR3, Californication DR5). Very dynamic material reads DR14 or more. Diament-era flat masters log about DR14-17.

### Cited Findings
- DR method: 3-second windows. DR = peak minus the average of the loudest 20% of RMS windows. Whole-number scale DR4-DR14 in the TT meter. Use the offline meter for the official value. — [Stereophile: Dynamic Range Database](https://stereophile.com/content/dynamic-range-database); [TT DR manual (Scribd)](https://www.scribd.com/doc/210234192/DR-Manual-V1-1-English)
- "Very dynamic material will often read DR14 or more. Heavily compressed music will often read DR6 or lower." (Reviewer description.) — [Stereophile: Dynamic Range Database](https://stereophile.com/content/dynamic-range-database)
- Criticism: the DR method is flawed, a higher DR does not guarantee better sound, and a single outlier peak can inflate DR. — [Hydrogenaudio thread](https://hydrogenaudio.org/index.php/topic,105173.0.html)
- Death Magnetic DR3; Californication DR5. — [Louder](https://loudersound.com/news/metallica-win-loudness-war-but-it-doesn-t-matter)
- Diament *Rastaman Vibration*: about DR14-17. — [DR Database](https://dr.loudness-war.info/album/view/207452)
- Ludwig: typical CD peaks around +6 to +6.5 dB on VU meters (per search summary of SXSW talk). — [Premier Guitar](https://www.premierguitar.com/sxsw-metallica-and-the-loudness-wars)

### Inferences
- A reasonable personal-listening target for this EP is a few DR points above the current CD and true peak at or below -1 dBTP. That probably lands around -13 to -15 LUFS integrated, but this is an inference, not a sourced target. Under streaming or player normalization, quieter masters lose nothing.

### Gaps
- No sourced LUFS figures for specific acclaimed remasters. The DR database reports DR, not LUFS.
- No DR value found for the specific EP or comparable 1980s punk/thrash first-issue CDs.

## 7. Stem separation (demixing) in remastering; stated artifacts

### Takeaway
Demixing has moved from remixing (Peter Jackson's MAL, used for Revolver 2022, the Red/Blue 2023 reissues, and "Now and Then") into mastering tools: Abbey Road De-mix for targeted EQ, and Ozone 12 Stem EQ. Engineers say earlier tools were too artifact-laden. The current tools are pitched on stems that sum back to the original mix.

### Cited Findings
- Okell: earlier demixing tools were "so full of artifacts, you couldn't really take things apart". MAL could separate sources without audible artifacts. (Per search summary.) — [MusicTech](https://musictech.com/news/gear/the-beatles-revolver-stereo-giles-martin-remixing); [Guitar Player interview](https://guitarplayer.com/news/i-think-it-comes-from-their-fingers-and-the-guitars-listen-to-tracks-from-the-beatles-new-revolver-releases-and-read-giles-martins-unmissable-interview-on-re-mixing-and-de-mixing-the-landmark-album)
- Guitar Player reported the separation kept room ambience intact without ugly artifacts, including individual drum-kit pieces. — [Guitar Player](https://guitarplayer.com/news/i-think-it-comes-from-their-fingers-and-the-guitars-listen-to-tracks-from-the-beatles-new-revolver-releases-and-read-giles-martins-unmissable-interview-on-re-mixing-and-de-mixing-the-landmark-album)
- The MAL acronym is given inconsistently: "Machine Audio Learning" (Sound & Vision) vs. "machine assisted learning". It was originally built to separate mono Nagra recordings for *Get Back*. — [Sound & Vision](https://soundandvision.com/node/121874); [Wikipedia: Revolver Special Edition](https://en.wikipedia.org/wiki/Revolver:_Special_Edition)
- MAL was later used on the 2023 Red and Blue expanded editions. — [Wikipedia: Revolver Special Edition](https://en.wikipedia.org/wiki/Revolver:_Special_Edition)
- Abbey Road De-mix: started by software engineer James Clarke around 2009. For remastering it is used for targeted EQ balancing of one instrument without affecting others. — [Abbey Road De-mix](https://www.abbeyroad.com/de-mix)
- Ozone 12 Stem EQ (Sept 2025): real-time, phase-aware separation into vocals, drums, bass and other. It claims "fewer artifacts" and better transients than earlier versions. Stems "must sum back to the original mix". No specific artifacts are described. — [iZotope: Inside Ozone 12](https://www.izotope.com/en/learn/inside-ozone-12)
- Debate: The Guardian asked "Do we really need the Beatles to sound new?" (Nov 2022). — [Guardian via PressReader](https://www.pressreader.com/australia/the-guardian-australia/20221104/282346863759082)

### Inferences
- For this EP, small stem-based rebalances (e.g. a vocal or bass nudge of a dB or two) are lower-risk than large moves. Artifacts in separated stems are masked when everything is summed back near unity, and exposed when one stem is boosted or soloed heavily. This is inferred from the "sum back to original" design, not measured.
- Distorted, dense punk/thrash guitars and cymbal wash are a hard case for separators. Expect bleed between "other" and "drums".

### Gaps
- "Emil Berliner" is Emil Berliner Studios (Berlin), not a person. I found no source on its use of AI demixing.
- No primary Giles Martin quote on artifacts was found. The artifact statements come from Sam Okell.
- "Now and Then" (2023) demixing details were not fetched within budget.
