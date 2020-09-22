import scrapy
from scrapy.http import HtmlResponse
from scrapy_proj_les_6.items import ScrapyProjLes6Item


class Book24RuSpider(scrapy.Spider):
    name = 'book24_ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D0%BE%D0%B2%D0%B0%D1%80']

    def parse(self, response):
        book_links = response.css('a.book__title-link::attr(href)').extract()
        for link in book_links:
            yield response.follow(link, callback=self.bookpage_parse)
        next_page = response.xpath("//a[contains(@class, '_text') and text()='Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def bookpage_parse(self, response: HtmlResponse):
        link = response.url
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//span[text()='Автор:']/following-sibling::span/a/text()").extract_first()
        main_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        if not main_price:
            main_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        discount_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        rating = response.css('span.rating__rate-value::text').extract_first()
        yield ScrapyProjLes6Item(title=title, authors=authors, main_price=main_price, discount_price=discount_price,
                                 rating=rating, link=link)
