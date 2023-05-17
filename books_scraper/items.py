"""
Data structure used to store the scraped data.
"""
from dataclasses import dataclass, field


def _serialize_price(value):
    """Serialize the price to include the currency symbol."""
    return f"£ {str(value)}"


@dataclass
class BookItem:
    """A book item scraped from books.toscrape.com."""

    url: str | None
    title: str | None
    upc: str | None
    product_type: str | None
    price_excl_tax: str | None
    price_incl_tax: str | None
    tax: str | None = field(metadata={"serializer": _serialize_price})
    availability: str | None
    num_reviews: str | None
    stars: str | None
    category: str | None
    description: str | None
    price: str | None
