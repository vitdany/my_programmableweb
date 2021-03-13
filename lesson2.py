from bs4 import BeautifulSoup as bs
import requests
import bs4
from pprint import pprint
import re



params = {}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
vacancies = []

def str_to_int(s):
    nums = re.findall(r'\d+', s)
    nums = [int(i) for i in nums]
    if len(nums) > 0:
        return nums[0]
    return None

def req_superjob():
    www_superjob = 'www.superjob.ru'
    main_link = 'https://www.superjob.ru/vacancy/search'

    response = requests.get(main_link , headers=headers)
    if response.ok:
        soup = bs(response.text, 'html.parser')
        vacancies_list = soup.findAll('div', {'class':'f-test-search-result-item'})

        for vacancy in vacancies_list:
            vacancy_data = {}

            vacancy_salary = vacancy.find('span', {'class':"_3mfro _2Wp8I PlM3e _2JVkc _2VHxz"})

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

            vacancies.append(vacancy_data)

def req_hh():
    www_superjob = 'www.hh.ru'
    main_link = 'https://hh.ru/search/vacancy'

    response = requests.get(main_link, headers=headers)
    if response.ok:
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
                vacancy_data['www'] = www_superjob

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
                        if len(s)>1:
                            vacancy_data['salary_max'] = str_to_int(s[1])

            vacancy_name = vacancy.find('a', href=True)
            if type(vacancy_name) == bs4.Tag:
                vacancy_link = main_link + vacancy_name.get('href')
                vacancy_name = vacancy_name.get_text()
                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = vacancy_link
                vacancy_data['www'] = www_superjob

            vacancies.append(vacancy_data)

req_superjob()
req_hh()

pprint(vacancies)
print(len(vacancies))