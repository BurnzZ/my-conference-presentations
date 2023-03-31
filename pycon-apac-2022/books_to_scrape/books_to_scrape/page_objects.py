from books_to_scrape.items import BookItem, BookSchemaItem
from web_poet import ItemWebPage, WebPage


class HomePage(WebPage):
    @property
    def category_urls(self):
        return self.css(".nav-list ul li a ::attr(href)").getall()


class BookCategoryPage(WebPage):
    @property
    def book_urls(self):
        return self.css(".product_pod a ::attr(href)").getall()

    @property
    def category_name(self):
        return self.css(".page-header h1 ::text").get()

    @property
    def next_page_url(self):
        return self.css(".pager .next a ::attr(href)").get()


class BookPage(ItemWebPage):
    def to_item(self):
        item = {
            "title": self.css(".product_main h1 ::text").get(),
            "price": self.css(".product_main .price_color ::text").get(),
            "url": self.url,
        }
        availability = self.css(".product_main .availability ::text").getall()
        item["availability"] = "".join(availability).strip()

        return BookItem(**item)


class BookPageUsingSchema(ItemWebPage):
    def to_item(self):
        item = {
            "title": self.css(".product_main h1 ::text").get(),
            "price": self.css(".product_main .price_color ::text").get(),
            "url": self.url,
        }
        availability = self.css(".product_main .availability ::text").getall()
        item["availability"] = "".join(availability).strip()

        return BookSchemaItem(**item)
