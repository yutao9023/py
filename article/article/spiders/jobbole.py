# -*- coding: utf-8 -*-
import scrapy
from article.items import ArticleItem


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts']

    def parse(self, response):
        for info in response.xpath('//div[@class="post floated-thumb"]'):
            href = info.xpath('.//a[@class="archive-title"]/@href').extract()[0]
            yield scrapy.Request(href,callback=self.parse_detail)
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        if next_page:
            yield scrapy.Request(next_page,callback=self.parse)

    def parse_detail(self,response):
        item = ArticleItem()
        item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        item['date'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·', '').strip()
        item['category'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[@rel="category tag"]/text()').extract()[0]
        # item['fav_num'] = int(response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0])
        fav_path = '//span[contains(@class, "vote-post-up")]/h10/text()'
        item['comment'] = 0 if not response.xpath(fav_path).re('\d+') else int(response.xpath(fav_path).re('\d+')[0])
        collections_path = '//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()'
        item['collections'] = 0 if not response.xpath(collections_path).re('\d+') else int(response.xpath(collections_path).re('\d+')[0])
        comment_path = '//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()'
        item['comment'] = 0 if not response.xpath(comment_path).re('\d+') else int(response.xpath(comment_path).re('\d+')[0])
        yield item



