from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
# search_vac = input('Введите искомую вакансию: ')
# site = input('Введите сайт - "sj" или "hh": ')
search_vac = 'Data science'
site = 'hh'
if site == 'hh':
    lnk = f'https://{site}.ru'
    # all_vac = []
    page = 0
    # page_vac = []
    params = {'area': 1,
              'fromSearchLine': 'true',
              'st': 'searchVacancy',
              'text': search_vac,
              'from': 'cluster_area',
              'enable_snippets': 'true',
              'clusters': 'true',
              'L_save_area': 'true',
              'customDomain': 1,
              'page': page
              }
    # params = {
    #     'st': 'searchVacancy',
    #     'text': search_vac
    # }
    html = requests.get(lnk + '/search/vacancy', params=params, headers=headers)
    soup = bs(html.text, 'html.parser')
    vac_block = soup.find('div', {'class': 'vacancy-serp'})
    vacs = vac_block.find_all('div', {'class': 'vacancy-serp-item'})
    # pprint(html)

print()
