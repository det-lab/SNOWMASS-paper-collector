import requests
from bs4 import BeautifulSoup
import os
import re
from pathlib import Path

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

BASE_URL = "https://snowmass21.org/submissions/"
FRONTIER = "ef"
URL = BASE_URL + FRONTIER
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# get a list of the name of the papers
# and a list of the urls for each pdf
paper_list = []
href_list = []
paper_containers = soup.find_all('div', {'class': 'level4'})
#('div', {'class': 'li'})
for section in paper_containers:
    #print(div.text)
    for div in section.find_all('div', {'class': 'li'}):
        paper_list.append(div.text)
        for link in div.find_all('a'):
            href = link.get('href')
            if 'pdf' in href:
                #print(href)
                href_list.append(href)


# write out a file with a list of the papers
if not os.path.exists(FRONTIER):
   os.makedirs(FRONTIER)

paper_list_file_name = os.path.join(FRONTIER, 'paper_list.txt')
#print(paper_list_file_name)
with open(paper_list_file_name, 'w', encoding='utf-8') as f:
    for paper in paper_list:
        #print (paper)
        print(paper, file=f)

# download all the papers
for paper in href_list:
    # this regex searches for 
    # https://arxiv.org/pdf/2109.10905
    # https://arxiv.org/pdf/arXiv:2203.10046
    result = re.search(r"/pdf/\D*(.+)$", paper)
    if result is None:
        # this regex searches for e.g.
        # https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PUBNOTES/ATL-PHYS-PUB-2022-018/ATL-PHYS-PUB-2022-018.pdf
        # https://www.slac.stanford.edu/~mpeskin/Snowmass2021/BelleIIPhysicsforSnowmass.pdf
        result = re.search(r"(?<=/)([^/]*)(?=\.pdf)", paper)

    # there could be other patterns but
    # I'm not inclined to try to match them all
    try:
        #print (result.group(1))
        paper_name = os.path.join(FRONTIER, result.group(1) + '.pdf')
    except:
        print ("Could not download ", paper)

    # only download the paper if it's not already present
    # I suppose papers could change
    # but TOO BAD
    if not Path(paper_name).exists():
        r = requests.get(paper)
        with open(paper_name, 'wb') as f:
            f.write(r.content)
