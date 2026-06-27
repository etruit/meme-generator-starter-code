"""Tests for the QuoteEngine ingestors."""

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from QuoteEngine import Ingestor  # noqa: E402
from QuoteEngine.pdf_ingestor import PdfIngestor  # noqa: E402
from QuoteEngine.quote_model import QuoteModel  # noqa: E402


@pytest.mark.parametrize(
    ("filename", "expected_count"),
    [
        ("DogQuotesTXT.txt", 2),
        ("DogQuotesCSV.csv", 2),
        ("DogQuotesDOCX.docx", 4),
        ("DogQuotesPDF.pdf", 3),
    ],
)
def test_ingestor_parses_supported_quote_files(filename, expected_count):
    base_dir = ROOT_DIR / "src" / "_data" / "DogQuotes"
    quote_path = base_dir / filename

    assert Ingestor.can_ingest(str(quote_path))

    quotes = Ingestor.parse(str(quote_path))

    assert len(quotes) == expected_count
    assert all(isinstance(quote, QuoteModel) for quote in quotes)


def test_pdf_ingestor_parses_multiple_quotes_from_concatenated_text():
    extracted_text = (
        '"Treat yo self" - Fluffles "Life is like a box of treats" '
        '- Forrest Pup "It\'s the size of the fight in the dog" '
        '- Bark Twain'
    )

    quotes = PdfIngestor._parse_extracted_text(extracted_text)

    assert len(quotes) == 3
    assert [quote.body for quote in quotes] == [
        "Treat yo self",
        "Life is like a box of treats",
        "It's the size of the fight in the dog",
    ]
    assert [quote.author for quote in quotes] == [
        "Fluffles",
        "Forrest Pup",
        "Bark Twain",
    ]
