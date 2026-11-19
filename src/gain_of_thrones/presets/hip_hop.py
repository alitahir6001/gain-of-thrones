"""hip-hop: hip hop and rap (kick/808 low end, loud forward vocal, sampled or programmed beat).

Research: docs/research/hip-hop.md. DRAFT: the middle values of the report's complaint table, not yet picked
in a blind A/B. It keeps the 808's fundamental, lifts its ~100 Hz harmonics, clears a pocket in the beat while
the vocal is loud, and leaves the sample's top end alone.

Envelope (separation-artifact ceiling, from the research): EQ moves within +-3 dB at Q <= 1.5, stem gain
within +-2 dB, no gating or expansion on "other" (sample, scratches, crackle) or on the vocal (ad-libs, throws).
"""
from pedalboard import Compressor, HighpassFilter, HighShelfFilter, Pedalboard, PeakFilter

from gain_of_thrones.dsp import activity, dyn_band


def de_ess(y, stems, sr):
    """Cut the vocal's 5-8 kHz while its own sibilance is in its loudest 10%."""
    y, gr = dyn_band(y, y, sr, 5000, 8000, pct=90, ratio=3, max_cut=6)
    print(f"    de-esser 5-8k: {activity(gr)}")
    return y


def vocal_pocket(y, stems, sr):
    """The beat gives way at 1.5-4 kHz only while the vocal is loud (keyed from the raw vocal stem)."""
    y, gr = dyn_band(y, stems["vocals"], sr, 1500, 4000, pct=70, ratio=2, max_cut=2)
    print(f"    vocal pocket keyed by vocals 1.5-4k: {activity(gr)}")
    return y


# Each stem runs its stages in order: a Pedalboard, or a function (signal, raw stems, sr) -> signal.
CHAINS = {
    # No compressor: limiting already damaged this stem most (musdb-XL).
    "drums": [Pedalboard([HighpassFilter(25), PeakFilter(1000, -1, 1.0), HighShelfFilter(8000, 1)])],
    # 25 Hz HPF keeps the 808 fundamental; slow release so the bass compressor doesn't ride the waveform.
    "bass": [Pedalboard([HighpassFilter(25), PeakFilter(100, 1.5, 1.0), PeakFilter(300, -1.5, 1.0),
                         Compressor(-20, 2, 30, 250)])],
    "vocals": [Pedalboard([HighpassFilter(90), PeakFilter(250, -1.5, 1.0)]),
               de_ess,  # before brightening
               Pedalboard([PeakFilter(4000, 1.5, 1.0), HighShelfFilter(10000, 1), Compressor(-18, 2, 20, 100)])],
    "other": [Pedalboard([HighpassFilter(40), PeakFilter(300, -1.5, 1.0)]),
              vocal_pocket],
}

# LU relative to each stem's original loudness, set explicitly so EQ and compression can't shift it by accident.
BALANCE = {"drums": 0.0, "bass": 0.0, "vocals": 1.0, "other": 0.0}

# Threshold is searched so the bus loses about target_drop_db of integrated loudness.
BUS_COMP = {"ratio": 2, "attack_ms": 30, "release_ms": 200, "target_drop_db": 1.0}

CEILING = -1.2  # dBTP
