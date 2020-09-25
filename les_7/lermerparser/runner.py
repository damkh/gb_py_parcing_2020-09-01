from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import shutil
import os

from lermerparser import settings
from lermerparser.spiders.leroymerlinru import LeroymerlinruSpider

if __name__ == '__main__':
    try:
        os.system("rm -rf ./images")
        os.remove("./scrapy.log")
    except:
        pass
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, params={'search': 'морилка'})

    process.start()


# def func1(*args, **kwargs):