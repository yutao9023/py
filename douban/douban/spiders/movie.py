import scrapy
from douban.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'movie'
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield scrapy.Request(url, headers=self.header)

    def parse(self, response):
        item = DoubanItem()
        for info in response.xpath('//ol[@class="grid_view"]/li'):
            item['name'] = info.xpath('.//div[@class="pic"]/a/img/@alt').extract()[0]
            item['rank'] = info.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['rate'] = info.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['num'] = info.xpath('.//div[@class="star"]/span/text()').re('\d+')[2]
            item['quote'] = info.xpath('.//span[@class="inq"]/text()').extract_first(None)
            item['movie_url'] = info.xpath('.//div[@class="pic"]/a/@href').extract()[0]
            yield item
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield scrapy.Request(next_url, headers=self.header,callback=self.parse)
