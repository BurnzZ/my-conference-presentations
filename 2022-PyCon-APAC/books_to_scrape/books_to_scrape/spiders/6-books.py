import scrapy
from books_to_scrape.page_objects import (BookCategoryPage,
                                          BookPageUsingSchema, HomePage)


class Books6Spider(scrapy.Spider):
    name = "6-books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_jsonschema.JsonSchemaValidatePipeline": 100,
        }
    }

    def parse(self, response, page: HomePage):
        for url in page.category_urls:
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response, page: BookCategoryPage):
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

    def parse_book(self, response, page: BookPageUsingSchema, category_name):
        item = page.to_item()
        item["category_name"] = category_name
        yield item
