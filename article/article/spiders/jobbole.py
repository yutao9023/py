# -*- coding: utf-8 -*-
import scrapy
from article.items import ArticleItem
from article.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts']

    def parse(self, response):
        for info in response.xpath('//div[@class="post floated-thumb"]'):
            href = info.xpath('.//a[@class="archive-title"]/@href').extract()[0]
            description = info.xpath('.//span[@class="excerpt"]/p/text()').extract()[0]
            #如果href是全的 那麽response.urljoin(href)相當於href 如果不是全的 response.urljoin 將href和域名拼接 重要
            image_url = info.xpath('.//div[@class="post-thumb"]/a/img/@src').extract_first('')
            yield scrapy.Request(url=response.urljoin(href), meta={'description': description,'front_image_url': image_url}, callback=self.parse_detail)  #把上一級的信息傳遞到下一級用meta屬性
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_detail(self,response):
        item = ArticleItem()
        item['url_object_id'] = get_md5(response.url)
        item['front_image_url'] = [response.meta.get('front_image_url', '')]
        item['post_url'] = response.url
        item['description'] = response.meta.get('description', '') #默认为空
        item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        item['date'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·', '').strip()
        item['category'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a[@rel="category tag"]/text()').extract()[0]
        fav_path = '//span[contains(@class, "vote-post-up")]/h10/text()'
        item['fav_num'] = 0 if not response.xpath(fav_path).re('\d+') else int(response.xpath(fav_path).re('\d+')[0])
        collections_path = '//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()'
        item['collections'] = 0 if not response.xpath(collections_path).re('\d+') else int(response.xpath(collections_path).re('\d+')[0])
        comment_path = '//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()'
        item['comment'] = 0 if not response.xpath(comment_path).re('\d+') else int(response.xpath(comment_path).re('\d+')[0])
        yield item



