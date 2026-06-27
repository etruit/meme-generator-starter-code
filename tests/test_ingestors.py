"""Tests for the QuoteEngine ingestors."""

from pathlib import Path
import sys

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from QuoteEngine import Ingestor
from QuoteEngine.quote_model import QuoteModel


@pytest.mark.parametrize(
    ("filename", "expected_count"),
    [
        ("DogQuotesTXT.txt", 2),
        ("DogQuotesCSV.csv", 2),
        ("DogQuotesDOCX.docx", 4),
        ("DogQuotesPDF.pdf", 0),
    ],
)
def test_ingestor_parses_supported_quote_files(filename, expected_count):
    base_dir = ROOT_DIR / "src" / "_data" / "DogQuotes"
    quote_path = base_dir / filename

    assert Ingestor.can_ingest(str(quote_path))

    quotes = Ingestor.parse(str(quote_path))

    assert len(quotes) == expected_count
    assert all(isinstance(quote, QuoteModel) for quote in quotes)
