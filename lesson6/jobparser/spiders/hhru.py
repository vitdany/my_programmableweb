import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python&showClusters=false']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//a[@data-qa ='vacancy-serp__vacancy-title']/@href").extract()
        for link in links:
            yield response.follow(link, callback = self.vacancy_parse)
        next_page = response.css("a.HH-Pager-Controls-Next::attr('href')").extract_first()
        if next_page:
            return
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        vacancy_name = response.xpath("//h1//text()").extract_first()
        vacancy_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        vacancy_href = response.url

        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, link=vacancy_href, source=self.name)
