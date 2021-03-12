# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 22:52:35 2021

@author: thiba
"""

# Importation pour la valeur actuelle du CAC
import bs4
import requests

ticker = '^FCHI'

# Défini l'url
url = ('https://fr.finance.yahoo.com/quote/') + ticker + ('/')
# Creer la requete
r = requests.get(url)

# Recupere le contenu du text de la requete
web_content = bs4.BeautifulSoup(r.text, 'lxml')

# Cherche l'element correspondant sur la page
web_content = web_content.find('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})

web_content = web_content.find('span').text

if web_content == []:
    web_content = 'REFRESH'

print(web_content)
