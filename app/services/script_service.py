from app.models import SceneSpec


def _make_title(index: int, base_prompt: str) -> str:
    mood = ["Cinematic", "Documentary", "Atmospheric", "Wide-angle", "Detailed", "Immersive"]
    label = mood[index % len(mood)]
    return f"{label} Scene {index}: {base_prompt[:24].strip()}"


def build_scene_plan(prompt: str, target_minutes: int = 30, scene_duration_seconds: int = 20) -> list[SceneSpec]:
    """Build a simple but practical scene plan from a narrative prompt.

    This is a startup pipeline for local generation. It creates a set of scenes
    with broad structure and narrative direction so the rest of the pipeline can
    render and stitch them together.
    """
    prompt_clean = prompt.strip() or "Create a cinematic educational video"
    scene_count = max(1, int((target_minutes * 60) / scene_duration_seconds))

    scenes: list[SceneSpec] = []
    for index in range(1, scene_count + 1):
        chapter = index if index <= 5 else (index % 5) + 1
        title = _make_title(index, prompt_clean)
        narration = (
            f"Scene {index} of {scene_count}. "
            f"This segment explores the visual direction for: {prompt_clean}. "
            f"Focus on cinematic composition, atmosphere, and clear narrative flow. "
            f"Use strong visual storytelling and a confident, engaging voiceover."
        )
        scenes.append(
            SceneSpec(
                index=index,
                title=title,
                prompt=(
                    f"Create a scene for chapter {chapter} based on this prompt: {prompt_clean}. "
                    f"Use a polished cinematic aesthetic with scenic composition, dynamic color, "
                    f"and storytelling focus."
                ),
                duration_seconds=scene_duration_seconds,
                narration_text=narration,
            )
        )
    return scenes
