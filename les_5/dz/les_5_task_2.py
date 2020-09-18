"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""
from selenium import webdriver
import time
from datetime import date
from pymongo import MongoClient

driver = webdriver.Firefox('/opt/Webdriver')
driver.get("https://www.mvideo.ru/")

#
# while True:
time.sleep(3)
button = driver.find_element_by_xpath(
    "//div[@class='gallery-layout sel-hits-block ']/div/div/div/div/a[@class='next-btn sel-hits-button-next']"
)
time.sleep(3)
button.click()
print()