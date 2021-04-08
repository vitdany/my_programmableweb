# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Any

import scrapy





class LeruaItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()
    photos = scrapy.Field()
    url = scrapy.Field()
    product_id = scrapy.Field()
    price = scrapy.Field()
    term_list = scrapy.Field()
    def_list = scrapy.Field()

