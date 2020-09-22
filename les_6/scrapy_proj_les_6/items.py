# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjLes6Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    main_price = scrapy.Field()
    discount_price = scrapy.Field()
    rating = scrapy.Field()
    link = scrapy.Field()
    pass
