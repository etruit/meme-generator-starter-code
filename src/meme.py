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
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Generate a meme with an image and a quote")
    args.add_argument('--path', type=str, help='Path to an image file')
    args.add_argument('--body', type=str, help='Quote body to add to the image')
    args.add_argument('--author', type=str, help='Quote author to add to the image')
    args = args.parse_args()
    print(generate_meme(args.path, args.body, args.author))
