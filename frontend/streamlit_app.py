from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
runpy.run_path(str(ROOT_DIR / "streamlit_app.py"), run_name="__main__")
