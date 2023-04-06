import scrapy


class Quotes7Spider(scrapy.Spider):
    name = "7-quotes"
    allowed_domains = ["quotes.toscrape.com"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            "http://quotes.toscrape.com/js",
            callback=self.parse,
            meta={"playwright": True},
        )

    def parse(self, response):
        for quote in response.css(".quote .text ::text").getall():
            yield {"quote": quote}
