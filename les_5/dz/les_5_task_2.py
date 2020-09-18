"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""
from selenium import webdriver
import time
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox('/opt/Webdriver')
main_link = "https://www.mvideo.ru/"
driver.get(main_link)

# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_ru']
hits = db.hits

time.sleep(3)
# hit_items = []
while True:
    try:
        button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "(//div[@class='gallery-layout sel-hits-block '])"
                                                    "[2]/div/div/div/div/a[@class='next-btn sel-hits-button-next']"))
                )
        button.click()
        time.sleep(3)
    except:
        print('OUT')
        hit_block = driver.find_elements_by_xpath("(//div[@class='gallery-layout sel-hits-block '])[2]")
        items_a = hit_block[0].find_elements_by_xpath(
            ".//ul/li[@class='gallery-list-item height-ready']/div/div/div/a"
        )
        for item in items_a:
            item_link = item.get_attribute('href')
            data_dict = eval(item.get_attribute('data-product-info').replace('\t', '').replace('\n', ''))
            hit_item_dict = {
                'Product_name': data_dict['productName'],
                'Product_category': data_dict['productCategoryName'],
                'Product_price': float(data_dict['productPriceLocal']),
                'Product_link': item_link
            }
            # hit_items.append(hit_item_dict)
            hits.insert_one(hit_item_dict)
        break
