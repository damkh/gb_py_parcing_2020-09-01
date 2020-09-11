"""
1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД

Установлен сервер MongoDB 4.4.1, скриншот les_3_task_1.png
"""
from pymongo import MongoClient
import csv


# Загрузка вакансий из CSV файла в список словарей
def csv_to_list(path):
    reader = csv.DictReader(open(path, 'r'))
    vacs_list = []
    for vac in reader:
        vacs_list.append(vac)
    return vacs_list


vacs = csv_to_list('../../les_2/dz/vacs.csv')
for el in vacs:
    if el['sal_max']:
        el['sal_max'] = int(el['sal_max'])
    else:
        el['sal_max'] = None
    if el['sal_min']:
        el['sal_min'] = int(el['sal_min'])
    else:
        el['sal_min'] = None


# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['vacs_db']
vacs_coll = db.vacs_coll

vacs_coll.insert_many(vacs)
