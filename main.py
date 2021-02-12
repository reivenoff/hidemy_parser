import requests
import fake_useragent

from bs4 import BeautifulSoup
from colorama import init, Fore

init(convert=True)

logo = Fore.GREEN + r"""
.   .--.--.--. .---..    .   .  .--.  .    .--. .-..---..--.
|   |  |  |   :|    |\  /|\ /   |   )/ \   |   |   )    |   )
|---|  |  |   ||--- | \/ | :    |--'/___\  |--' `-.|--- |--'
|   |  |  |   ;|    |    | |    |  /     \ |  \(   )    |  \
'   '--'--'--' '---''    ' '    ' '       `'   ``-''---''   `
""" + Fore.WHITE

info = '[' + Fore.BLUE + 'INFO' + Fore.WHITE + ']'

class Parsing():
    def __init__(self, u):
        self.url = u
        self.user = fake_useragent.UserAgent().random
        self.header = {'user-agent' : self.user}


    def get_pages_count(self):
        r = requests.get(self.url, headers=self.header).text
        soup = BeautifulSoup(r, 'lxml')
        links = soup.find('div', {'class': 'pagination'})
        links = links.find_all('li')[:-1]
        links = [str(link).split('href="')[1].split('">')[0] for link in links]

        return links


    def get_proxy_from_url(self):
        r = requests.get(self.url, headers=self.header).text
        soup = BeautifulSoup(r, 'lxml')
        blocks = soup.find('tbody')

        f = open('proxy.txt', mode='w', encoding='utf-8')
        for block in blocks:
            try:
                ip = str(block).split('<td>')[1].split('</')[0]
                port = str(block).split('</td><td>')[1]
                f.write(f'{ip}:{port}\n')
            except: pass
        f.close()


if __name__ == '__main__':
    print(logo)
    ping = input(f'{info} Скорость соединения с прокси в мс: ')

    pars = Parsing('http://hidemy.name/ru/proxy-list/?maxtime={ping}&type=h#list'.format(ping=ping))
    links= pars.get_pages_count()

    for link in links:
        pars.get_proxy_from_url()
