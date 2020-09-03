import requests
main_link = 'http://www.mail.ru'
pic_url = 'https://img.gazeta.ru/files3/845/7947845/upload-shutterstock_117062077-pic905v-895x505-99863.jpg'
response = requests.get(main_link)

response.status_code #Статус код ответа
# if response.ok:    #True если стаус код меньше 400

response.headers #Заголовки ответа от сервера
response.text    #Текстовое содержимое ответа от сервера

# pic = requests.get(pic_url)
#
# with open('sea.jpg','wb') as f:
#     f.write(pic.content)

print()