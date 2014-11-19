import scrapy
from scrapy.selector import Selector
from ibproduct.items import IBProductItem
from urlparse import parse_qs, urlparse
import itertools

plist_base = 'https://www.interactivebrokers.com/en/trading/'

plist_stk = plist_base +\
    'exchanges.php?exch=%s&showcategories=STK&showproducts=&' +\
    'sequence_idx=%s&sortproducts=&ib_entity=llc#show'

stk_exchanges = [
    # North America
    'nasdaq',
    'nyse',
    'amex',
    'arca',
    'pink',
    'tse',
    'mexi',
    # Europe
    'lse',  # London
    'fwb',  # Frankfurt
    # Asia / Pacific
    'tsej',  # Japan
    'sehk',  # Honk Kong
    'sgx',  # Singapore
    'asx',  # Australia
]

start_urls_stk = [plist_stk % (exch, page * 100) for exch, page in
                  itertools.product(stk_exchanges, range(1, 101))]

plist_fut = plist_base +\
    'exchanges.php?exch=%s&showcategories=FUTGRP&showproducts=&' +\
    'sortproducts=&ib_entity=llc#show'

fut_exchanges = [
    # North America
    'globex',
    'cbot',
    'cde',
    'mexider',
    # Europe
    'dtb',  # Eurex (Germany)
    'liffe',
    # Asia / Pacific
    'ose.jpn',
    'tsej',
    'hkfe',
    'sgx',
    'kse',
    'snfe',
]

start_urls_fut = [plist_fut % exch for exch in fut_exchanges]

fx_exchanges = [
    'ibfxpro',
]

plist_fx = plist_base +\
    'exchanges.php?exch=%s&showcategories=FX&showproducts=&' +\
    'sortproducts=&ib_entity=llc#show'

start_urls_fx = [plist_fx % exch for exch in fx_exchanges]


class IBProductSpider(scrapy.Spider):
    name = "IBProduct"
    allowed_domains = ['interactivebrokers.com']
    start_urls = start_urls_fut + start_urls_fx + start_urls_stk

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
