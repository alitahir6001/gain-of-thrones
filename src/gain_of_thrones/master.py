"""Chain engine: stems -> preset chains -> explicit balance -> + residual -> bus comp -> true-peak limiter -> dither.
Every render measures itself and prints the numbers."""
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from pedalboard import Compressor, Pedalboard

from . import measure
from .limiter import tp_limit, true_peak
from .measure import STEMS


def run_board(board, y, sr):
    return board(y.T.astype(np.float32), sr).T.astype(np.float64)


def load_stems(stems_dir):
    return {s: sf.read(Path(stems_dir) / f"{s}.wav", dtype="float64")[0] for s in STEMS}


def bus_compress(mix, sr, meter, ratio, attack_ms, release_ms, target_drop_db):
    """Bisect the threshold so the compressor takes about target_drop_db off integrated loudness."""
    L0 = meter.integrated_loudness(mix)
    lo, hi = -40.0, 0.0
    for _ in range(10):
        th = (lo + hi) / 2
        y = run_board(Pedalboard([Compressor(th, ratio, attack_ms, release_ms)]), mix, sr)
        drop = L0 - meter.integrated_loudness(y)
        lo, hi = (th, hi) if drop > target_drop_db else (lo, th)
    print(f"  bus comp: threshold {th:.1f} dBFS, loudness drop {drop:.2f} dB")
    return y


def master(x_in, S, sr, preset, targets, ceiling):
    """Render x_in's stems S through preset at each target LUFS. Returns {target: (24-bit-ready audio, limiter GR)}
    and the bypass null test (max |input - (stems + residual)|, exactly 0 when the stems are float32)."""
    residual = x_in - sum(S.values())
    print(f"  residual {10 * np.log10(np.sum(residual ** 2) / np.sum(x_in ** 2)):.1f} dB re input")
    null = np.abs(x_in - (sum(S.values()) + residual)).max()
    print(f"  null test (bypass): max |diff| {null:.2e}")

    P = {}
    for s in STEMS:
        y = S[s]
        for stage in preset.CHAINS.get(s, []):
            y = run_board(stage, y, sr) if isinstance(stage, Pedalboard) else stage(y, S, sr)
        P[s] = y

    meter = pyln.Meter(sr)
    for s in P:
        l0, l1 = meter.integrated_loudness(S[s]), meter.integrated_loudness(P[s])
        P[s] *= 10 ** ((l0 + preset.BALANCE.get(s, 0.0) - l1) / 20)
        print(f"  {s:6s} {l0:6.1f} -> {l1:6.1f} after chain -> {meter.integrated_loudness(P[s]):6.1f} LUFS balanced")
    bus = bus_compress(sum(P.values()) + residual, sr, meter, **preset.BUS_COMP)

    rng = np.random.default_rng(0)
    out_by_target = {}
    for t in targets:
        gain = t - meter.integrated_loudness(bus)
        for _ in range(8):  # limiting eats loudness: iterate the drive
            out, gr = tp_limit(bus * 10 ** (gain / 20), sr, ceiling - 0.1)
            err = t - meter.integrated_loudness(out)
            if abs(err) < 0.03:
                break
            gain += err
        out *= 10 ** (min(0, ceiling - true_peak(out)) / 20)
        out = out + (rng.random(out.shape) - rng.random(out.shape)) * 2.0 ** -23  # flat TPDF dither, 24-bit
        out_by_target[t] = (out, gr)
    return out_by_target, null


def render(stems_dir, split_input, out_dir, preset, targets, ceiling, name):
    """Read stems + split input, master, write 24-bit WAVs, and measure each written file."""
    track = Path(split_input).stem
    print(f"{track}:")
    x_in, sr = sf.read(split_input, dtype="float64")
    S = load_stems(stems_dir)
    outs, _ = master(x_in, S, sr, preset, targets, ceiling)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    meter = pyln.Meter(sr)
    paths = []
    for t, (out, gr) in outs.items():
        path = out_dir / f"{track}_{name}_{t:g}LUFS.wav"
        sf.write(path, out, sr, subtype="PCM_24")
        print(f"  {path.name}: {meter.integrated_loudness(out):.2f} LUFS, {true_peak(out):.2f} dBTP, "
              f"limiter GR max {gr.max():.1f} dB, active {100 * np.mean(gr > 0.1):.0f}% of time")
        print("  " + measure.report(path).replace("\n", "\n  "))
        paths.append(path)
    return paths
