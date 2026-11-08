import subprocess
from pathlib import Path

import pytest

from gain_of_thrones.io import AUDIO_EXTS

ROOT = Path(__file__).resolve().parents[1]


def test_git_tracks_no_audio():
    if not (ROOT / ".git").exists():
        pytest.skip("not a git repository yet")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    audio = [f for f in tracked.splitlines() if Path(f).suffix.lower() in AUDIO_EXTS]
    assert not audio, f"audio files tracked by git: {audio}"
