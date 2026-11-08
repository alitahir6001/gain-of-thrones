import numpy as np

from gain_of_thrones import dsp

SR = 44100


def test_band_split_is_complementary():
    x = np.random.default_rng(0).normal(0, 0.2, (SR * 2, 2))
    b = dsp.band(x, SR, 2500, 5000)
    assert np.allclose((x - b) + b, x, rtol=0, atol=1e-15)


def test_dyn_band_cuts_only_while_key_is_loud():
    rng = np.random.default_rng(2)
    x = rng.normal(0, 0.1, (SR * 4, 2))
    key = rng.normal(0, 0.1, (SR * 4, 2))
    key[:2 * SR] *= 0.01  # quiet for 2 s, normal to 3.5 s, then a +12 dB burst
    key[int(3.5 * SR):] *= 4  # 70th percentile lands in the normal part
    y, gr = dsp.dyn_band(x, key, SR, 2500, 5000, pct=70, ratio=2, max_cut=3)
    quiet = slice(0, 2 * SR - SR // 10)  # stop 100 ms early: envelope and 20 ms smoothing spread the onset
    assert np.all(gr[quiet] == 0)
    assert np.allclose(y[quiet], x[quiet], rtol=0, atol=1e-12)
    assert np.allclose(gr[int(3.6 * SR):], 3)  # ~12 dB over threshold at 2:1 -> capped at max_cut
    assert gr.max() <= 3 + 1e-9
