"""heavy-guitar: punk, hardcore, thrash and metal (distorted guitars, shouted vocals, dense cymbals).

Research: docs/research/heavy-metal-punk.md. The values are the v4 recipe that won a blind, level-matched
A/B on a 1980s thrash/punk EP ripped from CD. The complaints it answers: guitars small and cloudy, vocal
reverby and buried, cymbals lost at high volume.

Envelope (separation-artifact ceiling, from the research): EQ moves within +-3 dB at Q <= 1.5, stem gain
within +-2 dB, no gating or expansion on "other" (it exposes separation errors).
"""
from pedalboard import Compressor, HighpassFilter, HighShelfFilter, LowShelfFilter, NoiseGate, Pedalboard, PeakFilter

from gain_of_thrones.dsp import activity, dyn_band


def de_ess(y, stems, sr):
    """Cut the vocal's 5-8 kHz while its own sibilance is in its loudest 10%."""
    y, gr = dyn_band(y, y, sr, 5000, 8000, pct=90, ratio=3, max_cut=6)
    print(f"    de-esser 5-8k: {activity(gr)}")
    return y


def guitar_dip(y, stems, sr):
    """Guitars give way at 2.5-5 kHz only while cymbals are loud (keyed from the raw drum stem)."""
    y, gr = dyn_band(y, stems["drums"], sr, 2500, 5000, pct=70, ratio=2, max_cut=3)
    print(f"    guitar dip keyed by drums 2.5-5k: {activity(gr)}")
    return y


# Each stem runs its stages in order: a Pedalboard, or a function (signal, raw stems, sr) -> signal.
CHAINS = {
    "drums": [Pedalboard([HighpassFilter(30), PeakFilter(400, -1.5, 1.0), PeakFilter(4500, 1.5, 1.0),
                          HighShelfFilter(8000, 2.5), Compressor(-20, 2, 25, 120)])],
    "bass": [Pedalboard([HighpassFilter(35), LowShelfFilter(80, -1.5), PeakFilter(300, -2.5, 1.0),
                         PeakFilter(900, 2, 1.0), PeakFilter(2500, 1.5, 1.0), Compressor(-20, 2, 25, 150)])],
    "vocals": [Pedalboard([HighpassFilter(160), PeakFilter(300, -2.5, 1.0)]),
               de_ess,  # before brightening
               # The gate stays: the listener approved the drier vocal.
               Pedalboard([PeakFilter(3800, 3, 1.0), HighShelfFilter(10000, 1.5), NoiseGate(-38, 2.0, 2, 60),
                           Compressor(-18, 2, 20, 80)])],
    "other": [Pedalboard([HighpassFilter(90), PeakFilter(150, -1.5, 1.5), PeakFilter(300, -3, 0.7),
                          PeakFilter(1800, 1.5, 0.8), PeakFilter(3200, -2, 1.2)]),
              guitar_dip],
}

# LU relative to each stem's original loudness, set explicitly so EQ and compression can't shift it by accident.
BALANCE = {"drums": 0.0, "bass": 0.0, "vocals": 1.5, "other": -0.5}

# Threshold is searched so the bus loses about target_drop_db of integrated loudness.
BUS_COMP = {"ratio": 2, "attack_ms": 35, "release_ms": 120, "target_drop_db": 1.5}

CEILING = -1.2  # dBTP
