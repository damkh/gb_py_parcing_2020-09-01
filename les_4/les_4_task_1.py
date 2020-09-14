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
from datetime import date,timedelta


def search_lenta_ru():
    main_link = 'https://lenta.ru'
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


def search_yandex_ru():
    main_link = 'https://yandex.ru/news/rubric/cosmos'
    response = requests.get(main_link)
    root = html.fromstring(response.text)
    news_block = root.xpath(
        "//div[@class='mg-grid__col mg-grid__col_xs_12 mg-grid__col_sm_9']/*/div[contains(@class, 'mg-grid__col mg-grid__col_xs_')]/article"
    )

    for news in news_block:
        if 'mg-grid__col_xs_8' in news.attrib['class']:
            news_title = news.xpath(".//div/a/h2/text()")[0]
            news_src = news.xpath(
                ".//div/div/div/div[@class='mg-card-source news-card__source']/span/a/text()"
            )[0]
            news_datetime = news.xpath(
                ".//div/div/div/div[@class='mg-card-source news-card__source']/span/text()"
            )[0]
        else:
            news_title = news.xpath(".//a/h2/text()")[0]
            news_src = news.xpath(
                ".//div/div/div[@class='mg-card-source news-card__source']/span/a/text()"
            )[0]
            news_datetime = news.xpath(
                ".//div/div/div[@class='mg-card-source news-card__source']/span/text()"
            )[0]
        news_link = news.xpath(".//*/*/a/@href")[0]

        if len(news_datetime) == 5:
            news_datetime = f'{date.today().isoformat()} {news_datetime}'
        else:
            news_datetime_split = news_datetime.split(' ')
            if news_datetime_split[0] == 'вчера':
                news_datetime = f"{(date.today() - timedelta(1)).isoformat()} {news_datetime_split[2]}"

        news_dict = {
            'Title': news_title,
            'Datetime': news_datetime,
            'Source': news_src,
            'Link': news_link
        }
        all_news.append(news_dict)
        # print(news_title, news_link, news_datetime, news_src)


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}

all_news = []
# search_lenta_ru()
search_yandex_ru()

pprint(all_news)
