"""
3) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта
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


# Проверка вакансии в базе по ссылке.
def vac_in_db(vac):
    i = 0
    for el in vacs_coll.find({'link': {'$eq': vac['link']}}):
        i += 1
        break
    if i > 0:
        return True
    return False


# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['vacs_db']
vacs_coll = db.vacs_coll

# Загрузка новых данных (пробовал вручную добавлять и изменять записи в файле)
new_vacs = csv_to_list('./vacs_20200911.csv')

# Запись в БД новых данных. Значение 'link' используется как ключ. Если его нет - до добавялем новый элемент.
# Если такой же 'link' уже есть, то обновляем данные.
for vac in new_vacs:
    if not vac_in_db(vac):
        vacs_coll.insert_one(vac)
    else:
        vacs_coll.update_one({'link': vac['link']}, {'$set': vac})
