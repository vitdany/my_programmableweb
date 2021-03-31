import scrapy


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['sj.ru']
    start_urls = ['http://sj.ru/']

    def parse(self, response):
        pass
