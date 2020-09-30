# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Les8ScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    parse_username = scrapy.Field()
    user_id_of_obj = scrapy.Field()
    photo_of_obj = scrapy.Field()
    username_of_obj = scrapy.Field()
    type = scrapy.Field()
    # pass
