"""Blind, level-matched A/B in the browser. Every version is turned down to the quietest one, never up,
so "louder sounds better" can't decide the test. Served on 127.0.0.1 only. The server shuffles the slots and
keeps the slot-to-file map until Reveal, so the page never holds a file name it could show early. Every pick and
undo is appended to <work>/abtest-picks.tsv, marked blind or after Reveal; nothing else is written. One server can
serve every song of an album (--source), each with its own round."""
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
LOG_HEADER = "time\tevent\tsong\tround\tblind\tref\twinner_slot\twinner\tslots (slot gain_dB path)\n"


def match_gains(lufs):
    """Playback gain in dB per version so all match the quietest: always <= 0."""
    quietest = min(lufs)
    return [quietest - l for l in lufs]


def song_name(tags, path):
    """The title tag (any key case: FLAC has TITLE, MP3 title), else the file name without its extension."""
    title = next((str(v).strip() for k, v in tags.items() if k.lower() == "title"), "")
    return title or Path(path).stem



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



def open_log(log):
    """Append handle for the picks log. A log with another header (the v1 schema) is renamed first, so one file
    never mixes two schemas."""
    log = Path(log)
    if log.exists():
        with open(log) as fh:
            first = fh.readline()
        if first != LOG_HEADER:
            old = next(q for n in range(1, 1000)
                       if not (q := log.with_name(log.stem + (".v1" if n == 1 else f".v1-{n}") + log.suffix)).exists())
            log.rename(old)
            print(f"picks log had an older header; moved it to {old}", flush=True)
    new = not log.exists()
    log.parent.mkdir(parents=True, exist_ok=True)
    fh = open(log, "a")
    if new:
        fh.write(LOG_HEADER)
    return fh


def render_files(work):
    """Audio files in <work>/renders/ and <work>/renders/album/."""
    dirs = [Path(work) / "renders", Path(work) / "renders" / "album"]
    return [p for d in dirs if d.is_dir() for p in io.audio_files(d)]


def track_renders(work, track, tracks=()):
    """Renders of one track, paired as got export pairs them (io.track_of) among the track and its siblings."""
    return [p for p in render_files(work) if io.track_of(p.name, {track, *tracks}) == track]


class Song:
    """One track on offer: its references ("cd", and "album" when there is an album render), the renders to
    choose from (None: fixed on the command line) and its current round."""

    def __init__(self, refs, candidates=None, track=None):
        self.refs = {k: Path(p).resolve() for k, p in refs.items()}
        first = self.refs["cd"]
        self.track = track or first.stem
        self.name = song_name(io.probe(first)["format"].get("tags", {}), first)
        self.candidates = [Path(c).resolve() for c in candidates] if candidates is not None else None
        self.ref_kind = "cd"  # the next round's reference; the page's toggle sets it
        self.round = None

    def status(self):
        r = self.round
        return "none" if r is None else "picked" if r["picked"] is not None else "open"


class Library:
    """The server's state: every song on offer and each one's current round. Methods take the song's index and
    are safe to call from concurrent request threads. Errors are (http_code, message) via RoundError."""

    def __init__(self, songs, work=".", rng=random):
        self.songs = list(songs)
        self.log = Path(work) / LOG_NAME
        self.rng = rng
        self.lock = threading.Lock()
        self.lufs = {}
        self.rounds = 0
        self.run = time.strftime("%Y%m%dT%H%M%S")  # with the round number, names a round uniquely across restarts

    @classmethod
    def for_ref(cls, ref, versions=(), candidates=None, work=".", rng=random):
        """One song with the reference from --ref: a fixed round of versions, or a chooser of candidates."""
        lib = cls([Song({"cd": ref}, candidates)], work, rng)
        if versions:
            lib.start(lib.songs[0], [Path(v).resolve() for v in versions])
        return lib

    def song(self, i):
        if not (isinstance(i, int) and 0 <= i < len(self.songs)):
            raise RoundError(400, "unknown song")
        return self.songs[i]

    def measure(self, p):
        if p not in self.lufs:
            x, sr = io.decode(p)
            self.lufs[p] = pyln.Meter(sr).integrated_loudness(x)
        return self.lufs[p]

    def start(self, song, versions):
        if not 1 <= len(versions) <= MAX_VERSIONS:
            raise RoundError(400, f"choose 1 to {MAX_VERSIONS} renders, not {len(versions)}")
        files = [song.refs[song.ref_kind], *versions]
        lufs = [self.measure(p) for p in files]
        gains = match_gains(lufs)
        blind = list(range(1, len(files)))
        self.rng.shuffle(blind)
        self.rounds += 1
        song.round = {"id": self.rounds, "files": files, "order": [0, *blind],  # slot k plays files[order[k]]
                      "names": ["Album" if song.ref_kind == "album" else "Original",
                                *(chr(64 + k) for k in range(1, len(files)))],
                      "lufs": lufs, "gains": gains, "picked": None, "pick_blind": None, "revealed": False}
        print(f"round {self.rounds}, {song.track}:")
        for i, (p, l, g) in enumerate(zip(files, lufs, gains)):  # by index: a version may be the reference's file
            print(f"  {p.name}: {l:.2f} LUFS, plays at {g:+.2f} dB{' (reference)' if i == 0 else ''}")
        print(flush=True)

    def choose(self, i, indices, ref="cd"):
        """Start a round from candidate indices (the person's ticks in the chooser) against the chosen reference."""
        with self.lock:
            song = self.song(i)
            if song.candidates is None:
                raise RoundError(409, "this round's files were fixed on the command line")
            if ref not in song.refs:
                raise RoundError(400, f"no {ref} reference for {song.track}")
            if not isinstance(indices, list) or len(set(indices)) != len(indices) \
                    or not all(isinstance(k, int) and 0 <= k < len(song.candidates) for k in indices):
                raise RoundError(400, "unknown or repeated render")
            song.ref_kind = ref
            self.start(song, [song.candidates[k] for k in indices])

    def reset(self, i):
        with self.lock:
            song = self.song(i)
            if song.candidates is None:
                raise RoundError(409, "this round's files were fixed on the command line")
            song.round = None

    def slot_file(self, i, k):
        r = self.songs[i].round if isinstance(i, int) and 0 <= i < len(self.songs) else None
        return r["files"][r["order"][k]] if r and 0 <= k < len(r["order"]) else None

    def current(self, i):
        song = self.song(i)
        if song.round is None:
            raise RoundError(409, "no round in progress")
        return song, song.round

    def pick(self, i, k):
        with self.lock:
            song, r = self.current(i)
            if r["picked"] is not None:
                raise RoundError(409, f"slot {r['names'][r['picked']]} is already picked; undo it first")
            if not (isinstance(k, int) and 0 <= k < len(r["order"])):
                raise RoundError(400, "unknown slot")
            r["picked"], r["pick_blind"] = k, not r["revealed"]
            winner = self.slot_file(i, k)
            print(f"pick: {song.track} round {r['id']}: slot {r['names'][k]} = {winner} "
                  f"({'blind' if r['pick_blind'] else 'after reveal'})", flush=True)
            self.write_log(song, "pick", r["names"][k], winner)

    def undo(self, i):
        with self.lock:
            song, r = self.current(i)
            if r["picked"] is None:
                raise RoundError(409, "no pick to undo")
            print(f"undo: {song.track} round {r['id']}: slot {r['names'][r['picked']]}", flush=True)
            r["picked"] = r["pick_blind"] = None
            self.write_log(song, "undo", "-", "-")

    def write_log(self, song, event, slot, winner):
        r = song.round
        slots = " | ".join(f"{r['names'][j]} {r['gains'][f]:+.2f} {r['files'][f]}" for j, f in enumerate(r["order"]))
        row = [time.strftime("%Y-%m-%dT%H:%M:%S"), event, song.track, f"{self.run}-{r['id']}",
               "no" if r["revealed"] else "yes", r["files"][0], slot, winner, slots]
        with open_log(self.log) as fh:
            fh.write("\t".join(map(str, row)) + "\n")

    def reveal(self, i):
        with self.lock:
            self.current(i)[1]["revealed"] = True

    def state(self, i):
        """What the page may know about song i: never a file name during its round before Reveal, and nothing of
        the other songs but their names and status."""
        with self.lock:
            song = self.song(i)
            r = song.round
            s = {"index": i, "song": song.name,
                 "songs": [{"name": x.name, "status": x.status()} for x in self.songs],
                 "chooser": song.candidates is not None, "max": MAX_VERSIONS, "round": None,
                 "renders": [p.name for p in song.candidates] if song.candidates is not None and not r else [],
                 "refs": {k: p.name for k, p in song.refs.items()} if not r else {}, "ref": song.ref_kind}
            if r:
                s["round"] = {
                    "id": r["id"], "picked": r["picked"], "blind": r["pick_blind"], "revealed": r["revealed"],
                    "slots": [{"name": r["names"][k], "url": f"/audio/{i}/{k}?r={r['id']}",
                               "lufs": round(r["lufs"][f], 2), "gain_db": round(r["gains"][f], 2),
                               **({"file": r["files"][f].name} if r["revealed"] else {})}
                              for k, f in enumerate(r["order"])]}
            return s


class RoundError(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code


def album_songs(source, work):
    """A Song for every source file with renders in <work>/renders/ or renders/album/. Its references: the source
    file ("cd") and, if there is one, the newest renders/album/<track>_* ("album")."""
    tracks = {s.stem: s for s in io.audio_files(source)}
    by_track = {}
    for p in render_files(work):
        if (t := io.track_of(p.name, tracks)) is not None:
            by_track.setdefault(t, []).append(p)
    songs = []
    for t, renders in sorted(by_track.items()):
        refs = {"cd": tracks[t]}
        album = sorted((p for p in renders if p.parent.name == "album"), key=lambda p: p.stat().st_mtime)
        if album:
            refs["album"] = album[-1]
            if len(album) > 1:
                print(f"{t}: {len(album)} album renders; the album reference is the newest, {album[-1].name}")
        songs.append(Song(refs, renders, t))
    if not songs:
        raise SystemExit(f"no renders in {work}/renders match a file in {source}; check --work")
    return songs


def make_server(library, port=0):
    template = TEMPLATE.read_text()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            path, _, query = self.path.partition("?")
            if path == "/":
                q = dict(x.partition("=")[::2] for x in query.split("&") if x)
                i = int(q["song"]) if q.get("song", "").isdigit() and int(q["song"]) < len(library.songs) else 0
                data = json.dumps(library.state(i)).replace("</", "<\\/")  # a filename can't close the <script>
                return self.send(200, "text/html; charset=utf-8", template.replace("__STATE__", data).encode())
            parts = path.removeprefix("/audio/").split("/")
            f = library.slot_file(int(parts[0]), int(parts[1])) \
                if len(parts) == 2 and all(x.isdigit() for x in parts) else None
            if f is None:
                return self.send(404, "text/plain", b"")
            self.head(200, mimetypes.guess_type(f.name)[0] or "application/octet-stream", f.stat().st_size)
            with open(f, "rb") as fh:
                shutil.copyfileobj(fh, self.wfile)

        def do_POST(self):
            actions = {"/pick": lambda i, b: library.pick(i, b.get("slot")),
                       "/undo": lambda i, b: library.undo(i),
                       "/reveal": lambda i, b: library.reveal(i),
                       "/round": lambda i, b: library.choose(i, b.get("renders", []), b.get("ref", "cd")),
                       "/reset": lambda i, b: library.reset(i)}
            if self.path not in actions:
                return self.send(404, "text/plain", b"")
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                body = body if isinstance(body, dict) else {}
                i = body.get("song", 0)
                actions[self.path](i, body)
                state = library.state(i)
            except RoundError as e:
                return self.send(e.code, "application/json", json.dumps({"error": str(e)}).encode())
            except ValueError:
                return self.send(400, "application/json", b'{"error": "bad request"}')
            self.send(200, "application/json", json.dumps(state).encode())

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


def serve(ref=None, versions=(), work=None, source=None, open_browser=True, port=0):
    """--ref: one song (fixed versions, or a chooser of its renders). --source: every song of the album folder
    that has renders in the work folder."""
    if source:
        work = Path(work) if work else Path("work") / Path(source).resolve().name
        library = Library(album_songs(source, work), work)
        print(f"{len(library.songs)} songs with renders in {work}/renders")
    else:
        work = work_folder(ref, versions, work)
        candidates = None
        if not versions:
            siblings = [p.stem for p in io.audio_files(Path(ref).resolve().parent)]
            candidates = track_renders(work, Path(ref).stem, siblings)
            if not candidates:
                raise SystemExit(f"no renders of {Path(ref).stem} in {work}/renders; pass the files or --work")
            print(f"{len(candidates)} renders of {Path(ref).stem} to choose from in {work}/renders")
        if len(versions) > MAX_VERSIONS:
            raise SystemExit(f"at most {MAX_VERSIONS} versions per round (the page decodes every file into memory)")
        library = Library.for_ref(ref, versions, candidates, work)
    with make_server(library, port) as srv:
        url = f"http://127.0.0.1:{srv.server_port}/"
        print(f"A/B page: {url}  (Ctrl-C to stop)\npicks log: {library.log}", flush=True)
        if open_browser:
            webbrowser.open(url)
        srv.serve_forever()
