import requests

def parse_detail_page(url):
    html = requests.get(url)
    print(html.text)

parse_detail_page('https://movie.douban.com/subject/26747853/?tag=%E7%BB%BC%E8%89%BA&from=gaia')