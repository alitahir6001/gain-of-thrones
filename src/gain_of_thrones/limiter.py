"""Look-ahead true-peak limiter. pedalboard's Limiter adds make-up gain and is not a ceiling
(driven to loudness it left 1529 clipped flat-top runs on one track); this one never clips."""
import numpy as np
from scipy.ndimage import minimum_filter1d, uniform_filter1d
from scipy.signal import resample_poly


def true_peak(x):
    """Peak of the 4x-oversampled signal, in dBTP."""
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max())


def tp_limit(x, sr, ceil_db, look_ms=40):
    """Limit stereo x (n, ch) so its 4x-oversampled peak stays under ceil_db.
    Gain = min over a 2*look window, then averaged over look, which guarantees gain <= required gain
    at every sample. Returns (limited signal, gain reduction in dB per sample)."""
    up = np.abs(resample_poly(x, 4, 1, axis=0)).max(1).reshape(-1, 4).max(1)[: len(x)]
    need = np.minimum(1, 10 ** (ceil_db / 20) / np.maximum(up, 1e-9))
    L = int(sr * look_ms / 1000)
    g = uniform_filter1d(minimum_filter1d(need, 2 * L + 1), L)
    return x * g[:, None], -20 * np.log10(g)
