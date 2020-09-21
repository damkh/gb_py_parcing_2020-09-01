from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy_proj_les_6.spiders.labirint_ru import LabirintRuSpider
from scrapy_proj_les_6 import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintRuSpider)

    process.start()