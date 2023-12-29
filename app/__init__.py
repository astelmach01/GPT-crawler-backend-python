"""app package."""
from pathlib import Path

APP_DIR = Path(__file__).parent

OUTPUT_DIR = APP_DIR.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
