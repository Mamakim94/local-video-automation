# Local Video Automation v1

This repository is a practical local-first starter for generating long-form AI video from a prompt.

It is designed to run on a local machine and supports:
- prompt-driven scene planning
- optional uploaded images or generated visual placeholders
- local text-to-speech narration
- chapter-based long-video assembly
- scene-by-scene generation and final export to MP4

## What it does

The project takes a user prompt like:

> Create a 30-minute documentary about ancient Egypt with a calm narrator and cinematic visuals.

Then it:
1. turns the prompt into a scene plan
2. creates chapter and scene definitions
3. generates or reuses images per scene
4. converts narration to audio using local TTS
5. composes scene videos and merges them into a single long video

## Current v1 scope

This is a practical first milestone, not a full photorealistic studio pipeline.

Included in v1:
- local prompt-to-scene generation
- local image generation placeholders using Pillow
- local TTS using Python TTS engine support
- long-form scene assembly with FFmpeg/MoviePy
- REST API for triggering generation
- CLI entry point for local execution

Not included yet in this pass:
- full automatic lip-sync for every speaking frame
- advanced model-based realistic image generation
- true photorealistic character continuity across scenes
- distributed rendering or cloud orchestration

## Recommended local requirements

- Python 3.11+
- FFmpeg installed and available on PATH
- Optional: NVIDIA GPU for more realistic image generation via ComfyUI
- At least 16 GB RAM; 32 GB recommended for longer runs

## Quick start

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start the API

```bash
python run.py
```

4. Trigger a generation request

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 30-minute documentary about the ocean, with calm narration, cinematic landscapes, and educational scenes.",
    "target_minutes": 30,
    "uploaded_images": []
  }'
```

5. Check generated output in the `data/output` directory.

## Repository structure

```text
app/
  __init__.py
  config.py
  models.py
  api.py
  services/
    __init__.py
    script_service.py
    image_service.py
    tts_service.py
    video_service.py
run.py
requirements.txt
README.md
.gitignore
```

## How it works

The pipeline is intentionally simple and robust:

- `script_service.py` creates a scene timeline from the user prompt.
- `image_service.py` prepares a visual for each scene, using uploaded images when available or generated placeholders otherwise.
- `tts_service.py` generates narration audio for each scene.
- `video_service.py` renders each scene as a short video and concatenates them into a single MP4.

That approach is practical for local generation and makes it possible to retry or regenerate individual scenes without restarting the whole project.

## Notes on realism

For realistic pictures and lip sync, the next major step is to plug in local model pipelines such as:
- ComfyUI + SDXL/FLUX for image generation
- Wav2Lip or MuseTalk for lip sync
- more advanced narration models and voice cloning tools

This v1 is intentionally focused on a working local pipeline that can produce long-form video content reliably.

## License

This project is provided as a starter implementation for local experimentation and iteration.
