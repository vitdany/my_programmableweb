# 1) Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных (от кого,
# дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172
#
# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники
# mvideo и складывает данные в БД. Магазины можно выбрать свои.
#     Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pprint import pprint
from selenium.webdriver.chrome.options import Options


def get_letters_from_mail():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Режим без интерфейса
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.get("https://account.mail.ru/login")

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    element = driver.find_element_by_name("username")
    element.send_keys("study.ai_172")
    element = driver.find_element_by_xpath("//button[@data-test-id='next-button']")
    element.submit()

    driver.implicitly_wait(10)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    element.send_keys('NextPassword172')
    element.send_keys(Keys.ENTER)

    print("password ok")
    driver.implicitly_wait(10)  # seconds
    dataset = driver.find_element_by_class_name('dataset-letters')
    elements = dataset.find_elements_by_class_name('llc')
    print(f'Find {len(elements)} letters')
    items = []
    for element in elements:
        item = {}
        item['correspondent'] = element.find_element_by_class_name('llc__item_correspondent').text
        item['llc__item_title'] = element.find_element_by_class_name('llc__item_title').text
        item['llc__item_date'] = element.find_element_by_class_name('llc__item_date').text
        item['href'] = element.get_attribute('href')
        item['text'] = 'empty'
        items.append(item)

    for item in items:
        driver.get(item['href'])
        item['text'] = driver.find_element_by_class_name('letter-body').text
        print(f' {item["correspondent"]}')

    return items




import json
def get_data_from_mvideo():
    articals = []
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    #chrome_options.add_argument("--headless")  # Режим без интерфейса не работает?
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.mvideo.ru/")
    #driver.refresh()
    driver.implicitly_wait(10)  # seconds
    nclick = 0
    aset = set()
    while nclick < 3:
        sections = driver.find_elements_by_class_name('section')
        section = sections[3]
        elements = section.find_elements_by_class_name('fl-product-tile-title__link')
        for element in elements:
            s = element.get_attribute('data-product-info')
            aset.add(s)

        next_btn = section.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div[4]/div/div[2]/div/div[1]/a[2]")
        next_btn.click()
        time.sleep(2)
        nclick += 1

    for i in aset:
        d = json.loads(i)
        articals.append(d)

    pprint(articals)
    print(len(aset))
    print(f'total articals :{len(articals)}')
    return articals


def write(adata):
    if len(adata) < 1: return
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hot_articals']
    dblist = client.list_database_names()
    print(dblist)
    collection = db.collection_hot_articals
    collection.drop()
    print(f'Count docs = {collection.count_documents({})}')
    collection.insert_many(adata)
    print(f'Count docs = {collection.count_documents({})}')




print('Task 1. Mail.ru')
items = get_letters_from_mail()
pprint(items)

print('Task 2. mvideo.ru')
write(get_data_from_mvideo())

