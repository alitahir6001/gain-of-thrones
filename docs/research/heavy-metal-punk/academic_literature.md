# Academic Literature: Mastering/Remastering and Stem-Separation Remixing

Scope note: most AES papers are paywalled, so many findings below come from abstracts or reliable index pages, not full texts. Where a number came from an abstract, it is reported as written there. Hobbyist or forum claims are labelled as such.

## 1. Loudness perception, A/B bias, and validity of BS.1770 / R128

### Takeaway
Level-matched comparison is mandatory. Unmatched loudness dominates DRC cues in preference tests (a 10 dB difference strongly drove preference in one AES study). The common "match within 0.1 dB" rule comes from audio-review practice, though, not from a controlled study I could find. BS.1770 is validated for broadcast programme loudness, but it has known low-frequency weighting weaknesses and errors of several LU on individual tracks or stems.

### Cited Findings
- An AES paper on the "louder is better" hypothesis reported that a 10 dB level difference "had a significant influence of listener preferences as opposed to the arguably weak perceptual cues of DRC" (authors not identified in the index snippet; surfaced in the AES E-Library search) — [AES E-Library search result](https://www.aes.org/e-lib/browse.cfm?elib=17169)
- Stereophile's level-matching guidance (trade press, not peer-reviewed): match to within 0.1 dB, because a component 0.2 dB louder "won't be heard as being louder"; listeners instead report "greater apparent detail or better dynamics" — [Stereophile, Sidebar 1: Level Matching](https://stereophile.com/content/mark-levinson-no38s-preamplifier-level-matching)
- Forum threads asking for peer-reviewed proof of a 0.1-0.2 dB preference bias found no published references (blog/forum, unverified) — [WhatsBestForum thread](https://whatsbestforum.com/threads/in-double-blind-testing-is-louder-perceived-as-better.2640)
- "Influence of level setting on loudspeaker preference ratings" (HAL, Univ. Brest) identifies level/loudness matching as a main difference between lab and informal tests. Differences in procedure led to different subjective assessments (abstract only) — [HAL](https://hal.univ-brest.fr/hal-00612877)
- Multitrack loudness-balancing test (Huddersfield, "Alternative weighting filters for multi-track program loudness measurement"): listeners' by-ear balances deviated from BS.1770-equal loudness by more than 4 LU (vocal-referenced) and more than 8 LU (kick-referenced). Balancing every track to equal BS.1770 loudness would leave the vocal perceived about 2 LU above the kick — [Univ. Huddersfield Pure](https://pure.hud.ac.uk/en/publications/alternative-weighting-filters-for-multi-track-program-loudness-me/)
- BS.1770's K-weighting shows marked differences from listener results in the bottom two octaves (trade-press summary) — [TV Technology, Comparing loudness meters part 2](https://tvtechnology.com/opinions/the-forum-comparing-loudness-meters-part-2)
- A forum reading of Skovenborg and Nielsen's loudness-model evaluation puts the maximum subjective-vs-objective error at about 4 dB (forum interpretation, not verified against the paper) — [Hydrogenaudio](https://hydrogenaudio.org/index.php?msg=458357)
- Wendl and Lee (AES 136, 2014) found that perceived loudness changed significantly as crest factor was reduced from 15 to 9 dB in 1 dB steps, even with the limiting applied. This implies crest factor affects loudness beyond what simple metering captures — [Huddersfield Pure](https://pure.hud.ac.uk/en/publications/the-effect-of-dynamic-range-compression-on-loudness-and-quality-p/)

### Inferences
- For our A/B against the original CD, integrated-LUFS matching is necessary but may not be enough. Bass-heavy or more limited versions can sound louder at equal LUFS, given the BS.1770 low-frequency weaknesses and the crest-factor effect on loudness. A short by-ear trim, or a check on short-term loudness at choruses, is reasonable.
- Residual mismatches of about 0.5-1 LU are within BS.1770's per-track error band, so a "better" verdict at that margin is weak evidence.

### Gaps
- I found no peer-reviewed paper quantifying preference bias for 0.1-1 dB level offsets in music A/B tests. The 0.1 dB rule is trade-press convention.
- Skovenborg/Nielsen BS.1770 validation statistics were not retrieved from the original.

## 2. Dynamic range compression and listener preference

### Takeaway
Under loudness-matched conditions, the peer-reviewed evidence that heavy compression is disliked is weak and mixed. Untrained listeners cannot reliably detect up to 12 dB of limiting, mastering engineers only partly can, and audibility depends on the track's resulting crest factor. Effects depend on genre and listener, and listening fatigue remains untested in the main studies.

### Cited Findings
- Vickers, "The Loudness War: Background, Speculation and Recommendations," AES 129th Convention, 2010, paper 8175. The paper reviews history, listening fatigue, and game theory, and questions whether loudness correlates with preference or sales — [AES 129 paper page](https://www.aes.org/events/129/papers/?ID=2382); [author PDF/page](https://www.sfxmachine.com/docs/loudnesswar/)
- Hjortkjær and Walther-Hansen, "Perceptual Effects of Dynamic Range Compression in Popular Music Recordings," JAES 62(1/2):37-41, 2014. Comparing originals with more compressed commercial remasters, they found no evidence of an effect on preference or perceived depth. Response consistency across repeats was low, so listeners are "less sensitive to even high levels of dynamic range compression than often argued." Critique: the remasters also changed EQ and stereo image, and fatigue was not tested — [AAU VBN](https://vbn.aau.dk/da/publications/perceptual-effects-of-dynamic-range-compression-in-popular-music-); [AES forum discussion](https://secure.aes.org/forum/pubs/journal/?ID=350)
- Ronan, Ward and Sazdov, "The Perception of Hyper-Compression by Untrained Listeners," AES 60th Conference, 2016. ABX test with 49 participants: untrained listeners "cannot discriminate up to 12dB of compression limiting above chance" — [AES E-Library 18076](https://www.aes.org/e-lib/browse.cfm?elib=18076)
- Ronan, Ward, Sazdov and Lee, "The Perception of Hyper-Compression by Mastering Engineers," JAES 65(7/8):613-621, 2017. ABX test with 20 mastering engineers, averaging 17/24 correct. Audibility "depends on the crest factor of the music rather than the amount of CF reduction," which suggests a threshold of audibility — [AES E-Library 19176](https://www.aes.org/e-lib/browse.cfm?elib=19176); [UTS OPUS](https://opus.lib.uts.edu.au/handle/10453/126118)
- Ronan et al. 2015 (AES), MUSHRA-style test with 35 participants: programme material significantly affected ratings of dimension and distraction — [UL Pure](https://pure.ul.ie/en/publications/identifying-and-validating-program-material-a-hyper-compression-p/)
- Wendl and Lee, "The Effect of Dynamic Range Compression on Loudness and Quality Perception in Relation to Crest Factor," AES 136, 2014. Crest factor ran 15 to 9 dB across rock, electronic and jazz. Both loudness and quality differed significantly across crest factors, and loudness and quality correlated for rock and jazz but not electronic — [Huddersfield Pure](https://pure.hud.ac.uk/en/publications/the-effect-of-dynamic-range-compression-on-loudness-and-quality-p/); [AES 136 listing](https://www.aes.org/events/136/papers/?ID=3894)
- A Goldsmiths SysMus14 paper ("The Loudness War & Hypercompression: Quantifying the perception of compression effects," MUSHRA-style) found that more compression significantly reduced overall quality ratings — [SysMus14](https://journals.gold.ac.uk/index.php/sysmus14/article/view/236)
- Deruty and Tardieu, "About Dynamic Processing in Mainstream Music," JAES 62(1/2):42-55, 2014. Per an abstract summary: production fidelity rose 1967-1984, then 1984-2004 moved toward transient degradation. Macrodynamics (loud vs quiet passages) were largely preserved, so the loudness war mainly affected micro-dynamics and transients — [AES E-Library 17085](https://aes2.org/publications/elibrary-page/?id=17085) (summary via secondary listing)
- Deruty and Pachet, "The MIR Perspective on the Evolution of Dynamics in Mainstream Music," ISMIR 2015 — [ISMIR 2015 PDF](https://www.ismir2015.uma.es/articles/136_Paper.pdf)
- Croghan, Arehart and Kates, "Music Preferences With Hearing Aids," Ear and Hearing, 2014. Hearing-aid WDRC mattered more than music-industry compression limiting, and for rock, linear processing was preferred over slow WDRC. Individual variation was large (funded by GN ReSound) — [PMC4271761](https://pmc.ncbi.nlm.nih.gov/articles/PMC4271761); [CU Boulder release](https://www.colorado.edu/today/2014/10/27/when-hearing-aid-users-listen-music-less-more-says-cu-boulder-study)
- Kirchberger and Russo, "Dynamic Range Across Music Genres and the Perception of Dynamic Compression in Hearing-Impaired Listeners," Trends in Hearing, 2016. Linear processing got the highest ratings for dynamics and quality — [PMC4753356](https://pmc.ncbi.nlm.nih.gov/articles/PMC4753356/table/table1-2331216516630549)

### Inferences
- For dense, distorted thrash/punk (already low crest factor), the Ronan 2017 threshold finding implies that extra limiting artefacts are least detectable when the source is already dense. The original CD's crest factor is therefore the relevant baseline. Matching it, rather than squeezing further, avoids audible gains in hypercompression artefacts while giving up little perceived loudness.
- Because the macro- vs micro-dynamics distinction (Deruty and Tardieu) separates transient damage from section-level dynamics, bus compression and limiting should be judged on transient/snare integrity, not only on PLR/LRA.

### Gaps
- Taylor and Martens (AES 136, 2014, loudness-matched forced choice of 7 compression levels across 5 genres; age and genre exposure influenced preference) surfaced only in a search summary. The exact AES URL and numbers were not verified.
- No peer-reviewed study found that measures listening fatigue from hypercompression.
- No study specific to punk/thrash or distorted-guitar material was found.

## 3. Automatic / intelligent mastering and spectral-balance targets

### Takeaway
Intelligent-mixing and mastering research shows that rule-based or learned DRC can match semi-pro or pro results in listening tests. Commercial recordings converge on a consistent long-term average spectral tilt (Pestana et al. 2013), which supports matching-EQ approaches toward a genre or era reference spectrum.

### Cited Findings
- Pestana, Ma, Reiss, Barbosa and Black, "Spectral Characteristics of Popular Commercial Recordings 1950-2010," AES 135th Convention, 2013, paper 8960. They analysed long-term average spectra across a large commercial dataset by year and genre, and found "a consistent leaning towards a target equalization curve that stems from practices in the music industry but also to some extent mimics natural, acoustic spectra of ensembles" — [AES E-Library 17010](https://www.aes.org/e-lib/browse.cfm?elib=17010); [author PDF](https://joshreiss.github.io/documents/2013/Pestana%20Ma%20Reiss%20-%20AES135.pdf)
- Ma, De Man, Pestana, Black and Reiss, "Intelligent Multitrack Dynamic Range Compression," JAES 63(6):412-426, 2015. Compressor parameters (threshold, ratio, knee, attack, release) are set from side-chain features, using two new features (percussiveness, low-frequency strength) and regression fitted to human adjustment data. The system competes with or outperforms semi-professional mixes on amount of compression, imperfection, level stabilisation and overall preference. The authors call for larger evaluations — [AES E-Library 17821](https://www.aes.org/e-lib/browse.cfm?elib=17821); [author PDF](https://joshreiss.github.io/documents/2015/Ma%202015%20-%20Intelligent%20Multitrack%20Compression.pdf)
- Mimilakis, Drossos, Virtanen and Schuller, "Deep Neural Networks for Dynamic Range Compression in Mastering Applications," AES 140th Convention, 2016, paper 9539. A DNN predicts frequency-dependent DRC coefficients for unmastered audio. Listening tests with producers and mastering engineers showed "on average an equivalent performance compared to professionally mastered audio," with improvements over some commercial software — [AES E-Library 18237](https://www.aes.org/e-lib/browse.cfm?elib=18237)
- Hafezi and Reiss, "Autonomous Multitrack Equalization Based on Masking Reduction," JAES 63(5):312-323, 2015 (see section 4) — [AES E-Library 17637](https://www.aes.org/e-lib/browse.cfm?elib=17637)

### Inferences
- Matchering- or LANDR-style reference matching (spectrum plus loudness matched to a reference) is consistent with the Pestana finding that commercial masters share a target tilt. I found no peer-reviewed evaluation of Matchering or LANDR specifically.

### Gaps
- Exact slope values from Pestana et al. (for example dB/octave by decade, or 1980s rock vs later) were not extracted from the PDF.
- I found no peer-reviewed listening evaluation of LANDR, Matchering, or iZotope Ozone's assistant.
- De Man and Reiss mixing-practice studies (for example "Analysis of peer reviews in music production," JAES) were not retrieved this round.

## 4. Masking and spectral balance in dense mixes

### Takeaway
Automatic masking-reduction EQ lowers both perceived and objective masking and approaches professional mixes. The objective masking metrics, however, are weak proxies for perceived masking, so per-stem EQ decisions should be checked by ear.

### Cited Findings
- Hafezi and Reiss 2015 (JAES 63(5)) built a simplified masking measure from best practice and four EQ systems (offline fully and semi-autonomous, two real-time). Autonomous systems "reduce both the perceived and objective masking." The semi-autonomous version, with one user parameter, beat an amateur mix and came close to a professional mix. The paper argues objective masking metrics poorly predict perceived masking in multitrack audio — [AES E-Library 17637](https://www.aes.org/e-lib/browse.cfm?elib=17637); [Sonic Field library summary](https://labs.sonicfield.org/library/autonomous-multitrack-equalization-based-on-masking-reduction-Hafezi-2015)
- Later work extends masking-based mixing (arXiv 1803.09960, multitrack masking minimisation; listed in the same search) — [arXiv 1803.09960](https://arxiv.org/abs/1803.09960v3)
- The BS.1770 multitrack balancing result (vocal perceived about 2 LU above kick at equal LUFS) suggests that loudness models of individual stems mispredict perceived balance — [Huddersfield Pure](https://pure.hud.ac.uk/en/publications/alternative-weighting-filters-for-multi-track-program-loudness-me/)

### Inferences
- In a separated-stem remaster, guitars in "other" and the vocal compete in roughly 1-4 kHz. Cutting "other" in the vocal's presence band (a masking-reduction EQ) is a direct application of Hafezi and Reiss. Separation bleed means the vocal also partly lives in "other," however, so the cut also thins any vocal content left in that stem.

### Gaps
- No peer-reviewed "ideal spectral tilt" number was retrieved beyond Pestana's qualitative finding.
- Vocal-intelligibility-in-music studies (for example Fenton / Hermes on vocal level in mixes) were not retrieved.

## 5. Music source separation quality: HT Demucs, artifacts, remixing and residuals

### Takeaway
htdemucs_ft is about 9.0 dB mean SDR on MUSDB18-HQ, with "other" the weakest stem (about 6.3 dB) and bass and drums the strongest (about 10 dB). Listening tests of the earlier Hybrid Demucs rated quality around 2.8/5 and bleed-absence around 3.0/5. Standalone stems are therefore clearly imperfect, and remixing literature reports that level changes of up to about 6 dB cause small but audible degradation. Limiting and mastering in the input is a recognised domain gap.

### Cited Findings
- Rouard, Massa and Défossez, "Hybrid Transformers for Music Source Separation," ICASSP 2023 (arXiv 2211.08553). MUSDB18-HQ test SDR (dB), All / Drums / Bass / Other / Vocals:
  - HT Demucs fine-tuned (= htdemucs_ft), 800 extra songs: 9.00 / 10.08 / 10.39 / 6.32 / 9.20
  - HT Demucs, 800 extra songs: 8.80 / 10.05 / 9.78 / 6.42 / 8.93
  - Sparse HT Demucs fine-tuned (not released): 9.20 / 10.83 / 10.47 / 6.41 / 9.37
  - Hybrid Demucs, 800 extra songs: 8.34 / 9.31 / 9.13 / 6.18 / 8.75
  - HT Demucs trained on MUSDB only: 7.52 (performs poorly without extra data)
  - Band-Split RNN with 1750 extra mixes: 8.97 / 10.15 / 8.16 / 7.08 / 10.47
  - IRM oracle: 8.22
  - The 800 extra songs are internal, auto-labelled from producer stem names ("noisy"). The paper reports SDR only, with no perceptual tests — [arXiv 2211.08553](https://arxiv.org/abs/2211.08553); [ar5iv full text](https://ar5iv.labs.arxiv.org/html/2211.08553)
- Demucs README: htdemucs scores 9.00 dB SDR on MUSDB HQ; htdemucs_ft is about 4x slower "but might be a bit better." The 6-source model's piano has "a lot of bleeding and artifacts." Max segment is 7.8 s. `--shifts` averages predictions on randomly shifted inputs (N times slower), and `--overlap` defaults to 0.25. The repo is archived — [GitHub facebookresearch/demucs](https://github.com/facebookresearch/demucs)
- Défossez, "Hybrid Spectrogram and Waveform Source Separation," MDX Workshop 2021 (arXiv 2111.03600). Human MOS (musicians and sound engineers, 1-5 scale, 25 twelve-second clips each): Hybrid Demucs overall quality 2.83 vs 2.36 for waveform Demucs, and absence of contamination 3.04 vs 2.37 (Demucs) and 2.44 (second-ranked MDX entry). There was a small quality regression on bass, and KUIELab was best on vocals — [arXiv 2111.03600](https://arxiv.org/abs/2111.03600v3)
- Mitsufuji et al., "Music Demixing Challenge 2021," Frontiers in Signal Processing, 2022. Hidden test set MDXDB21: 27 scored songs, professionally produced by Sony Music Japan, loudness and tone not normalised. Leaderboard A winner Hybrid Demucs: vocals 7.97, drums 8.04, bass 8.12, other 5.19, mean 7.33. Leaderboard B winner Audioshake: 9.79 / 8.66 / 8.34 / 6.51, mean 8.33. "Other" is lowest for every top system. Electronic-heavy songs scored "considerably worse." The authors report a generalisation gap relative to MUSDB18 and flag bleeding in ground truth (one song dropped for drum/bass bleed) as an open problem — [Frontiers](https://www.frontiersin.org/articles/10.3389/frsip.2021.808395)
- SDX'23 (Fabbro et al., TISMIR) reports the best system improved by more than 1.6 dB SDR over the MDX'21 winner. Its tracks addressed label noise and bleeding (snippet only; full text not retrieved) — [TISMIR 10.5334/tismir.171](https://refworks.reference-global.com/article/10.5334/tismir.171)
- Ward, Wierstorf, Mason, Grais and Plumbley, "BSS Eval or PEASS? Predicting the Perception of Singing-Voice Separation," ICASSP 2018. BSS Eval SIR and PEASS IPS correlate comparably with perceived interference, and PEASS APS correlates best with perceived artifacts. The metrics remain "far from perfect" (large RMSE). So SDR differences of a few tenths of a dB do not reliably predict audible differences — [Surrey/CVSSP](https://cvssp.github.io/maruss-website/publications/Ward_2018.html); [PDF](https://hagenw.github.io/pubs/ward_et_al-2018-predicting_the_perception_of_singing_voice_separation.pdf)
- Wierstorf et al., "Perceptual Evaluation of Source Separation for Remixing Music," AES 143rd Convention, 2017. Five separation algorithms were used to raise vocal level in six songs. Some algorithms raised vocals by up to 6 dB "at the cost of introducing a small but perceptible degradation in sound quality" — [AES E-Library 19277](https://aes2.org/publications/elibrary-page/?id=19277)
- Yang et al., "Don't Separate, Learn to Remix: End-to-End Neural Remixing with Joint Optimization" (arXiv 2107.13634, Sony). A cascaded separate-then-remix pipeline suffers audible artifacts. Joint optimisation reduces them, especially when the remix is close to the original balance — [arXiv 2107.13634](https://arxiv.org/abs/2107.13634)
- A 2025 arXiv paper proposes remix-consistency metrics (Re-SDR, Re-SISDR): well-separated stems should sum back to the mixture with minimal distortion. Mixture consistency is treated as a desirable property, not a guarantee — [arXiv 2504.17782](https://arxiv.org/pdf/2504.17782)
- Jeon et al., "Music De-limiter Networks via Sample-wise Gain Inversion," WASPAA 2023 (arXiv 2308.01187). They introduce musdb-XL, made by passing MUSDB through a commercial limiter, which documents limiting as a distinct degradation. The de-limiter recovers the unlimited mix at about 23.8-24.0 dB SI-SDR (figure differs between arXiv versions). Gain-domain inversion is chosen to avoid audible artifacts — [arXiv 2308.01187](https://arxiv.org/html/2308.01187v2)

### Inferences
- Our measured stem-sum residual of -20 to -22 dB versus the original means the four stems reconstruct the mix to roughly 20+ dB SNR. The residual is not negligible: it plausibly holds transient and cymbal/high-frequency content and distortion products the model did not assign. A residual stem (original minus sum of stems), added back at unity or processed with the bus, guarantees null reconstruction when no per-stem processing is applied. This is standard practice in remix-from-separation workflows, but I found no peer-reviewed paper that evaluates "add residual back" perceptually.
- Separation artifacts are partly masked when stems are re-summed near their original balance, and they unmask as per-stem processing diverges from unity. The Wierstorf 2017 result (up to 6 dB vocal boost gives small but perceptible degradation) and Yang et al. support keeping per-stem gain and EQ moves modest (a few dB), not radical rebalancing. This is inferred from those results, not directly measured for mastered punk.
- The source is a mastered, limited, distorted 1980s CD. That is out-of-domain relative to MUSDB (mostly unmastered-style mixes), and musdb-XL work treats limiting as a separate distortion. Expect lower-than-benchmark separation, especially for "other" (distorted guitars, which carry vocal and cymbal bleed), and drum/bass bleed on palm-muted low guitars.
- Gating separated stems gates the bleed and the model's errors together. On "other" in particular, gating can expose "musical noise" and pumping where bleed is removed intermittently.

### Gaps
- No peer-reviewed study found that measures separation quality specifically on hard-limited, distorted punk or metal masters.
- No paper found that perceptually evaluates the "process stems then add back residual" technique.
- Artifact taxonomy (cymbal smearing, phasiness, transient loss) for HT Demucs specifically is not documented in the paper. These are widely reported anecdotally but are unverified here.
- SDX'23 per-track numbers were not retrieved (the TISMIR page returned an error).

## 6. Headphone listening: target curves and preference

### Takeaway
Harman's research (Olive, Welti, Khonsaripour) shows that listener preference for headphones is predicted well (r = 0.91 for in-ears) by deviation from the Harman target curve. Masters checked only on headphones are therefore checked through a transducer whose own deviation from the target shifts perceived tonal balance.

### Cited Findings
- Olive, Welti and Khonsaripour, "A Statistical Model That Predicts Listeners' Preference Ratings of In-Ear Headphones: Part 1," AES 143, 2017, paper 9840. Thirty in-ear models were rated by 71 trained and untrained listeners, and models deviating more from the target were less preferred. Best Peer-Reviewed Paper award — [AES E-Library 19237](https://aes2.org/publications/elibrary-page/?id=19237); [AES 143 session](https://www.aes.org/events/143/papers/?ID=5547)
- Part 2 (paper 9878): a linear regression on the size, standard deviation and slope of deviation from the Harman in-ear target predicts preference with r = 0.91 — [AES 143 P14](https://www.aes.org/events/143/papers/?ID=5578)
- Extension to around-ear and on-ear headphones (AES 144, 2018, paper 9919), and comparison with five review organisations (paper 10048) — [AES E-Library 19436](https://aes2.org/publications/elibrary-page/?id=19436); [AES E-Library 19774](https://aes2.org/publications/elibrary-page/?id=19774)
- A 2019 JASA overview, "The perception and measurement of headphone sound quality," describes a target curve preferred by most listeners — [Sonic Field library](https://labs.sonicfield.org/library/the-perception-and-measurement-of-headphone-sound-quality)

### Inferences
- Because the Harman target includes a bass shelf relative to diffuse-field, a master balanced on a Harman-like headphone may come out lean on flatter systems, and vice versa. Cross-check on at least one other playback system, or compare the long-term spectrum against the original CD numerically.

### Gaps
- The exact Harman target shape (bass shelf amount, treble) and regression coefficients were not retrieved (paywalled).
- No study found on headphone-specific mastering decisions (for example loudness or crossfeed) in peer-reviewed literature.
