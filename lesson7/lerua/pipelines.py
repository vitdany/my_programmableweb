# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pprint import pprint

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from urllib.parse import urlparse
from pymongo import MongoClient


import re
class LeruaPipeline:


     def __init__(self):
         client = MongoClient('localhost', 27017)
         self.mongo_base = client.lerua


    def process_def(value):
        s = value.replace('\n', '')
        s = re.sub(r'\s+', ' ', s)
        st = re.search(r'[^\W\d]', s)
        if st:
            return s
        nums = re.findall(r'[+-]?([0-9]*[.][0-9])+', s)
        return nums[0]

    def process_item(self, item, spider):


        # for d in item['def_list']:
        #     print(d)
        #     d = self.process_def(d)


        data_lerua_item = {
            'name': item['name'],
            'url': item['url'],
            'price': item['price'],
            'product_id': item['product_id'],
            'term': item['term_list'],
            'def': item['def_list']
        }
        #self.v_item.append(data_lerua_item)

        collection = self.mongo_base[spider.name]
        pprint(data_lerua_item)
        collection.insert_one(data_lerua_item)

        return item



class ImLeruaPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):

        request.meta['product_id'] = item['product_id'][0]
        path = super().file_path(request, response, info)
        return item['product_id'][0]+'/'+path

    def thumb_path(self, request, thumb_id, response=None, info=None):

         path = super().thumb_path(request, thumb_id, response, info)
         return request.meta['product_id'] + '/' + path

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item