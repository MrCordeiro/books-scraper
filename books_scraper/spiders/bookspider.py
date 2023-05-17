from collections.abc import Iterator

import scrapy
from scrapy.http import HtmlResponse

from ..items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # Override the default settings for the JSON feed exporter
    custom_settings = {
        "FEEDS": {
            "books.json": {"format": "json", "overwrite": True},
        },
    }

    def parse(self, response: HtmlResponse) -> Iterator[BookItem | scrapy.Request]:
        """Parse the response downloaded for each of the requests made and
        yield a dict with the book's name, price and url.

        Besides extracting the scraped data as dicts it's also used for finding
        new URLs to follow and creating new requests (Request) from them.
        """

        books = response.css("article.product_pod")
        for book in books:
            book_detail_page = book.css("h3 a ::attr(href)").get()
            if not book_detail_page:
                continue
            if "catalogue/" not in book_detail_page:
                book_detail_page = f"catalogue/{book_detail_page}"
            book_url = f"https://books.toscrape.com/{book_detail_page}"
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css("li.next a ::attr(href)").get()
        if next_page:
            if "catalogue/" not in next_page:
                next_page = f"catalogue/{next_page}"
            next_page_url = f"https://books.toscrape.com/{next_page}"
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response: HtmlResponse) -> Iterator[BookItem]:
        """Parse the book page and yield a dict with the book's info."""
        table_rows = response.css("table tr")

        yield BookItem(
            url=response.url,
            title=response.css(".product_main h1::text").get(),
            upc=table_rows[0].css("td ::text").get(),
            product_type=table_rows[1].css("td ::text").get(),
            price_excl_tax=table_rows[2].css("td ::text").get(),
            price_incl_tax=table_rows[3].css("td ::text").get(),
            tax=table_rows[4].css("td ::text").get(),
            availability=table_rows[5].css("td ::text").get(),
            num_reviews=table_rows[6].css("td ::text").get(),
            # E.g. "star-rating Three"
            stars=response.css("p.star-rating").attrib["class"],
            category=response.xpath(
                "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
            ).get(),
            description=response.xpath(
                "//div[@id='product_description']/following-sibling::p/text()"
            ).get(),
            price=response.css("p.price_color ::text").get(),
        )
