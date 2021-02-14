import requests
import fake_useragent

from bs4 import BeautifulSoup
from colorama import init, Fore
from random import choice, randint

__title__ = 'HideMy_Parser_2021'
__version__ = '1.0.0'
__author__ = 'reiven'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021 by Me'

init(convert=True)
info = '[' + Fore.LIGHTGREEN_EX + 'INFO' + Fore.WHITE + ']'
question = '[' + Fore.LIGHTBLUE_EX + 'QUESTION' + Fore.WHITE + ']'
logo = Fore.GREEN + r"""
.   .--.--.--. .---..    .   .  .--.  .    .--. .-..---..--.
|   |  |  |   :|    |\  /|\ /   |   )/ \   |   |   )    |   )
|---|  |  |   ||--- | \/ | :    |--'/___\  |--' `-.|--- |--'
|   |  |  |   ;|    |    | |    |  /     \ |  \(   )    |  \
'   '--'--'--' '---''    ' '    ' '       `'   ``-''---''   `
""" + Fore.WHITE

class Parsing():
    def __init__(self):
        self.users = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
        ]

        self.header = {
            'User-agent': choice(self.users),
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;'
                      'q=0.9,text/plain;q=0.8,image/png,*/*;q=0.%d' % randint(2, 5),
            'Accept-Language': 'en-us,en;q=0.%d' % randint(5, 9),
            'Accept-Charset': 'utf-8,windows-1251;q=0.7,*;q=0.%d' % randint(5, 7),
            'Keep-Alive': '300',
        }

    def get_pages_count(self, url_):
        r = requests.get(url_, headers=self.header).text
        soup = BeautifulSoup(r, 'lxml')
        links = soup.find('div', {'class': 'pagination'})
        links = links.find_all('li')[:-1]
        links_new = []
        for link in links:
            try:
                links_new.append('http://hidemy.name'+str(link).split('href="')[1].split('">')[0].replace("amp;", ""))
            except: pass # Если <li class="dots">. . .</li>
        return links_new


    def get_proxy_from_url(self, link):
        r = requests.get(link, headers=self.header).text
        soup = BeautifulSoup(r, 'lxml')
        blocks = soup.find('tbody')

        f = open('proxy.txt', mode='a', encoding='utf-8')
        for block in blocks:
            try:
                ip = str(block).split('<td>')[1].split('</')[0]
                port = str(block).split('</td><td>')[1]
                f.write(f'{ip}:{port}\n')
                print(f'{ip}:{port}')
            except: pass
        del soup
        f.close()


if __name__ == '__main__':
    type  = 'type='
    types = {
    'http':   {'h': None},
    'https':  {'s': None},
    'socks4': {'4': None},
    'socks5': {'5': None}}

    protocols = list(types.keys())
    while None in [list(types.get(protocol).values())[0] for protocol in protocols]:
        print(logo)
        for protocol in protocols:
            if list(types.get(protocol).values())[0] == None:
                answer = input(f'{question} Получать прокси {protocol} Y/n: ')
                if answer.lower() == 'y':
                    answer = True
                elif answer.lower() == 'n':
                    answer = False
                else:
                    answer = None

            types.get(protocol).update({list(types.get(protocol).keys())[0]: answer})

    ping = input(f'{info} Скорость соединения с прокси в мс: ')
    if False in [list(types.get(protocol).values())[0] for protocol in protocols]:
        for type_ in list(types.values()):
            if list(type_.values())[0] is True:
                type += list(type_.keys())[0]

        url = 'http://hidemy.name/ru/proxy-list/?maxtime={ping}&{type}#list'.format(ping=ping, type=type)
    else:
        url = 'http://hidemy.name/ru/proxy-list/?maxtime={ping}&#list'.format(ping=ping)

    pars = Parsing()
    links= pars.get_pages_count(url)
    for link in links:
        pars.get_proxy_from_url(link)
        print(f'{info} Обработана страница {links.index(link)+1}/{len(links)}')
