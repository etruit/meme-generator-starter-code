class QuoteModel:
    """Represent a quote with a body and an author."""

    def __init__(self, body: str, author: str):
        """Initialize a quote model.

        Args:
            body: The quote text.
            author: The quote author.

        Raises:
            ValueError: If the body or author is empty or whitespace.
        """
        if not body or not body.strip():
            raise ValueError("Quote body cannot be empty")
        if not author or not author.strip():
            raise ValueError("Quote author cannot be empty")

        self.body = body.strip()
        self.author = author.strip()

    def __str__(self) -> str:
        """Return a human-readable string representation of the quote."""
        return f'"{self.body}" - {self.author}'

    def __repr__(self) -> str:
        """Return an unambiguous representation of the quote model."""
        return f"QuoteModel(body={self.body!r}, author={self.author!r})"