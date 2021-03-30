import requests
from bs4 import BeautifulSoup
import csv
import time
import urllib
import fake_useragent

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0', 'accept': '*/*'}
session = requests.Session()
HOST = 'http://mir-priaji.ru/'
link = 'http://mir-priaji.ru/auth/?login=yes'
user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

data ={
	"backurl": "/auth/",
	"AUTH_FORM": "Y",
	"TYPE": "AUTH",
	"POPUP_AUTH": "N",
	"USER_LOGIN": "nikolay.4everr@mail.ru",
	"USER_PASSWORD": "123123",
	"Login": [
		"Войти",
		"Войти"
	]
}

responce = session.post(link, data=data, headers=header).text



def get_html(url, params=None):
    r = session.get(url, headers=header, params=params)
    return r

def get_html2(url, params=None):
    d = requests.get(url, headers=HEADERS, params=params)
    return d

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginationTo = soup.find('div', class_='navigation-pages')
    if paginationTo:
        paginationTo = soup.find('div', class_='navigation-pages')
        pagination = paginationTo.find_all('a') 
        return int(pagination[-1].get_text())  
    else:
        return 1
        

    


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('h2', class_='sale-personal-section-index-block-name')
    print(items)
    catalog = []
    for item in items:
        ImageLargePage = item.find('a').get('href'),
        ImageLargePage2 = str(ImageLargePage)[3:-3]
        PageImageHref =str(HOST) + str(ImageLargePage2)
        html2 = get_html2(PageImageHref)
  

        soup2 = BeautifulSoup(html2.text, 'html.parser')
        items2 = soup2.find('li', class_='current')
        bb = items2.find('link').get('href')        
        if bb:
            bb = items2.find('link').get('href')   
        else:
            bb = ''      
        items3 = soup2.find('div', class_='detail_text')
        if items3:
            text = str(items3.get_text)

            text2 = text.replace('<br/>', '')

            text3 = text2.replace('</div>>', '')

            text4 = text3.replace('<bound method Tag.get_text of <div class="detail_text">', '')

        else:
            text4 = ''     


        cost = item.find('div', class_='js_price_wrapper price')
        numberOf = item.find('div', class_='js_price_wrapper price')
        if cost and numberOf:

            cost = cost.find('span', class_='values_wrapper')
            cost2 = cost.get_text()
            cost3 = cost2.replace(' руб.', '')
            cost123 = ''.join(cost3.split())

            
            intcost = float(cost123)
            cost5 = intcost * 0.5 + intcost

            cost5 = float('{:.0f}'.format(cost5))

            cost7 = str(cost5)
            cost8 = cost7[:-2]
            print(cost8)

            visible = 'visible'
            
            
            numberOf = numberOf.find('span', class_='price_measure')
            numberOf2 = 'руб. ' + numberOf.get_text()
            print(numberOf2)
        else:
            cost = 'Цену уточняйте' 
            numberOf = ' '


        catalog.append({
            'title': item.find('a', class_='dark_link').get_text(strip=True),
            'kategory': soup.find('h1', id='pagetitle').get_text(strip=True),
            'image': HOST + bb[1:],
            'kol-vo': item.find('span', class_='value').get_text(strip=True),
            'text': text4,
            'cost': cost8,
            'numberOf': numberOf2,
            'visible': visible
        })
    return catalog




def save_file(items, path):
    with open(path, 'w',  encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Категории', 'Имя', 'Изображения', 'Описание', 'Базовая цена', 'Видимость в каталоге'])
        for item in items:
            writer.writerow([item['kategory'], item['title'], item['image'], item['text'], item['cost'], item['visible']])

def parse():
    for URL in [


    'http://mir-priaji.ru/personal/',  

    ]:

        html = get_html(URL)
        if html.status_code == 200:
            catalog = []
            pages_count = get_pages_count(html.text)
            for page in range (1, pages_count + 1):
                print(f'Парсинг страницы {page} {pages_count} {URL}...')
                html = get_html(URL, params={'PAGEN_1': page})
                catalog.extend(get_content(html.text))
                time.sleep(1)
            FILE = URL[34:-1] + '1,1' + '.csv'   
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров')
        else:
            print('Error')    





parse()