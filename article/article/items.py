# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ArticleItem(scrapy.Item):
    title = Field()
    date = Field()
    category = Field()
    fav_num = Field()
    collections = Field()
    comment = Field()
    description = Field()
    post_url = Field()
    front_image_url = Field()
    front_image_path = Field()
    url_object_id = Field()