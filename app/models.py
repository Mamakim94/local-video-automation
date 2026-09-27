from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SceneSpec:
    index: int
    title: str
    prompt: str
    duration_seconds: int = 20
    narration_text: str = ""
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    video_path: Optional[str] = None


@dataclass
class ProjectSpec:
    prompt: str
    target_minutes: int = 30
    scenes: List[SceneSpec] = field(default_factory=list)
    output_dir: str = "data/output"
