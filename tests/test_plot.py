import xml.etree.ElementTree as ET

import numpy as np
import soundfile as sf

from gain_of_thrones import measure, plot

SR = 44100
NS = "{http://www.w3.org/2000/svg}"


def sine(amp, secs=8):
    s = amp * np.sin(2 * np.pi * 1000 * np.arange(secs * SR) / SR)
    return np.stack([s, s], 1)


def texts(svg):
    return [t.text for t in ET.fromstring(svg).iter(NS + "text")]


def test_axis_range_is_on_3_db_steps_covers_the_data_and_spans_at_least_12():
    lo, hi = plot.axis_range([-20.5, -14.2, -10.4])
    assert (lo % 3, hi % 3) == (0, 0)
    assert lo <= -20.5 - 1 and hi >= -10.4 + 1
    assert plot.axis_range([-14.0, -13.5]) == (-24, -12)


def test_time_step_keeps_at_most_10_major_ticks():
    assert [plot.time_step(d) for d in (45, 180, 600, 3600)] == [5, 30, 60, 600]


def test_curve_drops_the_unfilled_window_and_caps_the_points():
    frames = [(i / 10, -20.0) for i in range(1, 100001)]
    t, s = plot.curve(frames)
    assert t[0] >= plot.WINDOW and len(t) <= plot.MAX_POINTS
    assert np.allclose(s, -20.0)


def test_render_shows_the_measured_numbers_and_a_valid_svg(tmp_path):
    ref, rem = tmp_path / "ref.wav", tmp_path / "rem.wav"
    sf.write(ref, sine(0.1), SR)
    sf.write(rem, sine(0.3), SR)  # +9.5 dB
    out = plot.render(ref, rem, tmp_path / "p.svg")
    t = texts(out.read_text())
    m0, m1 = measure.ebur128(ref), measure.ebur128(rem)
    assert f"I {plot.fmt_db(m0['I'], 'LUFS')}" in t and f"I {plot.fmt_db(m1['I'], 'LUFS')}" in t
    assert plot.fmt_db(m1["I"] - m0["I"], "LU", plus=True) in t
    assert "ref" in t  # no title tag: the file name


def test_title_is_escaped():
    s = {"I": -10.0, "TP": -1.0, "LRA": 4.0, "S_max": -8.0, "t": np.array([3.0, 6.0]), "S": np.array([-12.0, -9.0])}
    svg = plot.svg("Rock & Roll <Live>", [{"label": "Original", **s}, {"label": "Remaster", **s}])
    assert "Rock & Roll <Live>" in texts(svg)
