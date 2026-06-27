"""PDF-based quote ingestion."""

import os
import re
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
        try:
            result = subprocess.run(
                ["pdftotext", path, "-"],
                check=True,
                capture_output=True,
                text=True,
            )
            text = result.stdout
        except FileNotFoundError:
            return []
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Unable to extract PDF text: {exc.stderr}"
            ) from exc

        return cls._parse_extracted_text(text)

    @staticmethod
    def _parse_extracted_text(text: str) -> List[QuoteModel]:
        """Parse quote entries from extracted PDF text."""
        quotes: List[QuoteModel] = []
        normalized_text = re.sub(r"\s+", " ", text).strip()
        quote_pattern = re.compile(r'"([^"]+)"\s*-\s*([^"\n]+)')

        for match in quote_pattern.finditer(normalized_text):
            body = match.group(1).strip()
            author = match.group(2).strip()
            quotes.append(QuoteModel(body, author))

        return quotes
