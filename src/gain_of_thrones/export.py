"""Export renders with each source file's tags and cover: MP3 320k or AAC 256k (lossy), or 24-bit FLAC, ALAC or
WAV (lossless: the rendered samples unchanged). ReplayGain tags are dropped because the levels changed. Lossy
formats get one gain for all files of a run (so export an album in one run), lowered until every decoded file
measures <= -2 dBTP (encoders overshoot, so this is measured after encoding, not predicted)."""
from pathlib import Path

import soundfile as sf

from . import io, measure
from .limiter import true_peak

LOSSY_CEILING = -2.0
# name: (extension, lossy, ffmpeg audio options). Renders are 24-bit, so the lossless formats keep every sample.
FORMATS = {
    "mp3": ("mp3", True, ["-c:a", "libmp3lame", "-b:a", "320k", "-id3v2_version", "3"]),
    "aac": ("m4a", True, ["-c:a", "aac", "-b:a", "256k"]),  # built-in encoder: Apple's aac_at added 820 samples
    "flac": ("flac", False, ["-c:a", "flac", "-sample_fmt", "s32", "-bits_per_raw_sample", "24"]),
    "alac": ("m4a", False, ["-c:a", "alac", "-sample_fmt", "s32p", "-bits_per_raw_sample", "24"]),
    "wav": ("wav", False, ["-c:a", "pcm_s24le"]),
}
NO_COVER = {"wav": "WAV can't hold cover art"}  # ffmpeg refuses an attached picture there


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


def has_cover(info):
    return any(s["codec_type"] == "video" for s in info["streams"])


def encode(render, source, out, fmt, gain_db=0.0):
    _, lossy, opts = FORMATS[fmt]
    info = io.probe(source)
    drop = [k for k in info["format"].get("tags", {}) if k.upper().startswith("REPLAYGAIN_")]
    cmd = [io.tool("ffmpeg"), "-v", "error", "-y", "-i", render, "-i", source, "-map", "0:a", "-map_metadata", "1"]
    if has_cover(info) and fmt not in NO_COVER:
        cmd += ["-map", "1:v:0", "-c:v", "copy", "-disposition:v", "attached_pic"]
    for k in drop:
        cmd += ["-metadata", f"{k}="]  # empty value deletes the tag
    if lossy:
        cmd += ["-af", f"volume={gain_db:.2f}dB"]
    io.run(cmd + opts + [out])
    return drop


def carried(source, out, fmt):
    """(cover status, source tags the exported file lacks, number of source tags), ReplayGain aside."""
    src, dst = io.probe(source), io.probe(out)
    tags = {k.lower() for k in src["format"].get("tags", {}) if not k.upper().startswith("REPLAYGAIN_")}
    lost = sorted(tags - {k.lower() for k in dst["format"].get("tags", {})})
    if not has_cover(src):
        cover = "none in the source"
    elif has_cover(dst):
        cover = "kept"
    else:
        cover = f"none ({NO_COVER[fmt]})" if fmt in NO_COVER else "lost"
    return cover, lost, len(tags)


def run(renders, source_dir, fmt, out_dir):
    ext, lossy, _ = FORMATS[fmt]
    pairs = pair(renders, source_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outs = {s: out_dir / f"{s.stem}.{ext}" for s in pairs}
    gain = 0.0
    if lossy:
        gain = min(0.0, LOSSY_CEILING - max(true_peak(sf.read(r)[0]) for r in pairs.values()))
    dropped = set()
    for _ in range(6):
        for s, r in pairs.items():
            dropped |= set(encode(r, s, outs[s], fmt, gain))
        if not lossy:
            break
        worst = max(true_peak(io.decode(o)[0]) for o in outs.values())
        print(f"  {fmt.upper()} gain {gain:+.2f} dB -> loudest decoded true peak {worst:.2f} dBTP")
        if worst <= LOSSY_CEILING:
            break
        gain -= worst - LOSSY_CEILING + 0.05
    else:
        raise SystemExit(f"{fmt.upper()} files still over {LOSSY_CEILING} dBTP after 6 tries")
    print(f"exported {len(outs)} files to {out_dir} (uniform gain {gain:+.2f} dB; "
          f"dropped tags: {', '.join(sorted(dropped)) or 'none'})")
    for s, o in outs.items():
        print(measure.report(o))
        cover, lost, n = carried(s, o, fmt)
        print(f"  carried: cover {cover} | tags {n - len(lost)} of {n}"
              + (f"; no slot in {ext.upper()}: {', '.join(lost)}" if lost else ""))
    return outs
