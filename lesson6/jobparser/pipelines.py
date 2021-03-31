# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re
from pprint import pprint


def str_to_value(sal, v):
    patterns = [r'(от)(\d+)([до]+)(\d+)([А-Яа-яЁёa-zA-Z]{3})',
                r'\s*(от)(\d+)([А-Яа-яЁёa-zA-Z]{3})\s*',
                r'\s*(до)(\d+)([А-Яа-яЁёa-zA-Z]{3})\s*'
                ]
    s = ''.join(sal).replace(' ', '').replace('\xa0', '')

    for i, p in enumerate(patterns):
        match = re.search(p, s)
        if match is not None:
            if i == 1:
                v['min_salary'] = match[2]
                v['currency'] = match[3]
                return
            elif i == 2:
                v['max_salary'] = match[2]
                v['currency'] = match[3]
                return
            elif i == 0:
                v['min_salary'] = match[2]
                v['max_salary'] = match[4]
                v['currency'] = match[5]
                return
            else:
                v['currency'] = s


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2003

    def process_item(self, item, spider):

        if spider.name == 'hhru':

            ready_salary = self.process_salary(item['salary'])
            vacancy = {
                'name': item['name'],
                'min_salary': ready_salary['min_salary'],
                'max_salary': ready_salary['max_salary'],
                'currency': ready_salary['currency'],
                'link': item['link'],
                'source': item['source']
            }

            collection = self.mongo_base[spider.name]
            pprint(vacancy)
            collection.insert_one(vacancy)
            return vacancy

    def process_salary(self, salary):

        vacancy_data = {}
        vacancy_data['min_salary'] = None
        vacancy_data['max_salary'] = None
        vacancy_data['currency'] = None
        str_to_value(salary, vacancy_data)

        return vacancy_data
