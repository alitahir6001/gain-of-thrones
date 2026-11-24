import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from gain_of_thrones.abtest import (LOG_HEADER, LOG_NAME, MAX_VERSIONS, Session, make_server, match_gains, song_name, track_renders,
                                    work_folder)


def test_song_name_prefers_title_tag_in_any_case():
    assert song_name({"TITLE": " Cattle Mutilation "}, "x/02 Cattle Mutilation.flac") == "Cattle Mutilation"
    assert song_name({"artist": "A", "title": "Freaks"}, "x/03 Freaks.mp3") == "Freaks"


def test_song_name_falls_back_to_file_name():
    assert song_name({}, "Freaks [EP]/02 Cattle Mutilation.flac") == "02 Cattle Mutilation"
    assert song_name({"title": "  "}, "Freaks [EP]/02 Cattle Mutilation.flac") == "02 Cattle Mutilation"


def test_level_match_only_turns_down():
    lufs = [-11.64, -10.82, -9.52, -12.3]
    g = match_gains(lufs)
    assert max(g) == 0 and all(x <= 0 for x in g)
    assert g[lufs.index(min(lufs))] == 0  # the quietest plays as is
    assert len({round(l + x, 9) for l, x in zip(lufs, g)}) == 1  # all land at the same loudness


SR = 44100


def tone(path, db, freq=440):
    t = np.arange(SR) / SR
    sf.write(path, np.stack([np.sin(2 * np.pi * freq * t)] * 2, 1) * 10 ** (db / 20), SR, subtype="PCM_24")
    return path


@pytest.fixture
def album(tmp_path):
    """album/01 Tone.wav, and work/renders/ with two renders of it at different levels plus another track's."""
    (tmp_path / "album").mkdir()
    ren = tmp_path / "work" / "renders"
    (ren / "album").mkdir(parents=True)
    ref = tone(tmp_path / "album" / "01 Tone.wav", -20)
    a = tone(ren / "01 Tone_v1_-10LUFS.wav", -12, 550)
    b = tone(ren / "01 Tone_v2_-9LUFS.wav", -10, 660)
    c = tone(ren / "album" / "01 Tone_heavy-guitar_-10LUFS.wav", -11, 770)
    tone(ren / "02 Other_v1_-10LUFS.wav", -12)
    return ref, [a, b, c], tmp_path / "work"


@pytest.fixture
def server():
    srvs = []

    def start(session):
        srv = make_server(session)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        srvs.append(srv)
        return f"http://127.0.0.1:{srv.server_port}"

    yield start
    for s in srvs:
        s.shutdown()
        s.server_close()


def post(url, body=None):
    req = urllib.request.Request(url, json.dumps(body or {}).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def get(url):
    with urllib.request.urlopen(url) as r:
        return r.read()


def test_work_folder_and_track_renders(album):
    ref, (a, b, c), work = album
    assert work_folder(ref, [a]) == work.resolve()
    assert work_folder(ref, [], "elsewhere") == Path("elsewhere")
    assert work_folder(ref, []) == Path("work") / "album"
    assert track_renders(work, ref) == [a, b, c]  # not 02 Other's render


def test_page_hides_file_names_until_reveal(album, server):
    ref, versions, work = album
    url = server(Session(ref, versions[:2], work=work))
    page = get(url + "/").decode()
    assert all(v.name not in page for v in versions[:2])
    code, s = post(url + "/reveal")
    assert code == 200 and {x["file"] for x in s["round"]["slots"][1:]} == {v.name for v in versions[:2]}
    assert versions[0].name in get(url + "/").decode()  # after reveal a reload shows them


def rows(work):
    header, *rest = (work / LOG_NAME).read_text().splitlines()
    assert header == LOG_HEADER.rstrip("\n")
    return [dict(zip([h.split(" ")[0] for h in header.split("\t")], r.split("\t"))) for r in rest]


def test_pick_prints_and_logs_the_blind_file(album, server, capsys):
    ref, versions, work = album
    session = Session(ref, versions[:2], work=work)
    url = server(session)
    winner = session.slot_file(2)
    assert get(url + "/audio/2") == winner.read_bytes()  # the slot plays the file that gets logged

    code, s = post(url + "/pick", {"slot": 2})
    assert code == 200 and s["round"]["picked"] == 2 and s["round"]["blind"] is True
    assert f"pick: 01 Tone round 1: slot B = {winner} (blind)" in capsys.readouterr().out
    [row] = rows(work)
    assert (row["event"], row["song"], row["blind"], row["ref"], row["winner_slot"], row["winner"]) == \
        ("pick", "01 Tone", "yes", str(ref.resolve()), "B", str(winner))
    for k, name in enumerate(["Original", "A", "B"]):
        assert f"{name} {session.round['gains'][session.round['order'][k]]:+.2f} {session.slot_file(k)}" in row["slots"]
    assert "Original +0.00" in row["slots"]  # the -20 dB reference is the quietest, so it plays as is

    code, s = post(url + "/pick", {"slot": 1})
    assert code == 409 and "undo it first" in s["error"]  # one current pick per round
    assert len(rows(work)) == 1


def test_pick_after_reveal_is_logged_not_blind(album, server, capsys):
    ref, versions, work = album
    session = Session(ref, versions[:2], work=work)
    url = server(session)
    assert post(url + "/reveal")[0] == 200
    code, s = post(url + "/pick", {"slot": 1})
    assert code == 200 and s["round"]["blind"] is False
    assert f"slot A = {session.slot_file(1)} (after reveal)" in capsys.readouterr().out
    assert [(r["event"], r["blind"], r["winner_slot"]) for r in rows(work)] == [("pick", "no", "A")]


def test_undo_appends_a_row_and_allows_a_new_pick(album, server, capsys):
    ref, versions, work = album
    session = Session(ref, versions[:2], work=work)
    url = server(session)
    assert post(url + "/undo")[0] == 409  # nothing to undo yet
    post(url + "/pick", {"slot": 1})
    code, s = post(url + "/undo")
    assert code == 200 and s["round"]["picked"] is None
    assert "undo: 01 Tone round 1: slot A" in capsys.readouterr().out
    post(url + "/reveal")
    post(url + "/pick", {"slot": 2})
    log = rows(work)
    assert [(r["event"], r["blind"], r["winner_slot"], r["winner"]) for r in log] == [
        ("pick", "yes", "A", str(session.slot_file(1))), ("undo", "yes", "-", "-"),
        ("pick", "no", "B", str(session.slot_file(2)))]
    assert len({r["round"] for r in log}) == 1  # the last row of the round is the current pick


def test_old_log_is_moved_aside(album):
    ref, versions, work = album
    (work / LOG_NAME).write_text("time\tref\twinner_slot\twinner\tslots (slot gain_dB path)\nold row\n")
    session = Session(ref, versions[:1], work=work)
    session.pick(1)
    assert (work / "abtest-picks.v1.tsv").read_text().endswith("old row\n")
    assert len(rows(work)) == 1


def test_bad_slot_is_refused(album, server):
    ref, versions, work = album
    url = server(Session(ref, versions[:1], work=work))
    assert post(url + "/pick", {"slot": 5})[0] == 400
    assert post(url + "/pick", {"slot": "A"})[0] == 400
    assert post(url + "/pick", {"slot": 1})[0] == 200  # a refused pick doesn't use up the round


def test_chooser_starts_a_blind_round_of_the_chosen_renders(album, server):
    ref, versions, work = album
    session = Session(ref, candidates=track_renders(work, ref), work=work)
    url = server(session)
    assert all(v.name in get(url + "/").decode() for v in versions)  # names are fine before the round
    assert post(url + "/pick", {"slot": 1})[0] == 409  # no round yet
    assert post(url + "/round", {"renders": list(range(MAX_VERSIONS + 1))})[0] == 400
    assert post(url + "/round", {"renders": [0, 0]})[0] == 400
    code, s = post(url + "/round", {"renders": [0, 2]})
    assert code == 200 and len(s["round"]["slots"]) == 3
    assert {session.slot_file(k) for k in (1, 2)} == {versions[0], versions[2]}
    page = get(url + "/").decode()
    assert '"round": {' in page and all(v.name not in page for v in versions)  # nor the candidate list
    assert max(x["gain_db"] for x in s["round"]["slots"]) == 0  # level matching only turns down
    post(url + "/reveal")
    assert post(url + "/reset")[0] == 200 and session.round is None


def test_fixed_round_refuses_the_chooser(album, server):
    ref, versions, work = album
    url = server(Session(ref, versions[:1], work=work))
    assert post(url + "/round", {"renders": [0]})[0] == 409
    assert post(url + "/reset")[0] == 409


def test_round_printout_labels_only_the_reference_slot(album, capsys):
    ref, versions, work = album
    Session(versions[0], [versions[0], versions[1]], work=work)  # the reference's own file as a blind version
    lines = [l for l in capsys.readouterr().out.splitlines() if versions[0].name in l]
    assert len(lines) == 2 and sum("(reference)" in l for l in lines) == 1


def test_page_uses_no_browser_dialogs():
    from gain_of_thrones.abtest import TEMPLATE
    js = TEMPLATE.read_text()
    assert not any(f"{f}(" in js for f in ("alert", "confirm", "prompt"))
