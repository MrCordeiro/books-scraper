# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


import random
from typing import Any, Self
from urllib.parse import urlencode

import requests
from scrapy import Spider, signals

# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter

Settings = dict[str, Any]
Headers = dict[str, str]


class BookscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        yield from result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        yield from start_requests

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeOpsFakeUserAgentMiddleware:
    """
    Middleware to handle fake user-agent for ScrapeOps.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the middleware with the given settings.
        """
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get(
            "SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT",
            "http://headers.scrapeops.io/v1/user-agents?",
        )
        self.scrapeops_fake_user_agents_active = settings.get(
            "SCRAPEOPS_FAKE_USER_AGENT_ENABLED", False
        )
        self.scrapeops_num_results = settings.get("SCRAPEOPS_NUM_RESULTS")
        self.user_agents_list: list[str] = []
        self._fetch_user_agents()
        self._validate_fake_user_agents()

    @classmethod
    def from_crawler(cls, crawler: Any) -> Self:
        """
        Factory method to create an instance from a crawler.

        :param crawler: The crawler to create the instance from.
        :return: An instance of ScrapeOpsFakeUserAgentMiddleware.
        """
        return cls(crawler.settings)

    def _fetch_user_agents(self) -> None:
        """
        Fetch user agents from the ScrapeOps API.
        """
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload["num_results"] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get("result", [])

    def _get_random_user_agent(self) -> str:
        """
        Get a random user agent from the fetched list.

        """
        return random.choice(self.user_agents_list)

    def _validate_fake_user_agents(self) -> None:
        """
        Validate if the fake user agents feature should be enabled or not.
        """
        self.scrapeops_fake_user_agents_active = bool(
            self.scrapeops_api_key and self.scrapeops_fake_user_agents_active
        )

    def process_request(self, request: Any, spider: Spider) -> None:
        """
        Process a request by attaching a random user agent to it.
        """
        if not self.scrapeops_fake_user_agents_active:
            return

        random_user_agent = self._get_random_user_agent()
        request.headers["User-Agent"] = random_user_agent

        spider.logger.debug("************ NEW HEADER ATTACHED *******")
        spider.logger.debug(request.headers["User-Agent"])


class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    """
    Middleware to handle fake browser headers for ScrapeOps.
    """

    def __init__(self, settings: Settings) -> None:
        self.scrapeops_api_key: str | None = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint: str = settings.get(
            "SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT",
            "http://headers.scrapeops.io/v1/browser-headers",
        )
        self.scrapeops_fake_browser_headers_active: bool = settings.get(
            "SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED", True
        )
        self.scrapeops_num_results: str | None = settings.get("SCRAPEOPS_NUM_RESULTS")
        self.headers_list: list[Headers] = []
        self._fetch_headers()
        self._validate_fake_browser_headers()

    @classmethod
    def from_crawler(cls, crawler: Any) -> Self:
        """
        Factory method to create an instance from a crawler.
        """
        return cls(crawler.settings)

    def _fetch_headers(self) -> None:
        """
        Fetch headers from the ScrapeOps API.
        """
        payload = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload["num_results"] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get("result", [])

    def _get_random_browser_header(self) -> Headers:
        """
        Get a random browser header from the fetched list.

        :return: A random browser header.
        """
        return random.choice(self.headers_list)

    def _validate_fake_browser_headers(self) -> None:
        """
        Validate if the fake browser headers feature should be enabled or not.
        """
        self.scrapeops_fake_browser_headers_active = bool(
            self.scrapeops_api_key and self.scrapeops_fake_browser_headers_active
        )

    def process_request(self, request: Any, spider: Spider) -> None:
        """
        Process a request by attaching random browser headers to it.
        """
        if not self.scrapeops_fake_browser_headers_active:
            return

        random_browser_header = self._get_random_browser_header()

        for header, value in random_browser_header.items():
            request.headers[header] = value

        spider.logger.debug("************ NEW HEADER ATTACHED *******")
        spider.logger.debug(request.headers)
