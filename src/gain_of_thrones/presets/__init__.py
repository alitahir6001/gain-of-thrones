"""Preset registry. A preset is a module with CHAINS, BALANCE, BUS_COMP and CEILING (see heavy_guitar.py).
--preset also takes a path to a .py file, so a session can iterate on a copy without touching the shipped one."""
import importlib
import importlib.util
from pathlib import Path

PRESETS = {"heavy-guitar": "gain_of_thrones.presets.heavy_guitar"}


def load(name):
    if name in PRESETS:
        return importlib.import_module(PRESETS[name])
    p = Path(name)
    if p.suffix == ".py" and p.is_file():
        spec = importlib.util.spec_from_file_location(p.stem, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    raise SystemExit(f"unknown preset {name!r}; known: {', '.join(PRESETS)}, or a path to a preset .py file")
