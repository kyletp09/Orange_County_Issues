from bs4 import BeautifulSoup
import re
import requests
import os

link = 'https://www.ocregister.com/2025/12/17/dense-fog-advisory-active-for-orange-county-until-wednesday-morning-visibility-as-low-as-1-4-mile/'

file = link.split("/")[-2] + ".html"
#r = requests.get(link)
#with open(f'html_files/{file}', "w+b") as f:
#    f.write(r.text.encode('utf-8'))

with open(f'html_files/{file}', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

text = str(soup.select_one("div.article-body").text)
clean = re.sub(r'\s+', ' ', text).strip()
print(clean)

# os.remove(f'html_files/{file}')
