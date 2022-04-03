import requests
from bs4 import BeautifulSoup
from time import sleep, time
from datetime import date, timedelta

import random
import os
import re

link_day = str(date.today() - timedelta(days=1)).replace('-', '/') + '/'

HEAD = 'https://auto.ria.com'
URL = 'https://www.mk.ru/news/' + link_day
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
           'accept': ACCEPT}
PROXY = {'http': 'http://161.202.226.194:8123', 'https': 'https://161.202.226.194:8123'}
#149.129.134.39:3128   http://20.97.28.47:8080 62.113.113.155:16286 95.85.24.83:8118


FILE = 'cars.csv'
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='news-listing__item')
    urls = []
    for item in items:
        urls.append(item.find('a', class_='news-listing__item-link').get('href'))
    print(urls)
    return urls


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1', class_='article__title').get_text()
    item = soup.find('div', class_='article__body').get_text()

    title = re.sub(r'[/|\\^:;*"?<>]', '', title)
    print(item)
    print(title)
    print(type(item))
    return item, title


def save_file(items, path):
    with open(path, 'w') as file:
        items = items.replace("\r", "").replace("\n", "")
        items = items.replace(".", ". ")[:-1]
        file.write(items)



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print(f'status {html.status_code}')
        urls = get_urls(html.text)  #список ссылок на новости
        sleep(random.uniform(0.99, 2.99))
        #text, title = get_content(html.text)
        #save_file(text, title + str(time()) + '.txt')

        print(len(urls))
        os.chdir('C:\\Users\\Igoryan\\Desktop\\PyTelegramBot\\parsing_text\\mk_news')
        for url in urls:
            try:
                html = get_html(url)
                if html.status_code == 200:
                    text, title = get_content(html.text)
                    save_file(text, title + ' ' + str(time()) + '.txt')
                    print(f'Loading URL: {url}')
                else:
                    print(f'ERROR: {url}')
                sleep(random.uniform(2.99, 6.99))
            except:
                print((f'ERROR SAVE DATA {url}'))
                continue


if __name__ == '__main__':
    parse()
