import scrapy
from scrapy.selector import Selector
from ibproduct.items import IBExchangeItem
from urlparse import parse_qs, urlparse

base_url = 'https://www.interactivebrokers.com/en/index.php?f=products&p=%s'

product_cats = [
    'stk',
    'europe_stk',
    'asia_stk',
    'fut',
    'europe_fut',
    'asia_fut',
    'etf',
    'fx',
]


def strip_extract(xtract):
    return [x for x in map(lambda z: z.strip(), xtract) if x]


class IBExchangeSpider(scrapy.Spider):
    name = "IBExchange"
    allowed_domains = ['interactivebrokers.com']
    start_urls = [base_url % pcat for pcat in product_cats]

    def parse(self, response):
        hxs = Selector(response)
        rows = hxs.xpath(
            '//table/tbody/tr[@class="linebottom"]')
        ps = parse_qs(urlparse(response.url).query,
                      keep_blank_values=True)
        assert set(ps.keys()) == set(['f', 'p']), ps
        country = []
        col_adj = -1
        for idx, row in enumerate(rows):
            item = IBExchangeItem()
            tmp_country = row.xpath('td/b/text()').extract()
            if tmp_country:
                country = tmp_country
                col_adj = 0
            else:
                col_adj = -1
            item['country'] = country
            item['market_center_details'] = \
                strip_extract(row.xpath('td/a/text()').extract())
            item['products_info'] = \
                strip_extract(
                    row.xpath('td[%s]/text()' % (3 + col_adj)).extract())
            item['hours_info'] = \
                strip_extract(
                    row.xpath('td[%s]/text()' % (4 + col_adj)).extract())
            item['products_cat'] = ps['p']
            if idx == 0:
                print row.extract()
                print item
            yield item
