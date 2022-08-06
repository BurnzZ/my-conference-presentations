import scrapy

from books_to_scrape.items import BookItem


class Books3Spider(scrapy.Spider):
    name = '3-books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for url in response.css(".nav-list ul li a ::attr(href)").getall():
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response):
        for url in response.css(".product_pod a ::attr(href)").getall():
            category_name = response.css(".page-header h1 ::text").get()
            yield response.follow(
                url,
                callback=self.parse_book,
                cb_kwargs={"category_name": category_name},
            )

            if next_page_url := response.css(".pager .next a ::attr(href)").get():
                yield response.follow(
                    next_page_url,
                    callback=self.parse_category,
                )

    def parse_book(self, response, category_name):
        item = {
            "category_name": category_name,
            "title": response.css(".product_main h1 ::text").get(),
            "price": response.css(".product_main .price_color ::text").get(),
            "url": response.url,
        }
        availability = response.css(".product_main .availability ::text").getall()
        item["availability"] = "".join(availability).strip()

        yield BookItem(**item)
