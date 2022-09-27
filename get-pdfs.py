import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

URL = "https://snowmass21.org/submissions/ef"
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

#print(page.text)
for div in soup.find_all('div', {'class': 'li'}):
    print(div.text)
    for link in div.find_all('a'):
        href = link.get('href')
        if 'pdf' in href:
            print(href)

