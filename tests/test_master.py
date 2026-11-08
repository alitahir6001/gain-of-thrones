import numpy as np
import pyloudnorm as pyln
import pytest
from scipy.signal import butter, sosfilt

from gain_of_thrones import master, presets
from gain_of_thrones.limiter import true_peak

SR = 44100


@pytest.mark.parametrize("name", presets.PRESETS)
def test_preset_smoke(name):
    rng = np.random.default_rng(0)
    n = SR * 10

    def noise(lo, hi, level):
        return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), rng.normal(0, 1, (n, 2)), axis=0) * level

    S = {"drums": noise(40, 15000, 0.15), "bass": noise(40, 400, 0.2),
         "vocals": noise(200, 8000, 0.1), "other": noise(100, 6000, 0.15)}
    f32 = lambda y: y.astype(np.float32).astype(np.float64)  # Demucs writes float32 stems
    S = {k: f32(v) for k, v in S.items()}
    x_in = f32(sum(S.values()) + rng.normal(0, 0.003, (n, 2)))
    preset = presets.load(name)

    outs, null = master.master(x_in, S, SR, preset, [-12.0, -10.0], preset.CEILING)

    assert null == 0
    meter = pyln.Meter(SR)
    for t, (out, _) in outs.items():
        assert abs(meter.integrated_loudness(out) - t) < 0.03
        assert true_peak(out) <= preset.CEILING + 1e-4
