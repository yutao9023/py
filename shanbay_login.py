import requests

response = requests.get('https://www.shanbay.com/web/account/login')
response.encoding = response.apparent_encoding
print(response.text)
