# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 21:29:18 2021

@author: thiba
"""

# Importation pour la valeur actuelle du CAC
import bs4
import requests


def real_time_value(ticker):
    """


    Parameters
    ----------
    ticker : STR
        Correspond au ticker de l'indice recherché.

    Returns
    -------
    web_content : FLOAT
        Correspond à la valeur actuelle de l'indice.

    """

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
    return web_content


def last_closure_value(ticker):
    """


    Parameters
    ----------
    ticker : STR
        Correspond au ticker de l'indice recherché.

    Returns
    -------
    web_content : FLOAT
        Correspond à la valeur à la cloture de l'indice.

    """

    # Défini l'url
    url = ('https://fr.finance.yahoo.com/quote/') + ticker + ('/')
    # Creer la requete
    r = requests.get(url)

    # Recupere le contenu du text de la requete
    web_content = bs4.BeautifulSoup(r.text, 'lxml')

    # Cherche l'element correspondant sur la page
    web_content = web_content.find('td', {'class': 'Ta(end) Fw(600) Lh(14px)'})

    web_content = web_content.find('span').text

    if web_content == []:
        web_content = 'REFRESH'

    return web_content


if __name__ == '__main__':

    ticker_cac = '%5EFCHI'
    print(last_closure_value(ticker_cac))
    print(real_time_value(ticker_cac))
