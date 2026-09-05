#!/usr/bin/env python3
"""Compatibility entry point; implementation lives in .softkit/scripts."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    target = Path(__file__).resolve().parents[4] / ".softkit/scripts" / Path(__file__).name
    runpy.run_path(str(target), run_name="__main__")
