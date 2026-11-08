"""Loudness, dynamics and spectral balance: the numbers the agent reads back after every step."""
import re
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

from . import io

BANDS = [(20, 60, "sub"), (60, 250, "bass"), (250, 500, "low-mid"), (500, 2000, "mid"),
         (2000, 4000, "upper-mid"), (4000, 8000, "presence"), (8000, 16000, "air"), (16000, 20000, ">16k")]
HF_BANDS = [(2000, 4000, "2-4k"), (4000, 6000, "4-6k"), (6000, 10000, "6-10k"), (10000, 16000, "10-16k")]
STEMS = ("drums", "bass", "vocals", "other")


def ebur128(path):
    """ffmpeg EBU R128: integrated LUFS, LRA, max short-term LUFS, true peak (dBTP).
    Per-frame short-term values only print with -loglevel verbose."""
    e = io.run([io.tool("ffmpeg"), "-nostats", "-loglevel", "verbose", "-i", path, "-map", "0:a:0",
                "-af", "ebur128=peak=true", "-f", "null", "-"], text=True).stderr
    cut = e.rfind("Summary:")
    g = lambda k: float(re.search(k + r":\s+([-+]?[\d.]+)", e[cut:]).group(1))
    s_max = max(float(m) for m in re.findall(r"S:\s*([-+]?[\d.]+)", e[:cut]))
    return {"I": g("I"), "LRA": g("LRA"), "S_max": s_max, "TP": g("Peak")}


def dr(x, sr):
    """TT DR meter: 3 s blocks per channel, 2nd-highest block peak vs RMS of the loudest 20% of blocks.
    The RMS carries a sqrt(2), so a full-scale sine reads DR0. Undefined (nan) under 6 s."""
    n = 3 * sr
    if len(x) < 2 * n:
        return float("nan")
    out = []
    for ch in x.T:
        blocks = ch[: len(ch) // n * n].reshape(-1, n)
        rms = np.sqrt(2 * np.mean(blocks ** 2, 1))
        pk = np.sort(np.abs(blocks).max(1))
        top = np.sort(rms)[-max(1, int(round(0.2 * len(rms)))):]
        out.append(20 * np.log10(pk[-2] / np.sqrt(np.mean(top ** 2))))
    return float(np.mean(out))


def flat_tops(x, min_run=3):
    """Runs of >= min_run consecutive samples at the file's max level: a sign of clipping."""
    runs = 0
    for ch in np.abs(x).T:
        hit = ch >= ch.max() * 0.9999
        d = np.diff(np.concatenate([[0], hit.astype(int), [0]]))
        lengths = np.flatnonzero(d == -1) - np.flatnonzero(d == 1)
        runs += int(np.sum(lengths >= min_run))
    return runs


def spectrum(x, sr, n=8192):
    """Hann-windowed power spectrum of the channel mean, 50% overlap."""
    m = x.mean(1) if x.ndim > 1 else x
    w = np.hanning(n)
    p = np.zeros(n // 2 + 1)
    for i in range(0, len(m) - n, n // 2):
        p += np.abs(np.fft.rfft(m[i:i + n] * w)) ** 2
    return np.fft.rfftfreq(n, 1 / sr), p


def band_db(f, p, bands):
    """Energy per band in dB relative to the total."""
    tot = p.sum()
    return {name: 10 * np.log10(p[(f >= lo) & (f < hi)].sum() / tot) for lo, hi, name in bands}


def hf_crest(x, sr):
    """Crest factor above 6 kHz in dB: higher means cymbal transients are less squashed."""
    hp = sosfilt(butter(4, 6000, "hp", fs=sr, output="sos"), x.mean(1))
    return 20 * np.log10(np.abs(hp).max() / np.sqrt(np.mean(hp ** 2)))


def stem_share(stems_dir):
    """Percent of each high band's energy held by each Demucs stem."""
    P = {}
    for s in STEMS:
        x, sr = sf.read(Path(stems_dir) / f"{s}.wav")
        f, P[s] = spectrum(x, sr)
    share = {}
    for lo, hi, name in HF_BANDS:
        m = (f >= lo) & (f < hi)
        tot = sum(P[s][m].sum() for s in P)
        share[name] = {s: 100 * P[s][m].sum() / tot for s in P}
    return share


def analyze(path):
    """Every number for one file."""
    st = io.audio_stream(path)
    x, sr = io.decode(path)
    f, p = spectrum(x, sr)
    return {**ebur128(path), "DR": dr(x, sr), "flat_tops": flat_tops(x), "bands": band_db(f, p, BANDS),
            "hf": band_db(f, p, HF_BANDS), "hf_crest": hf_crest(x, sr), "sr": sr, "channels": st["channels"],
            "codec": st["codec_name"], "bits": st.get("bits_per_raw_sample") or st.get("bits_per_sample"),
            "duration": len(x) / sr}


def report(path):
    a = analyze(path)
    drs = "DR n/a (under 6 s)" if np.isnan(a["DR"]) else f"DR{a['DR']:.0f} ({a['DR']:.1f})"
    return "\n".join([
        f"{Path(path).name}: I {a['I']:.1f} LUFS | LRA {a['LRA']:.1f} | max S {a['S_max']:.1f} LUFS | "
        f"TP {a['TP']:+.1f} dBTP | PLR {a['TP'] - a['I']:.1f} dB | {drs} | flat-top runs(>=3) {a['flat_tops']}",
        f"  format: {a['codec']} {a['sr']} Hz {a['channels']} ch {a['bits'] or '?'}-bit {a['duration']:.3f} s",
        "  bands:  " + " | ".join(f"{k} {v:.1f}" for k, v in a["bands"].items()) + " dB re total",
        "  highs:  " + " | ".join(f"{k} {v:.1f}" for k, v in a["hf"].items())
        + f" dB re total | >6k crest {a['hf_crest']:.1f} dB",
    ])


def stem_report(stems_dir):
    lines = [f"{Path(stems_dir).name}: share of each band's energy by stem"]
    for name, by in stem_share(stems_dir).items():
        lines.append(f"  {name:>6s}  " + "  ".join(f"{s} {v:3.0f}%" for s, v in by.items()))
    return "\n".join(lines)
