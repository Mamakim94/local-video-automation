from fastapi import FastAPI
from pydantic import BaseModel

from app.config import DEFAULT_TARGET_MINUTES, OUTPUT_DIR
from app.models import ProjectSpec, SceneSpec
from app.services.image_service import ImageService
from app.services.script_service import build_scene_plan
from app.services.tts_service import TTSService
from app.services.video_service import VideoService

app = FastAPI(title="Local Video Automation")


class GenerateRequest(BaseModel):
    prompt: str
    target_minutes: int = DEFAULT_TARGET_MINUTES
    uploaded_images: list[str] | None = None


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "local-video-automation"}


@app.post("/generate")
def generate_video(request: GenerateRequest):
    if not request.prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    scenes = build_scene_plan(request.prompt, target_minutes=request.target_minutes)
    image_service = ImageService()
    tts_service = TTSService()
    video_service = VideoService(OUTPUT_DIR)

    scene_video_paths: list[str] = []
    for scene in scenes:
        image_path = image_service.use_uploaded_or_generate(scene, request.uploaded_images)
        narration_path = tts_service.synthesize_scene(scene.narration_text, scene.index)
        scene.video_path = video_service.render_scene_video(scene, image_path, narration_path)
        scene_video_paths.append(scene.video_path)

    final_path = video_service.render_long_video(scenes, scene_video_paths)

    return {
        "status": "completed",
        "prompt": request.prompt,
        "scene_count": len(scenes),
        "output_video": final_path,
        "estimated_length_minutes": request.target_minutes,
    }
