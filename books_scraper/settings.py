# Scrapy settings for books_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "books_scraper"

SPIDER_MODULES = ["books_scraper.spiders"]
NEWSPIDER_MODULE = "books_scraper.spiders"
CLOSESPIDER_ERRORCOUNT = 1

# Used to create a default output file, without having to specify it in the
# command line
# FEEDS = {
#     "books.json": {"format": "json"},
# }

# Sets a default user agent
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "books_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "books_scraper.middlewares.BookscraperSpiderMiddleware": 543,
# }

# The downloader middleware a system for globally altering Scrapy's requests
# and responses.
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "books_scraper.middlewares.BookscraperDownloaderMiddleware": 543,
    "books_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 500,
    "books_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 600,
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "books_scraper.pipelines.BookscraperPipeline": 300,
    "books_scraper.pipelines.SaveToSQLitePipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Scrapeops settings
SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = "https://headers.scrapeops.io/v1/user-agents"
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = (
    "https://headers.scrapeops.io/v1/browser-headers"
)
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5

# Proxy settings
# Proxies are used to disguise the IP address of the scraper, so that the
# website doesn't block it
# A possible source of free proxies is https://free-proxy-list.net/ or
# https://geonode.com/free-proxy-list
# ! Free proxies can be considerably slow
ROTATING_PROXY_LIST = [
    "177.101.135.84:5678",
    "66.97.37.164:80",
    "103.76.188.241:4153",
]
# Alternatively, you can read the proxies from a file
# ROTATING_PROXY_LIST_PATH = "proxies.txt"
