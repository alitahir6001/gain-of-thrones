# Demucs and source separation on hip hop

Source caveat: no published work found reports Demucs (or any 4-stem separator) scores broken out by genre, and no study tests 808s, sampled loops, scratches or rap ad-libs directly. The hard numbers come from four places: the MUSDB18 tracklist, the MoisesDB benchmark paper, the Demucs README, and the Jeon and Lee loud-music paper. Everything on 808s, samples and rap vocals is anecdotal: vendor pages, a GitHub thread, and the community UVR/MVSEP guide by deton24, which mostly discusses Roformer/MVSEP models, not htdemucs_ft. Not read beyond abstracts and snippets: the arXiv 2211.08553 body, Défossez 2021 (2111.03600), the MDX 2021/2023 papers.

## 1. Benchmarks and genre coverage

### Takeaway
MUSDB18 has 8 tracks tagged Rap and 8 tagged Electronic out of 150; most of the rest is pop/rock. The SDR figures quoted for htdemucs_ft (about 9.0 dB overall) are therefore dominated by rock and pop. Nothing published says how Demucs does on rap specifically.

### Cited Findings
- The MUSDB18 tracklist CSV has a Genre column. Counts: Pop/Rock 72, Rock 17, Singer/Songwriter 14, Heavy Metal 12, Pop 11, Rap 8, Electronic 8, Country 3, Jazz 3, Reggae 2. Rap: ANiMAL (Clinic A, Easy Tiger, Rockshow), Grants - PunchDrunk, Little Chicago's Finest - My Own, Lushlife - Toynbee Suite, M.E.R.C. Music - Knockout, Side Effects Project - Sing With Me. No train/test column. [tracklist.csv](https://raw.githubusercontent.com/sigsep/website/master/content/datasets/assets/tracklist.csv)
- MUSDB18 is 150 tracks split 100 train / 50 test; 100 from DSD100, 46 from MedleyDB. [MoisesDB paper, ISMIR 2023](https://archives.ismir.net/ismir2023/paper/000073.pdf); [sigsep MUSDB page](https://sigsep.github.io/datasets/musdb.html)
- MoisesDB has 240 tracks in 12 genres, mostly Rock, then Singer/Songwriter and Pop. Rap is the 4th-largest genre (roughly 15 to 20 tracks, read off the bar chart, not a number in the text). [MoisesDB](https://archives.ismir.net/ismir2023/paper/000073.pdf)
- HT-Demucs 4-stem SDR on MoisesDB, all genres pooled (N=235), mean ± std, with oracle IRM: vocals 10.05 ± 2.48 (10.72), bass 11.64 ± 3.35 (8.43), drums 10.94 ± 2.30 (8.98), other 7.00 ± 2.76 (7.74). HT-Demucs beats the oracle masks on bass and drums but not on other. No per-genre table; per-track results are in the paper's GitHub repo. [MoisesDB](https://archives.ismir.net/ismir2023/paper/000073.pdf)
- MoisesDB mixes are unmastered (no compression or EQ), quieter and more dynamic than commercial tracks. The authors still say HT-Demucs generalizes "reasonably well" to mastered recordings. Same source.
- Demucs README: 9.0 dB overall SDR on MUSDB HQ test for htdemucs_ft (v4), trained on MUSDB HQ plus 800 extra songs; about 4x slower than htdemucs. Nothing on genre. [Demucs README](https://cdn.jsdelivr.net/gh/facebookresearch/demucs@main/README.md)
- HT Demucs abstract: the model does poorly trained on MUSDB alone; the 800 extra songs give +0.45 dB over Hybrid Demucs. [arXiv 2211.08553](https://arxiv.org/abs/2211.08553)
- An ISMIR 2025 poster argues average SDR hides variance that depends on the test set's musical character (search result only). [ISMIR 2025 P7-13](https://ismir2025program.ismir.net/poster_221.html)
- Hip-hop-specific separation work exists but only snippets surfaced: an MIT data-scarce study with Hip-Hop among 8 genres (SI-SDR, numbers not extracted) [MIT PDF](https://web.mit.edu/paramuth/www/assets/data_scarce.pdf); an MTG paper on data augmentation for hip hop separation [MTG](https://mtg.upf.edu/node/3825).

### Inferences
- With 8 Rap tracks in MUSDB18 and the 800-song extra set undisclosed, how much rap htdemucs_ft saw in training is unknown.
- Pooled MoisesDB numbers rank bass and drums strongest and "other" weakest. Whether that holds on 808-driven rap is untested.

### Gaps
- No per-genre SDR for any Demucs model. MoisesDB's per-track results could be filtered to Rap for a real number (not done). MDX 2021/2023 papers not read for genre breakdowns; the SDX23 snippet says only that test songs came from 6 genres. [arXiv 2308.06979](https://arxiv.org/pdf/2308.06979)

## 2. 808s and sub bass

### Takeaway
No primary source says where a pitched 808 lands in htdemucs_ft. Vendor guides list 808s under "bass" and warn that 808 kicks and sub split unpredictably between bass and drums. Expect splits and check them by measurement.

### Cited Findings
- A vendor guide lists "sub-bass, 808s" under the bass category of 4-stem models. Vendor, unmeasured. [stemsplit guide, via search result](https://stemsplit.io/blog/ai-stem-splitter-guide)
- A drum-separation vendor says 808 kicks blend into sub-bass, so kick and sub can split unpredictably. Marketing claim, no numbers. [drumsplit hip hop guide](https://drumsplit.pages.dev/guides/drum-separation-for-hip-hop)
- Demucs GitHub issue #392 (anecdotal): a commenter, not a maintainer, says Demucs can only work with timbres it has seen, using 808 variations as the example. An EDM producer wants to split bass at about 100 Hz into sub and mid-bass. No measurements. [issue #392](https://github.com/facebookresearch/demucs/issues/392)
- UVR/MVSEP community guide (anecdotal, not about Demucs): RX 12 separates well except for very low subs; acapellas show a bass dip where the drums hit. [deton24 guide](https://docs.google.com/document/u/0/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c/mobilebasic)
- Ableton's stem separation manual warns some elements end up in stems you did not expect (search result). [Ableton manual](https://www.ableton.com/de/manual/stem-separation/)

### Inferences
- A long, pitched 808 tail is tonal and sustained, so it probably pulls toward "bass", while the click pulls toward "drums". Reasoning from the stem definitions, not a measurement.
- With the residual added back at unity, a split 808 matters only if bass and drums get different processing: then the 808's attack and tail move apart.
- A check: per track, measure each stem's energy below 60 Hz and its correlation with kick onsets.

### Gaps
- No issue, paper or measured comparison on 808 placement in Demucs. Nothing on handling below 40 Hz.

## 3. Sampled loops, vinyl noise, scratches

### Takeaway
Nearly nothing published. Anecdotes say sampled material leaks into the drum stem and that vocal chops are hard to place. Nothing Demucs-specific on vinyl crackle or scratches.

### Cited Findings
- A vendor page says boom-bap with heavy sampling sometimes leaves traces of the sample in the drum stems. Anecdotal/vendor. [drumsplit hip hop guide](https://drumsplit.pages.dev/guides/drum-separation-for-hip-hop)
- UVR/MVSEP guide (anecdotal, not Demucs): one processing option makes hip hop scratches and their vocal chops much quieter; an FX model can remove vinyl scratches; one model handles vocal chops well because chops were in its training set, implying standard models do not. [deton24 guide](https://docs.google.com/document/u/0/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c/mobilebasic)

### Inferences
- A soul sample with its own drums, bass and vocal probably gets split across all four stems by role. So a vocal-stem move also moves the sampled singer, and a drum-stem move also moves the sample's own drums.
- Scratches and crackle have no target stem, so they most likely land in "other" or the residual. Unverified.

### Gaps
- No measured study on samples, crackle or scratches with any 4-stem model.

## 4. Rap vocals

### Takeaway
No benchmark compares vocal separation on rap against singing. Community reports say backing vocals, doubles and ad-libs are where models disagree most.

### Cited Findings
- A search-result summary of an older Demucs README says Demucs is strong on drums and bass while KUIELAB-MDX-Net is better for vocals and other (2021-era wording; not in the fetched README). [Demucs README](https://cdn.jsdelivr.net/gh/facebookresearch/demucs@main/README.md)
- UVR/MVSEP guide (anecdotal, mostly Roformer and karaoke models): ad-libs stacked on the lead stay in the lead stem; karaoke models can catch doubles; "bleedless" models often make backing vocals too quiet; Roformer preferred over SCNet for trap because SCNet bleeds more. [deton24 guide](https://docs.google.com/document/u/0/d/17fjNvJzj8ZGSer7c7OFe_CNfUKbAxEh_OBv94ZdRG5c/mobilebasic)
- A blog says hip hop and trap are hard to separate because vocals and instruments overlap spectrally. No measurements. [Genre Is the Real Quality Filter](https://sites.google.com/view/gs-5110c1bc82d157a8)

### Inferences
- Autotuned hooks and vocal-like synth leads share timbre; expect some hook doubles and pads to swap between "vocals" and "other". Reverb and delay throws probably split between vocals and other or the residual, so a vocal-stem gain move may not move a throw by the same amount. Unverified.

### Gaps
- No rap-vs-singing vocal SDR, nothing on autotune or delay throws for any Demucs model.

## 5. Loud, limited masters (musdb-XL)

### Takeaway
Limiting hurts Demucs most on drums; bass and other barely move. Loudness-normalizing the input before separating recovered most of the drum loss in the paper's test.

### Cited Findings
- musdb-L and musdb-XL are the musdb-hq test set run through Ozone 9 Maximizer, with about 3 to 4 dB and 6 to 7 dB of gain reduction on loud parts, about 5 and 7 LUFS louder than musdb-hq. [Jeon and Lee 2022, arXiv 2208.14355](https://ar5iv.labs.arxiv.org/html/2208.14355)
- Median SDR hq to XL, Demucs v3-B (extra data): drums 11.73 to 9.22 (-2.51 dB, the largest drop), vocals 9.24 to 8.76, bass 11.65 to 11.56, other 7.83 to 7.52. Same source.
- The authors attribute the drum drop to drums having the largest momentary energy, so the limiter acts on them most. Stem-level SI-SDR between hq and XL: 19.97 dB drums, 25.12 dB bass. Same source.
- Loudness-normalizing the input at evaluation cut Demucs v3-B's drum drop from 2.5 dB to 0.4 dB; the authors read this as overfitting to level. Same source.
- Their de-limiter reconstructs musdb-HQ from musdb-XL at 24.0 dB SI-SDR (v2 figure). [arXiv 2308.01187](https://arxiv.org/abs/2308.01187)

### Inferences
- These results are for Demucs v3, not htdemucs_ft. If they carry over, a loud rap master most likely damages the drums stem, with more drum content in other or the residual.
- Feeding Demucs a level-reduced copy is a cheap test; whether it helps v4 is unmeasured.
- Clipped flat-tops cannot be divided back into stems; they likely end up in the residual, which this tool adds back at unity.

### Gaps
- No musdb-XL numbers for htdemucs or htdemucs_ft. No genre split. No study of hard clipping as distinct from limiting.
