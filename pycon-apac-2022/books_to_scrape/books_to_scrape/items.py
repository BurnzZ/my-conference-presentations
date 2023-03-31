# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Optional

from scrapy_jsonschema.item import JsonSchemaItem


@dataclass
class BookItem:
    url: str
    category_name: Optional[str] = None
    title: Optional[str] = None
    price: Optional[str] = None
    availability: Optional[str] = None


class BookSchemaItem(JsonSchemaItem):
    jsonschema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Book",
        "description": "A Book item extracted from books.toscrape.com",
        "type": "object",
        "properties": {
            "url": {
                "description": "Book's URL",
                "type": "string",
                "pattern": "^https?://[\\S]+$",
            },
            "category_name": {
                "description": "Name of the category which the book belongs to",
                "type": "string",
            },
            "title": {"description": "Book's title", "type": "string"},
            "price": {"description": "Book's price", "minimum": 0, "type": "number"},
            "availability": {"description": "Book's availability", "type": "string"},
        },
        "required": ["url"],
    }
