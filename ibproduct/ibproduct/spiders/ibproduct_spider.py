import scrapy
from scrapy.selector import Selector
from ibproduct.items import IBProductItem


class IBProductSpider(object):
    allowed_domains = ['interactivebrokers.com']

    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath(
            '//table[@class="comm_table_background"]/tr[@class="linebottom"]')
        for row in rows:
            item = IBProductItem()
            item['ib_symbol'] = row.xpath('td[1]/text()').extract()
            item['symbol'] = row.xpath('td[3]/text()').extract()
            item['currency'] = row.xpath('td[4]/text()').extract()
            item['product_description'] = row.xpath('td[2]/a/text()').extract()
            yield item


ib_plist_nasdaq_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=nasdaq&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'


class IBNASDAQProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductNASDAQ"
    start_urls = [ib_plist_nasdaq_url % (100 * i) for i in range(1, 101)]


ib_plist_nyse_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=nyse&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'


class IBNYSEProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductNYSE"
    start_urls = [ib_plist_nyse_url % (100 * i) for i in range(1, 101)]


ib_plist_mexi_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=mexi&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'


class IBMEXIProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductMEXI"
    start_urls = [ib_plist_mexi_url % (100 * i) for i in range(1, 101)]


ib_plist_tse_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=tse&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'


class IBTSEProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductTSE"
    start_urls = [ib_plist_tse_url % (100 * i) for i in range(1, 101)]


ib_plist_globex_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=globex&showcategories=FUTGRP&ib_entity=llc'


class IBGlobexProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductGlobex"
    start_urls = [ib_plist_globex_url]
