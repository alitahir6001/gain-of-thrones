"""Export renders as MP3 320k or 24-bit FLAC with each source file's tags and cover. ReplayGain tags are
dropped because the levels changed. MP3 gets one gain for all files of a run (so export an album in one
run), lowered until every decoded MP3 measures <= -2 dBTP (encoders overshoot, so this is measured after
encoding, not predicted)."""
from pathlib import Path

import soundfile as sf

from . import io, measure
from .limiter import true_peak

MP3_CEILING = -2.0


def pair(renders, source_dir):
    """{source: render} for render .wav files and folders of them, matching render names that start with
    '<source stem>_'."""
    sources = io.audio_files(source_dir)
    files = []
    for p in map(Path, renders):
        if not p.exists():
            raise SystemExit(f"no such render: {p}")
        files += [f for f in io.audio_files(p) if f.suffix.lower() == ".wav"] if p.is_dir() else [p]
    by_src = {}
    # a file listed twice, or also inside a listed folder, counts once
    for r in {f.resolve(): f for f in files}.values():
        if r.suffix.lower() != ".wav":
            raise SystemExit(f"not a .wav render: {r}")
        match = [s for s in sources if r.name.startswith(s.stem + "_")]
        if not match:
            raise SystemExit(f"no source file in {source_dir} matches {r.name}")
        by_src.setdefault(max(match, key=lambda s: len(s.stem)), []).append(r)
    dup = [f"{s.name}: {', '.join(r.name for r in rs)}" for s, rs in by_src.items() if len(rs) > 1]
    if dup:
        raise SystemExit("more than one render per track; pass the render files you want instead:\n  "
                         + "\n  ".join(dup))
    if not by_src:
        raise SystemExit(f"no .wav renders in {', '.join(map(str, renders))}")
    return {s: rs[0] for s, rs in sorted(by_src.items())}


def default_out(renders, fmt):
    """<work>/export/<fmt>: the folder above the first render's nearest renders/ folder, else its folder's parent."""
    d = Path(renders[0]).resolve()
    d = d if d.is_dir() else d.parent
    return next((p.parent for p in (d, *d.parents) if p.name == "renders"), d.parent) / "export" / fmt


def encode(render, source, out, fmt, gain_db=0.0):
    info = io.probe(source)
    drop = [k for k in info["format"].get("tags", {}) if k.upper().startswith("REPLAYGAIN_")]
    cmd = [io.tool("ffmpeg"), "-v", "error", "-y", "-i", render, "-i", source, "-map", "0:a", "-map_metadata", "1"]
    if any(s["codec_type"] == "video" for s in info["streams"]):  # embedded cover
        cmd += ["-map", "1:v:0", "-c:v", "copy", "-disposition:v", "attached_pic"]
    for k in drop:
        cmd += ["-metadata", f"{k}="]  # empty value deletes the tag
    if fmt == "mp3":
        cmd += ["-af", f"volume={gain_db:.2f}dB", "-c:a", "libmp3lame", "-b:a", "320k", "-id3v2_version", "3"]
    else:
        cmd += ["-c:a", "flac", "-sample_fmt", "s32", "-bits_per_raw_sample", "24"]
    io.run(cmd + [out])
    return drop


def run(renders, source_dir, fmt, out_dir):
    pairs = pair(renders, source_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outs = {s: out_dir / f"{s.stem}.{fmt}" for s in pairs}
    gain = 0.0
    if fmt == "mp3":
        gain = min(0.0, MP3_CEILING - max(true_peak(sf.read(r)[0]) for r in pairs.values()))
    dropped = set()
    for _ in range(6):
        for s, r in pairs.items():
            dropped |= set(encode(r, s, outs[s], fmt, gain))
        if fmt != "mp3":
            break
        worst = max(true_peak(io.decode(o)[0]) for o in outs.values())
        print(f"  MP3 gain {gain:+.2f} dB -> loudest decoded true peak {worst:.2f} dBTP")
        if worst <= MP3_CEILING:
            break
        gain -= worst - MP3_CEILING + 0.05
    else:
        raise SystemExit(f"MP3s still over {MP3_CEILING} dBTP after 6 tries")
    print(f"exported {len(outs)} files to {out_dir} (uniform gain {gain:+.2f} dB; "
          f"dropped tags: {', '.join(sorted(dropped)) or 'none'})")
    for o in outs.values():
        print(measure.report(o))
    return outs
