"""Demucs wrapper. The input is lowered 1.5 dB in float first: CD rips can peak over 0 dBTP, which would
clip the stems. MPS crashes with htdemucs_ft ("Output channels > 65536 not supported"), so Apple Silicon
runs on CPU."""
import subprocess
import sys
import time
from pathlib import Path

import soundfile as sf

from . import io
from .measure import STEMS

MODEL = "htdemucs_ft"


def default_device():
    import torch
    return "cuda" if torch.cuda.is_available() else "cpu"


def split(track, work, shifts=2, device=None):
    """Write work/input/<track>.wav (input -1.5 dB, float) and work/stems/htdemucs_ft/<track>/*.wav.
    Skips whatever already exists. Returns (stems_dir, split_input)."""
    track, work = Path(track), Path(work)
    split_input = work / "input" / f"{track.stem}.wav"
    stems_dir = work / "stems" / MODEL / track.stem
    if not split_input.exists():
        split_input.parent.mkdir(parents=True, exist_ok=True)
        tmp = split_input.with_suffix(".partial.wav")
        io.run([io.tool("ffmpeg"), "-v", "error", "-y", "-i", track, "-map", "0:a:0", "-af", "volume=-1.5dB",
                "-c:a", "pcm_f32le", tmp])
        tmp.rename(split_input)
    if all((stems_dir / f"{s}.wav").exists() for s in STEMS):
        print(f"{track.stem}: stems exist, skipping split")
    else:
        device = device or default_device()
        log = work / "stems" / f"{track.stem}.log"
        partial = stems_dir.with_name(stems_dir.name + ".partial")
        log.parent.mkdir(parents=True, exist_ok=True)
        print(f"{track.stem}: splitting with {MODEL} on {device}, shifts {shifts} (log: {log})", flush=True)
        t0 = time.time()
        with open(log, "w") as f:
            p = subprocess.run([sys.executable, "-m", "demucs", "-n", MODEL, "-d", device, "--float32",
                                "--shifts", str(shifts), "-o", str(work / "stems"),
                                "--filename", "{track}.partial/{stem}.{ext}", str(split_input)],
                               stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT)
        if p.returncode:
            raise SystemExit(f"demucs failed ({p.returncode}); see {log}")
        partial.rename(stems_dir)
        secs = time.time() - t0
        dur = sf.info(split_input).duration
        print(f"{track.stem}: split in {secs:.0f} s ({secs / dur:.1f} s per audio second)")
    print(f"  stems: {stems_dir}\n  split input: {split_input}")
    return stems_dir, split_input
