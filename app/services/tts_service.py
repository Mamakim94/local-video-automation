from pathlib import Path

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

from app.config import AUDIO_DIR


class TTSService:
    def __init__(self, audio_dir: str | Path | None = None):
        self.audio_dir = Path(audio_dir) if audio_dir else AUDIO_DIR
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def synthesize_scene(self, text: str, scene_index: int) -> str:
        if pyttsx3 is None:
            raise RuntimeError(
                "pyttsx3 is not installed. Install requirements.txt and ensure a local TTS engine is available."
            )

        output_path = self.audio_dir / f"scene_{scene_index:03d}.wav"
        engine = pyttsx3.init()
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        return str(output_path)
