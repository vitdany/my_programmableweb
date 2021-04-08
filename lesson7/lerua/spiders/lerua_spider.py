import scrapy
from scrapy.http import HtmlResponse
from lerua.items import LeruaItem
from scrapy.loader import ItemLoader


class LeruaSpider(scrapy.Spider):
    name = 'lerua_spider'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/stolyarnye-izdeliya/']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath("//a[@class='plp-item__info__title']")
        for link in goods_links[0:1]:
            yield response.follow(link, callback=self.parse_good)


    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaItem(), response=response)

        #loader.add_css('name', 'h1::text')
        loader.add_css('name', "div[class='product-detailed-page']::attr(data-product-name)")
        loader.add_css('product_id', "div[class='product-detailed-page']::attr(data-product-id)")
        loader.add_css('price', "div[class='product-detailed-page']::attr(data-product-price)")
        loader.add_xpath('term_list', "//dt[contains(@class,'def-list__term')]/text()")
        loader.add_xpath('def_list', "//dd[contains(@class,'def-list__definition')]/text()")

        loader.add_xpath('photos', "//uc-pdp-media-carousel//img/@src")
        loader.add_value('url', response.url)

        yield loader.load_item()
