from bs4 import BeautifulSoup as bs
import requests
import bs4
from pymongo import MongoClient
from pprint import pprint
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
    'Accept': '*/*'}

vacancies = []  # найденные вакансии
limit_pages = 1  # количество просматриваемых страниц
client = MongoClient('mongodb://localhost:27017/')

db = client['vacancy']
dblist = client.list_database_names()
print(dblist)
collection = db.collection_vacancy
collection.drop()
print(f'Count docs = {collection.count_documents({})}')


def str_to_int(s):
    nums = re.findall(r'\d+', s)
    nums = [int(i) for i in nums]
    if len(nums) > 0:
        return nums[0]
    return None


def req_superjob(only_new):
    www_superjob = 'www.superjob.ru'
    main_link = 'https://russia.superjob.ru/vacancy/search/'
    next_page = True
    page = 0
    n_new = 0
    while next_page:
        params_requests = {'page': str(page)}

        if page + 1 > limit_pages:
            break
        print(f'Page superjob = {page}')
        response = requests.get(main_link, params=params_requests, headers=headers)
        next_page = response.ok
        if next_page:
            page += 1

            soup = bs(response.text, 'html.parser')
            vacancies_list = soup.findAll('div', {'class': 'f-test-search-result-item'})

            for vacancy in vacancies_list:
                vacancy_data = {}

                vacancy_salary = vacancy.find('span', {'class': "_3mfro _2Wp8I PlM3e _2JVkc _2VHxz"})

                if type(vacancy_salary) == bs4.Tag:

                    text_salary_check = vacancy_salary.get_text() \
                        .replace(u'\xa0', u' ') \
                        .split(' ', 1)[0]
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = None
                    vacancy_data['name'] = None
                    vacancy_data['link'] = None
                    vacancy_data['www'] = www_superjob

                    s = vacancy_salary.get_text() \
                        .replace(u'\xa0', u'') \
                        .split(r'-')
                    if len(s) > 0:
                        if text_salary_check == 'до':
                            vacancy_data['salary_max'] = str_to_int(s[0])
                        elif text_salary_check == 'от':
                            vacancy_data['salary_min'] = str_to_int(s[0])
                        elif text_salary_check != 'По':
                            vacancy_data['salary_min'] = str_to_int(s[0])
                            if len(s) > 1:
                                vacancy_data['salary_max'] = str_to_int(s[1])

                vacancy_name = vacancy.find('a', href=True)
                if type(vacancy_name) == bs4.Tag:
                    vacancy_link = main_link + vacancy_name.get('href')
                    vacancy_name = vacancy_name.get_text()
                    vacancy_data['name'] = vacancy_name
                    vacancy_data['link'] = vacancy_link
                    vacancy_data['www'] = www_superjob

                    if only_new:
                        #print(vacancy_link)
                        if collection.find_one({'link': vacancy_link}) is None:
                            vacancies.append(vacancy_data)
                            n_new += 1
                    else:
                        #print(vacancy_link)
                        vacancies.append(vacancy_data)
                        n_new += 1
    if only_new:
        print(f'Найдено {n_new} новых вакансий')
    else:
        print(f'Найдено {n_new} вакансий')


def req_hh(only_new):
    www_hh = 'www.hh.ru'
    main_link = 'https://hh.ru/search/vacancy'
    next_page = True
    page = 0
    n_new = 0
    while next_page:
        params_requests = {'page': str(page)}

        if page + 1 > limit_pages:
            break
        print(f'Page hh = {page}')
        response = requests.get(main_link, params=params_requests, headers=headers)
        next_page = response.ok
        if next_page:
            page += 1
            soup = bs(response.text, 'html.parser')
            vacancies_list = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

            for vacancy in vacancies_list:
                vacancy_data = {}
                salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})

                if type(salary) == bs4.Tag:
                    text_salary_check = salary.get_text() \
                        .replace(u'\xa0', u' ') \
                        .split(' ', 1)[0]
                    vacancy_data['salary_min'] = None
                    vacancy_data['salary_max'] = None
                    vacancy_data['name'] = None
                    vacancy_data['link'] = None
                    vacancy_data['www'] = www_hh

                    s = salary.get_text() \
                        .replace(u'\xa0', u'') \
                        .split(r'-')
                    if len(s) > 0:
                        if text_salary_check == 'до':
                            vacancy_data['salary_max'] = str_to_int(s[0])
                        elif text_salary_check == 'от':
                            vacancy_data['salary_min'] = str_to_int(s[0])
                        elif text_salary_check != 'По':
                            vacancy_data['salary_min'] = str_to_int(s[0])
                            if len(s) > 1:
                                vacancy_data['salary_max'] = str_to_int(s[1])

                vacancy_name = vacancy.find('a', href=True)
                if type(vacancy_name) == bs4.Tag:
                    vacancy_link = vacancy_name.get('href')
                    vacancy_name = vacancy_name.get_text()
                    vacancy_data['name'] = vacancy_name
                    vacancy_data['link'] = vacancy_link
                    vacancy_data['www'] = www_hh

                if only_new:
                    if collection.find_one({'link': vacancy_link}) is None:
                        vacancies.append(vacancy_data)
                        n_new += 1
                else:
                    vacancies.append(vacancy_data)
                    n_new += 1
    if only_new:
        print(f'Найдено {n_new} новых вакансий')
    else:
        print(f'Найдено {n_new} вакансий')


def mongo_insert():
    collection.insert_many(vacancies)
    print(f'Insert vacancies= {len(vacancies)}')
    print(f'Count docs = {collection.count_documents({})}')

def mongo_select(val):
    result = collection.find({'$or': [{'salary_min': {'$gt': val}}, {'salary_max': {'$gt': val}}]})
    n = 0
    for i in result:
        # pprint(i)
        n += 1
    print(f'Сумма больше {val} найдена в {n} вакансиях.')


find_new = False
print(f'limit_pages = {limit_pages}')
# Поиск
req_superjob(find_new)
req_hh(find_new)
#pprint(vacancies)

# запись результатов
mongo_insert()
# Поиск по значению зарплаты
mongo_select(100000)

# поиск и запись новых вакансий
limit_pages = 2
vacancies.clear()
print(f'limit_pages = {limit_pages}')
find_new = True
req_superjob(find_new)
req_hh(find_new)
