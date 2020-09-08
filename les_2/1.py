from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'http://127.0.0.1:5000/'
html = requests.get(main_link)

soup = bs(html.text,'html.parser')

a = soup.find('a')


div = a.parent.parent  #Получаем родителя

div.children #Возвращает всех детей со скрытыми нодами
div.findChildren()  #Возвращает всех потомков

children = div.findChildren(recursive=False)
children[0].findNextSibling()
children[1].findPreviousSibling()

# pprint(div)

elem = soup.find_all(attrs={'id':'d'})

elem2 = soup.find_all('p',{'class':['red paragraph','red paragraph left']})

elem3 = soup.find_all('p', limit = 3)

elem4 = soup.find(text='Шестой параграф')
print(type(elem4))

pprint(elem4.parent)

