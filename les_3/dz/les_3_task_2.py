"""
2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы.
 Поиск по двум полям (мин и макс зарплату)
"""
from pymongo import MongoClient
from pprint import pprint

# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['vacs_db']
vacs_coll = db.vacs_coll

# for user in vacs_coll.find({'$or':[{'sal_min':'','age':43},{'author':'Anna','age':36}]}):
#       pprint(user)

# sal = int(input('Введите минимальную зарплату в месяц: '))
sal = 100000
for user in vacs_coll.find({'$or':
                                [{'sal_min': {'$exists': 'true', '$ne': ''}},
                                 {'sal_max': {'$exists': 'true', '$ne': ''}}]}):

    pprint(user)
