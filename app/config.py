from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"
IMAGE_DIR = DATA_DIR / "images"
AUDIO_DIR = DATA_DIR / "audio"
VIDEO_DIR = DATA_DIR / "videos"

for directory in (DATA_DIR, OUTPUT_DIR, IMAGE_DIR, AUDIO_DIR, VIDEO_DIR):
    directory.mkdir(parents=True, exist_ok=True)

DEFAULT_TARGET_MINUTES = 30
DEFAULT_SCENE_DURATION_SECONDS = 20
