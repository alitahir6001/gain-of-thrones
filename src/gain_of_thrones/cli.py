"""got: the agent's toolbelt. Each command does one verifiable step and prints measured numbers."""
import argparse
from pathlib import Path


def cmd_analyze(a):
    import soundfile as sf

    from . import measure
    if a.stems:
        drums, sr = sf.read(Path(a.stems) / "drums.wav")
        hits = measure.snare_hits(drums, sr)
    for p in a.files:
        print(measure.report(p))
        if a.stems:
            print(measure.snare_report(p, drums, sr, hits))
    if a.blocks:
        print(measure.block_report(a.files, a.stems))
    if a.stems:
        print(measure.stem_report(a.stems))


def cmd_master(a):
    from . import master, presets
    preset = presets.load(a.preset)
    ceiling = preset.CEILING if a.ceiling is None else a.ceiling
    name = a.name or Path(a.preset).stem.replace("_", "-")
    out = Path(a.out) if a.out else Path(a.split_input).resolve().parent.parent / "renders"
    master.render(a.stems_dir, a.split_input, out, preset, a.target, ceiling, name)


def default_work(folder):
    """./work/<album folder name>, printed so the agent knows where files went."""
    return Path("work") / Path(folder).resolve().name


def cmd_split(a):
    from . import separate
    separate.split(a.track, a.work or default_work(Path(a.track).resolve().parent), a.shifts, a.device)


def cmd_album(a):
    from . import album
    album.run(a.src_dir, a.target, a.work or default_work(a.src_dir), a.preset, a.shifts, a.device)


def cmd_abtest(a):
    from . import abtest
    abtest.serve(a.ref, a.versions, open_browser=not a.no_browser, port=a.port)


def cmd_plot(a):
    from . import plot
    plot.render(a.ref, a.remaster, a.out)


def cmd_export(a):
    from . import export
    export.run(a.renders, a.source, a.format, Path(a.out) if a.out else export.default_out(a.renders, a.format))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="got", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("analyze", help="loudness, dynamics, clipping and band balance of audio files")
    p.add_argument("files", nargs="*")
    p.add_argument("--stems", metavar="DIR",
                   help="also print each stem's share of the high bands, and a snare line for files of the stems' track")
    p.add_argument("--blocks", action="store_true", help="also print loudness per 5 s block (files, and stems)")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("master", help="render one track's stems through a preset at one or more loudness targets")
    p.add_argument("stems_dir", help="folder with drums/bass/vocals/other.wav")
    p.add_argument("split_input", help="the exact file the stems were split from (got split writes it)")
    p.add_argument("--preset", default="heavy-guitar", help="registered name or path to a preset .py")
    p.add_argument("--target", type=float, action="append", required=True, help="integrated LUFS; repeatable")
    p.add_argument("--ceiling", type=float, help="true-peak ceiling in dBTP (default: the preset's, -1.2)")
    p.add_argument("--name", help="label in the output filename (default: preset name)")
    p.add_argument("--out", help="output folder (default: renders/ next to the split input's folder)")
    p.set_defaults(func=cmd_master)

    def split_opts(p):
        p.add_argument("--work", help="work folder (default: ./work/<album folder name>)")
        p.add_argument("--shifts", type=int, default=2, help="Demucs random shifts (default 2; N times slower)")
        p.add_argument("--device", help="torch device (default: cuda if available, else cpu; never mps)")

    p = sub.add_parser("split", help="Demucs 4-stem split of one track (skips if the stems exist)")
    p.add_argument("track")
    split_opts(p)
    p.set_defaults(func=cmd_split)

    p = sub.add_parser("album", help="one loudness shift for all tracks, then split + master each")
    p.add_argument("src_dir", help="folder of the album's source files")
    p.add_argument("--target", type=float, required=True, help="LUFS for the loudest track")
    p.add_argument("--preset", default="heavy-guitar", help="registered name or path to a preset .py")
    split_opts(p)
    p.set_defaults(func=cmd_album)

    p = sub.add_parser("abtest", help="serve a blind, level-matched A/B page on 127.0.0.1 (Ctrl-C to stop)")
    p.add_argument("versions", nargs="+", help="renders to compare")
    p.add_argument("--ref", required=True, help="the original, shown labelled as the reference")
    p.add_argument("--port", type=int, default=0, help="default: a random free port")
    p.add_argument("--no-browser", action="store_true", help="print the URL without opening a browser")
    p.set_defaults(func=cmd_abtest)

    p = sub.add_parser("plot", help="SVG of short-term loudness over time, original vs remaster")
    p.add_argument("remaster", help="the render to plot against the original")
    p.add_argument("--ref", required=True, help="the original")
    p.add_argument("--out", "-o", required=True, help="output .svg path")
    p.set_defaults(func=cmd_plot)

    from .export import FORMATS
    p = sub.add_parser("export", help="MP3/AAC (one gain, <= -2 dBTP) or 24-bit FLAC/ALAC/WAV, with the source "
                                      "tags and cover")
    p.add_argument("renders", nargs="+",
                   help="render .wav files, or folders with one render per track (e.g. <work>/renders/album)")
    p.add_argument("--source", required=True, help="folder of the original files (tags and cover come from here)")
    p.add_argument("--format", choices=list(FORMATS), required=True, help="the person's choice; one per run")
    p.add_argument("--out", help="default: <work>/export/<format>")
    p.set_defaults(func=cmd_export)

    a = ap.parse_args(argv)
    a.func(a)


if __name__ == "__main__":
    main()
