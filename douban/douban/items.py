# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    name = scrapy.Field()
    rank = scrapy.Field()
    rate = scrapy.Field()
    num = scrapy.Field()
    quote = scrapy.Field()
    movie_url = scrapy.Field()
