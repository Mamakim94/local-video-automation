from pathlib import Path

from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

from app.config import OUTPUT_DIR


class VideoService:
    def __init__(self, output_dir: str | Path | None = None):
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render_scene_video(self, scene, image_path: str, narration_path: str) -> str:
        clip = ImageClip(image_path, duration=scene.duration_seconds)
        clip = clip.resize((1280, 720))

        audio = AudioFileClip(narration_path)
        if audio.duration > scene.duration_seconds:
            audio = audio.subclip(0, scene.duration_seconds)

        final = clip.set_audio(audio)
        output_path = self.output_dir / f"scene_{scene.index:03d}.mp4"
        final.write_videofile(
            str(output_path),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            threads=2,
            preset="medium",
            verbose=False,
            logger=None,
        )
        return str(output_path)

    def render_long_video(self, scenes, scene_video_paths) -> str:
        clips = []
        for scene in scenes:
            for path in scene_video_paths:
                if f"scene_{scene.index:03d}" in path:
                    clips.append(VideoFileClip(path))
                    break

        if not clips:
            raise RuntimeError("No scene videos were generated. Check the pipeline inputs.")

        final = concatenate_videoclips(clips, method="compose")
        final_path = self.output_dir / "final_video.mp4"
        final.write_videofile(
            str(final_path),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            threads=2,
            preset="medium",
            verbose=False,
            logger=None,
        )
        return str(final_path)
