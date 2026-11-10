"""Zero-phase band split, the keyed dynamic band cut used by presets (de-esser, ducking dips), and the band
transient lift behind the opt-in crack_lift drum stage."""
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter, lfilter, sosfiltfilt


def band(x, sr, lo, hi):
    """lo-hi band of x, zero-phase (so x - band + band == x)."""
    return sosfiltfilt(butter(4, [lo, hi], "bandpass", fs=sr, output="sos"), x, axis=0)


def env_db(x, sr, ms):
    """One-pole power envelope of the channel mean, in dB."""
    a = np.exp(-1 / (sr * ms / 1000))
    return 10 * np.log10(lfilter([1 - a], [1, -a], np.mean(x ** 2, 1)) + 1e-12)


def dyn_band(x, key, sr, lo, hi, pct, ratio, max_cut):
    """Cut x's lo-hi band only while the key's lo-hi energy is above its pct-th percentile.
    Returns (processed x, gain reduction in dB per sample)."""
    b = band(x, sr, lo, hi)
    e = env_db(band(key, sr, lo, hi), sr, 10)
    thr = np.percentile(e[e > -80], pct)
    gr = np.clip((e - thr) * (1 - 1 / ratio), 0, max_cut)
    gr = uniform_filter1d(gr, int(sr * 0.02))  # smooth gain changes over 20 ms
    return (x - b) + b * 10 ** (-gr[:, None] / 20), gr


def transient_lift(x, sr, lo, hi, amount, max_db):
    """Raise x's lo-hi band on its attacks only: (1 ms minus 30 ms envelope) x amount, clipped to 0..max_db and
    smoothed over 2 ms, so sustained sound is left alone. Returns (processed x, lift in dB per sample)."""
    b = band(x, sr, lo, hi)
    g = uniform_filter1d(np.clip((env_db(b, sr, 1) - env_db(b, sr, 30)) * amount, 0, max_db), int(sr * 0.002))
    return (x - b) + b * 10 ** (g[:, None] / 20), g


def crack_lift(y, stems, sr):
    """Opt-in drum-stem stage: snare crack and snap (3-8 kHz) attacks up by at most 2 dB, cymbal wash untouched.
    Add it at the end of a preset copy's drum chain. One track's blind win, drum compressor off (ADR 0016)."""
    y, g = transient_lift(y, sr, 3000, 8000, amount=0.5, max_db=2.0)
    on = g > 0.1
    mean = g[on].mean() if on.any() else 0.0
    print(f"    crack lift 3-8k: active {100 * on.mean():.0f}% of time, mean lift when active {mean:.1f} dB")
    return y


def activity(gr):
    """One-line summary of a gain-reduction trace."""
    on = gr > 0.1
    mean = gr[on].mean() if on.any() else 0.0
    return f"active {100 * np.mean(on):.0f}% of time, mean cut when active {mean:.1f} dB"
