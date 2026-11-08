"""Zero-phase band split and the keyed dynamic band cut used by presets (de-esser, ducking dips)."""
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


def activity(gr):
    """One-line summary of a gain-reduction trace."""
    on = gr > 0.1
    mean = gr[on].mean() if on.any() else 0.0
    return f"active {100 * np.mean(on):.0f}% of time, mean cut when active {mean:.1f} dB"
