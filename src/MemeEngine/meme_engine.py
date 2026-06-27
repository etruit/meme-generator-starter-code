"""Image processing helpers for creating meme images."""

import random
from pathlib import Path
from typing import Tuple, Union

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Create meme images by overlaying text onto a source image."""

    def __init__(self, output_dir: Union[str, Path]) -> None:
        """Initialize the meme engine with an output directory."""
        self.output_dir = output_dir

    def make_meme(
        self,
        img_path: Union[str, Path],
        text: str,
        author: str,
        width: int = 500,
    ) -> str:
        """Load an image, resize, add quote, save."""
        image = self._load_and_resize_image(img_path, width)
        draw = ImageDraw.Draw(image)
        font = self._get_font(image)
        message = self._build_message(text, author)
        wrapped_message = self._wrap_message(
            draw, message, font, width - 40
        )
        text_width, text_height = self._get_text_size(
            draw, wrapped_message, font
        )
        x, y = self._get_text_position(
            width, image.height, text_width, text_height
        )
        self._draw_text(
            draw, wrapped_message, font, x, y, text_width, text_height
        )
        return self._save_image(image)

    def _load_and_resize_image(
        self, img_path: Union[str, Path], width: int
    ) -> Image.Image:
        """Open an image and resize it to the requested width."""
        image = Image.open(img_path)
        ratio = width / float(image.width)
        height = int(image.height * ratio)
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def _get_font(self, image: Image.Image) -> ImageFont.ImageFont:
        """Return a font suitable for the current image size."""
        try:
            return ImageFont.truetype(
                "arial.ttf",
                size=max(12, int(image.height / 20)),
            )
        except OSError:
            return ImageFont.load_default()

    def _build_message(self, text: str, author: str) -> str:
        """Create the quote text to display on the meme."""
        return f'"{text}"\n- {author}'

    def _wrap_message(
        self,
        draw: ImageDraw.ImageDraw,
        message: str,
        font: ImageFont.ImageFont,
        max_width: int,
    ) -> str:
        """Wrap the message so it fits within the image width."""
        words = message.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)

    def _get_text_size(
        self,
        draw: ImageDraw.ImageDraw,
        message: str,
        font: ImageFont.ImageFont,
    ) -> Tuple[int, int]:
        """Measure the rendered text dimensions."""
        text_bbox = draw.multiline_textbbox((0, 0), message, font=font)
        return text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    def _get_text_position(
        self,
        width: int,
        height: int,
        text_width: int,
        text_height: int,
    ) -> Tuple[int, int]:
        """Choose a random position for the text box within the image."""
        margin = 10
        x = random.randint(10, max(10, width - text_width - margin))
        y = random.randint(10, max(10, height - text_height - margin))
        return x, y

    def _draw_text(
        self,
        draw: ImageDraw.ImageDraw,
        message: str,
        font: ImageFont.ImageFont,
        x: int,
        y: int,
        text_width: int,
        text_height: int,
    ) -> None:
        """Render the meme text and its background box onto the image."""
        margin = 10
        background_box = [
            x - margin,
            y - margin,
            x + text_width + margin,
            y + text_height + margin,
        ]
        draw.rectangle(background_box, fill=(0, 0, 0, 150))
        draw.multiline_text((x, y), message, fill="white", font=font)

    def _save_image(self, image: Image.Image) -> str:
        """Save the meme image to the configured output directory."""
        output_dir = Path(self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        while True:
            filename = f"{random.randint(10**9, (10**10) - 1)}.png"
            output_path = output_dir / filename
            if not output_path.exists():
                break

        image.save(output_path)
        return str(output_path)
