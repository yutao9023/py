from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pymongo
import json
import time

client = pymongo.MongoClient('localhost', 27017)
db_name = client['douban_tv2']


headers={
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2162.400 QQBrowser/9.5.10262.400'
}


def get_tv_url(tag,offest):
    data = {
        'type': 'tv',
        'tag': tag,
        'sort': 'recommend',
        'page_limit': '20',
        'page_start': offest,
    }
    url = 'https://movie.douban.com/j/search_subjects?'+urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        time.sleep(0.5)
        response.raise_for_status()
        return response.text
    except:
        print('请求索引页失败')
        return None


def parse_detail_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    time.sleep(0.5)
    html = etree.HTML(response.text)
    title = html.xpath('//span[@property="v:itemreviewed"]/text()')[0]
    rating = html.xpath('//strong[@property="v:average"]/text()')[0]
    votes = html.xpath('//span[@property="v:votes"]/text()')[0]
    category = html.xpath('//span[@property="v:genre"]/text()')
    summary = html.xpath('//span[@property="v:summary"]/text()')[0].strip() if soup.find('span',property='v:summary') else None
    actors = html.xpath('//a[@rel="v:starring"]/text()')
    print({'title':title, 'rating':float(rating),'votes':int(votes),'catagory':category,'summary':summary,'actors':actors})
    yield {'title':title, 'rating':float(rating),'votes':int(votes),'catagory':category,'summary':summary,'actors':actors}




if __name__ == '__main__':
    tags = ['热门','美剧','英剧','韩剧','日剧','国产剧','港剧','日本动画','综艺']
    for tag in tags:
        db_table = db_name[tag]
        for offest in range(0,500,20):
            info = json.loads(get_tv_url(tag,offest))
            tv_info = info['subjects']
            for info in tv_info:
                for detail_info in parse_detail_page(info['url']):
                    db_table.insert(detail_info)


                # try:
                #     db_table.insert({info['title'].replace('.', ''): info['url']})
                # except:
                #     pass
                # print({info['title']: info['url']})


















