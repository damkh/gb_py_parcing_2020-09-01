"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл.

Выбран сервис kaggle.com. Для работы с api необходимо установить пакет kaggle (https://www.kaggle.com/docs/api).
Для аутентификации требуется скачать файл с токеном и выложить его в домашнюю директорию (~/.kaggle/kaggle.json).
Следующий код получает список сабмитов определенного пользователя (kaggle_username)
в определенном соревновании (kaggle_competition).
"""
import kaggle
import zipfile


kaggle_competition = 'realestatepriceprediction'
kaggle_username = 'damkkh'
# Результат запроса - zip архив с именем <competition_name>.zip
response = kaggle.api.competition_leaderboard_cli(kaggle_competition, download=True)
# Распаковка архива
with zipfile.ZipFile(f'{kaggle_competition}.zip', 'r') as zip_ref:
    zip_ref.extractall(kaggle_competition)
# В архиве лежит файл <competition_name>-publicleaderboard.csv.
# Открываем его и в списке сабмитов ищем совпадению по имени пользователя
with open(f'{kaggle_competition}/{kaggle_competition}-publicleaderboard.csv', 'r') as f:
    for submit in f:
        if submit.split(',')[1] == kaggle_username:
            print(submit, end='')
