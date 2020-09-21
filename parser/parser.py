'''
    Парсер логиниться на сайт onlinemektep.org проходится по старнице уроков
    и считывает оценки полученные учениками за прохождение уроков онлайн
    результаты сохраняет в csv файл по дням недели

    Используется файл config.py
    где хрангяться логин и пароль
    в виде
    login = 'login'
    password = 'password'
    для входа на сайт onlinemektep.org
'''
import time
#from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
from config import login, password
import requests
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=chrome_options)

start_url = "https://onlinemektep.org/login"
driver.get(start_url)

def write_csv(data, name):
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],
                        data['ex'],
                        data['price'],
                        data['total']))


def locator_all(xpath):
    return WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


def locator_click(xpath):
    button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
    button.click()


def locator_link(link):
    link = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, link)))
    link.click()


def locator_send(xpath, key):
    sender = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
    sender.send_keys(key)


#переключение на русский

driver.find_element(By.XPATH, "//span[@class='sa-header__menu-item ol-str-ico ol-ico--fa ol-ico--fa-solid ol-ico--thm-globe']").click()

locator_click("//li[@class='sa-dropdown__area-item']")

#авторизация
locator_send("//input[@type='text']", login)
locator_send("//input[@type='password']", password)
locator_click("//button[@type='submit']")

#переход на страницы предметов

locator_link("Домашние задания")
time.sleep(5)
locator_link("Расписание")

#Получаем текущий день недели
#day = str(datetime.now().weekday())

# Сворачиваем меньшку чтобы не мешала
locator_click("//div[@class='ol-ico ol-ico--fa ol-ico--thm-chevron-left']")

# Собираем все кнопки  "перейти"

table = driver.find_elements(By.TAG_NAME, 'td')

buttons = []
for i in range(len(table)):
   if table[i].get_attribute('data-table-head') == 'Урок':
       buttons.append(table[i].find_element(By.XPATH, "//button[@class='ol-btn ol-w-100 ol-notify-count__wrapper  ol-btn--thm-aqua']"))

# Кликаем по кнопкам и собираем страницы с оценками
pages = []
for i in range(len(buttons)):
    buttons[i].click()
    time.sleep(5)
    tables = driver.find_elements(By.XPATH, "//div[@class='ol-week__tab']")
    for j in range(len(tables)):
        print(tables[j].text)

#     pages.append(driver.page_source)
#     driver.back()
#
# print(pages)







#buttons = locator_all("//button[@class='ol-btn ol-w-100 ol-notify-count__wrapper  ol-btn--thm-aqua']")


