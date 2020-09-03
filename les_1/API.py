#e5e4cd692a72b0b66ea0a6b80255d1c3
#https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=439d4b804bc8187953eb36d2a8c26a02
from pprint import pprint
import requests
main_link = 'https://api.openweathermap.org/data/2.5/weather'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
           'Accept':'*/*'}

params = {'q':'Paris',
          'appid':'e5e4cd692a72b0b66ea0a6b80255d1c3'}

response = requests.get(main_link,headers=headers,params=params)
j_data = response.json()
# pprint(response.json())
print(f"В городе {j_data['name']} температура {j_data['main']['temp'] -273.15} градусов")

