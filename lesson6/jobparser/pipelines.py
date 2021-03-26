# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2003


    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        # ready_salary = self.process_salary(item['salary'])
        # item['min_salary'] = ready_salary[0]
        # item['max_salary'] = ready_salary[1]
        # item['currency'] = ready_salary[2]
        # del item['salary']
        return item

    def process_salary(self, salary):
        pass