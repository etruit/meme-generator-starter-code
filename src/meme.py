"""Command-line helper for generating memes from images and quotes."""

import argparse
import os
import random

try:
    from QuoteEngine.ingestor import Ingestor
    from QuoteEngine.quote_model import QuoteModel
    from MemeEngine.meme_engine import MemeEngine
except ImportError:  # pragma: no cover
    from ingestor import Ingestor
    from quote_model import QuoteModel
    from meme_engine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme from an image path and a quote."""
    image_path = None
    quote = None

    if path is None:
        images_dir = "./_data/photos/dog/"
        image_paths = []
        for root, _, files in os.walk(images_dir):
            image_paths = [os.path.join(root, name) for name in files]

        image_path = random.choice(image_paths)
    else:
        image_path = path if isinstance(path, str) else path[0]

    if body is None:
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        quotes = []
        for quote_file in quote_files:
            quotes.extend(Ingestor.parse(quote_file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError("Author required if body is used")
        quote = QuoteModel(body, author)

    meme_engine = MemeEngine("./tmp")
    generated_path = meme_engine.make_meme(image_path, quote.body, quote.author)
    return generated_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a meme with an image and a quote"
    )
    parser.add_argument("--path", type=str, help="Path to an image file")
    parser.add_argument("--body", type=str, help="Quote body to add to the image")
    parser.add_argument("--author", type=str, help="Quote author to add to the image")
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
