import numpy as np
import pyloudnorm as pyln
import soundfile as sf

from gain_of_thrones import io, measure

SR = 44100


def sine(f, secs, amp=1.0):
    s = amp * np.sin(2 * np.pi * f * np.arange(int(secs * SR)) / SR)
    return np.stack([s, s], 1)


def test_dr_full_scale_sine_is_dr0():
    assert abs(measure.dr(sine(1000, 30), SR)) < 0.05


def test_dr_half_scale_sine_with_full_scale_clicks_is_dr6():
    x = sine(1000, 30, 0.5)
    x[4 * SR] = x[10 * SR] = 1.0  # two blocks peak at full scale
    assert abs(measure.dr(x, SR) - 20 * np.log10(2)) < 0.05


def test_flat_tops_counts_clipped_half_cycles():
    x = np.clip(sine(900, 1, 2.0), -1, 1)  # 49 samples per cycle: 900 cycles, 1800 clipped runs per channel
    assert measure.flat_tops(x) == 2 * 1800


def test_flat_tops_zero_on_clean_sine():
    assert measure.flat_tops(sine(1000, 1, 0.5)) == 0


def test_pyloudnorm_agrees_with_ffmpeg(tmp_path):
    x = np.random.default_rng(0).normal(0, 0.1, (SR * 10, 2))
    x[3 * SR:5 * SR] *= 0.3  # a quieter passage so the gating matters
    p = tmp_path / "noise.wav"
    sf.write(p, x, SR, subtype="FLOAT")
    I_py = pyln.Meter(SR).integrated_loudness(sf.read(p)[0])
    assert abs(measure.ebur128(p)["I"] - I_py) < 0.1


def test_format_line_shows_bit_depth_only_for_lossless(tmp_path):
    for name, opts in (("t.mp3", ["-c:a", "libmp3lame"]),
                       ("t.flac", ["-c:a", "flac", "-sample_fmt", "s32", "-bits_per_raw_sample", "24"])):
        io.run([io.tool("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=3", *opts,
                tmp_path / name])
    mp3, flac = (measure.report(tmp_path / n).splitlines()[1] for n in ("t.mp3", "t.flac"))
    assert "-bit" not in mp3 and "?" not in mp3
    assert " 24-bit " in flac
