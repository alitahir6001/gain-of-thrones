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


def quadrature(f, amp, secs):
    """Left sine, right cosine: the channel-mean power is constant, so a steady tone has no envelope ripple."""
    t = np.arange(int(secs * SR)) / SR
    return np.stack([np.sin(2 * np.pi * f * t), np.cos(2 * np.pi * f * t)], 1) * np.asarray(amp)[:, None]


def step(lo, hi, secs=2.0):
    """Amplitude lo, then hi from 1.0 to 1.5 s: one attack and one release."""
    a = np.full(int(secs * SR), lo)
    a[SR:int(1.5 * SR)] = hi
    return a


def test_transient_lift_raises_attacks_only_and_caps():
    x = quadrature(5000, step(0.03, 0.3), 2.0)  # +20 dB attack inside 3-8 kHz
    y, g = dsp.transient_lift(x, SR, 3000, 8000, amount=0.5, max_db=2.0)
    assert 1.99 < g.max() <= 2.0 + 1e-12 and SR <= np.argmax(g) < int(1.05 * SR)
    steady = slice(int(0.6 * SR), int(0.95 * SR))
    assert g[steady].max() < 1e-6 and np.allclose(y[steady], x[steady], rtol=0, atol=1e-9)
    assert g[int(1.3 * SR):int(1.45 * SR)].max() < 1e-3  # the held note settles back to no lift
    assert g[int(1.51 * SR):int(1.6 * SR)].max() < 1e-12  # releases are never lifted (smoothing leaves ~1e-16)
    assert np.array_equal(dsp.crack_lift(x, None, SR), y)  # the stage is this recipe


def test_transient_lift_leaves_a_low_attack_alone():
    a = np.zeros(2 * SR)
    a[SR:] = 0.3
    k = int(0.01 * SR)
    a[SR:SR + k + 1] *= np.hanning(2 * k + 1)[:k + 1]  # 10 ms attack from silence: a hard step would click at 3-8 kHz
    x = quadrature(100, a, 2.0)  # a kick-like attack far below 3 kHz
    y, _ = dsp.transient_lift(x, SR, 3000, 8000, amount=0.5, max_db=2.0)
    body = slice(0, int(1.9 * SR))  # the array's abrupt end is a filter edge, not an attack
    assert np.abs(y[body] - x[body]).max() < 1e-5  # measured 6.4e-7, -113 dB re the tone
