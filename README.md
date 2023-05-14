# Bookscraper Sandbox

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
scrapy crawl <spider_name>
```
