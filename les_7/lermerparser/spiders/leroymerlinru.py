import scrapy
from scrapy.http import HtmlResponse
from lermerparser.items import LermerparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, params, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={params["search"]}']


    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@class='plp-item__info__title']")
        for link in links:
            yield response.follow(link, callback=self.parse_prod)
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_prod(self, response:HtmlResponse):
        loader = ItemLoader(item=LermerparserItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[@srcset][1]/@srcset")
        loader.add_xpath('description', "//uc-pdp-section-vlimited/div/p//text()")
        loader.add_xpath('specifications_keys', "//dl/div/dt/text()")
        loader.add_xpath('specifications_vals', "//dl/div/dd/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@class='primary-price']/span[@slot='price' or @slot='fract']/text()")
        yield loader.load_item()
        # name = response.xpath("//h1/text()")
        # photos = response.xpath("//picture[@slot='pictures']/source[@srcset][1]/@srcset").extract()
        # print()
        # pass
        # yield LermerparserItem(name=name, photos=photos)