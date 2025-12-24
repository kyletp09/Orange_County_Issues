from bs4 import BeautifulSoup
import pandas as pd
import lxml
import time
import re
import requests
import os
from tqdm import tqdm

def getText(link: str) -> str:
     try:       
        file = link.split("/")[-2] + ".html"
        r = requests.get(link)
        with open(f'html_files/{file}', "w+b") as f:
            f.write(r.text.encode('utf-8'))
                
        with open(f'html_files/{file}', 'r') as f:
            html = f.read()
                
        soup = BeautifulSoup(html, 'html.parser')

        text = str(soup.select_one("div.article-body").text)
        clean = re.sub(r'\s+', ' ', text).strip()
        author = soup.select_one(".author-name").text
        os.remove(f'html_files/{file}')

        return clean, author
     except AttributeError:
        file = link.split("/")[-2] + ".html"
        r = requests.get(link)
        with open(f'html_files/{file}', "w+b") as f:
            f.write(r.text.encode('utf-8'))
                
        with open(f'html_files/{file}', 'r') as f:
            html = f.read()
                
        soup = BeautifulSoup(html, 'html.parser')

        text = str(soup.select_one("div.article-body").text)
        clean = re.sub(r'\s+', ' ', text).strip()
        author = 'None'
        os.remove(f'html_files/{file}')
        return clean, author
         
    
def get_links(xml: str):
    r = requests.get(xml)

    s = BeautifulSoup(r.text, features='xml')

    links = [i.text for i in s.find_all('loc')]
    titles = [i.text for i in s.find_all('news:title')]
    dates = [i.text for i in s.find_all('news:publication_date')]

    return links, titles, dates

with open("html_files/sitemap.xml", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, features='xml')
xml_links = [xml_link.text for xml_link in soup.find_all('loc') if xml_link.text.split('=')[1].split('&')[0] == '2025']

df = pd.DataFrame(columns = ['Title', 'Date', 'Author', 'Link', 'Text'])
failed_links = pd.Series()

for xml in tqdm(xml_links):
    links, titles, dates = get_links(xml)

    for i in tqdm(range(len(links))):
        try:
            link = links[i]
            text, author = getText(link)
            title = titles[i]
            date = dates[i]
            df.loc[len(df)] = [title, date, author, link, text]
            time.sleep(2)
        except KeyboardInterrupt:
            print('Exiting and Saving Data')
            df.to_pickle("Datasets/df.pkl")
            break
        except Exception as e:
            print(f'\n Exception: {e}')
            failed_links = pd.concat([failed_links, pd.Series(link)])

            
    time.sleep(5)

print('Done. Saving Data!')
failed_links.to_pickle("Datasets/failed_links.pkl")
df.to_pickle("Datasets/df.pkl")
