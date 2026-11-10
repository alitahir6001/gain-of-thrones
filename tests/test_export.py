import re
import shutil

import numpy as np
import pytest
import soundfile as sf

from gain_of_thrones import export, io
from gain_of_thrones.limiter import true_peak

SR = 44100


def make_album(tmp_path):
    """One source FLAC with tags (lyrics: WAV has no slot for them), ReplayGain and a cover; one 24-bit render
    peaking at -1.3 dBTP."""
    src, ren = tmp_path / "src", tmp_path / "renders"
    src.mkdir(), ren.mkdir()
    io.run([io.tool("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
            "-f", "lavfi", "-i", "color=c=red:s=32x32", "-map", "0:a", "-map", "1:v", "-frames:v", "1",
            "-c:v", "mjpeg", "-disposition:v", "attached_pic", "-metadata", "title=Tone", "-metadata", "lyrics=la",
            "-metadata", "REPLAYGAIN_TRACK_GAIN=-3.00 dB", "-metadata", "replaygain_album_peak=0.99",
            src / "01 Tone.flac"])
    rng = np.random.default_rng(0)
    t = np.arange(3 * SR) / SR
    x = np.stack([np.sin(2 * np.pi * 440 * t), np.sin(2 * np.pi * 660 * t)], 1) * 0.6 + rng.normal(0, 0.1, (3 * SR, 2))
    x *= 10 ** (-1.3 / 20) / 10 ** (true_peak(x) / 20)
    sf.write(ren / "01 Tone_test_-10LUFS.wav", x, SR, subtype="PCM_24")
    return src, ren


@pytest.mark.parametrize("fmt", ["mp3", "aac"])
def test_lossy_export_is_under_ceiling_and_keeps_tags_and_cover(tmp_path, fmt):
    src, ren = make_album(tmp_path)
    out = export.run([ren], src, fmt, tmp_path / fmt)[src / "01 Tone.flac"]
    assert io.audio_stream(out)["codec_name"] == fmt
    assert true_peak(io.decode(out)[0]) <= export.LOSSY_CEILING
    tags = {k.upper(): v for k, v in io.probe(out)["format"]["tags"].items()}
    assert tags["TITLE"] == "Tone" and not [k for k in tags if k.startswith("REPLAYGAIN")]
    assert export.carried(src / "01 Tone.flac", out, fmt)[:2] == ("kept", [])


@pytest.mark.parametrize("fmt", ["flac", "alac", "wav"])
def test_lossless_export_keeps_the_rendered_samples(tmp_path, fmt):
    src, ren = make_album(tmp_path)
    out = export.run([ren], src, fmt, tmp_path / fmt)[src / "01 Tone.flac"]
    st = io.audio_stream(out)
    assert int(st.get("bits_per_raw_sample") or st["bits_per_sample"]) == 24
    # float32 holds 24-bit samples exactly
    assert np.array_equal(io.decode(out)[0], io.decode(ren / "01 Tone_test_-10LUFS.wav")[0])
    tags = {k.upper() for k in io.probe(out)["format"]["tags"]}
    assert "TITLE" in tags and not [k for k in tags if k.startswith("REPLAYGAIN")]
    cover, lost, _ = export.carried(src / "01 Tone.flac", out, fmt)
    assert cover == ("none (WAV can't hold cover art)" if fmt == "wav" else "kept")
    assert lost == (["lyrics"] if fmt == "wav" else [])


def test_export_takes_picked_render_files(tmp_path):
    src, ren = make_album(tmp_path)
    one, v2, two = (ren / n for n in ("01 Tone_test_-10LUFS.wav", "01 Tone_v2_-10LUFS.wav", "02 Tone_test_-10LUFS.wav"))
    x = sf.read(one)[0]
    sf.write(v2, x * 0.5, SR, subtype="PCM_24")
    sf.write(two, x * 0.7, SR, subtype="PCM_24")
    shutil.copy(src / "01 Tone.flac", src / "02 Tone.flac")
    with pytest.raises(SystemExit, match=re.escape(f"{one.name}, {v2.name}")):
        export.pair([ren], src)  # the folder holds two versions of track 1
    assert export.pair([v2, two, v2], src) == {src / "01 Tone.flac": v2, src / "02 Tone.flac": two}
    outs = export.run([v2], src, "flac", tmp_path / "one")
    assert list(outs) == [src / "01 Tone.flac"]
    assert np.array_equal(sf.read(outs[src / "01 Tone.flac"])[0], sf.read(v2)[0])


def test_default_out_is_beside_renders(tmp_path):
    work = tmp_path.resolve() / "work"
    (work / "renders" / "album").mkdir(parents=True)
    (work / "renders" / "x.wav").touch()
    (tmp_path / "picked").mkdir()
    assert export.default_out([work / "renders" / "x.wav"], "flac") == work / "export" / "flac"
    assert export.default_out([work / "renders" / "album"], "mp3") == work / "export" / "mp3"
    assert export.default_out([tmp_path / "picked"], "flac") == tmp_path.resolve() / "export" / "flac"
