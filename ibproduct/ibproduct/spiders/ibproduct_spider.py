import scrapy
from scrapy.selector import Selector
from ibproduct.items import IBProductItem
from urlparse import parse_qs, urlparse


class IBProductSpider(object):
    allowed_domains = ['interactivebrokers.com']

    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath(
            '//table[@class="comm_table_background"]/tr[@class="linebottom"]')
        ps = parse_qs(urlparse(response.url).query,
                      keep_blank_values=True)
        assert ps.keys() == ['f']
        assert len(ps['f']) == 1
        ps = parse_qs(urlparse(ps['f'][0]).query)
        for row in rows:
            item = IBProductItem()
            item['ib_symbol'] = row.xpath('td[1]/text()').extract()
            item['symbol'] = row.xpath('td[3]/text()').extract()
            item['currency'] = row.xpath('td[4]/text()').extract()
            item['product_description'] = row.xpath('td[2]/a/text()').extract()
            item['exchange'] = ps['exch']
            item['ib_category'] = ps['showcategories']
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


ib_plist_pink_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=pink&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'


class IBPinkProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductPink"
    start_urls = [ib_plist_pink_url % (100 * i) for i in range(1, 101)]


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


ib_plist_mexder_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=mexder&showcategories=FUTGRP&ib_entity=llc'


class IBMEXDERProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductMEXDER"
    start_urls = [ib_plist_mexder_url]


ib_plist_cde_url = 'https://www.interactivebrokers.com/en/trading/' +\
    'exchanges.php?exch=cde&showcategories=FUTGRP&ib_entity=llc'


class IBCDEProductSpider(IBProductSpider, scrapy.Spider):
    name = "IBProductCDE"
    start_urls = [ib_plist_cde_url]
