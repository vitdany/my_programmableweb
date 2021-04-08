import requests
from lxml import html
from pprint import pprint

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

main_url = 'https://leroymerlin.ru/product/plita-osb-3-ultralam-8-mm-2500x1250-mm-3-125-m-18693669/'
response = requests.get(main_url, headers=header)

dom = html.fromstring(response.text)
# "dt[@class='def-list__term']/text()"
import re


def str_to_int(s):
    s = s.replace('\n', '')
    s = re.sub(r'\s+', ' ', s)
    st = re.search(r'[^\W\d]', s)
    if st:
        return s
    nums = re.findall(r'[+-]?([0-9]*[.][0-9])+', s)
    return nums[0]


# items = dom.xpath('//div[contains(@class,"def-list__group")]')
# fishing_item = {}
# for item in items:
#     name = item.xpath("dt[@class='def-list__term']/text()")[0]
#     value = item.xpath("dd[@class='def-list__definition']/text()")[0]
#     fishing_item[name] = str_to_int(value)
# pprint(fishing_item)


items = dom.xpath('//dt[contains(@class,"def-list__term")]/text()')
fishing_item = {}
for item in items:
    name = item
    #value = item.xpath("dd[@class='def-list__definition']/text()")[0]
    #fishing_item[name] = str_to_int(value)
    print(name)