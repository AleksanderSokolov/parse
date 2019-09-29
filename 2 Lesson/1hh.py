import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import lxml
import time
import random

mongo_url = 'mongodb://localhost:27017'
client = MongoClient('localhost', 27017)
database = client.vacancy

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'

url = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=%D0%A2%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D1%89%D0%B8%D0%BA&from=suggest_post'

def req_ads():
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        vacanciesHH = soup.body.findAll('div', attrs={'class': 'vacancy-serp-item'})
    except IndexError:
        vacanciesHH = None

    for vacancy in vacanciesHH:
        try:
            salary = vacancy.findAll('div', attrs={'class': 'vacancy-serp-item__compensation'})[0].text
        except IndexError:
            salary=None
        result = {'name': vacancy.findAll('a', attrs={'class': 'bloko-link HH-LinkModifier'})[0].text,
                  'salary': salary,
                  'href': vacancy.findAll('a', attrs={'class': 'bloko-link HH-LinkModifier'})[0].attrs.get('href'),
                  'site': 'hh.ru'
        }
        collection.insert_one(result)

collection = database.vacancyBySearch

collection.drop()
result = req_ads()

#
print(1)

for x in collection.find():
    print(x)

print(database.command("collstats", "events"))

# print database statistics
print(database.command("dbstats"))

