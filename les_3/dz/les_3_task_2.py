"""
2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы.
 Поиск по двум полям (мин и макс зарплату)
"""
from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import requests


# Функция поиска по условиям задания
def greater_sal(sal_by_today_curr):
    res = []
    for sal_cur in sal_by_today_curr:
        # print(sal_cur)
        # print(f'sal: {sal_by_today_curr[sal_cur]}')
        for vac in vacs_coll.find({'$or':
                                        [{'sal_min': {'$ne': None}, 'sal_max': {'$eq': None}},
                                         {'sal_max': {'$gt': sal_by_today_curr[sal_cur]}, 'sal_cur': {'$eq': sal_cur}},
                                         ]}):
            res.append(vac)
            # print(vac)
    return res


# Получить из базы список валют, кроме рубля
def get_cur():
    curs = set()
    for user in vacs_coll.find({'$and': [{'sal_cur': {'$ne': 'руб.'}}, {'sal_cur': {'$ne': ''}}]}):
        curs.add(user['sal_cur'])
    return list(curs)


# Функция конвертации зарплаты в другие валюты, найденные в базе.
# Для получения актуальных курсов используется сервис currconv.com
def convert_sal_to_curs(sal_rub, curs):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    lnk = 'https://free.currconv.com/api/v7/convert'
    curs_dict = {
        'руб.': sal
    }
    from_currency = "RUB"
    for to_currency in curs:
        params = {
            'q': f'{from_currency}_{to_currency}',
            'compact': 'ultra',
            'apiKey': 'bc0cdef88cfee95777d6'
        }
        # pprint(params)
        response = requests.get(lnk, headers=headers, params=params)
        j_data = response.json()
        curs_dict[to_currency] = float(j_data[params['q']]) * sal_rub
    return curs_dict


# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['vacs_db']
vacs_coll = db.vacs_coll

sal = int(input('Введите минимальную зарплату в месяц (в рублях): '))
# sal = 500000

curs = get_cur()
# Зарплата, конвертированная в валюты, найденные в вакансиях в базе
sal_by_today_curr = convert_sal_to_curs(sal, curs)
# sal_by_today_curr = {
#     'руб.': sal,
#     'USD': 0.011273 * sal,
#     'EUR': 0.013365 * sal
# }

search_vac = pd.DataFrame(greater_sal(sal_by_today_curr))
search_vac.to_csv('search_vac.csv', index=False)

