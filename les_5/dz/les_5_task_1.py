"""
1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные
о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
"""
from selenium import webdriver
import time
from datetime import date
from pymongo import MongoClient

driver = webdriver.Firefox('/opt/Webdriver')
driver.get("http://mail.ru")

elem = driver.find_element_by_xpath("//input[@id='mailbox:login-input']")
elem.send_keys('study.ai_172')
elem.submit()

time.sleep(2)
elem = driver.find_element_by_xpath("//input[@id='mailbox:password-input']")
elem.send_keys('SomePassword')
elem.submit()

time.sleep(5)

# Определение количества писем в папке Входящие
try:
    mail_quantity = int(driver.find_elements_by_xpath("//a[@href='/inbox/']")[0].get_attribute('title').split()[1])
    flag = True
except:
    flag = False
    mail_quantity = 0
    print('ящик пустой')

all_mails_links = set()
while flag:
    time.sleep(2)
    emails = driver.find_elements_by_xpath("//a[contains(@class, 'js-letter-list-item')]")
    time.sleep(2)
    for email in emails:
        email_link = email.get_attribute('href')
        all_mails_links.add(email_link)
    driver.execute_script("arguments[0].scrollIntoView();", emails[-1])
    time.sleep(2)
    if len(all_mails_links) > mail_quantity:
        flag = False

# Инициализация MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['mail_ru']
inbox = db.inbox

for email_link in all_mails_links:
    driver.get(email_link)
    time.sleep(5)
    email_from = driver.find_element_by_xpath(
        "//div[@class='letter__author']/span[@class='letter-contact']"
    ).get_attribute('title')
    email_subject = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    email_datetime = driver.find_element_by_xpath("//div[@class='letter__date']").\
        text.replace('Сегодня', date.today().isoformat())
    email_body = driver.find_element_by_xpath("//div[contains(@class,'cl_')]")
    email_body_text = email_body.text
    # Все HTML-содержимое тела письма, закомментировал, чтоб не засорять
    # email_body_html = email_body.get_attribute("innerHTML")
    email_dict = {
        'Subject': email_subject,
        'Datetime': email_datetime,
        'From': email_from,
        'Link': email_link,
        'Body_text': email_body_text,
        # 'Body_html': email_body_html
    }
    inbox.insert_one(email_dict)
