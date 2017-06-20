# -*- coding: utf-8 -*-
import scrapy
import re

class GithubSpider(scrapy.Spider):
    name = "github"
    allowed_domains = ["github.com"]
    start_urls = ['http://github.com/']

    headers = {
        "HOST": "www.github.com",
        "Referer": "https://www.github.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def start_requests(self):
        return [scrapy.Request('https://github.com/login',headers=self.headers, callback=self.login)]


    def login(self, response):
        token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        post_url = "https://github.com/session"
        post_data = {
            # 'commit':'Sign in',
            'utf8':'✓',
            'authenticity_token':token,
            'login':'yutao1016@gmail.com',
            'password':'yutao07161016',
        }
        return scrapy.FormRequest(post_url, formdata=post_data,headers=self.headers,callback=self.login_after,dont_filter=True)

    def login_after(self, response):
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.body)
        # print(response.text)
        print(response.body)