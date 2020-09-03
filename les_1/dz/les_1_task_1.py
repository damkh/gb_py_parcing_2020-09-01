import requests
import json

username = 'damkh'
repos_lnk = f'https://api.github.com/users/{username}/repos'
headers = {'User-Agent': 'damkh',
           'Accept': 'application/vnd.github.v3+json'}

params = {'sort': 'full_name'}

response = requests.get(repos_lnk, headers=headers, params=params)
j_data = response.json()
with open('les_1_task_1.json', 'w') as f:
    json.dump(j_data, f)
with open('les_1_task_1.json') as f:
    data = json.load(f)
    for rep in data:
        print(rep['name'])

