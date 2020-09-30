from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from les_8_scrapy.spiders.igm import IgmSpider
from les_8_scrapy import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(IgmSpider)
    process.start()