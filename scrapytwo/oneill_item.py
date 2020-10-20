from scrapy.item import Item, Field

class ScrapytwoItem(Item):
    url = Field()
    price = Field()