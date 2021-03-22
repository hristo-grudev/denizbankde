import scrapy


class DenizbankdeItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
