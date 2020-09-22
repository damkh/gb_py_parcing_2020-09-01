# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ScrapyProjLes6Pipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books


    def process_item(self, item, spider):
        book = {
            'authors': self.process_none(item.get('authors')),
            'title': self.process_title(item.get('title')),
            'main_price': self.process_float(item.get('main_price')),
            'discount_price': self.process_float(item.get('discount_price')),
            'rating': self.process_float(item.get('rating')),
            'link': self.process_none(item.get('link'))
        }
        collection = self.mongobase[spider.name]
        collection.insert_one(book)
        return item


    def process_float(self, val):
        try:
            float_val = float(val.replace(',', '.').replace('р.', '').replace(' ', ''))
            return float_val
        except:
            pass


    def process_title(self, val):
        try:
            split_val = val.split('"')[1]
            return split_val
        except:
            return val


    def process_none(self, val):
        if val:
            return val
        else:
            pass