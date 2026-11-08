from gain_of_thrones.abtest import match_gains, song_name


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
