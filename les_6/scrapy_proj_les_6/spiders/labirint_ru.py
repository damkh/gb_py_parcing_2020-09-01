import scrapy
from scrapy.http import HtmlResponse
from scrapy_proj_les_6.items import ScrapyProjLes6Item


class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D0%BE%D0%B2%D0%B0%D1%80/?order=relevance&way=back&stype=0&paperbooks=1&ebooks=1&available=1&preorder=1&wait=1&no=1&price_min=&price_max=']

    def parse(self, response):
        book_links = response.css('a.product-title-link::attr(href)').extract()
        for link in book_links:
            yield response.follow(link, callback=self.bookpage_parse)
        next_page = response.css('a.pagination-next__text::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def bookpage_parse(self, response:HtmlResponse):
        link = response.url
        title = response.xpath("//span[@class='only_desc']/text()").extract_first() # .split('"')[1]
        authors = response.xpath("//div[@class='authors']/a[@class='analytics-click-js']/text()").extract_first()
        main_price = response.css('span.buying-priceold-val-number::text').extract_first()
        discount_price = response.css('span.buying-pricenew-val-number::text').extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()
        yield ScrapyProjLes6Item(title=title, authors=authors, main_price=main_price, discount_price=discount_price,
                                 rating=rating, link=link)
