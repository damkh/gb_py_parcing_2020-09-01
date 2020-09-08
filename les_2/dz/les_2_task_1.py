"""
Вариант 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
- Наименование вакансии.
- Предлагаемую зарплату (отдельно минимальную и максимальную).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.

На сайте hh.ru посик производится по региону Москва (area=1).
Результаты записываются в список all_vac.
Пролистывание страниц производится по определению атрибута 'data-page' кнопки 'дальше' на каждой итерации.
"""

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd


def hh_search(search_vac):
    lnk = f'https://hh.ru'
    site_vac = []
    page = 0
    search_pers = {
        1: 'день',
        3: '3 суток',
        7: 'неделя',
        30: 'месяц'
    }
    while page is not None:
        page_vac = []
        params = {'area': 1,
                  'fromSearchLine': 'true',
                  'st': 'searchVacancy',
                  'text': search_vac,
                  'from': 'cluster_area',
                  'enable_snippets': 'true',
                  'clusters': 'true',
                  'L_save_area': 'true',
                  'customDomain': 1,
                  'search_period': search_pers[30],
                  'page': page
                  }
        html = requests.get(lnk + '/search/vacancy', params=params, headers=headers)
        soup = bs(html.text, 'html.parser')
        vac_block = soup.find('div', {'class': 'vacancy-serp'})
        vacs = vac_block.find_all('div', {'class': 'vacancy-serp-item'})
        for vac in vacs:
            vac_data = {}
            vac_head = vac.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
            vac_a = vac_head.find('div', {'class': 'vacancy-serp-item__info'}).find('a')
            vac_name = vac_a.getText()
            vac_link = vac_a['href'].split('?')[0]
            vac_sal_block = vac_head.find('div', {'class': 'vacancy-serp-item__sidebar'})
            try:
                vac_sal_str = vac_sal_block.find('span').getText()
                vac_sal_split = vac_sal_str.split()
                if vac_sal_split[0] == 'до':
                    vac_sal_min = ''
                    vac_sal_max = int(''.join(vac_sal_split[1:-1]))
                    vac_sal_cur = vac_sal_split[-1]
                elif vac_sal_split[0] == 'от':
                    vac_sal_min = int(''.join(vac_sal_split[1:-1]))
                    vac_sal_max = ''
                    vac_sal_cur = vac_sal_split[-1]
                else:
                    vac_sal_split = vac_sal_str.split('-')
                    vac_sal_min = int(vac_sal_split[0].replace('\xa0', ''))
                    vac_sal_max = int(vac_sal_split[1].split(' ')[0].replace('\xa0', ''))
                    vac_sal_cur = vac_sal_split[1].split(' ')[1]
                vac_sal_term = search_pers[30]
            except:
                vac_sal_min = ''
                vac_sal_max = ''
                vac_sal_cur = ''
                vac_sal_term = ''
            vac_data['name'] = vac_name
            vac_data['link'] = vac_link
            vac_data['sal_min'] = vac_sal_min
            vac_data['sal_max'] = vac_sal_max
            vac_data['sal_cur'] = vac_sal_cur
            vac_data['sal_term'] = vac_sal_term
            vac_data['site'] = lnk
            page_vac.append(vac_data)
        site_vac += page_vac
        try:
            page = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['data-page']
        except:
            page = None
    return site_vac


def make_full_link(site, rel_lnk):
    if 'http://' not in rel_lnk or 'https://' not in rel_lnk:
        return site + rel_lnk


def sj_search(search_vac):
    lnk = f'https://superjob.ru'
    site_vac = []
    page = 1
    while page is not None:
        page_vac = []
        params = {'geo[t][0]': 4,
                  'keywords': search_vac,
                  'page': page
                  }
        html = requests.get(lnk + '/vacancy/search/', params=params, headers=headers)
        soup = bs(html.text, 'html.parser')
        vac_block = soup.find('div', {'class': '_1Ttd8 _2CsQi'})
        vacs = vac_block.find_all('div', {'class': 'Fo44F QiY08 LvoDO'})
        for vac in vacs:
            vac_data = {}
            vac_head = vac.find('div', {'class': 'jNMYr GPKTZ _1tH7S'})
            vac_a = vac_head.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).find('a')
            vac_name = vac_a.getText()
            vac_link = vac_a['href'].split('?')[0]
            vac_link_full = make_full_link(lnk, vac_link)
            vac_sal_block = vac_head.find('span', {'class': 'f-test-text-company-item-salary'})
            try:
                vac_sal_str = vac_sal_block.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
                vac_sal_term = vac_sal_block.find('span', {'class': '_3mfro PlM3e _2JVkc _2VHxz'}).getText()
                vac_sal_split = vac_sal_str.split()
                if vac_sal_split[0] == 'до':
                    vac_sal_min = ''
                    vac_sal_max = int(''.join(vac_sal_split[1:-1]))
                    vac_sal_cur = vac_sal_split[-1]
                elif vac_sal_split[0] == 'от':
                    vac_sal_min = int(''.join(vac_sal_split[1:-1]))
                    vac_sal_max = ''
                    vac_sal_cur = vac_sal_split[-1].split('/')[0]
                elif vac_sal_split[0] == 'По':
                    vac_sal_min = ''
                    vac_sal_max = ''
                    vac_sal_cur = ''
                    vac_sal_term = ''
                else:

                    if '—' in vac_sal_str:
                        vac_sal_split = vac_sal_str.split('—')
                        vac_sal_min = int(vac_sal_split[0].replace('\xa0', ''))
                        vac_sal_max_str = ''
                        vac_sal_max_raw = vac_sal_split[1].split('\xa0')
                        for dig in vac_sal_max_raw:
                            if dig.isdigit():
                                vac_sal_max_str += dig
                            else:
                                vac_sal_cur = dig
                        vac_sal_max = int(vac_sal_max_str)
                    else:
                        vac_sal_max_str = ''
                        vac_sal_max_raw = vac_sal_str.split('\xa0')
                        for dig in vac_sal_max_raw:
                            if dig.isdigit():
                                vac_sal_max_str += dig
                            else:
                                vac_sal_cur = dig
                        vac_sal_max = int(vac_sal_max_str)
                        vac_sal_min = vac_sal_max
            except:
                vac_sal_min = ''
                vac_sal_max = ''
                vac_sal_cur = ''
                vac_sal_term = ''
            vac_data['name'] = vac_name
            vac_data['link'] = vac_link_full
            vac_data['sal_min'] = vac_sal_min
            vac_data['sal_max'] = vac_sal_max
            vac_data['sal_cur'] = vac_sal_cur
            vac_data['sal_term'] = vac_sal_term
            vac_data['site'] = lnk
            page_vac.append(vac_data)
        site_vac += page_vac
        try:
            page = soup.find('a', {'class': 'f-test-link-Dalshe'})['href'].split('page=')[1]
        except:
            page = None
    return site_vac


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
# search_vac = input('Введите искомую вакансию: ')
all_vac = []
search_vac = 'java senior developer'
all_vac += hh_search(search_vac)
all_vac += sj_search(search_vac)


pprint(all_vac)
# print(f'Найдено вакансий: {len(all_vac)}')
# all_vac_pd = pd.DataFrame(all_vac)

