"""Blind, level-matched A/B in the browser. Every version is turned down to the quietest one, never up,
so "louder sounds better" can't decide the test. Served on 127.0.0.1 only; nothing is written to disk."""
import http.server
import json
import mimetypes
import shutil
import webbrowser
from pathlib import Path

import pyloudnorm as pyln

from .. import io

TEMPLATE = Path(__file__).with_name("ab_blind_template.html")


def match_gains(lufs):
    """Playback gain in dB per version so all match the quietest: always <= 0."""
    quietest = min(lufs)
    return [quietest - l for l in lufs]


def song_name(tags, path):
    """The title tag (any key case: FLAC has TITLE, MP3 title), else the file name without its extension."""
    title = next((str(v).strip() for k, v in tags.items() if k.lower() == "title"), "")
    return title or Path(path).stem


def serve(ref, others, open_browser=True, port=0):
    files = [Path(ref), *map(Path, others)]
    lufs = []
    for p in files:
        x, sr = io.decode(p)
        lufs.append(pyln.Meter(sr).integrated_loudness(x))
    versions = [{"url": f"/audio/{i}", "label": p.name, "lufs": round(l, 2), "gain_db": round(g, 2), "ref": i == 0}
                for i, (p, l, g) in enumerate(zip(files, lufs, match_gains(lufs)))]
    for v in versions:
        print(f"  {v['label']}: {v['lufs']} LUFS, plays at {v['gain_db']:+.2f} dB{' (reference)' if v['ref'] else ''}")
    data = json.dumps(versions).replace("</", "<\\/")  # a filename can't close the <script>
    song = json.dumps(song_name(io.probe(files[0])["format"].get("tags", {}), files[0])).replace("</", "<\\/")
    html = TEMPLATE.read_text().replace("__VERSIONS__", data).replace("__SONG__", song).encode()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.reply(200, "text/html; charset=utf-8", len(html))
                self.wfile.write(html)
                return
            i = self.path.removeprefix("/audio/")
            if not (i.isdigit() and int(i) < len(files)):
                self.reply(404, "text/plain", 0)
                return
            f = files[int(i)]
            self.reply(200, mimetypes.guess_type(f.name)[0] or "application/octet-stream", f.stat().st_size)
            with open(f, "rb") as fh:
                shutil.copyfileobj(fh, self.wfile)

        def reply(self, code, ctype, length):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def log_message(self, *args):
            pass

    with http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler) as srv:
        url = f"http://127.0.0.1:{srv.server_port}/"
        print(f"A/B page: {url}  (Ctrl-C to stop)", flush=True)
        if open_browser:
            webbrowser.open(url)
        srv.serve_forever()
