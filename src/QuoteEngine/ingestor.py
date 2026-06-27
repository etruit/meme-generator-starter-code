import argparse
import os
from typing import List, Type

try:
    from .csv_ingestor import CsvIngestor
    from .docx_ingestor import DocxIngestor
    from .pdf_ingestor import PdfIngestor
    from .quote_model import QuoteModel
    from .txt_ingestor import TxtIngestor
    from .ingestor_interface import IngestorInterface
except ImportError:  # pragma: no cover
    from csv_ingestor import CsvIngestor
    from docx_ingestor import DocxIngestor
    from pdf_ingestor import PdfIngestor
    from quote_model import QuoteModel
    from txt_ingestor import TxtIngestor
    from ingestor_interface import IngestorInterface


class Ingestor(IngestorInterface):
    """Dispatch parsing to the appropriate quote strategy."""

    allowed_extensions = {
        ext
        for ingestor in [CsvIngestor, DocxIngestor, PdfIngestor, TxtIngestor]
        for ext in ingestor.allowed_extensions
    }

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True when any concrete ingestor supports the given path."""
        return any(ingestor.can_ingest(path) for ingestor in cls._ingestors())

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a quote file by selecting the appropriate ingestor strategy."""
        for ingestor in cls._ingestors():
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"Unsupported file type for {path}")

    @staticmethod
    def _ingestors() -> List[Type[IngestorInterface]]:
        """Return the registered concrete ingestor classes."""
        return [CsvIngestor, DocxIngestor, PdfIngestor, TxtIngestor]


def main() -> None:
    """Run the ingestor from the command line."""
    parser = argparse.ArgumentParser(
        description="Parse quote files using the appropriate ingestor strategy"
    )
    parser.add_argument(
        "path", help="Path to a .csv, .docx, .pdf, or .txt quote file"
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        raise FileNotFoundError(args.path)

    for quote in Ingestor.parse(args.path):
        print(quote)


if __name__ == "__main__":
    main()
