from collections.abc import Iterator

import scrapy
from scrapy.http import HtmlResponse


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response: HtmlResponse) -> Iterator[dict[str, str | None]]:
        """Parse the response downloaded for each of the requests made and
        yield a dict with the book's name, price and url.

        Besides extracting the scraped data as dicts it's also used forfinding
        new URLs to follow and creating new requests (Request) from them.
        """

        books = response.css("article.product_pod")
        for book in books:
            yield {
                "name": book.css("h3 a::text").get(),
                "price": book.css(".product_price .p.price_color::text").get(),
                "url": book.css("h3 a").attrib["href"],
            }
