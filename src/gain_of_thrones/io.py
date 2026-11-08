"""ffmpeg/ffprobe I/O. Paths are pathlib and never globbed, so folder names like "Freaks [EP]" are safe.
Every subprocess gets stdin=DEVNULL so it cannot swallow a caller's piped input."""
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np

AUDIO_EXTS = {".wav", ".flac", ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".aif", ".aiff", ".aifc",
              ".alac", ".ape", ".wv", ".dsf"}


def tool(name):
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"{name} not found on PATH. Install ffmpeg (brew / winget / apt) and retry.")
    return path


def run(cmd, text=False):
    """Run a command with stdin closed; raise with the tail of its stderr on failure."""
    p = subprocess.run([str(c) for c in cmd], stdin=subprocess.DEVNULL, capture_output=True, text=text)
    if p.returncode:
        err = p.stderr if text else p.stderr.decode(errors="replace")
        raise RuntimeError(f"{Path(cmd[0]).name} failed ({p.returncode}): {err.strip()[-2000:]}")
    return p


def probe(path):
    """ffprobe's streams and format (incl. tags) as a dict."""
    out = run([tool("ffprobe"), "-v", "error", "-show_streams", "-show_format", "-of", "json", path], text=True)
    return json.loads(out.stdout)


def audio_stream(path):
    return next(s for s in probe(path)["streams"] if s["codec_type"] == "audio")


def decode(path, channels=2):
    """Any audio file -> (float64 array of shape (n, channels), sample rate)."""
    sr = int(audio_stream(path)["sample_rate"])
    raw = run([tool("ffmpeg"), "-v", "error", "-i", path, "-map", "0:a:0", "-f", "f32le", "-ac", channels, "-"]).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, channels).astype(np.float64), sr


def audio_files(folder):
    """Audio files directly in folder, sorted by name (skips macOS ._ files)."""
    return sorted(p for p in Path(folder).iterdir()
                  if p.is_file() and p.suffix.lower() in AUDIO_EXTS and not p.name.startswith("."))
