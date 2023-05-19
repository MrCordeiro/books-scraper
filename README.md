# Books Scraper Sandbox

A sandbox for testing and developing `Scrapy` spiders.

## Development

### Start a Scrapy project

```bash
scrapy startproject <project_name> [project_dir]
```

### Create a spider

```bash
cd <project_dir>/spiders
scrapy genspider <spider_name> <url_domain_to_be_scraped>
```

Use the scrapy shell to determine the correct CSS selectors for the spider. Open it with the `scrapy shell` command. Then, use the following template commands to test how the page could be scraped.

```python
fetch('<url_to_be_scraped>')
items = response.css('<css_selector>')
item = items[0]

# Iteractively test the CSS selectors and see if they return the correct values
item.css('<css_selector>').get()

# To get attributtes
item.css('<css_selector>').attrib['<attribute_name>']
```

### Run the spider

```bash
scrapy crawl <spider_name> -O <output_file_name>
```

## Deployment

### Deployment services

- [ScrapyD](https://github.com/scrapy/scrapyd): **Free and open source** application that allows us to deploy Scrapy spiders on a server and run them remotely. You'll need your own server to deploy the spiders. There is not scheduling or monitoring. Control is done via a REST API. UI is done via 3rd party tools.
- [ScrapeOps](https://scrapeops.io): **Paid and free** service that allows us to deploy Scrapy spiders on a server and run them remotely. It has scheduling and monitoring. Built-in UI and monitoring.
- [ScrapyCloud](https://www.zyte.com/scrapy-cloud/): **Paid** service that allows us to deploy Scrapy spiders on their servers and run them remotely. It has scheduling and monitoring. Built-in UI and monitoring.
