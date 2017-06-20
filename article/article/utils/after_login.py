import requests
import json
with open('cookie.txt', 'r',encoding='utf-8') as f:
    cookie = f.read()
    cookie = json.loads(cookie)
    print(cookie)

html = requests.get('https://www.shanbay.com/', cookies=cookie)
print(html.text)

with open('shanbay.html', 'wb') as f:
    f.write(html.text.encode('utf-8'))