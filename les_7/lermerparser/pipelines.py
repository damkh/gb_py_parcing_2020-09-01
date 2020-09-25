# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LermerparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.lm

    def process_item(self, item, spider):
        product = {
            'title': item.get('title'),
            'photos': item.get('photos'),
            'price': item.get('price')[0],
            'description': item.get('description'),
            'link': item.get('link')[0],
            'specifications': dict(
                zip(
                    item.get('specifications_keys'),
                    map(self.process_float, item.get('specifications_vals'))
                )
            )
        }

        collection = self.mongobase[spider.name]
        collection.insert_one(product)
        return item

    def process_float(self, val):
        try:
            return float(val)
        except:
            return val



class LermerPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [i[1] for i in results if i[0]]
        return item
