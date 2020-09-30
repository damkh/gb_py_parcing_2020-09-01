# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class Les8ScrapyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.igm


    def process_item(self, item, spider):
        account_data = {
            'user_id_of_obj': item.get('user_id_of_obj'),
            'photo_of_obj': item.get('photo_of_obj'),
            'username_of_obj': item.get('username_of_obj'),
            'type': item.get('type')
        }

        collection = self.mongobase[item.get('parse_username')]
        collection.insert_one(account_data)
        return item
