"""Blind, level-matched A/B in the browser. Every version is turned down to the quietest one, never up,
so "louder sounds better" can't decide the test. Served on 127.0.0.1 only. The server shuffles the slots and
keeps the slot-to-file map until Reveal, so the page never holds a file name it could show early. The person's
pick is appended to <work>/abtest-picks.tsv; nothing else is written."""
import http.server
import json
import mimetypes
import random
import shutil
import threading
import time
import webbrowser
from pathlib import Path

import pyloudnorm as pyln

from .. import io

TEMPLATE = Path(__file__).with_name("ab_blind_template.html")
MAX_VERSIONS = 6  # renders per round, plus the reference: each decodes to ~110 MB in the browser
LOG_NAME = "abtest-picks.tsv"
LOG_HEADER = "time\tref\twinner_slot\twinner\tslots (slot gain_dB path)\n"


def match_gains(lufs):
    """Playback gain in dB per version so all match the quietest: always <= 0."""
    quietest = min(lufs)
    return [quietest - l for l in lufs]


def song_name(tags, path):
    """The title tag (any key case: FLAC has TITLE, MP3 title), else the file name without its extension."""
    title = next((str(v).strip() for k, v in tags.items() if k.lower() == "title"), "")
    return title or Path(path).stem


def slot_name(k):
    return "Original" if k == 0 else chr(64 + k)


def work_folder(ref, versions, work=None):
    """--work, else the folder above the first version's renders/ folder, else ./work/<ref's album folder>."""
    if work:
        return Path(work)
    for v in versions:
        d = Path(v).resolve()
        hit = next((p.parent for p in d.parents if p.name == "renders"), None)
        if hit:
            return hit
    return Path("work") / Path(ref).resolve().parent.name


def track_renders(work, ref):
    """Renders of the reference's track: <work>/renders/<track>_*.wav and renders/album/<track>_*.wav."""
    prefix = Path(ref).stem + "_"
    dirs = [Path(work) / "renders", Path(work) / "renders" / "album"]
    return [p for d in dirs if d.is_dir() for p in io.audio_files(d) if p.name.startswith(prefix)]


class Session:
    """The server's state: the files on offer and the current round. Every method is safe to call from
    concurrent request threads. Errors are (http_code, message) via RoundError."""

    def __init__(self, ref, versions=(), candidates=None, work=".", rng=random):
        self.ref = Path(ref).resolve()
        self.song = song_name(io.probe(self.ref)["format"].get("tags", {}), self.ref)
        self.candidates = [Path(c).resolve() for c in candidates] if candidates is not None else None
        self.log = Path(work) / LOG_NAME
        self.rng = rng
        self.lock = threading.Lock()
        self.lufs = {}
        self.round = None
        self.round_id = 0
        if versions:
            self.start([Path(v).resolve() for v in versions])

    def measure(self, p):
        if p not in self.lufs:
            x, sr = io.decode(p)
            self.lufs[p] = pyln.Meter(sr).integrated_loudness(x)
        return self.lufs[p]

    def start(self, versions):
        if not 1 <= len(versions) <= MAX_VERSIONS:
            raise RoundError(400, f"choose 1 to {MAX_VERSIONS} renders, not {len(versions)}")
        files = [self.ref, *versions]
        lufs = [self.measure(p) for p in files]
        gains = match_gains(lufs)
        blind = list(range(1, len(files)))
        self.rng.shuffle(blind)
        order = [0, *blind]  # slot k plays files[order[k]]; the reference stays in slot 0
        self.round_id += 1
        self.round = {"files": files, "order": order, "lufs": lufs, "gains": gains, "picked": None, "revealed": False}
        print(f"round {self.round_id}:")
        for p, l, g in zip(files, lufs, gains):
            print(f"  {p.name}: {l:.2f} LUFS, plays at {g:+.2f} dB{' (reference)' if p == self.ref else ''}")
        print(flush=True)

    def choose(self, indices):
        """Start a round from candidate indices (the person's ticks in the chooser)."""
        with self.lock:
            if self.candidates is None:
                raise RoundError(409, "this round's files were fixed on the command line")
            if not all(isinstance(i, int) and 0 <= i < len(self.candidates) for i in indices) \
                    or len(set(indices)) != len(indices):
                raise RoundError(400, "unknown or repeated render")
            self.start([self.candidates[i] for i in indices])

    def reset(self):
        with self.lock:
            if self.candidates is None:
                raise RoundError(409, "this round's files were fixed on the command line")
            self.round = None

    def slot_file(self, k):
        r = self.round
        return r["files"][r["order"][k]] if r and 0 <= k < len(r["order"]) else None

    def pick(self, k):
        with self.lock:
            r = self.round
            if r is None:
                raise RoundError(409, "no round in progress")
            if r["revealed"]:
                raise RoundError(409, "the files are revealed; a pick now would not be blind")
            if r["picked"] is not None:
                raise RoundError(409, f"slot {slot_name(r['picked'])} is already picked")
            if not (isinstance(k, int) and 0 <= k < len(r["order"])):
                raise RoundError(400, "unknown slot")
            r["picked"] = k
            winner = self.slot_file(k)
            print(f"pick: slot {slot_name(k)} = {winner}", flush=True)
            slots = " | ".join(f"{slot_name(j)} {r['gains'][i]:+.2f} {r['files'][i]}" for j, i in enumerate(r["order"]))
            new = not self.log.exists()
            self.log.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log, "a") as fh:
                fh.write((LOG_HEADER if new else "") +
                         f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{self.ref}\t{slot_name(k)}\t{winner}\t{slots}\n")

    def reveal(self):
        with self.lock:
            if self.round is None:
                raise RoundError(409, "no round in progress")
            self.round["revealed"] = True

    def state(self):
        """What the page may know: never a file name of a blind slot before Reveal."""
        with self.lock:
            r = self.round
            s = {"song": self.song,
                 "chooser": self.candidates is not None,
                 "renders": [p.name for p in self.candidates] if self.candidates is not None and not r else [],
                 "max": MAX_VERSIONS, "round": None}
            if r:
                s["round"] = {
                    "id": self.round_id, "picked": r["picked"], "revealed": r["revealed"],
                    "slots": [{"name": slot_name(k), "url": f"/audio/{k}?r={self.round_id}",
                               "lufs": round(r["lufs"][i], 2), "gain_db": round(r["gains"][i], 2),
                               **({"file": r["files"][i].name} if r["revealed"] else {})}
                              for k, i in enumerate(r["order"])]}
            return s


class RoundError(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code


def make_server(session, port=0):
    template = TEMPLATE.read_text()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                data = json.dumps(session.state()).replace("</", "<\\/")  # a filename can't close the <script>
                return self.send(200, "text/html; charset=utf-8", template.replace("__STATE__", data).encode())
            i = path.removeprefix("/audio/")
            f = session.slot_file(int(i)) if i.isdigit() else None
            if f is None:
                return self.send(404, "text/plain", b"")
            self.head(200, mimetypes.guess_type(f.name)[0] or "application/octet-stream", f.stat().st_size)
            with open(f, "rb") as fh:
                shutil.copyfileobj(fh, self.wfile)

        def do_POST(self):
            actions = {"/pick": lambda b: session.pick(b.get("slot")), "/reveal": lambda b: session.reveal(),
                       "/round": lambda b: session.choose(b.get("renders", [])), "/reset": lambda b: session.reset()}
            if self.path not in actions:
                return self.send(404, "text/plain", b"")
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                actions[self.path](body if isinstance(body, dict) else {})
            except RoundError as e:
                return self.send(e.code, "application/json", json.dumps({"error": str(e)}).encode())
            except ValueError:
                return self.send(400, "application/json", b'{"error": "bad request"}')
            self.send(200, "application/json", json.dumps(session.state()).encode())

        def send(self, code, ctype, body):
            self.head(code, ctype, len(body))
            self.wfile.write(body)

        def head(self, code, ctype, length):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def log_message(self, *args):
            pass

    return http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)


def serve(ref, versions, work=None, open_browser=True, port=0):
    work = work_folder(ref, versions, work)
    candidates = None
    if not versions:
        candidates = track_renders(work, ref)
        if not candidates:
            raise SystemExit(f"no renders of {Path(ref).stem} in {work}/renders; pass the files or --work")
        print(f"{len(candidates)} renders of {Path(ref).stem} to choose from in {work}/renders")
    if len(versions) > MAX_VERSIONS:
        raise SystemExit(f"at most {MAX_VERSIONS} versions per round (the page decodes every file into memory)")
    session = Session(ref, versions, candidates, work)
    with make_server(session, port) as srv:
        url = f"http://127.0.0.1:{srv.server_port}/"
        print(f"A/B page: {url}  (Ctrl-C to stop)\npicks log: {session.log}", flush=True)
        if open_browser:
            webbrowser.open(url)
        srv.serve_forever()
