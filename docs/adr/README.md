# Architecture decision records

One file per decision, in MADR 4.0 format. Read this index first: it lists every decision that shapes the project. To change a decision, write a new ADR and mark the old one `superseded by ADR-NNNN`; never rewrite an accepted one.

ADRs 0001-0015 were backfilled on 2026-11-08 from the repository. Each one is dated by its evidence: 2026-11-05 for decisions grounded in the research notes, 2026-11-08 (the first commit) for the rest.

- [0001 - Remaster from Demucs stems, not the stereo master alone - accepted - 2026-11-05](0001-remaster-from-demucs-stems.md)
- [0002 - Keep per-stem moves inside the separation envelope - accepted - 2026-11-05](0002-stay-inside-the-separation-envelope.md)
- [0003 - Add the stem residual back at unity, before bus processing - accepted - 2026-11-05](0003-add-the-residual-back-at-unity.md)
- [0004 - No repair stage: don't de-clip, de-limit or denoise the source - accepted - 2026-11-05](0004-no-repair-stage.md)
- [0005 - One fixed mastering chain; presets fill in only the per-stem stages - accepted - 2026-11-05](0005-fixed-mastering-chain-order.md)
- [0006 - Use a look-ahead true-peak limiter, not pedalboard's Limiter - accepted - 2026-11-08](0006-own-true-peak-limiter.md)
- [0007 - Lower the input 1.5 dB in float before splitting - accepted - 2026-11-08](0007-lower-the-input-before-splitting.md)
- [0008 - Judge versions in a blind A/B that only turns them down - accepted - 2026-11-08](0008-blind-level-matched-ab.md)
- [0009 - The person decides by ear; the agent measures and explains - accepted - 2026-11-08](0009-person-decides-agent-measures.md)
- [0010 - Presets are Python modules, loaded by name or by path - accepted - 2026-11-08](0010-presets-are-python-modules.md)
- [0011 - Carry one loudness shift across the whole album - accepted - 2026-11-08](0011-one-loudness-shift-per-album.md)
- [0012 - Measure the MP3 gain after encoding, with one gain for the album - accepted - 2026-11-08](0012-measure-mp3-gain-after-encoding.md)
- [0013 - A new genre ships only with a research report and a blind A/B win - accepted - 2026-11-08](0013-new-genre-needs-research-and-blind-ab.md)
- [0014 - Never commit audio; tests use synthetic signals - accepted - 2026-11-08](0014-no-audio-in-git.md)
- [0015 - License the project GPL-3.0-or-later - accepted - 2026-11-08](0015-gpl-3-or-later-license.md)
