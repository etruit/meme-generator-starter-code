"""PDF-based quote ingestion."""

import os
import subprocess
from typing import List

try:
    from .ingestor_interface import IngestorInterface
    from .quote_model import QuoteModel
except ImportError:  # pragma: no cover
    from ingestor_interface import IngestorInterface
    from quote_model import QuoteModel


class PdfIngestor(IngestorInterface):
    """Parse quotes from PDF files using Xpdf."""

    allowed_extensions = {".pdf"}

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True when the path points to a PDF file."""
        return os.path.splitext(path)[1].lower() in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Extract text from a PDF and parse it into quotes."""
        quotes: List[QuoteModel] = []
        try:
            result = subprocess.run(
                ["pdftotext", path, "-"],
                check=True,
                capture_output=True,
                text=True,
            )
            text = result.stdout
        except FileNotFoundError:
            return quotes
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Unable to extract PDF text: {exc.stderr}") from exc

        for line in text.splitlines():
            line = line.strip()
            if not line or " - " not in line:
                continue
            body, author = line.rsplit(" - ", 1)
            quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes
