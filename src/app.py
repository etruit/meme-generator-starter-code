"""Flask application for generating and displaying memes."""

import os
import random

import requests
from flask import Flask, render_template, request, send_from_directory

try:
    from QuoteEngine.ingestor import Ingestor
    from MemeEngine.meme_engine import MemeEngine
except ImportError:  # pragma: no cover
    from ingestor import Ingestor
    from meme_engine import MemeEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "_data")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config["STATIC_FOLDER"] = os.path.join(BASE_DIR, "static")

meme = MemeEngine(app.config["STATIC_FOLDER"])


def setup():
    """Load all resources used by the application."""
    quote_files = [
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesTXT.txt"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesDOCX.docx"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesPDF.pdf"),
        os.path.join(DATA_DIR, "DogQuotes", "DogQuotesCSV.csv"),
    ]

    loaded_quotes = []
    for quote_file in quote_files:
        loaded_quotes.extend(Ingestor.parse(quote_file))

    images_path = os.path.join(DATA_DIR, "photos", "dog")
    loaded_image_paths = []
    for root, _, files in os.walk(images_path):
        loaded_image_paths.extend(os.path.join(root, name) for name in files)

    return loaded_quotes, loaded_image_paths


quotes, image_paths = setup()


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve generated meme images from the static directory."""
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img = random.choice(image_paths)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    filename = os.path.basename(path)
    return render_template("meme.html", path=f"/static/{filename}")


@app.route("/create", methods=["GET"])
def meme_form():
    """Display the meme creation form."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a meme from submitted form data."""
    image_url = request.form["image_url"]
    body = request.form["body"]
    author = request.form["author"]

    tmp_dir = os.path.join(BASE_DIR, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    image_path = os.path.join(tmp_dir, "image.jpg")

    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    with open(image_path, "wb") as handle:
        handle.write(response.content)

    path = meme.make_meme(image_path, body, author)
    os.remove(image_path)

    filename = os.path.basename(path)
    return render_template("meme.html", path=f"/static/{filename}")


if __name__ == "__main__":
    app.run()
