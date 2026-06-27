"""Image processing helpers for creating meme images."""

from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Create meme images by overlaying text onto a source image."""

    def __init__(self, output_dir: Union[str, Path]) -> None:
        """Initialize the meme engine with an output directory."""
        self.output_dir = output_dir

    def make_meme(
        self, img_path: Union[str, Path], text: str, author: str, width: int = 500
    ) -> str:
        """Load an image, resize it, add quote text and author, then save it."""
        image = Image.open(img_path)
        ratio = width / float(image.width)
        height = int(image.height * ratio)
        image = image.resize((width, height), Image.Resampling.LANCZOS)

        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", size=int(height / 15))
        except OSError:
            font = ImageFont.load_default()

        message = f'"{text}"\n- {author}'
        text_bbox = draw.multiline_textbbox((0, 0), message, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = 10
        y = height - text_height - 10
        if y < 0:
            y = 10

        margin = 10
        background_box = [
            x - margin,
            y - margin,
            x + text_width + margin,
            y + text_height + margin,
        ]
        draw.rectangle(background_box, fill=(0, 0, 0, 150))
        draw.multiline_text((x, y), message, fill="white", font=font)

        output_dir = Path(self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "meme.png"
        image.save(output_path)
        return str(output_path)
