import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import lxml
import csv

async def event(sess, page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    url = f'https://www.etagi.com/realty/?page={page}'
    async with sess.get(url=url, headers=headers) as response:
        res = await response.text()
        soup = BeautifulSoup(res, 'lxml')
        list = soup.find_all('div', class_='y8VEv')
        for j in list:
            prise = j.find('span', class_='uwvkD').text
            square = j.find('div', class_='templates-object-card__row').find_all('span')
            rooms, width, floor = square
            street = j.find('div', class_='EDAsp').find('a').text + j.find('div', class_='EDAsp').text + j.find('div', class_='_mbOx').find('a').text
            url = f"https://www.etagi.com{j.find('a').get('href')}"

            with open("House in Tumen.csv", 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([prise, rooms.text, width.text, floor.text, street, url])

            print(f'Записана квартира с ценой {prise} - {url}')

async def houses():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    url = 'https://www.etagi.com/realty/'

    async with aiohttp.ClientSession() as sess:
        res = await sess.get(url=url, headers=headers)
        soup = BeautifulSoup(await res.text(), 'lxml')
        tasks = []
        last_page = soup.find('div', class_='aoYyv').find_all('button', class_='Q7VHf')[-1].text
        for i in range(1, int(last_page) + 1):
            task = asyncio.create_task(event(sess, i))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    asyncio.run(houses())

if __name__ == '__main__':
    main()