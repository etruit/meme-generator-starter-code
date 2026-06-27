import random
import os
import requests
from flask import Flask, render_template, abort, request, send_from_directory

try:
    from QuoteEngine.ingestor import Ingestor
    from QuoteEngine.quote_model import QuoteModel
    from MemeEngine.meme_engine import MemeEngine
except ImportError:  # pragma: no cover
    from ingestor import Ingestor
    from quote_model import QuoteModel
    from meme_engine import MemeEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "_data")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config["STATIC_FOLDER"] = os.path.join(BASE_DIR, "static")

meme = MemeEngine(app.config["STATIC_FOLDER"])


def setup():
    """Load all resources."""

    quote_files = [
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesTXT.txt"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesDOCX.docx"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesPDF.pdf"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesCSV.csv"),
    ]

    quotes = []
    for quote_file in quote_files:
        quotes.extend(Ingestor.parse(quote_file))

    images_path = os.path.join(DATA_DIR, "photos", "dog")

    imgs = []
    for root, _, files in os.walk(images_path):
        imgs.extend(os.path.join(root, name) for name in files)

    return quotes, imgs


quotes, imgs = setup()


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve generated meme images from the static directory."""
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    filename = os.path.basename(path)
    return render_template('meme.html', path=f'/static/{filename}')


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    # Save the image from the URL to a temporary file
    response = requests.get(image_url)
    with open('./tmp/image.jpg', 'wb') as f:
        f.write(response.content)

    path = meme.make_meme('./tmp/image.jpg', body, author)

    # Remove the temporary saved image
    os.remove('./tmp/image.jpg')

    filename = os.path.basename(path)
    return render_template('meme.html', path=f'/static/{filename}')


if __name__ == "__main__":
    app.run()
