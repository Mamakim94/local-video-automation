from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from PIL import Image, ImageDraw, ImageFilter

from app.config import IMAGE_DIR


class ImageService:
    def __init__(self, image_dir: str | Path | None = None):
        self.image_dir = Path(image_dir) if image_dir else IMAGE_DIR
        self.image_dir.mkdir(parents=True, exist_ok=True)

    def use_uploaded_or_generate(self, scene, uploaded_images: Iterable[str] | None = None) -> str:
        uploaded_images = list(uploaded_images or [])

        if uploaded_images:
            for candidate in uploaded_images:
                path = Path(candidate)
                if path.exists():
                    target_path = self.image_dir / f"scene_{scene.index:03d}_uploaded.png"
                    target_path.write_bytes(path.read_bytes())
                    return str(target_path)

        return self.generate_placeholder_scene_image(scene)

    def generate_placeholder_scene_image(self, scene) -> str:
        width, height = 1280, 720
        image = Image.new("RGB", (width, height), color=(18, 24, 36))
        draw = ImageDraw.Draw(image)

        # Background gradient effect
        for y in range(height):
            r = int(18 + (y / height) * 35)
            g = int(24 + (y / height) * 52)
            b = int(36 + (y / height) * 54)
            draw.line((0, y, width, y), fill=(r, g, b))

        # Large soft horizon bands
        for band in range(6):
            top = int((height / 6) * band)
            bottom = int((height / 6) * (band + 1))
            alpha = 70 + band * 18
            draw.rectangle((0, top, width, bottom), fill=(30, 50, 68, alpha))

        # Center glow
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((260, 120, 1010, 600), fill=(140, 180, 220, 90))
        image = Image.alpha_composite(image.convert("RGBA"), glow).convert("RGB")

        # Subtle text
        draw = ImageDraw.Draw(image)
        draw.text((70, 90), scene.title[:35], fill=(240, 244, 248), font=None)
        draw.text((70, 150), "Generated local scene", fill=(170, 200, 230), font=None)
        draw.text((70, 620), scene.prompt[:60], fill=(226, 232, 240), font=None)

        output_path = self.image_dir / f"scene_{scene.index:03d}.png"
        image = image.filter(ImageFilter.GaussianBlur(radius=0.35))
        image.save(output_path)
        return str(output_path)
