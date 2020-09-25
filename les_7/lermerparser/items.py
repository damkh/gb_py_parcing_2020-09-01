# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join, Compose
from w3lib.html import remove_tags


def to_float(value):
    try:
        return float(value)
    except:
        return value

def remove_empty_space(value):
    try:
        return value.replace('\t', ' ').replace('\n', ' ').replace('  ', '').strip(' ')
    except:
        return value

class LermerparserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=Join('.'), output_processor=MapCompose(to_float))
    description = scrapy.Field(input_processor=Join(''), output_processor=TakeFirst())
    specifications_keys = scrapy.Field()
    specifications_vals = scrapy.Field(input_processor=MapCompose(remove_empty_space))
    link = scrapy.Field()
    # _id = scrapy.Field()

    # pass
