# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd 

headers = {
        'Referer': 'https://www.residentevildatabase.com/personagens/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp


def get_infos(soup):
    div_page = soup.find('div', class_= 'td-page-content')
    paragrafo = div_page.find_all("p")[1]
    em = paragrafo.find_all('em')
    data = {}
    for i in em:
        chave, valor, *_ = i.text.split(':')
        data[chave.strip(' ')] = valor.strip(' ')
    return data


def get_aparicoes(soup):
    lis = (soup.find('div', class_= 'td-page-content')
           .find('h4')
           .find_next()
           .find_all('li'))
    aparicoes = [i.text for i in lis]
    return aparicoes


def get_data(url):
    response = get_content(url)

    if response.status_code != 200 :
        print('Não foi possivel acessar a pagina')
        return {}
    else:
        soup = BeautifulSoup(response.text)
        data = get_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
    return data


def get_links():
    url_2 = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url_2, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = soup_personagens.find('div', class_ = 'td-page-content').find_all('a')
    links = [i['href'] for i in ancoras]
    return links

# %%

links = get_links()

data = []

for i in tqdm(links):
    d = get_data(i)
    d['link'] = i
    nome = i.split('/')[-2].replace('-', ' ').title()
    d['nome'] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df.to_csv('ResidentEvil_Personagens.csv', index=False)
df.to_parquet('ResidentEvil_Personagens.parquet')

# %%
