"""
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
"""

from pprint import pprint
from lxml import html
import requests


def search_lenat_ru():
    response = requests.get(main_link)
    root = html.fromstring(response.text)
    news_block = root.xpath(
        "//section[@class='row b-top7-for-main js-top-seven']/div[@class='span4']/div[contains(@class,'item')]"
    )

    for news in news_block:
        if news.attrib['class'] == 'first-item':
            news_link_part = news.xpath(".//h2/a/@href")[0]
            news_title = news.xpath(".//h2/a/text()")[0].replace('\xa0', ' ')
            news_datetime = news.xpath(".//h2/a/time")[0].attrib['datetime']
        else:
            news_link_part = news.xpath(".//a/@href")[0]
            news_title = news.xpath(".//a/text()")[0].replace('\xa0', ' ')
            news_datetime = news.xpath(".//a/time")[0].attrib['datetime']

        if 'https://' in news_link_part:
            news_src = news_link_part.split('/')[2]
            news_link = news_link_part
        else:
            news_src = main_link.split('/')[2]
            news_link = main_link

        news_dict = {
            'Title': news_title,
            'Datetime': news_datetime,
            'Source': news_src,
            'Link': news_link
        }
        all_news.append(news_dict)
        # print()
        # print(news_title, news_link, news_time, news_src)


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
main_link = 'https://lenta.ru'
all_news = []
search_lenat_ru()

pprint(all_news)
