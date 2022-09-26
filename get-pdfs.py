import requests

URL = "https://snowmass21.org/submissions/ef"
page = requests.get(URL)

print(page.text)