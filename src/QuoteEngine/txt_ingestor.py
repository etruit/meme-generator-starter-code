import os
from typing import List

try:
    from .ingestor_interface import IngestorInterface
    from .quote_model import QuoteModel
except ImportError:  # pragma: no cover
    from ingestor_interface import IngestorInterface
    from quote_model import QuoteModel


class TxtIngestor(IngestorInterface):
    """Parse quotes from plain-text files."""

    allowed_extensions = {".txt"}

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True when the path points to a text file."""
        return os.path.splitext(path)[1].lower() in cls.allowed_extensions

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse quotes from a text file."""
        quotes: List[QuoteModel] = []
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or " - " not in line:
                    continue
                body, author = line.rsplit(" - ", 1)
                quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes
