import numpy as np
import soundfile as sf

from gain_of_thrones import export, io
from gain_of_thrones.limiter import true_peak

SR = 44100


def make_album(tmp_path):
    """One source FLAC with tags, ReplayGain and a cover; one 24-bit render peaking at -1.3 dBTP."""
    src, ren = tmp_path / "src", tmp_path / "renders"
    src.mkdir(), ren.mkdir()
    io.run([io.tool("ffmpeg"), "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
            "-f", "lavfi", "-i", "color=c=red:s=32x32", "-map", "0:a", "-map", "1:v", "-frames:v", "1",
            "-c:v", "mjpeg", "-disposition:v", "attached_pic", "-metadata", "title=Tone",
            "-metadata", "REPLAYGAIN_TRACK_GAIN=-3.00 dB", "-metadata", "replaygain_album_peak=0.99",
            src / "01 Tone.flac"])
    rng = np.random.default_rng(0)
    t = np.arange(3 * SR) / SR
    x = np.stack([np.sin(2 * np.pi * 440 * t), np.sin(2 * np.pi * 660 * t)], 1) * 0.6 + rng.normal(0, 0.1, (3 * SR, 2))
    x *= 10 ** (-1.3 / 20) / 10 ** (true_peak(x) / 20)
    sf.write(ren / "01 Tone_test_-10LUFS.wav", x, SR, subtype="PCM_24")
    return src, ren


def test_mp3_export_is_under_ceiling_and_drops_replaygain(tmp_path):
    src, ren = make_album(tmp_path)
    outs = export.run(ren, src, "mp3", tmp_path / "mp3")
    mp3 = outs[src / "01 Tone.flac"]
    assert true_peak(io.decode(mp3)[0]) <= export.MP3_CEILING
    info = io.probe(mp3)
    tags = {k.upper(): v for k, v in info["format"]["tags"].items()}
    assert tags["TITLE"] == "Tone"
    assert not [k for k in tags if k.startswith("REPLAYGAIN")]
    assert any(s["codec_type"] == "video" for s in info["streams"])  # cover kept


def test_flac_export_is_24_bit_as_rendered(tmp_path):
    src, ren = make_album(tmp_path)
    flac = export.run(ren, src, "flac", tmp_path / "flac")[src / "01 Tone.flac"]
    st = io.audio_stream(flac)
    assert st["codec_name"] == "flac" and st["bits_per_raw_sample"] == "24"
    rendered = sf.read(ren / "01 Tone_test_-10LUFS.wav")[0]
    assert np.array_equal(sf.read(flac)[0], rendered)  # lossless: same samples
    tags = {k.upper() for k in io.probe(flac)["format"]["tags"]}
    assert "TITLE" in tags and not [k for k in tags if k.startswith("REPLAYGAIN")]
