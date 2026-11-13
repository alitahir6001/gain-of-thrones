"""Before/after short-term loudness as a self-contained SVG, styled like the A/B page (walnut, brass, chart paper)."""
import math
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

from . import io, measure

W, H = 1200, 640
PAPER = (110, 168, 1140, 508)  # x0, y0, x1, y1
WINDOW = 3.0  # s: short-term frames before this are a partly filled window
MAX_POINTS = 900
SERIES_STYLE = [  # original, then remaster
    {"stroke": "#3b2414", "width": 2.2, "dash": "", "fill": None},
    {"stroke": "#a3392a", "width": 2.8, "dash": "", "fill": "#a3392a"},
]
MINUS = "−"


def axis_range(values, pad=1.0, step=3, min_span=12):
    """LUFS axis (lo, hi) on multiples of step: covers the 2nd percentile to the max, at least min_span wide."""
    v = np.asarray(values, float)
    lo = math.floor((np.percentile(v, 2) - pad) / step) * step
    hi = math.ceil((v.max() + pad) / step) * step
    if hi - lo < min_span:
        lo = hi - min_span
    return lo, hi


def time_step(dur):
    """Major x tick spacing in seconds: at most 10 ticks."""
    return next((s for s in (5, 10, 15, 30, 60, 120, 300) if dur / s <= 10), 600)


def curve(frames):
    """Short-term frames after the window fills, averaged into at most MAX_POINTS buckets: (t, S) arrays."""
    f = np.array([p for p in frames if p[0] >= WINDOW], float).reshape(-1, 2)
    k = max(1, math.ceil(len(f) / MAX_POINTS))
    n = len(f) // k * k
    return f[:n, 0].reshape(-1, k).mean(1), f[:n, 1].reshape(-1, k).mean(1)


def fmt_db(v, unit="", plus=False):
    s = f"{abs(v):.1f}"
    sign = MINUS if v < 0 else ("+" if plus and v > 0 else "")
    return f"{sign}{s}{' ' + unit if unit else ''}"


def fmt_time(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def svg(title, series):
    """series: [{"label", "I", "TP", "LRA", "S_max", "t", "S"}], original first. Returns the SVG text."""
    x0, y0, x1, y1 = PAPER
    dur = max(s["t"][-1] for s in series)
    lo, hi = axis_range(np.concatenate([s["S"] for s in series]))
    X = lambda t: x0 + (x1 - x0) * t / dur
    Y = lambda v: y1 - (y1 - y0) * (min(max(v, lo), hi) - lo) / (hi - lo)
    out = []
    a = out.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
      f'aria-label="Short-term loudness of {escape(title)}: original and remaster">')
    a(f"<title>{escape(title)}: short-term loudness, original vs remaster</title>")
    a("""<defs>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.003 0.11" numOctaves="4" seed="9"/>
<feColorMatrix values="0 0 0 0 0.16 0 0 0 0 0.07 0 0 0 0 0.02 0 0 0 1.6 -0.45"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7a4421"/><stop offset=".55" stop-color="#5a2f15"/><stop offset="1" stop-color="#4a2510"/></linearGradient>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#241b15"/><stop offset="1" stop-color="#15100c"/></linearGradient>
<pattern id="brushed" width="3" height="10" patternUnits="userSpaceOnUse"><rect width="1" height="10" fill="#ffebc8" fill-opacity=".02"/></pattern>
<radialGradient id="paper" cx=".5" cy="1.1" r="1"><stop offset="0" stop-color="#fbefd2"/><stop offset=".6" stop-color="#f2e2bf"/><stop offset="1" stop-color="#dcc497"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".32"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecca83"/><stop offset=".45" stop-color="#d4ab5f"/><stop offset="1" stop-color="#8f6a30"/></linearGradient>
<radialGradient id="screw" cx=".4" cy=".35" r=".6"><stop offset="0" stop-color="#e9d9b8"/><stop offset=".5" stop-color="#a68b62"/><stop offset="1" stop-color="#4d3d29"/></radialGradient>
<radialGradient id="lamp" cx=".5" cy="0" r=".8"><stop offset="0" stop-color="#ffbe6e" stop-opacity=".22"/><stop offset="1" stop-color="#ffbe6e" stop-opacity="0"/></radialGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a3392a" stop-opacity=".22"/><stop offset="1" stop-color="#a3392a" stop-opacity=".03"/></linearGradient>
""")
    a(f'<clipPath id="paperclip"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath></defs>')

    # Walnut frame, faceplate, lamp glow, screws
    a(f'<rect width="{W}" height="{H}" rx="22" fill="url(#wood)"/>')
    a(f'<rect width="{W}" height="{H}" rx="22" fill="#000" filter="url(#grain)"/>')
    a(f'<rect x="18" y="16" width="{W - 36}" height="{H - 32}" rx="12" fill="url(#panel)" stroke="#000" stroke-opacity=".6"/>')
    a(f'<rect x="18" y="16" width="{W - 36}" height="{H - 32}" rx="12" fill="url(#brushed)"/>')
    a(f'<rect x="18" y="16" width="{W - 36}" height="{H - 32}" rx="12" fill="url(#lamp)"/>')
    for cx, cy in ((34, 32), (W - 34, 32), (34, H - 32), (W - 34, H - 32)):
        a(f'<circle cx="{cx}" cy="{cy}" r="5" fill="url(#screw)" stroke="#000" stroke-opacity=".5"/>'
          f'<path d="M{cx - 3},{cy} h6" stroke="#3b2f22" stroke-width="1.2"/>')

    # Header
    mono = 'font-family="ui-monospace, SF Mono, SFMono-Regular, Menlo, Consolas, monospace"'
    serif = 'font-family="Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif"'
    a(f'<text x="{x0}" y="62" {mono} font-size="13" font-weight="600" letter-spacing="3.6" fill="#d4ab5f">'
      "GAIN OF THRONES · LOUDNESS CHART</text>")
    a(f'<text x="{x0}" y="102" {serif} font-size="34" font-weight="600" fill="#fff1d8">{escape(title)}</text>')
    a(f'<text x="{x0}" y="134" {serif} font-size="18" font-style="italic" fill="#ffb84d">'
      "Short-term loudness (3 s window), original and remaster</text>")
    # Headline readouts: remaster minus original
    rx = x1
    for name, d in (("Δ LRA", series[1]["LRA"] - series[0]["LRA"]), ("Δ LOUDNESS", series[1]["I"] - series[0]["I"])):
        txt = fmt_db(d, "LU", plus=True)
        w = 30 + 15.5 * len(txt)
        rx -= w
        a(f'<rect x="{rx:.0f}" y="44" width="{w:.0f}" height="22" rx="3" fill="url(#brass)"/>'
          f'<text x="{rx + w / 2:.1f}" y="60" text-anchor="middle" {mono} font-size="12" font-weight="700" '
          f'letter-spacing="2.4" fill="#2b1a08">{name}</text>'
          f'<rect x="{rx:.0f}" y="72" width="{w:.0f}" height="50" rx="5" fill="#0d0806" stroke="#3a2516"/>'
          f'<text x="{rx + w / 2:.1f}" y="107" text-anchor="middle" {mono} font-size="26" font-weight="700" '
          f'fill="#ffb84d">{txt}</text>')
        rx -= 16

    # Chart paper in a dark bezel
    a(f'<rect x="{x0 - 6}" y="{y0 - 6}" width="{x1 - x0 + 12}" height="{y1 - y0 + 12}" rx="8" fill="#2a150a" '
      'stroke="#5a3418"/>')
    a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="3" fill="url(#paper)"/>')
    tstep = time_step(dur)
    grid = []
    for v in range(lo, hi + 1):
        major = (v - lo) % 3 == 0
        grid.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#8a3b24" '
                    f'stroke-opacity="{".42" if major else ".14"}" stroke-width="{1 if major else .7}"/>')
        if major:
            a(f'<text x="{x0 - 14}" y="{Y(v) + 4:.1f}" text-anchor="end" {mono} font-size="14" fill="#d4ab5f">'
              f"{fmt_db(v).removesuffix('.0')}</text>")
    minor = tstep / 5
    for i in range(int(dur / minor) + 1):
        t = i * minor
        major = i % 5 == 0
        grid.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{y0}" y2="{y1}" stroke="#8a3b24" '
                    f'stroke-opacity="{".42" if major else ".14"}" stroke-width="{1 if major else .7}"/>')
        if major:
            a(f'<text x="{X(t):.1f}" y="{y1 + 26}" text-anchor="middle" {mono} font-size="14" fill="#d4ab5f">'
              f"{fmt_time(t)}</text>")
    a('<g clip-path="url(#paperclip)">' + "".join(grid))

    # Curves, remaster on top, each with its integrated loudness as a dashed line
    for s, st in zip(series, SERIES_STYLE):
        pts = " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in zip(s["t"], s["S"]))
        if st["fill"]:
            a(f'<path d="M{X(s["t"][0]):.1f},{y1} L{pts} L{X(s["t"][-1]):.1f},{y1} Z" fill="url(#area)"/>')
        a(f'<line x1="{x0}" x2="{x1}" y1="{Y(s["I"]):.1f}" y2="{Y(s["I"]):.1f}" stroke="{st["stroke"]}" '
          'stroke-width="1.4" stroke-dasharray="7 6" stroke-opacity=".75"/>')
        a(f'<polyline points="{pts}" fill="none" stroke="{st["stroke"]}" stroke-width="{st["width"]}" '
          'stroke-linejoin="round" stroke-linecap="round"/>')
    for s, st in zip(series, SERIES_STYLE):  # tags last, so no curve covers them
        ty = Y(s["I"])
        a(f'<rect x="{x1 - 146}" y="{ty - 12:.1f}" width="138" height="22" rx="3" fill="#f6ecd6" '
          f'stroke="{st["stroke"]}" stroke-opacity=".6"/>'
          f'<text x="{x1 - 77}" y="{ty + 4.5:.1f}" text-anchor="middle" {mono} font-size="13" font-weight="700" '
          f'fill="{st["stroke"]}">I {fmt_db(s["I"], "LUFS")}</text>')
    a("</g>")
    a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{(y1 - y0) * .4:.0f}" fill="url(#glass)"/>')

    # Legend: a swatch, the name and amber readouts per series
    ly = 574
    for i, (s, st) in enumerate(zip(series, SERIES_STYLE)):
        lx = x0 + i * (x1 - x0) / 2
        a(f'<rect x="{lx}" y="{ly - 18}" width="40" height="24" rx="3" fill="url(#paper)" stroke="#2a150a" stroke-width="2"/>'
          f'<line x1="{lx + 7}" x2="{lx + 33}" y1="{ly - 6}" y2="{ly - 6}" stroke="{st["stroke"]}" '
          f'stroke-width="{st["width"] + .6}" stroke-linecap="round"/>')
        a(f'<text x="{lx + 52}" y="{ly}" {serif} font-size="20" font-weight="600" fill="#f3e6cf">'
          f'{escape(s["label"])}</text>')
        rx = lx + 160
        for txt in (f'TP {fmt_db(s["TP"], "dBTP", plus=True)}', f'LRA {s["LRA"]:.1f} LU'):
            w = 12 + 9 * len(txt)
            a(f'<rect x="{rx}" y="{ly - 19}" width="{w:.0f}" height="26" rx="4" fill="#0d0806" stroke="#3a2516"/>'
              f'<text x="{rx + w / 2:.1f}" y="{ly - 1}" text-anchor="middle" {mono} font-size="15" font-weight="600" '
              f'fill="#ffb84d">{txt}</text>')
            rx += w + 10
    a(f'<text x="{x1}" y="{H - 30}" text-anchor="end" {mono} font-size="12" letter-spacing="1.2" fill="#8c7458">'
      "measured with ffmpeg ebur128 · EBU R128</text>")
    a("</svg>")
    return "\n".join(out)


def render(ref, remaster, out, labels=("Original", "Remaster")):
    from .abtest import song_name
    series = []
    for path, label in zip((ref, remaster), labels):
        m = measure.ebur128(path)
        t, s = curve(m["frames"])
        if not len(t):
            raise SystemExit(f"{Path(path).name}: under {WINDOW:.0f} s, too short to plot short-term loudness")
        series.append({"label": label, **{k: m[k] for k in ("I", "TP", "LRA", "S_max")}, "t": t, "S": s})
        print(f"  {label}: {Path(path).name}: I {m['I']:.1f} LUFS | TP {m['TP']:+.1f} dBTP | LRA {m['LRA']:.1f} LU "
              f"| max S {m['S_max']:.1f} LUFS")
    title = song_name(io.probe(ref)["format"].get("tags", {}), ref)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg(title, series))
    print(f"plot: {out}")
    return out
