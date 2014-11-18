# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IBExchangeItem(scrapy.Item):
    country = scrapy.Field()
    exchange = scrapy.Field()
    market_center_details = scrapy.Field()
    products_info = scrapy.Field()
    hours_info = scrapy.Field()
    products_cat = scrapy.Field()


class IBProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ib_symbol = scrapy.Field()
    product_description = scrapy.Field()
    symbol = scrapy.Field()
    currency = scrapy.Field()
    exchange = scrapy.Field()
    ib_category = scrapy.Field()
