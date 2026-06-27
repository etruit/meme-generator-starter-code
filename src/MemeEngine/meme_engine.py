from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Load an image, resize it, add quote text and author, then save it."""
        img = Image.open(img_path)
        ratio = width / float(img.width)
        height = int(img.height * ratio)
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        draw = ImageDraw.Draw(img)
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
        img.save(output_path)
        return str(output_path)
