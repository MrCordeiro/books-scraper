"""Pipeline for cleaning the scraped data."""
from itemadapter.adapter import ItemAdapter

from books_scraper.items import BookItem
from books_scraper.spiders.bookspider import BooksSpider


class BookscraperPipeline:
    """Pipeline for cleaning book data."""

    @staticmethod
    def _strip_values(adapter: ItemAdapter, field_names: list[str]) -> None:
        """Strip values for each field in the adapter."""
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if not value:
                    continue
                adapter[field_name] = value.strip()

    @staticmethod
    def _lowercase_values(adapter: ItemAdapter, keys: list[str]) -> None:
        """Lowercase values for the specified keys in the adapter."""
        for key in keys:
            adapter[key] = adapter[key].lower()

    @staticmethod
    def _parse_prices(adapter: ItemAdapter, keys: list[str]) -> None:
        """Parse and convert price-related fields to float."""
        for key in keys:
            adapter[key] = float(adapter[key].replace("£", ""))

    @staticmethod
    def _parse_availability(adapter: ItemAdapter):
        """Parse and convert availability field to integer."""
        availability_string = adapter.get("availability", "")
        split_string_array = availability_string.split("(")
        if len(split_string_array) < 2:
            adapter["availability"] = 0
        if len(split_string_array) > 1:
            adapter["availability"] = int(split_string_array[1].split(" ")[0])

    @staticmethod
    def _parse_num_reviews(adapter: ItemAdapter):
        """Parse and convert num_reviews field to integer."""
        num_reviews_string = adapter.get("num_reviews", 0)
        adapter["num_reviews"] = int(num_reviews_string)

    @staticmethod
    def _parse_stars(adapter: ItemAdapter):
        """Parse and convert stars field to integer."""
        stars_string = adapter.get("stars")
        if not stars_string:
            return

        n_stars = stars_string.split(" ")[1].lower()
        match n_stars:
            case "one":
                adapter["stars"] = 1
            case "two":
                adapter["stars"] = 2
            case "three":
                adapter["stars"] = 3
            case "four":
                adapter["stars"] = 4
            case "five":
                adapter["stars"] = 5
            case _:
                adapter["stars"] = 0

    def process_item(self, item: BookItem, spider: BooksSpider):
        """Clean the scraped data."""
        adapter = ItemAdapter(item)
        field_names = list(adapter.field_names())

        self._strip_values(adapter, field_names)
        self._lowercase_values(adapter, ["category", "product_type"])
        self._parse_prices(
            adapter, ["price_excl_tax", "price_incl_tax", "price", "tax"]
        )
        self._parse_availability(adapter)
        self._parse_num_reviews(adapter)
        self._parse_stars(adapter)

        return item
