"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""
from selenium import webdriver
import time
from datetime import date
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox('/opt/Webdriver')
driver.get("https://www.mvideo.ru/")

#
# while True:
time.sleep(3)
# button = driver.find_element_by_xpath(
#     "//div[@class='gallery-layout sel-hits-block ']/div/div/div/div/a[@class='next-btn sel-hits-button-next']"
# )
while True:
    try:
        button = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//div[@class='gallery-layout sel-hits-block ']/div/div/div/div/a[@class='next-btn sel-hits-button-next']"))
                )
        button.click()
    except:
        print('OUT')
        break

# next-btn sel-hits-button-next disabled
# //div[@class='gallery-layout sel-hits-block ']/div/div/div/div/div/ul/li[@class='gallery-list-item height-ready']
time.sleep(3)
# button.click()
print()