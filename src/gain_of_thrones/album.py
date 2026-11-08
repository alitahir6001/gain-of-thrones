"""Album: one loudness shift for every track, so the loudest lands at the target and the CD's
song-to-song levels survive. Resumable: existing stems and renders are skipped."""
from pathlib import Path

import pyloudnorm as pyln

from . import io, master, presets, separate


def loudness(path):
    x, sr = io.decode(path)
    return pyln.Meter(sr).integrated_loudness(x)


def shifted_targets(L, target):
    """{track: original LUFS} -> {track: target LUFS}: one shift for all, rounded to 0.1 LU
    (renders only land within 0.03 LU anyway)."""
    shift = target - max(L.values())
    return {t: round(l + shift, 1) for t, l in L.items()}


def run(src_dir, target, work, preset_name="heavy-guitar", shifts=2, device=None):
    work = Path(work)
    preset = presets.load(preset_name)
    name = Path(preset_name).stem.replace("_", "-")
    tracks = io.audio_files(src_dir)
    if not tracks:
        raise SystemExit(f"no audio files in {src_dir}")
    L = {p.stem: loudness(p) for p in tracks}
    T = shifted_targets(L, target)
    work.mkdir(parents=True, exist_ok=True)
    (work / "targets.tsv").write_text("track\toriginal_lufs\ttarget_lufs\n"
                                      + "".join(f"{t}\t{L[t]:.2f}\t{T[t]:g}\n" for t in L))
    print(f"shift {target - max(L.values()):+.2f} LU for all {len(tracks)} tracks (targets: {work / 'targets.tsv'})")
    out_dir = work / "renders" / "album"
    for p in tracks:
        t = T[p.stem]
        if (out_dir / f"{p.stem}_{name}_{t:g}LUFS.wav").exists():
            print(f"{p.stem}: render exists, skipping")
            continue
        print(f"=== {p.stem}: {L[p.stem]:.2f} -> {t:g} LUFS", flush=True)
        stems_dir, split_input = separate.split(p, work, shifts, device)
        master.render(stems_dir, split_input, out_dir, preset, [t], preset.CEILING, name)
    print(f"album renders: {out_dir}")
