from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://www.kinopoisk.ru'
params = {'quick_filters':'serials',
          'tab':'all'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

html = requests.get(main_link + '/popular/films/',params=params,headers=headers)

soup = bs(html.text,'html.parser')

serials_block = soup.find('div',{'class':'selection-list'})
serials_list = serials_block.find_all('div',{'class':'desktop-rating-selection-film-item'})


serials = []
for serial in serials_list:
    serial_data = {}
    serial_info = serial.find('p')
    serial_link = main_link + serial_info.parent['href']
    serial_name = serial_info.getText()
    serial_genre = serial.find('span',{'class':'selection-film-item-meta__meta-additional-item'}).nextSibling.getText()
    serial_rating = serial.find('span',{'class':'rating__value'})
    if serial_rating:
        serial_rating = serial_rating.getText()
        try:
            serial_rating = float(serial_rating)
        except:
            pass

    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['genre'] = serial_genre
    serial_data['rating'] = serial_rating

    serials.append(serial_data)

pprint(serials)