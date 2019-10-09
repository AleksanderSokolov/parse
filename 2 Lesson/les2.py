import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml
import time
import random

mongo_url = 'mongodb://localhost:27017'
client = MongoClient('localhost', 27017)
database = client.leson2

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'


def req_ads(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        price = soup.body.findAll('span', attrs={'class': 'js-item-price', 'itemprop': 'price'})[0].attrs.get('content')
    except IndexError:
        price = None
    result = {'title': soup.head.title.text,
              'name': soup.body.findAll('div', attrs={'class': 'seller-info-name js-seller-info-name'})[0].findAll('a')[0].getText(),
              'name_url': soup.body.findAll('div', attrs={'class': 'seller-info-name js-seller-info-name'})[0].findAll('a')[0].attrs.get('href'),
              #'phone': soup.body.findAll('div', attrs={'class': 'item-phone-big-number js-item-phone-big-number'})[0].findAll('img')[0].attrs.get('src').encode("base64"),
              'price': int(price) if price and price.isdigit else None,
              'url': response.url,
              'params': [tuple(itm.text.split(':')) for itm in
                         soup.body.findAll('li', attrs={'class': 'item-params-list-item'})]
              }
    return result


base_url = 'https://www.avito.ru'
url = 'https://www.avito.ru/krasnodarskiy_kray/nedvizhimost'

response = requests.get(url, headers={'User-Agent': USER_AGENT}, proxies={'ip': 'port'})
soup = BeautifulSoup(response.text, 'lxml')
body = soup.html.body
result = body.findAll('h2', attrs={'data-marker': 'bx-recommendations-block-title'})
ads = body.findAll('div', attrs={'data-marker': 'bx-recommendations-block-item'})
urls = [f'{base_url}{itm.find("a").attrs["href"]}' for itm in ads]

collection = database.avito
collection.drop()
# collection.insert_many(list(map(req_ads, urls)))

for itm in urls:
    time.sleep(random.randint(1, 2))
    result = req_ads(itm)
    collection.insert_one(result)

for x in collection.find():
  print(x)

# print database statistics
print(database.command("collstats", "events"))
print(database.command("dbstats"))