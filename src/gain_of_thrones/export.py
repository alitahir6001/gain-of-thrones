"""Export renders as MP3 320k or 24-bit FLAC with each source file's tags and cover. ReplayGain tags are
dropped because the levels changed. MP3 gets one gain for the whole album, lowered until every decoded
MP3 measures <= -2 dBTP (encoders overshoot, so this is measured after encoding, not predicted)."""
from pathlib import Path

import soundfile as sf

from . import io, measure
from .limiter import true_peak

MP3_CEILING = -2.0


def pair(render_dir, source_dir):
    """{source: render}, matching render names that start with '<source stem>_'."""
    sources = io.audio_files(source_dir)
    by_src = {}
    for r in (p for p in io.audio_files(render_dir) if p.suffix.lower() == ".wav"):
        match = [s for s in sources if r.name.startswith(s.stem + "_")]
        if not match:
            raise SystemExit(f"no source file in {source_dir} matches {r.name}")
        by_src.setdefault(max(match, key=lambda s: len(s.stem)), []).append(r)
    dup = [f"{s.name}: {', '.join(r.name for r in rs)}" for s, rs in by_src.items() if len(rs) > 1]
    if dup:
        raise SystemExit("more than one render per track; export a folder with one each:\n  " + "\n  ".join(dup))
    if not by_src:
        raise SystemExit(f"no .wav renders in {render_dir}")
    return {s: rs[0] for s, rs in sorted(by_src.items())}


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


def run(render_dir, source_dir, fmt, out_dir):
    pairs = pair(render_dir, source_dir)
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
