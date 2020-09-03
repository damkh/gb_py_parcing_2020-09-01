"""
1.  Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
    сохранить JSON-вывод в файле *.json.
"""
import requests
import json

username = input('Введите имя пользователя GitHub: ')
repos_lnk = f'https://api.github.com/users/{username}/repos'

# В качестве User-Agent указывается имя пользователя GitHub
headers = {'User-Agent': username,
           'Accept': 'application/vnd.github.v3+json'}

# Указывается сортировка по full_name
params = {'sort': 'full_name'}

# Запрос репозиториев для пользователя damkh и запись в json-файл les_1_task_1.json
response = requests.get(repos_lnk, headers=headers, params=params)
j_data = response.json()
with open('les_1_task_1.json', 'w') as f:
    json.dump(j_data, f)
# Чтение файла les_1_task_1.json и вывод списка репозиториев по ключу name
with open('les_1_task_1.json') as f:
    data = json.load(f)
    for rep in data:
        print(rep['name'])

