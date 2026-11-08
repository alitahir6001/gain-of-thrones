import numpy as np

from gain_of_thrones.limiter import tp_limit, true_peak
from gain_of_thrones.measure import flat_tops

SR = 44100
TOL = 0.05  # dB: gain is computed on the oversampled input, peaks are re-measured on the output


def test_true_peak_under_ceiling_on_bursts_and_spike():
    rng = np.random.default_rng(1)
    x = rng.normal(0, 0.2, (SR * 5, 2))
    x[SR:SR + 50] *= 6
    x[3 * SR] = 1.8
    y, gr = tp_limit(x, SR, -1.3)
    assert true_peak(x) > 0
    assert true_peak(y) <= -1.3 + TOL


def test_catches_intersample_peak():
    n = np.arange(SR)
    s = np.sin(2 * np.pi * n / 4 + np.pi / 4)  # fs/4 at 45 degrees: samples at +-0.707, true peak 1.0
    x = np.stack([s, s], 1) * 10 ** (-1.0 / 20)
    assert np.abs(x).max() < 10 ** (-1.3 / 20) < 10 ** (true_peak(x) / 20)  # only the true peak is over
    y, _ = tp_limit(x, SR, -1.3)
    assert true_peak(y) <= -1.3 + TOL


def test_leaves_signal_alone_far_from_peaks():
    rng = np.random.default_rng(3)
    x = rng.normal(0, 0.05, (SR * 3, 2))
    x[SR] = 1.5
    y, gr = tp_limit(x, SR, -1.3)
    far = np.r_[0:SR - SR // 10, SR + SR // 10:3 * SR]  # > 100 ms from the spike; look-ahead is 40 ms
    assert gr[SR] > 3
    assert np.allclose(y[far], x[far], rtol=0, atol=1e-12)


def test_no_flat_tops_when_driven_hard():
    rng = np.random.default_rng(4)
    x = rng.normal(0, 0.9, (SR * 10, 2))  # about 10 dB over the ceiling
    ceil = 10 ** (-1.3 / 20)
    assert flat_tops(np.clip(x, -ceil, ceil)) > 100  # clipping to the same ceiling would show
    y, _ = tp_limit(x, SR, -1.3)
    assert flat_tops(y) == 0
