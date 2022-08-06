import scrapy


class Books1Spider(scrapy.Spider):
    name = '1-books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for url in response.css(".product_pod a ::attr(href)").getall():
            yield response.follow(url, callback=self.parse_book)

    def parse_book(self, response):
        item = {
            "title": response.css(".product_main h1 ::text").get(),
            "price": response.css(".product_main .price_color ::text").get(),
            "url": response.url,
        }
        availability = response.css(".product_main .availability ::text").getall()
        item["availability"] = "".join(availability).strip()

        yield item
