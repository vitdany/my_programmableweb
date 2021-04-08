# Написать приложение, которое собирает основные новости
# с сайтов news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

from pprint import pprint
from lxml import html
import requests
#from pymongo import MongoClient

#client = MongoClient('mongodb://localhost:27017/')

#db = client['my_news']
#dblist = client.list_database_names()
#print(dblist)
#collection = db.collection_mynews
#collection.drop()
#print(f'Count docs = {collection.count_documents({})}')

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

def request_to(news):
    for link in news:
        response = requests.get(link['source'], headers=header)
        root = html.fromstring(response.text)
        titles = root.xpath(link['xpath'])
        for title in titles:
            sdate = '20.03.2010'
            anews = {'source': link['source'],  'title': title, 'sdate': sdate}
            #collection.insert_one(anews)
            print(title)
        print(len(titles))

yandex = {'source':'https://yandex.ru/news', 'xpath':"//h2[@class='mg-card__title']/text()"}
mail = {'source':'https://news.mail.ru',
        'xpath':"//span[@class='newsitem__title-inner']/text() | //span[@class='link__text']/text()"}
lenta = {'source': 'https://lenta.ru',
            'xpath': "//section[@class='b-tabloid js-tabloid']//a//span/text() | //section[@class='b-layout js-layout b-layout_main']//a//span/text()"}

source_news = [yandex, mail, lenta]
request_to(source_news)
#print(f'Count docs = {collection.count_documents({})}')