import scrapy
from books_to_scrape.page_objects import BookCategoryPage, BookPage, HomePage


class Books5Spider(scrapy.Spider):
    name = "5-books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    custom_settings = {
        "SPIDERMON_ENABLED": True,
        "EXTENSIONS": {
            "spidermon.contrib.scrapy.extensions.Spidermon": 500,
        },
        "SPIDERMON_SPIDER_CLOSE_MONITORS": "spidermon.contrib.scrapy.monitors.SpiderCloseMonitorSuite",
        "SPIDERMON_MIN_ITEMS": 10,
        "SPIDERMON_MAX_ERRORS": 1,
        "SPIDERMON_MAX_WARNINGS": 1000,
        "SPIDERMON_ADD_FIELD_COVERAGE": True,
    }

    def parse(self, response, page: HomePage):
        for url in page.category_urls:
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response, page: BookCategoryPage):
        raise ValueError  # simulate that something has gone wrong

        for url in page.book_urls:
            yield response.follow(
                url,
                callback=self.parse_book,
                cb_kwargs={"category_name": page.category_name},
            )

            if next_page_url := page.next_page_url:
                yield response.follow(
                    next_page_url,
                    callback=self.parse_category,
                )

    def parse_book(self, response, page: BookPage, category_name):
        item = page.to_item()
        item.category_name = category_name
        yield item
